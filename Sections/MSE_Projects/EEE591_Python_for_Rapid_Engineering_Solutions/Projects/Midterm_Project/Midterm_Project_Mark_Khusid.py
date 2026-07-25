#!/usr/bin/env python
# coding: utf-8

# In[1]:


##########################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - Midterm_Project_Mark_Khusid.py
# Mark Khusid
##########################################################################################

##########################################################################################
# Midterm Project
##########################################################################################


# # Midterm Project

# ## Import Libraries

# In[2]:


import numpy as np
import pyarrow.parquet as pq
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import time


# ## Define Constants and Directories

# In[3]:


N_FEATURES = 10000
CHUNK_SIZE = 1000
TRAIN_DIR = "midterm_dataset/train"
TEST_DIR = "midterm_dataset/test"


# ## Define Functions

# ### Define load_chunk() Function

# In[4]:


def load_chunk(start, dataset="train", chunk_size=CHUNK_SIZE):
    """
    Load a contiguous chunk of feature data from Parquet files.

    This function assumes data has been pre-split into fixed-size chunks
    saved as `features_{start}_{end}.parquet` in TRAIN_DIR or TEST_DIR.
    Useful for memory-efficient training/inference on large datasets.

    Args:
        start (int): Starting index of the chunk (inclusive).
        dataset (str): Either "train" or "test". Defaults to "train".
        chunk_size (int): Number of samples in the chunk. 
                         Must match the chunking used during data preparation.

    Returns:
        np.ndarray: Feature matrix of shape (chunk_size, n_features).

    Raises:
        FileNotFoundError: If the corresponding Parquet file doesn't exist.
        Other exceptions from pyarrow/pandas if the file is corrupted.
    """
    # Calculate the end index (exclusive, following Python slicing convention)
    end = start + chunk_size

    # Determine the correct base directory based on dataset type
    if dataset == "train":
        directory = TRAIN_DIR
    else:
        directory = TEST_DIR

    # Construct the filename using the established naming convention
    # This assumes consistent chunking across the entire dataset
    filename = f"{directory}/features_{start}_{end}.parquet"

    # Read the Parquet file using PyArrow (fast columnar format)
    # Then convert to pandas DataFrame and finally to NumPy array
    # This chain is common but has some overhead
    table = pq.read_table(filename)           # pq is pyarrow.parquet
    df = table.to_pandas()                    # Preserves dtypes, handles categoricals well
    return df.to_numpy()                      # Returns float64 by default (or object if mixed)


# ### Define load_labels() Function

# In[5]:


def load_labels(dataset: str = "train") -> np.ndarray:
    """
    Load the full set of class labels for the specified dataset.

    This function reads a single Parquet file containing labels.
    Unlike load_chunk(), this loads the entire label vector at once
    (labels files are typically much smaller than feature chunks).

    Args:
        dataset (str): Either "train" or "test". Defaults to "train".

    Returns:
        np.ndarray: 1D array of class labels, shape (n_samples,).
                    dtype is usually int32/int64 depending on your label encoding.

    Raises:
        FileNotFoundError: If the labels file is missing.
        KeyError: If the 'class_label' column does not exist in the file.
    """
    # Select the correct directory
    if dataset == "train":
        directory = TRAIN_DIR
    else:
        directory = TEST_DIR

    # Build the filename using consistent naming convention
    filename = f"{directory}/labels_param.parquet"

    # Read only the needed column directly with PyArrow (more memory efficient)
    # Avoid loading the entire table if the file has extra columns.
    table = pq.read_table(filename, columns=["class_label"])

    # Convert to pandas → select column → to numpy
    # The parentheses allow nice multi-line chaining
    return (
        table
        .to_pandas()
        ["class_label"]
        .to_numpy()
    )


# ### Define rank_features_by_f_score() Function

# In[6]:


