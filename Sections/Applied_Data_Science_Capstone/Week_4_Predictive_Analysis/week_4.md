# Week 4 — Classification

The saved run predicts `Class` from the feature table built in week 2. It standardizes the features, splits off 18 test rows, and searches four models with 10-fold cross-validation. The score is accuracy. The test score is the one that counts.

| Algorithm | Test accuracy | Best cross-validation score |
| --- | ---: | ---: |
| Logistic regression | 0.833 | 0.846 |
| Support vector machine | 0.833 | 0.848 |
| Decision tree | 0.667 | 0.875 |
| K nearest neighbors | 0.833 | 0.848 |

Logistic regression, the support vector machine, and k-nearest neighbors tie at 0.833 on the test rows. The decision tree's cross-validation score is 0.875 and its test accuracy is 0.667.

The block below is the search that produced this table. It is a record of that run. The site build does not fit the models again. `max_features="auto"` was accepted by the scikit-learn used in 2022. Current scikit-learn rejects it and expects `"sqrt"`.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

flights = pd.read_csv("dataset_part_2.csv")
features = pd.read_csv("dataset_part_3.csv")
X = StandardScaler().fit_transform(features.to_numpy(dtype=float))
y = flights["Class"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=2
)

searches = {
    "logistic regression": (
        LogisticRegression(),
        {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]},
    ),
    "support vector machine": (
        SVC(),
        {
            "kernel": ["linear", "rbf", "poly", "sigmoid"],
            "C": np.logspace(-3, 3, 5),
            "gamma": np.logspace(-3, 3, 5),
        },
    ),
    "decision tree": (
        DecisionTreeClassifier(),
        {
            "criterion": ["gini", "entropy"],
            "splitter": ["best", "random"],
            "max_depth": [2 * n for n in range(1, 10)],
            "max_features": ["auto", "sqrt"],
            "min_samples_leaf": [1, 2, 4],
            "min_samples_split": [2, 5, 10],
        },
    ),
    "k nearest neighbors": (
        KNeighborsClassifier(),
        {
            "n_neighbors": list(range(1, 11)),
            "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
            "p": [1, 2],
        },
    ),
}

fitted = {}
for name, (model, grid) in searches.items():
    search = GridSearchCV(model, grid, scoring="accuracy", cv=10)
    search.fit(X_train, y_train)
    fitted[name] = {
        "cv_score": search.best_score_,
        "test_accuracy": search.score(X_test, y_test),
        "confusion_matrix": confusion_matrix(y_test, search.predict(X_test)),
    }
```

`X` is the 90 by 72 dummy matrix from week 2, after `StandardScaler`. `test_size=0.2` and `random_state=2` hold out 18 rows. `fitted[...]["test_accuracy"]` is the test column above, and `fitted[...]["cv_score"]` is the cross-validation column.

## Confusion matrices

Logistic regression, the support vector machine, and k-nearest neighbors produced the same matrix on the 18 test rows. Three flights that did not land were predicted as landings, and all 12 flights that landed were predicted as landings. That is (3 + 12) / 18 = 0.833.

```{figure} ../images/cm_logistic_regression.png
:alt: Confusion matrix shared by logistic regression, the support vector machine, and k-nearest neighbors.
:align: center
:class: clickable-figure

Shared test matrix for logistic regression, the support vector machine, and k-nearest neighbors. Rows are the true label and columns are the prediction.
```

The decision tree misses three landings and three flights that did not land. That is (3 + 9) / 18 = 0.667.

```{figure} ../images/cm_decision_tree.png
:alt: Confusion matrix for the decision tree on the 18 test rows.
:align: center
:class: clickable-figure

Decision tree on the same 18 test rows.
```

## Score comparison

```{figure} ../images/best_cv_score.png
:alt: Bar chart of the best cross-validation score for each classifier.
:align: center
:class: clickable-figure

Best cross-validation score. The decision tree is the tallest bar, at 0.875.
```

```{figure} ../images/test_accuracy.png
:alt: Bar chart of test accuracy for each classifier.
:align: center
:class: clickable-figure

Test accuracy. Logistic regression, the support vector machine, and k-nearest neighbors are equal at 0.833, and the decision tree is at 0.667.
```
