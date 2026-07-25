import numpy as np
import pyarrow.parquet as pq


# # --- CONFIGURATION MATCHING THE CHUNK DATASET ---
# DATASET_DIR = "final_dataset"
# TRAIN_DIR = f"{DATASET_DIR}/train"
# TEST_DIR = f"{DATASET_DIR}/test"

# # This is an example on how to read a chunk of the features of the training dataset:
# X_train_chunk = pq.read_table(f"{TRAIN_DIR}/features_1000_2000.parquet").to_pandas().to_numpy()
# print(np.shape(X_train_chunk))

# # This is an example on how to read the testing labels of the dataset:
# y_test = pq.read_table(f"{TEST_DIR}/labels_param.parquet").to_pandas()["class_label"].to_numpy()
# print(np.shape(y_test))

# ──────────────────────────────────────────────────────────────────────────────
# Print Your Name and ASU ID number:
# ──────────────────────────────────────────────────────────────────────────────
NAME = "FIRST LAST"
ASU_ID = 123456789
print("\n" + "="*70)
print("START CODE FOR",NAME, "ASU ID:", ASU_ID)

# ──────────────────────────────────────────────────────────────────────────────
# Imputation-Based Method:
# ──────────────────────────────────────────────────────────────────────────────
print("\nImputation-Based Method: PROVIDE ALGORITHM NAME")
##### YOUR IMPUTATION-BASED ALGORITHM GOES HERE

# Printing Accuracy and "Imputation-Based Justification" comment paragraph:
imp_based_acc = 1
# print("Imputation-Based Accuracy:", imp_based_acc)
print("Imputation-Based Justification:")
print("    PROVIDE YOUR COMMENT PARAGRAPH HERE. IT MUST PRINT NICELY")

# ──────────────────────────────────────────────────────────────────────────────
# Imputation-Free Method:
# ──────────────────────────────────────────────────────────────────────────────
print("\nImputation-Free Method: PROVIDE ALGORITHM NAME")
##### YOUR IMPUTATION-FREE ALGORITHM GOES HERE

# Printing Accuracy and "Imputation-Based Justification" comment paragraph:
imp_free_acc = 1
print("Imputation-Free Accuracy:", imp_free_acc)
print("Imputation-Free Justification:")
print("    PROVIDE YOUR COMMENT PARAGRAPH HERE. IT MUST PRINT NICELY")


# ──────────────────────────────────────────────────────────────────────────────
# Conclusion:
# ──────────────────────────────────────────────────────────────────────────────
print("\nConclusion:")
# Print accuracy for each method again
# print("Imputation-Based Accuracy:", imp_based_acc)
# print("Imputation-Free Accuracy:", imp_free_acc)

# Then print "Conclusion Paragraph":
print("Conclusion Comment:")
print("    PROVIDE YOUR COMMENT PARAGRAPH HERE. IT MUST PRINT NICELY")

print("\nEND CODE FOR",NAME, "ASU ID:", ASU_ID)
print("="*70)
