from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.feature_selection import SelectorMixin
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import check_is_fitted, check_X_y

from .metrics import RegressionMetricSpec, resolve_regression_metric


@dataclass(frozen=True)
class BCPORegressionResult:
    best_fitness: float
    best_loss: float
    best_score: float
    num_features_selected: int
    total_features: int
    selected_features_indices: np.ndarray
    runtime_sec: float
    convergence_curve: np.ndarray
    metric_name: str


class BCPORegressorSelector(SelectorMixin, BaseEstimator):
    """Binary Crested Porcupine Optimizer (BCPO) feature selection for regression tasks.

    This transformer uses a bio-inspired optimization algorithm to select the
    best subset of features that minimizes the regression loss (e.g., MSE)
    while minimizing the number of selected features.

    Parameters
    ----------
    estimator : object, default=None
        The base estimator used for evaluating feature subsets. If None,
        Ridge regression is used.

    metric : str, default='neg_mean_squared_error'
        The metric to optimize.
        Common options: 'neg_mean_squared_error', 'r2',
        'neg_mean_absolute_error'.

    max_features : int, callable or None, default=None
        The maximum number of features to select.
        - If None, no limit is enforced (other than total features).
        - If int, must be > 0.
        - If callable, should take X (n_features) and return int.

    num_agents : int, default=30
        Number of search agents (population size).

    max_iter : int, default=100
        Maximum number of iterations.

    t_cycle : int, default=2
        Cycle length parameter for population reduction.

    n_min : int, default=5
        Minimum number of agents.

    alpha_max : float, default=0.2
        Maximum alpha parameter.

    w_loss : float, default=0.99
        Weight for the loss term in the fitness function.
        Fitness = w_loss * loss + w_feat * (num_selected / total_features).

    w_feat : float, default=0.01
        Weight for the feature reduction term.

    test_size : float, default=0.3
        Proportion of the dataset for internal validation.

    random_state : int, RandomState instance or None, default=None
        Seed for reproducibility.

    verbose : int, default=0
        Verbosity level.

    position_bounds : tuple of float, default=(-5.0, 5.0)
        Bounds for continuous positions.

    Attributes
    ----------
    support_ : ndarray of shape (n_features,)
        The mask of selected features.

    best_position_ : ndarray of shape (n_features,)
        The best continuous position vector found.

    best_fitness_ : float
        The best fitness value achieved.

    best_loss_ : float
        The loss (error) of the best feature subset on the internal test set.

    best_score_ : float
        The score (e.g. R2) corresponding to the best subset.

    n_iter_ : int
        Number of iterations run.

    Examples
    --------
    >>> from sklearn.datasets import load_diabetes
    >>> from sklearn.linear_model import Ridge
    >>> from bcpo_feature_selector.regression import BCPORegressorSelector
    >>> X, y = load_diabetes(return_X_y=True)
    >>> selector = BCPORegressorSelector(estimator=Ridge(), random_state=42)
    >>> selector.fit(X, y)
    BCPORegressorSelector(...)
    >>> X_new = selector.transform(X)
    """

    def __init__(
        self,
        estimator: Optional[RegressorMixin] = None,
        *,
        metric: str = "neg_root_mean_squared_error",
        max_features: Optional[Union[int, Callable[[np.ndarray], int]]] = None,
        num_agents: int = 30,
        max_iter: int = 100,
        t_cycle: int = 2,
        n_min: int = 5,
        alpha_max: float = 0.2,
        w_loss: float = 0.99,
        w_feat: float = 0.01,
        test_size: float = 0.3,
        random_state: Optional[int] = None,
        verbose: int = 0,
        position_bounds: Tuple[float, float] = (-5.0, 5.0),
    ) -> None:
        self.estimator = estimator
        self.metric = metric
        self.max_features = max_features
        self.num_agents = num_agents
        self.max_iter = max_iter
        self.t_cycle = t_cycle
        self.n_min = n_min
        self.alpha_max = alpha_max
        self.w_loss = w_loss
        self.w_feat = w_feat
        self.test_size = test_size
        self.random_state = random_state
        self.verbose = verbose
        self.position_bounds = position_bounds

    def _resolve_max_features(self, X: np.ndarray) -> Optional[int]:
        if self.max_features is None:
            return None
        k = (
            self.max_features(X)
            if callable(self.max_features)
            else self.max_features
        )
        try:
            k_int = int(k)
        except (TypeError, ValueError) as e:
            raise TypeError(
                "max_features must be None, an int, or a callable "
                "returning an int"
            ) from e
        if k_int <= 0:
            raise ValueError("max_features must be a positive integer or None")
        return k_int

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BCPORegressorSelector":
        """Run the BCPO feature selection algorithm.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.

        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        X, y = check_X_y(X, y, ensure_2d=True)

        self.n_features_in_ = X.shape[1]

        rng = np.random.default_rng(self.random_state)
        est = self.estimator if self.estimator is not None else Ridge()

        metric_func: RegressionMetricSpec = resolve_regression_metric(
            self.metric)
        self.metric_name_ = metric_func.name
        self.n_iter_ = self.max_iter

        self.max_features_ = self._resolve_max_features(X)
        if (
            self.max_features_ is not None
            and self.max_features_ > self.n_features_in_
        ):
            raise ValueError(
                "max_features cannot be larger than the number of features in X"
            )

        if not (0.0 < self.test_size < 1.0):
            raise ValueError("test_size must be between 0 and 1 (exclusive)")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
        )

        start = time.time()

        population = rng.uniform(-1.0, 1.0,
                                 size=(self.num_agents, self.n_features_in_))
        fitness_scores = np.full(self.num_agents, np.inf, dtype=float)

        gb_position = np.zeros(self.n_features_in_, dtype=float)
        gb_fitness = np.inf
        gb_loss = np.inf
        gb_score = -np.inf

        for i in range(self.num_agents):
            fit, loss, score, n_feat = self._fitness(
                rng,
                population[i],
                est,
                metric_func.loss,
                metric_func.score,
                X_train,
                y_train,
                X_test,
                y_test,
            )
            fitness_scores[i] = fit
            if fit < gb_fitness:
                gb_fitness = fit
                gb_position = population[i].copy()
                gb_loss = loss
                gb_score = score

        current_n = self.num_agents
        convergence: list[float] = []

        for t in range(1, self.max_iter + 1):
            if self.t_cycle and self.t_cycle > 0:
                cycle_length = self.max_iter / self.t_cycle
                cur_t = t % cycle_length
                if cur_t == 0:
                    cur_t = cycle_length
                progress = cur_t / cycle_length
                n_new = int(self.n_min + (self.num_agents -
                            self.n_min) * (1 - progress))
                n_new = max(n_new, self.n_min)
                if n_new < current_n:
                    num_features = np.array([
                        self._to_binary_deterministic(pos).sum()
                        for pos in population
                    ])
                    # Sort by fitness first, then by num_features (fewer is
                    # better)
                    sort_indices = np.lexsort((num_features, fitness_scores))
                    keep = sort_indices[:n_new]
                    population = population[keep]
                    fitness_scores = fitness_scores[keep]
                    current_n = n_new

            new_population = population.copy()

            alpha = self.alpha_max * (1 - t / self.max_iter)
            rand_val = rng.random()
            gamma_t = 2 * rand_val * \
                ((1 - t / self.max_iter) ** (t / self.max_iter))

            for i in range(current_n):
                tau1 = rng.random(self.n_features_in_)
                tau2 = rng.random(self.n_features_in_)
                u1 = rng.random(self.n_features_in_)
                rand_strategy = rng.random()

                available = [idx for idx in range(current_n) if idx != i]
                if len(available) >= 2:
                    r1, r2 = rng.choice(available, 2, replace=False)
                else:
                    r1 = r2 = i

                if rand_strategy < 0.5:
                    if rng.random() < 0.5:  # sight
                        y_t = (population[i] + gb_position) / 2
                        term = np.abs(2 * tau2 * gb_position - y_t)
                        new_population[i] = population[i] + tau1 * term
                    else:  # sound
                        y_t = (population[i] + population[r1]) / 2
                        term = tau2 * (population[r1] - population[r2])
                        new_population[i] = (1 - tau1) * \
                            population[i] + tau1 * (y_t + term)
                else:
                    if rng.random() < 0.5:  # odor
                        delta_k = rng.choice([-1, 1], size=self.n_features_in_)
                        attraction = (gamma_t * gb_position) - population[i]
                        repulsion = tau2 * delta_k * gamma_t
                        new_population[i] = (
                            (1 - u1) * population[i] + u1 * attraction - repulsion
                        )
                    else:  # physical attack
                        force = 2 * gamma_t * (gb_position - population[i])
                        decay = alpha * (1 - tau1)
                        new_population[i] = gb_position + decay + force

                # Clip to bounds
                new_population[i] = np.clip(
                    new_population[i],
                    self.position_bounds[0],
                    self.position_bounds[1])

            population = new_population

            for i in range(current_n):
                fit, loss, score, n_feat = self._fitness(
                    rng,
                    population[i],
                    est,
                    metric_func.loss,
                    metric_func.score,
                    X_train,
                    y_train,
                    X_test,
                    y_test,
                )

                # Update fitness
                fitness_scores[i] = fit

                if fit < gb_fitness:
                    gb_fitness = fit
                    gb_position = population[i].copy()
                    gb_loss = loss
                    gb_score = score

            convergence.append(float(gb_fitness))
            if self.verbose and (t == 1 or t % 10 == 0):
                gb_feat_deterministic = int(
                    self._to_binary_deterministic(gb_position).sum())
                print(
                    f"Iter {t:03d}/{self.max_iter} | Pop: {current_n:02d} | "
                    f"Best Fit: {gb_fitness:.6f} | "
                    f"Feat: {gb_feat_deterministic}/{self.n_features_in_}"
                )

        runtime = time.time() - start

        support = self._to_binary_deterministic(gb_position).astype(bool)
        if support.sum() == 0:
            support = self._fallback_best_single_feature(
                est,
                metric_func.loss,
                metric_func.score,
                X_train,
                y_train,
                X_test,
                y_test,
            )

        idx_final = np.where(support)[0]
        if idx_final.size > 0:
            reg_final = clone(est)
            reg_final.fit(X_train[:, idx_final], y_train)
            pred_final = reg_final.predict(X_test[:, idx_final])
            final_loss = float(metric_func.loss(y_test, pred_final))
            final_score = float(metric_func.score(y_test, pred_final))
        else:
            final_loss = gb_loss
            final_score = gb_score

        self.support_ = support
        self.best_position_ = gb_position
        self.best_fitness_ = gb_fitness
        self.best_loss_ = final_loss  # Use recalculated loss
        self.best_score_ = final_score  # Use recalculated score
        self.num_features_selected_ = int(
            self._to_binary_deterministic(gb_position).sum()
        )
        self.convergence_curve_ = np.array(convergence)
        self.runtime_sec_ = float(runtime)

        return self

    def _get_support_mask(self) -> np.ndarray:
        """Get the boolean mask indicating which features are selected."""
        self._check_is_fitted()
        return self.support_.copy()

    def result_(self) -> BCPORegressionResult:
        self._check_is_fitted()
        return BCPORegressionResult(
            best_fitness=self.best_fitness_,
            best_loss=self.best_loss_,
            best_score=self.best_score_,
            num_features_selected=self.num_features_selected_,
            total_features=self.n_features_in_,
            selected_features_indices=np.where(self.support_)[0],
            runtime_sec=self.runtime_sec_,
            convergence_curve=self.convergence_curve_.copy(),
            metric_name=self.metric_name_,
        )

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        x = np.clip(x, -10, 10)
        return 1.0 / (1.0 + np.exp(-x))

    def _to_binary(self, rng: np.random.Generator,
                   position: np.ndarray) -> np.ndarray:
        probs = self._sigmoid(position)
        binary = (probs > rng.random(self.n_features_in_)).astype(int)

        if getattr(self, "max_features_", None) is not None:
            k = int(self.max_features_)
            selected = int(binary.sum())
            if selected > k:
                keep = np.argsort(probs)[-k:]
                binary[:] = 0
                binary[keep] = 1
        return binary

    def _to_binary_deterministic(self, position: np.ndarray) -> np.ndarray:
        probs = self._sigmoid(position)
        binary = (probs >= 0.5).astype(int)

        if getattr(self, "max_features_", None) is not None:
            k = int(self.max_features_)
            selected = int(binary.sum())
            if selected > k:
                keep = np.argsort(probs)[-k:]
                binary[:] = 0
                binary[keep] = 1
        return binary

    def _fitness(
        self,
        rng: np.random.Generator,
        position: np.ndarray,
        estimator: RegressorMixin,
        loss_func: Callable[[np.ndarray, np.ndarray], float],
        score_func: Callable[[np.ndarray, np.ndarray], float],
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
    ) -> Tuple[float, float, float, int]:
        binary = self._to_binary(rng, position)
        idx = np.where(binary == 1)[0]
        if idx.size == 0:
            # Empty subset is invalid. Return +inf fitness so it can never be
            # selected.
            return float("inf"), float("inf"), -float("inf"), 0

        # Penalize if exceeds max_features constraint
        penalty = 0.0
        if self.max_features_ is not None and idx.size > self.max_features_:
            # Add penalty proportional to excess features
            excess = (idx.size - self.max_features_) / self.n_features_in_
            penalty = 0.5 * excess

        reg = clone(estimator)
        reg.fit(X_train[:, idx], y_train)
        pred = reg.predict(X_test[:, idx])

        loss = float(loss_func(y_test, pred))
        score = float(score_func(y_test, pred))

        # Guard against numerical issues producing NaN/Inf from either
        # estimator or metric.
        if not np.isfinite(loss) or not np.isfinite(score):
            return float("inf"), float("inf"), -float("inf"), int(idx.size)

        feat_ratio = idx.size / self.n_features_in_
        fitness = self.w_loss * loss + self.w_feat * feat_ratio + penalty
        return float(fitness), float(loss), float(score), int(idx.size)

    def _fallback_best_single_feature(
        self,
        estimator: RegressorMixin,
        loss_func: Callable[[np.ndarray, np.ndarray], float],
        score_func: Callable[[np.ndarray, np.ndarray], float],
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
    ) -> np.ndarray:
        best_j = 0
        best_fit = float("inf")
        for j in range(self.n_features_in_):
            reg = clone(estimator)
            reg.fit(X_train[:, [j]], y_train)
            pred = reg.predict(X_test[:, [j]])
            loss = float(loss_func(y_test, pred))
            feat_ratio = 1 / self.n_features_in_
            fit = self.w_loss * loss + self.w_feat * feat_ratio
            if fit < best_fit:
                best_fit = fit
                best_j = j
        mask = np.zeros(self.n_features_in_, dtype=bool)
        mask[best_j] = True
        return mask

    def _check_is_fitted(self) -> None:
        check_is_fitted(self, "support_")
