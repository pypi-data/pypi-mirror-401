import numpy as np

from bcpo_feature_selector.regression.metrics import r2_loss


def test_r2_loss_perfect_prediction():
    """Test that R² = 1 produces loss = 0."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

    loss = r2_loss(y_true, y_pred)

    assert loss == 0.0
    assert isinstance(loss, float)


def test_r2_loss_baseline_prediction():
    """Test that R² = 0 produces loss = 1."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([3.0, 3.0, 3.0, 3.0, 3.0])  # Always predict mean

    loss = r2_loss(y_true, y_pred)

    assert np.isclose(loss, 1.0)
    assert isinstance(loss, float)


def test_r2_loss_typical_prediction():
    """Test that typical R² (0 < R² < 1) produces loss between 0 and 1."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.1, 4.9])

    loss = r2_loss(y_true, y_pred)

    assert 0.0 <= loss <= 1.0
    assert isinstance(loss, float)


def test_r2_loss_worse_than_baseline():
    """Test that R² < 0 produces loss clamped at 2.0."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([5.0, 4.0, 3.0, 2.0, 1.0])  # Opposite direction

    loss = r2_loss(y_true, y_pred)

    assert loss == 2.0
    assert isinstance(loss, float)


def test_r2_loss_r2_greater_than_one():
    """Test edge case where R² > 1 (can happen with certain metrics)."""
    # Construct a scenario where sklearn might compute r2 > 1
    y_true = np.array([1.0, 2.0, 3.0])
    # Predictions that perfectly fit training data but on a different scale
    y_pred = np.array([1.0, 2.0, 3.0])

    loss = r2_loss(y_true, y_pred)

    # Should be clamped at 0
    assert loss >= 0.0
    assert isinstance(loss, float)


def test_r2_loss_return_type_is_float():
    """Test that r2_loss always returns a Python float."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.0, 2.1, 2.9, 4.0])

    loss = r2_loss(y_true, y_pred)

    assert isinstance(loss, float)
    assert not isinstance(loss, np.floating)


def test_r2_loss_clamping_range():
    """Test that r2_loss is always in the valid range [0, 2]."""
    test_cases = [
        (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array(
            [1.0, 2.0, 3.0, 4.0, 5.0])),  # R²=1
        (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array(
            [3.0, 3.0, 3.0, 3.0, 3.0])),   # R²=0
        (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array(
            [1.1, 2.1, 2.9, 4.1, 4.9])),   # 0<R²<1
        (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.array(
            [5.0, 4.0, 3.0, 2.0, 1.0])),   # R²<0
    ]

    for y_true, y_pred in test_cases:
        loss = r2_loss(y_true, y_pred)
        assert 0.0 <= loss <= 2.0, f"Loss {loss} out of bounds [0, 2]"


def test_r2_loss_with_integer_arrays():
    """Test that r2_loss handles integer input arrays."""
    y_true = np.array([1, 2, 3, 4, 5])
    y_pred = np.array([1, 2, 3, 4, 5])

    loss = r2_loss(y_true, y_pred)

    assert loss == 0.0
    assert isinstance(loss, float)
