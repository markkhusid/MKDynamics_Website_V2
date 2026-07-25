import os
import shutil
import time
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

# --- CONFIGURATION PARAMETERS ---
SEED = 42
N_FEATURES = 10000
CHUNK_SIZE = int(N_FEATURES / 10)  # Exactly 10% of N_FEATURES
N_CLASSES = 100             
TRAIN_ROWS = 70000          
TEST_ROWS = 30000           
STD_DEV = 7                        # Used for generating feature-wise noise scales

train_dir = "midterm_dataset/train"
test_dir = "midterm_dataset/test"

# ──────────────────────────────────────────────────────────────────────────────
# Step 1: Delete and Recreate Directories (Wipe clean before run)
# ──────────────────────────────────────────────────────────────────────────────
print("Cleaning up old project directories...")
for directory in [train_dir, test_dir]:
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f" -> Cleared existing directory: {directory}")
    os.makedirs(directory, exist_ok=True)

start_time = time.time()

# Set the global seed for reproducibility across all random generations
np.random.seed(SEED)

# ──────────────────────────────────────────────────────────────────────────────
# Step 2: Prepare Full Noiseless Base & Dynamic SIGMA Vector
# ──────────────────────────────────────────────────────────────────────────────
print("\nGenerating full noiseless base rules matrix...")
noiseless_base = np.random.standard_normal((N_CLASSES, N_FEATURES)).astype(np.float32)
for i in range(N_CLASSES):
    noiseless_base[i, :] += i

# Updated dynamically to use your STD_DEV variable
print(f"Generating fixed feature-wise SIGMA vector (std={STD_DEV})...")
SIGMA_VECTOR = np.abs(np.random.normal(0, STD_DEV, size=N_FEATURES)).astype(np.float32)

# Pre-generate target label blueprints
train_labels = np.repeat(np.arange(N_CLASSES), int(TRAIN_ROWS / N_CLASSES))
test_labels = np.repeat(np.arange(N_CLASSES), int(TEST_ROWS / N_CLASSES))

np.random.shuffle(train_labels)
np.random.shuffle(test_labels)

# ──────────────────────────────────────────────────────────────────────────────
# Step 3: Save Target Labels with Uppercase Parameters Metadata
# ──────────────────────────────────────────────────────────────────────────────
print("Saving target label blueprints and encoding metadata parameters...")

# Pack all uppercase parameters into a text-based dictionary for the Parquet footer
generation_metadata = {
    "SEED": str(SEED),
    "N_FEATURES": str(N_FEATURES),
    "CHUNK_SIZE": str(CHUNK_SIZE),
    "N_CLASSES": str(N_CLASSES),
    "TRAIN_ROWS": str(TRAIN_ROWS),
    "TEST_ROWS": str(TEST_ROWS),
    "STD_DEV": str(STD_DEV)
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
# Step 4: The Column-Chunk Loop (Iterative Disk Writing)
# ──────────────────────────────────────────────────────────────────────────────
print(f"\nStarting column-chunk loop. Processing {CHUNK_SIZE} features per iteration...")

for col_start in range(0, N_FEATURES, CHUNK_SIZE):
    col_end = min(col_start + CHUNK_SIZE, N_FEATURES)
    
    # Slice the corresponding chunk of the fixed SIGMA vector for these features
    SIGMA_chunk = SIGMA_VECTOR[col_start:col_end]
    
    # --- TRAINING CHUNK ---
    train_chunk = noiseless_base[train_labels, col_start:col_end]
    train_noise = np.random.standard_normal(size=train_chunk.shape).astype(np.float32) * SIGMA_chunk
    train_chunk += train_noise
    
    train_feature_names = [f"f_{j}" for j in range(col_start, col_end)]
    train_columns = [pa.array(train_chunk[:, c]) for c in range(train_chunk.shape[1])]
    train_table = pa.Table.from_arrays(train_columns, names=train_feature_names)
    pq.write_table(train_table, f"{train_dir}/features_{col_start}_{col_end}.parquet", compression="snappy")
    
    # --- TESTING CHUNK ---
    test_chunk = noiseless_base[test_labels, col_start:col_end]
    test_noise = np.random.standard_normal(size=test_chunk.shape).astype(np.float32) * SIGMA_chunk
    test_chunk += test_noise
    
    test_columns = [pa.array(test_chunk[:, c]) for c in range(test_chunk.shape[1])]
    test_table = pa.Table.from_arrays(test_columns, names=train_feature_names)
    pq.write_table(test_table, f"{test_dir}/features_{col_start}_{col_end}.parquet", compression="snappy")
    
    print(f" -> Successfully flushed column chunk: features {col_start} to {col_end} to disk.")

print("\n" + "="*60)
print("SUCCESS: Vertically partitioned dataset complete!")
print("Stored in folder: contents of 'midterm_dataset/'")
print(f"Total Runtime: {time.time() - start_time:.2f} seconds")
print("="*60)
