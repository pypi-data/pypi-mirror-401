import numpy as np
import pytest


def _cycle_step(max_iter: int, t_cycle: int, t: int) -> float:
    # Mirrors current implementation in selectors.
    cycle_length = max_iter / t_cycle
    cur_t = t % cycle_length
    if cur_t == 0:
        cur_t = cycle_length
    return cur_t / cycle_length


@pytest.mark.parametrize(
    "max_iter,t_cycle",
    [
        (100, 2),
        (10, 3),
        (7, 2),
    ],
)
def test_cycle_progress_stays_in_0_1(max_iter, t_cycle):
    # Basic invariant: progress should always be in (0, 1].
    for t in range(1, max_iter + 1):
        progress = _cycle_step(max_iter, t_cycle, t)
        assert 0.0 < progress <= 1.0


def test_cycle_progress_hits_exactly_one_at_cycle_boundaries():
    max_iter, t_cycle = 100, 4
    cycle_length = max_iter // t_cycle

    for k in range(1, t_cycle + 1):
        t = k * cycle_length
        progress = _cycle_step(max_iter, t_cycle, t)
        assert np.isclose(progress, 1.0)
