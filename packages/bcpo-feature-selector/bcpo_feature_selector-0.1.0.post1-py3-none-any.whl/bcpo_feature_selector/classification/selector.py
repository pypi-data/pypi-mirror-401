from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.feature_selection import SelectorMixin
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import check_is_fitted, check_X_y

from .metrics import _safe_proba_positive, resolve_metric


@dataclass(frozen=True)
class BCPOResult:
    best_fitness: float
    best_score: float
    num_features_selected: int
    total_features: int
    selected_features_indices: np.ndarray
    runtime_sec: float
    convergence_curve: np.ndarray
    metric_name: str


MetricFunc = Callable[[np.ndarray, np.ndarray, Optional[np.ndarray]], float]


class BCPOClassifierSelector(SelectorMixin, BaseEstimator):
    """Binary Crested Porcupine Optimizer (BCPO) feature selection.

    This transformer uses a bio-inspired optimization algorithm to select the
    best features that maximizes the classification performance while
    minimizing the number of selected features.

    Parameters
    ----------
    estimator : object, default=None
        The base estimator used for evaluating feature subsets. If None,
        KNeighborsClassifier(n_neighbors=5) is used.

    metric : str, default='accuracy'
        The metric to optimize. Available metrics depend on the task
        (classification).
        Common options: 'accuracy', 'f1', 'precision', 'recall', 'roc_auc'.

    metric_average : str, default='binary'
        The averaging method for multiclass/multilabel metrics.
        Options: 'micro', 'macro', 'weighted', 'binary'.

    max_features : int, callable or None, default=None
        The maximum number of features to select.
        - If None, no limit is enforced (other than total features).
        - If int, must be > 0.
        - If callable, should take X (n_features) and return int.

    num_agents : int, default=30
        Number of search agents (population size) in the BCPO algorithm.

    max_iter : int, default=100
        Maximum number of iterations for the optimization.

    t_cycle : int, default=2
        Cycle length parameter for the cyclic population reduction mechanism.

    n_min : int, default=5
        Minimum number of agents to keep during population reduction.

    alpha_max : float, default=0.2
        Maximum value for the alpha parameter in the BCPO update rule.

    w_error : float, default=0.99
        Weight for the error term in the fitness function.
        Fitness = w_error * (1 - score) + w_feat * (feat_ratio).

    w_feat : float, default=0.01
        Weight for the feature reduction term in the fitness function.

    test_size : float, default=0.3
        Proportion of the dataset to include in the validation split used
        internally during fitness evaluation.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the estimator and the BCPO algorithm
        for reproducibility.

    verbose : int, default=0
        Controls the verbosity: the higher, the more messages.

    position_bounds : tuple of float, default=(-5.0, 5.0)
        The bounds for the continuous position values before sigmoid transformation.

    Attributes
    ----------
    support_ : ndarray of shape (n_features,)
        The mask of selected features.

    best_position_ : ndarray of shape (n_features,)
        The best continuous position vector found by the optimizer.

    best_fitness_ : float
        The best fitness value achieved.

    best_score_ : float
        The score (e.g., accuracy) of the best feature subset on the internal
        test set.

    num_features_selected_ : int
        Number of features selected.

    convergence_curve_ : ndarray of shape (max_iter,)
        The history of the best fitness value at each iteration.

    metric_name_ : str
        The name of the metric used.

    runtime_sec_ : float
        Total runtime of the fit method in seconds.

    n_features_in_ : int
        Number of features seen during fit.

    n_iter_ : int
        Number of iterations run.

    max_features_ : int
        The resolved maximum number of features allowed.

    Examples
    --------
    >>> from sklearn.datasets import load_breast_cancer
    >>> from sklearn.naive_bayes import GaussianNB
    >>> from bcpo_feature_selector.classification import BCPOClassifierSelector
    >>> X, y = load_breast_cancer(return_X_y=True)
    >>> selector = BCPOClassifierSelector(estimator=GaussianNB(), random_state=42)
    >>> selector.fit(X, y)
    BCPOClassifierSelector(...)
    >>> X_new = selector.transform(X)
    >>> X_new.shape
    (569, ...)
    """

    def __init__(
        self,
        estimator: Optional[ClassifierMixin] = None,
        *,
        metric: str = "accuracy",
        metric_average: str = "binary",
        max_features: Optional[Union[int, Callable[[np.ndarray], int]]] = None,
        num_agents: int = 30,
        max_iter: int = 100,
        t_cycle: int = 2,
        n_min: int = 5,
        alpha_max: float = 0.2,
        w_error: float = 0.99,
        w_feat: float = 0.01,
        test_size: float = 0.3,
        random_state: Optional[int] = None,
        verbose: int = 0,
        position_bounds: Tuple[float, float] = (-5.0, 5.0),
    ) -> None:
        self.estimator = estimator
        self.metric = metric
        self.metric_average = metric_average
        self.max_features = max_features
        self.num_agents = num_agents
        self.max_iter = max_iter
        self.t_cycle = t_cycle
        self.n_min = n_min
        self.alpha_max = alpha_max
        self.w_error = w_error
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

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BCPOClassifierSelector":
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
        est = self.estimator if self.estimator is not None \
            else KNeighborsClassifier(n_neighbors=5)

        metric_spec = resolve_metric(self.metric, average=self.metric_average)
        metric_func: MetricFunc = metric_spec.func

        self.metric_name_ = metric_spec.name
        self.n_iter_ = self.max_iter

        self.max_features_ = self._resolve_max_features(X)
        if self.max_features_ is not None \
                and self.max_features_ > self.n_features_in_:
            raise ValueError(
                "max_features cannot be larger than the number "
                "of features in X"
            )

        if not (0.0 < self.test_size < 1.0):
            raise ValueError("test_size must be between 0 and 1 (exclusive)")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y,
        )

        start = time.time()

        population = rng.uniform(-1.0, 1.0,
                                 size=(self.num_agents, self.n_features_in_))
        fitness_scores = np.full(self.num_agents, np.inf, dtype=float)

        gb_position = np.zeros(self.n_features_in_, dtype=float)
        gb_fitness = np.inf
        gb_score = 0.0

        for i in range(self.num_agents):
            fit, score, n_feat = self._fitness(
                rng,
                population[i],
                est,
                metric_func,
                X_train,
                y_train,
                X_test,
                y_test,
            )
            fitness_scores[i] = fit
            if fit < gb_fitness:
                gb_fitness = fit
                gb_position = population[i].copy()
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
                            1 - u1) * population[i] + u1 * attraction - repulsion
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
                fit, score, n_feat = self._fitness(
                    rng,
                    population[i],
                    est,
                    metric_func,
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
                    gb_score = score

            convergence.append(float(gb_fitness))
            if self.verbose and (t == 1 or t % 10 == 0):
                gb_num_features_display = self._to_binary_deterministic(
                    gb_position).sum()
                print(
                    f"Iter {t:03d}/{self.max_iter} | Pop: {current_n:02d} | "
                    f"Best Fit: {gb_fitness:.5f} | "
                    f"Feat: {gb_num_features_display}/{self.n_features_in_}"
                )

        runtime = time.time() - start

        support = self._to_binary_deterministic(gb_position).astype(bool)
        if support.sum() == 0:
            support = self._fallback_best_single_feature(
                est, metric_func, X_train, y_train, X_test, y_test)

        idx_final = np.where(support)[0]
        if idx_final.size > 0:
            clf_final = clone(est)
            clf_final.fit(X_train[:, idx_final], y_train)
            _safe_proba_positive(clf_final, X_test[:, idx_final])

        self.support_ = support
        self.best_position_ = gb_position
        self.best_fitness_ = gb_fitness
        self.best_score_ = gb_score
        self.num_features_selected_ = int(
            self._to_binary_deterministic(gb_position).sum()
        )
        self.convergence_curve_ = np.array(convergence)
        self.metric_name_ = metric_spec.name
        self.runtime_sec_ = float(runtime)

        return self

    def _get_support_mask(self) -> np.ndarray:
        """Get the boolean mask indicating which features are selected."""
        self._check_is_fitted()
        return self.support_.copy()

    def result_(self) -> BCPOResult:
        self._check_is_fitted()
        return BCPOResult(
            best_fitness=self.best_fitness_,
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
        estimator: ClassifierMixin,
        metric_func: MetricFunc,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
    ) -> Tuple[float, float, int]:
        binary = self._to_binary(rng, position)
        idx = np.where(binary == 1)[0]
        if idx.size == 0:
            return 1.0, 0.0, 0

        # Penalize if exceeds max_features constraint
        penalty = 0.0
        if self.max_features_ is not None and idx.size > self.max_features_:
            # Add penalty proportional to excess features
            excess = (idx.size - self.max_features_) / self.n_features_in_
            penalty = 0.5 * excess  # Penalty weight

        clf = clone(estimator)
        clf.fit(X_train[:, idx], y_train)
        pred = clf.predict(X_test[:, idx])
        y_score = _safe_proba_positive(clf, X_test[:, idx])
        score = float(metric_func(y_test, pred, y_score))

        error_rate = 1.0 - score
        feat_ratio = idx.size / self.n_features_in_
        fitness = self.w_error * error_rate + self.w_feat * feat_ratio + penalty
        return float(fitness), float(score), int(idx.size)

    def _fallback_best_single_feature(
        self,
        estimator: ClassifierMixin,
        metric_func: MetricFunc,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
    ) -> np.ndarray:
        best_j = 0
        best_score = -np.inf
        for j in range(self.n_features_in_):
            clf = clone(estimator)
            clf.fit(X_train[:, [j]], y_train)
            pred = clf.predict(X_test[:, [j]])
            y_score = _safe_proba_positive(clf, X_test[:, [j]])
            s = float(metric_func(y_test, pred, y_score))
            if s > best_score:
                best_score = s
                best_j = j
        mask = np.zeros(self.n_features_in_, dtype=bool)
        mask[best_j] = True
        return mask

    def _check_is_fitted(self) -> None:
        check_is_fitted(self, "support_")
