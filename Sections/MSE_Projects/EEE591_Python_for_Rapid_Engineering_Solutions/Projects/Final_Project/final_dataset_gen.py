import os
import shutil
import time
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import gc

# --- CONFIGURATION PARAMETERS ---
SEED = 42
N_FEATURES = 10000
CHUNK_SIZE = int(N_FEATURES / 10)  # Exactly 10% of N_FEATURES
N_CLASSES = 100                      # Updated to 2 classes only
TRAIN_ROWS = 70000
TEST_ROWS = 30000
STD_DEV = 17                  

# MISSING DATA SPECIFICATIONS (As specified earlier)
PERCE_ROW_w_NAN = 0.9999            # Percentage of dataset points with missing data
PERCE_COL_w_NAN = 0.5               # Percentage of columns with NaNs in each row

train_dir = "final_dataset/train"
test_dir = "final_dataset/test"

# ──────────────────────────────────────────────────────────────────────────────
# Step 1: Delete and Recreate Directories (Wipe clean before run)
# ──────────────────────────────────────────────────────────────────────────────
print("[*] Step 1")
for directory in [train_dir, test_dir]:
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f" -> Cleared existing directory: {directory}")
    os.makedirs(directory, exist_ok=True)

start_time = time.time()

# Set the global seed for reproducibility across all random generations
rng = np.random.default_rng(SEED)

# ──────────────────────────────────────────────────────────────────────────────
# Step 2: Prepare Full Noiseless Base & Dynamic SIGMA Vector
# ──────────────────────────────────────────────────────────────────────────────
print("[*] Step 2")
noiseless_base = np.random.standard_normal((N_CLASSES, N_FEATURES)).astype(np.float32)
for i in range(N_CLASSES):
    noiseless_base[i, :] += i

SIGMA_VECTOR = np.abs(np.random.normal(0, STD_DEV, size=N_FEATURES)).astype(np.float32)

# Pre-generate target label blueprints
train_labels = np.repeat(np.arange(N_CLASSES), int(TRAIN_ROWS / N_CLASSES))
test_labels = np.repeat(np.arange(N_CLASSES), int(TEST_ROWS / N_CLASSES))

np.random.shuffle(train_labels)
np.random.shuffle(test_labels)

# Pre-determine which row indices will have missing data globally
n_train_missing_rows = int(PERCE_ROW_w_NAN * TRAIN_ROWS)
n_test_missing_rows = int(PERCE_ROW_w_NAN * TEST_ROWS)

train_nan_rows = np.random.choice(TRAIN_ROWS, size=n_train_missing_rows, replace=False)
test_nan_rows = np.random.choice(TEST_ROWS, size=n_test_missing_rows, replace=False)

# ──────────────────────────────────────────────────────────────────────────────
# Step 3: Save Target Labels with Uppercase Parameters Metadata
# ──────────────────────────────────────────────────────────────────────────────
print("[*] Step 3")
print("Saving target label blueprints and encoding metadata parameters...")

generation_metadata = {
    "SEED": str(SEED),
    "N_FEATURES": str(N_FEATURES),
    "CHUNK_SIZE": str(CHUNK_SIZE),
    "N_CLASSES": str(N_CLASSES),
    "TRAIN_ROWS": str(TRAIN_ROWS),
    "TEST_ROWS": str(TEST_ROWS),
    "STD_DEV": str(STD_DEV),
    "PERCE_ROW_w_NAN": str(PERCE_ROW_w_NAN),
    "PERCE_COL_w_NAN": str(PERCE_COL_w_NAN)
}

# Write training labels to labels_param.parquet with metadata
train_table = pa.Table.from_arrays([pa.array(train_labels)], names=["class_label"])
train_table = train_table.replace_schema_metadata(generation_metadata)
pq.write_table(train_table, f"{train_dir}/labels_param.parquet")

# Write testing labels to labels_param.parquet with metadata
test_table = pa.Table.from_arrays([pa.array(test_labels)], names=["class_label"])
test_table = test_table.replace_schema_metadata(generation_metadata)
pq.write_table(test_table, f"{test_dir}/labels_param.parquet")

# ──────────────────────────────────────────────────────────────────────────────
# Step 4: The Column-Chunk Loop (Iterative Disk Writing with NaNs)
# ──────────────────────────────────────────────────────────────────────────────
print("[*] Step 4")
print(f"\nStarting column-chunk loop. Processing {CHUNK_SIZE} features per iteration...")

for col_start in range(0, N_FEATURES, CHUNK_SIZE):
    col_end = min(col_start + CHUNK_SIZE, N_FEATURES)
    current_chunk_width = col_end - col_start
    
    # Calculate how many column items must become NaN within this chunk slice
    actual_missing_feats = int(PERCE_COL_w_NAN * current_chunk_width)
    
    # Slice the corresponding chunk of the fixed SIGMA vector for these features
    SIGMA_chunk = SIGMA_VECTOR[col_start:col_end]
    train_feature_names = [f"f_{j}" for j in range(col_start, col_end)]
    
    # --- TRAINING CHUNK ---
    train_chunk = noiseless_base[train_labels, col_start:col_end]
    train_noise = rng.standard_normal(size=train_chunk.shape, dtype=np.float32) * SIGMA_chunk
    train_chunk += train_noise
    
    # Inject NaNs to specified percentage of rows inside the chunk vector completely loop-free
    train_noise_mask = np.random.rand(n_train_missing_rows, current_chunk_width)
    train_sorted_cols = np.argsort(train_noise_mask, axis=1)[:, :actual_missing_feats]
    train_chunk[train_nan_rows[:, None], train_sorted_cols] = np.nan
    
    train_columns = [pa.array(train_chunk[:, c]) for c in range(train_chunk.shape[1])]
    train_table = pa.Table.from_arrays(train_columns, names=train_feature_names)
    pq.write_table(train_table, f"{train_dir}/features_{col_start}_{col_end}.parquet", compression="snappy")
    del (
        train_chunk, train_noise, train_noise_mask, train_sorted_cols, train_columns, train_table,
    )
    gc.collect()
    # --- TESTING CHUNK ---
    test_chunk = noiseless_base[test_labels, col_start:col_end]
    test_noise = rng.standard_normal(size=test_chunk.shape, dtype=np.float32) * SIGMA_chunk
    test_chunk += test_noise
    
    # Inject NaNs to specified percentage of rows inside the chunk vector completely loop-free
    test_noise_mask = np.random.rand(n_test_missing_rows, current_chunk_width)
    test_sorted_cols = np.argsort(test_noise_mask, axis=1)[:, :actual_missing_feats]
    test_chunk[test_nan_rows[:, None], test_sorted_cols] = np.nan
    
    test_columns = [pa.array(test_chunk[:, c]) for c in range(test_chunk.shape[1])]
    test_table = pa.Table.from_arrays(test_columns, names=train_feature_names)
    pq.write_table(test_table, f"{test_dir}/features_{col_start}_{col_end}.parquet", compression="snappy")
    
    print(f" -> Successfully flushed column chunk: features {col_start} to {col_end} to disk.")
    # ──────────────────────────────────────────────────────────────────────────
    # Clear chunk variables from RAM and force immediate garbage collection
    # ──────────────────────────────────────────────────────────────────────────
    del (
        test_chunk, test_noise, test_noise_mask, test_sorted_cols, test_columns, test_table
    )
    gc.collect()

print("\n" + "="*60)
print("SUCCESS: Vertically partitioned dataset complete!")
print("Stored in folder: contents of 'final_dataset/'")
print(f"Total Runtime: {time.time() - start_time:.2f} seconds")
print("="*60)
