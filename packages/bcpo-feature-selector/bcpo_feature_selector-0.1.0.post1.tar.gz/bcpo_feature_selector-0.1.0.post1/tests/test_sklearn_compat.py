from sklearn.utils.estimator_checks import check_estimator
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from bcpo_feature_selector.classification import BCPOClassifierSelector
from bcpo_feature_selector.regression import BCPORegressorSelector


def test_classifier_compatibility():
    """Check BCPOClassifierSelector compliance with scikit-learn standards."""
    # We use DecisionTree to have a deterministic base estimator if
    # random_state is fixed
    clf_selector = BCPOClassifierSelector(
        estimator=DecisionTreeClassifier(random_state=42),
        random_state=42,
        max_iter=2,
        num_agents=5
    )
    # check_estimator calls fit, transform, ensuring strict sklearn compliance
    check_estimator(clf_selector)


def test_regressor_compatibility():
    """Check BCPORegressorSelector compliance with scikit-learn standards."""
    reg_selector = BCPORegressorSelector(
        estimator=DecisionTreeRegressor(random_state=42),
        random_state=42,
        max_iter=2,
        num_agents=5
    )
    check_estimator(reg_selector)
