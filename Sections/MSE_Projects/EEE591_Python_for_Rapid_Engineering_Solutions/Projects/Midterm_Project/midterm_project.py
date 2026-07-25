import pyarrow.parquet as pq    # Install pyarrow
import numpy as np


N_FEATURES = 10000
CHUNK_SIZE = int(N_FEATURES / 10)  # Dynamically set to 10% of total features
TRAIN_DIR = "midterm_dataset/train"
TEST_DIR = "midterm_dataset/test"

# This is an example on how to read a chunck of the features of the training dataset:
X_train_chunk = pq.read_table(f"{TRAIN_DIR}/features_1000_2000.parquet").to_pandas().to_numpy()
print(np.shape(X_train_chunk))

# This is an example on how to read the testing labels of the dataset:
y_test = pq.read_table(f"{TEST_DIR}/labels_param.parquet").to_pandas()["class_label"].to_numpy()
print(np.shape(y_test))

