# bcpo-feature-selector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**bcpo-feature-selector** is a Python library that implements the **Binary Crested Porcupine Optimizer (BCPO)** for feature selection. It provides a robust, `scikit-learn` compatible interface to select the optimal subset of features for both classification and regression tasks.

The library is based on the Crested Porcupine Optimizer (CPO), a nature-inspired meta-heuristic algorithm that mimics the defensive behaviors of the crested porcupine. By adapting CPO to a binary search space, `bcpo-feature-selector` efficiently explores the feature space to maximize model performance while minimizing the number of selected features.

## Key Features

-   **Scikit-learn Compatibility**: Designed to work seamlessly with `scikit-learn` estimators, pipelines, and cross-validation tools.
-   **Dual Support**: Supports both **Classification** (`BCPOClassifierSelector`) and **Regression** (`BCPORegressorSelector`) tasks.
-   **Customizable Metrics**: Optimizes for various built-in metrics (Accuracy, F1-score, ROC-AUC, MAE, MSE, R2) or accepts custom scoring functions.
-   **Efficiency**: Leverages swarm intelligence to solve the NP-hard problem of feature selection more efficiently than exhaustive search.

## Installation

### From PyPI

You can install the package directly from PyPI:

```bash
pip install bcpo-feature-selector
```

### From Source

This project uses `pyproject.toml`. You can install it directly from the source:

```bash
# Clone the repository
git clone https://github.com/ThienNguyen3001/bcpo-feature-selector.git
cd bcpo-feature-selector

# Install in editable mode
pip install -e .
```

For development (including testing dependencies):

```bash
pip install -e .[dev]
```

## Quick Start

### Classification Example

Optimize accuracy using a Naive Bayes classifier on the Breast Cancer dataset.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from bcpo_feature_selector.classification import BCPOClassifierSelector

# Load data
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize selector
selector = BCPOClassifierSelector(
    estimator=GaussianNB(),
    metric="accuracy",
    num_agents=30,
    max_iter=50,
    random_state=42,
    verbose=1
)

# Fit and transform
selector.fit(X_train, y_train)
X_train_selected = selector.transform(X_train)
X_test_selected = selector.transform(X_test)

# Evaluate
print(f"Original features: {X.shape[1]}")
print(f"Selected features: {X_train_selected.shape[1]}")
print(f"Selected indices: {selector.get_support(indices=True)}")

# Train a model on selected features
model = GaussianNB()
model.fit(X_train_selected, y_train)
y_pred = model.predict(X_test_selected)
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
```

### Regression Example

Optimize Mean Absolute Error (MAE) using ElasticNet on the Diabetes dataset.

```python
from sklearn.datasets import load_diabetes
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from bcpo_feature_selector.regression import BCPORegressorSelector

# Load data
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize selector (Note: for regression, metrics like 'mae', 'mse' are minimized internally)
selector = BCPORegressorSelector(
    estimator=ElasticNet(random_state=42),
    metric="neg_mean_absolute_error",
    num_agents=20,
    max_iter=30,
    random_state=42
)

# Fit
selector.fit(X_train, y_train)

# Transform
X_train_sel = selector.transform(X_train)
X_test_sel = selector.transform(X_test)

print(f"Best internal validation score (MAE): {selector.best_score_:.4f}")
print(f"Features reduced from {X.shape[1]} to {X_train_sel.shape[1]}")
```

## Configuration

The `BCPOClassifierSelector` and `BCPORegressorSelector` expose several parameters to control the optimization process:

-   `estimator`: The base estimator used to evaluate feature subsets. If None, uses `KNeighborsClassifier` (n_neighbors=5) for classification and `Ridge` regression for regression.
-   `metric`: The metric to optimize.
    -   **Classification**: `'accuracy'`, `'f1'`, `'precision'`, `'recall'`, `'roc_auc'`.
    -   **Regression**: `'neg_mean_squared_error'`, `'neg_root_mean_squared_error'`, `'neg_mean_absolute_error'`, `'r2'`.
-   `metric_average`: (Classification only) Averaging method for multi-class metrics (e.g., `'binary'`, `'micro'`, `'macro'`, `'weighted'`). Default is `'binary'`.
-   `num_agents`: Number of search agents (population size). Higher values explore more but are slower (default: 30).
-   `max_iter`: Maximum number of iterations for the optimization (default: 100).
-   `max_features`: The maximum number of features to select. Can be an integer, a callable, or None (default: None).
-   `test_size`: Proportion of the dataset to include in the internal validation split (default: 0.3).
-   `w_error` (Classification) / `w_loss` (Regression): Weight for the error/loss component in the fitness function (default: 0.99).
-   `w_feat`: Weight for the feature reduction component (default: 0.01).
-   `t_cycle`: Cycle length parameter for the population reduction mechanism (default: 2).
-   `n_min`: Minimum number of agents to keep during population reduction (default: 5).
-   `alpha_max`: Maximum value for the alpha parameter in the update rule (default: 0.2).
-   `verbose`: Level of verbosity (0, 1, or 2).

### The Fitness Function

The library uses a weighted fitness function to balance prediction performance and dimensionality reduction:

$$ Fitness = \alpha \times Error + \beta \times \frac{|S|}{|Total|} $$

Where:
- $Error = 1 - Metric$ (for maximization metrics) or the normalized loss (for regression).
- $|S|$ is the number of selected features.
- $\alpha$ (`w_error` or `w_loss`) and $\beta$ (`w_feat`) control the trade-off.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to report bugs, suggest features, or submit pull requests.

This project enforces a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