def rank_features_by_f_score(y_train: np.ndarray) -> list[tuple[int, float]]:
    """
    Rank all features by their ANOVA F-score (univariate feature selection).

    This function processes features in chunks to keep memory usage low
    when dealing with very high-dimensional data (common in your engineering/ML projects).
    It uses `sklearn.feature_selection.f_classif` which computes the ANOVA
    F-value between each feature and the target labels.

    Args:
        y_train (np.ndarray): 1D array of class labels for the training set.
                             Length must match total number of training samples.

    Returns:
        list[tuple[int, float]]: List of (global_feature_index, f_score) sorted
                                 by score in descending order (best features first).

    Notes:
        - Requires `N_FEATURES` and `CHUNK_SIZE` to be defined globally.
        - Assumes `load_chunk()` returns shape (n_samples, chunk_size).
    """
    all_scores: list[tuple[int, float]] = []

    # Iterate over feature chunks (memory-efficient processing)
    for start in range(0, N_FEATURES, CHUNK_SIZE):
        print(f"Scoring features {start}-{start + CHUNK_SIZE - 1}")  # improved end index

        # Load one chunk of features (n_samples x chunk_features)
        X_chunk = load_chunk(
            start,
            dataset="train",
            chunk_size=CHUNK_SIZE
        )

        # Compute F-scores for this chunk only
        # f_classif returns (scores, pvalues); we discard p-values
        scores, _ = f_classif(X_chunk, y_train)

        # Map local chunk indices back to global feature indices
        for local_index, score in enumerate(scores):
            global_index = start + local_index
            all_scores.append((global_index, score))

        # Explicitly free memory — important for large feature spaces
        del X_chunk

    # Sort by F-score descending (highest discriminative power first)
    all_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return all_scores


# ### Define build_selected_matrix() Function

# In[7]:


def build_selected_matrix(
    selected_features: list[int] | np.ndarray, 
    dataset: str = "train"
) -> np.ndarray:
    """
    Build a reduced feature matrix containing only the selected features.

    This function loads feature chunks one at a time (memory-efficient) 
    and extracts only the columns corresponding to the selected global 
    feature indices. Ideal for high-dimensional data after feature ranking/selection.

    Args:
        selected_features (list[int] | np.ndarray): List or array of 
            global feature indices to keep (0-based). Can be unsorted.
        dataset (str): "train" or "test". Defaults to "train".

    Returns:
        np.ndarray: Feature matrix of shape (n_samples, n_selected_features).
                    Columns appear in the order of `selected_features`.

    Raises:
        ValueError: If selected_features are out of range or invalid.
        FileNotFoundError / other: Propagated from load_chunk().
    """
    # Convert to numpy array once for fast operations
    selected_features = np.asarray(selected_features, dtype=int)

    if len(selected_features) == 0:
        return np.empty((0, 0))  # or raise error depending on use case

    # Optional but strongly recommended: sort indices for predictable column order
    # and better cache locality. If you want to preserve input order, skip this.
    # sort_idx = np.argsort(selected_features)
    # selected_features = selected_features[sort_idx]

    X_parts: list[np.ndarray] = []

    # Process one chunk at a time
    for start in range(0, N_FEATURES, CHUNK_SIZE):
        end = start + CHUNK_SIZE

        # Create boolean mask for features belonging to this chunk
        mask = (selected_features >= start) & (selected_features < end)
        features_in_chunk = selected_features[mask]

        if len(features_in_chunk) == 0:
            continue

        # Convert global indices → local column indices in this chunk
        local_indices = features_in_chunk - start

        print(
            f"Loading selected features from chunk "
            f"{start}-{end-1}: {len(local_indices)} features"
        )

        # Load full chunk (n_samples x CHUNK_SIZE)
        X_chunk = load_chunk(
            start,
            dataset=dataset,
            chunk_size=CHUNK_SIZE
        )

        # Extract only the needed columns
        X_parts.append(X_chunk[:, local_indices])

        # Free memory immediately
        del X_chunk
        # gc.collect()  # uncomment if you experience memory pressure

    if not X_parts:
        return np.empty((load_chunk(0, dataset, 1).shape[0], 0))  # empty matrix with correct rows

    # Horizontally stack all extracted parts
    # Order will match the order of selected_features (after any sorting)
    X_selected = np.hstack(X_parts)

    return X_selected


# ## Load Data, Obtain F-Scores and Select Top Features

# In[8]:


import time

# Start timing the entire feature selection pipeline
start_time = time.time()

# Load full label vectors (small files, loaded entirely into memory)
print()
print("Loading label data into memory")
y_train = load_labels("train")
y_test = load_labels("test")

# Compute univariate F-scores across all features using chunked processing
print()
print("Obtaining feature F-scores")
feature_scores = rank_features_by_f_score(y_train)

# Define how many top features to keep
TOP_FEATURES = 300

# Extract the top-K feature indices (already sorted best → worst by rank_features_by_f_score)
selected_features = [
    feature_index
    for feature_index, score in feature_scores[:TOP_FEATURES]
]

# Optional: Convert to numpy array for faster downstream use
# selected_features = np.array(selected_features, dtype=int)
print()
print("Top selected features (first 20):")
print(selected_features[:20])
print()
# Report total time for this stage
elapsed = time.time() - start_time
print(f"Feature ranking + selection completed in {elapsed:.1f} seconds "
      f"({TOP_FEATURES} features kept)")


# ## Build Training and Testing Matrices from Selected Features

