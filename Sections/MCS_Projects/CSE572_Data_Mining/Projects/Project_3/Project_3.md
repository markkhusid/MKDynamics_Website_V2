# CSE572 Data Mining - Project 3 - Cluster Validation

Created with Grok Build

## Problem

The question was whether an unsupervised clustering of meal glucose windows recovers the carbohydrate amount of the meal. Carbohydrate entries in the pump log were the ground truth. Glucose windows were the observations.

## Approach

Carbohydrate amounts were divided into six bins between the smallest and largest intake. Those bins were the labels used only for scoring, after clustering.

Meal glucose windows were extracted the same way as in Project 2, then cleaned. Missing samples were filled with a K-nearest-neighbors imputer. The same style of features was computed and scaled so that a feature with a large numeric range would not dominate distance calculations.

K-means was fit first and viewed in the first two principal components. DBSCAN was fit on the same scaled features. Each clustering was compared with the six carbohydrate bins. Agreement was scored with entropy and purity. Entropy falls when a cluster contains one bin. Purity rises when one bin dominates a cluster.

## Result

K-means and DBSCAN both mis-assigned bins 1 and 4. The two partitions still looked different, which follows from how they group points: K-means pulls points toward a centroid, and DBSCAN keeps points that sit in a dense neighborhood. Across the clusters, DBSCAN had the lower entropy and K-means had the higher purity. Neither partition reproduced the carbohydrate bins.
