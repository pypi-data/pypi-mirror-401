import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge

from bcpo_feature_selector.classification import BCPOClassifierSelector
from bcpo_feature_selector.regression import BCPORegressorSelector


def test_bcpo_feature_selector_smoke():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        num_agents=10,
        max_iter=5,
        random_state=42,
    )
    selector.fit(X, y)

    Xt = selector.transform(X)
    assert Xt.shape[0] == X.shape[0]
    assert 1 <= Xt.shape[1] <= X.shape[1]
    assert np.isfinite(selector.best_fitness_)
    assert 0.0 <= selector.best_score_ <= 1.0


def test_max_features_callable_resolves_and_caps():
    X, y = load_breast_cancer(return_X_y=True)

    def half_callable(X_):
        return round(X_.shape[1] / 2)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        num_agents=10,
        max_iter=5,
        random_state=0,
        max_features=half_callable,
    )
    selector.fit(X, y)

    assert selector.max_features_ == half_callable(X)
    assert selector.get_support().sum() <= selector.max_features_


def test_bcpo_supports_f1_metric():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        metric="f1",
        num_agents=8,
        max_iter=3,
        random_state=0,
    )
    selector.fit(X, y)

    assert selector.metric_name_ == "f1"
    assert 0.0 <= selector.best_score_ <= 1.0


def test_bcpo_supports_precision_metric():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        metric="precision",
        num_agents=8,
        max_iter=3,
        random_state=0,
    )
    selector.fit(X, y)

    assert selector.metric_name_ == "precision"
    assert 0.0 <= selector.best_score_ <= 1.0


def test_bcpo_supports_recall_metric():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        metric="recall",
        num_agents=8,
        max_iter=3,
        random_state=0,
    )
    selector.fit(X, y)

    assert selector.metric_name_ == "recall"
    assert 0.0 <= selector.best_score_ <= 1.0


def test_bcpo_supports_roc_auc_metric_when_proba_available():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=LogisticRegression(max_iter=20000, solver="lbfgs"),
        metric="roc_auc",
        num_agents=8,
        max_iter=3,
        random_state=0,
    )
    selector.fit(X, y)

    assert selector.metric_name_ == "roc_auc"
    assert 0.0 <= selector.best_score_ <= 1.0


def test_bcpo_max_features_is_respected():
    X, y = load_breast_cancer(return_X_y=True)

    selector = BCPOClassifierSelector(
        estimator=GaussianNB(),
        max_features=5,
        num_agents=10,
        max_iter=5,
        random_state=42,
    )
    selector.fit(X, y)

    assert selector.support_.sum() <= 5


def test_bcpo_regression_feature_selector_smoke():
    X, y = load_diabetes(return_X_y=True)

    selector = BCPORegressorSelector(
        estimator=Ridge(),
        metric="neg_root_mean_squared_error",
        num_agents=10,
        max_iter=5,
        random_state=42,
    )
    selector.fit(X, y)

    Xt = selector.transform(X)
    assert Xt.shape[0] == X.shape[0]
    assert 1 <= Xt.shape[1] <= X.shape[1]
    assert np.isfinite(selector.best_fitness_)
    assert np.isfinite(selector.best_loss_)


def test_bcpo_regression_respects_max_features():
    X, y = load_diabetes(return_X_y=True)

    selector = BCPORegressorSelector(
        estimator=Ridge(),
        metric="neg_mean_absolute_error",
        max_features=3,
        num_agents=10,
        max_iter=5,
        random_state=0,
    )
    selector.fit(X, y)

    assert selector.get_support().sum() <= 3