# In[9]:


# Build reduced feature matrices using only the top selected features
# This step loads data in chunks and extracts only the relevant columns,
# keeping memory usage manageable even for very high-dimensional datasets.
print()
print("Building selected training matrix")
X_train_selected = build_selected_matrix(
    selected_features,
    dataset="train"
)

print()
print("Building selected testing matrix")
X_test_selected = build_selected_matrix(
    selected_features,
    dataset="test"
)

# Report shapes to verify correctness
print()
print("Selected train shape:", X_train_selected.shape)
print("Selected test shape:", X_test_selected.shape)
print()
print(f"Successfully reduced from {N_FEATURES:,} to "
      f"{X_train_selected.shape[1]:,} features")


# ## Scale Selected Features with StandardScaler()

# In[10]:


print()
print("Scaling selected features...")
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_selected)
X_test_scaled = scaler.transform(X_test_selected)

print()
print(f"Scaled train shape: {X_train_scaled.shape}")
print(f"Scaled test shape : {X_test_scaled.shape}")


# ## Apply Principle Component Analysis

# In[11]:


print()
print("Applying PCA for further dimensionality reduction...")

N_PCA_COMPONENTS = 30

pca = PCA(
    n_components=N_PCA_COMPONENTS,
    random_state=42
)

# Fit + transform on training data
X_train_pca = pca.fit_transform(X_train_scaled)

# Transform test data using the fitted PCA
X_test_pca = pca.transform(X_test_scaled)

# Evaluate retained variance
total_explained = np.sum(pca.explained_variance_ratio_)
print(f"Total explained variance ratio with {N_PCA_COMPONENTS} components: "
      f"{total_explained:.4f} ({total_explained*100:.2f}%)")
print()

print(f"PCA completed -> X_train_pca shape: {X_train_pca.shape}")


# In[12]:


#X_train_selected[1:2]


# In[13]:


#X_train_pca[0:1]


# In[14]:


#y_train[0:10]


# ## Train Neural Network, Make Predictions and Report Accuracy

# In[15]:


print()
print("Instantiating Multi-Layer Perceptron (Neural Network)...")
# Initialize a Multi-Layer Perceptron (MLP) classifier from scikit-learn
# This is a basic feed-forward neural network suitable for classification.
clf = MLPClassifier(
    hidden_layer_sizes=(100,),      # Single hidden layer with 100 neurons
    activation="relu",              # ReLU is the modern default — fast and helps with vanishing gradients
    max_iter=100,                   # Maximum training epochs (this is relatively low)
    random_state=42,                # For reproducible results
    early_stopping=True             # Automatically stops if validation score doesn't improve
    # Other useful params you might want:
    # solver='adam', alpha=0.0001 (L2 regularization), learning_rate_init=0.001,
    # validation_fraction=0.1, n_iter_no_change=10
)

print()
print("Training Neural Network...")
# Train the model on the PCA-reduced, scaled training data
# Note: MLP benefits greatly from the scaling + PCA you did earlier
clf.fit(X_train_pca, y_train)

print()
print("Obtaining predictions.....")
# Generate predictions on the test set
y_pred = clf.predict(X_test_pca)

print()
print("Predictions completed....")
print()

# Compute overall accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"Final validation accuracy: {accuracy:.4f}")
print(f"Total execution time: {time.time() - start_time:.2f} seconds")


# ## Plots

# In[16]:


#import matplotlib.pyplot as plt

#plt.figure(figsize=(8,5))

#plt.plot(
#    clf.loss_curve_,
#    linewidth=2
#)

#plt.xlabel("Epoch")
#plt.ylabel("Training Loss")
#plt.title("MLP Training Loss vs Epoch")
#plt.grid(True)
#plt.tight_layout()
#plt.show()


# In[17]:


#plt.figure(figsize=(8,5))

#plt.plot(
#    clf.validation_scores_,
#    linewidth=2
#)

#plt.xlabel("Epoch")
#plt.ylabel("Validation Accuracy")
#plt.title("MLP Validation Accuracy vs Epoch")
#plt.grid(True)
#plt.tight_layout()
#plt.show()


# In[18]:


#print(f"Final training loss: {clf.loss_curve_[-1]:.6f}")

#if hasattr(clf, "validation_scores_"):
#    print(f"Final internal validation accuracy: {clf.validation_scores_[-1]:.4f}")
#    print(f"Best internal validation accuracy: {max(clf.validation_scores_):.4f}")


# In[19]:


#y_pred = clf.predict(X_test_pca)

#accuracy = accuracy_score(y_test, y_pred)

#print(f"Final test accuracy: {accuracy:.4f}")

