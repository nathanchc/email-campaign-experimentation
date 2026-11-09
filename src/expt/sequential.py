"""Monitoring an experiment while it runs: peeking, sequential tests, Bayesian rules.

Experiments are usually watched daily. Checking a fixed-horizon test every
day and stopping at the first p < 0.05 inflates the false-positive rate. The
functions here simulate many experiments day by day (using daily counts, so
thousands of experiments run in seconds) to measure that, and to calibrate a
group-sequential boundary that allows daily looks at an honest error rate.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class SimulatedPaths:
    """Cumulative z-statistics and Bayesian probabilities after each day, per experiment."""
    z: np.ndarray            # shape (n_sims, days): treatment minus control, pooled z-test
    prob_better: np.ndarray  # shape (n_sims, days): P(treatment rate > control rate | data), Beta(1, 1) priors


def simulate_daily_paths(
    p_control: float,
    p_treatment: float,
    n_per_arm_per_day: int,
    days: int,
    n_sims: int,
    seed: int | None = 0,
) -> SimulatedPaths:
    """Simulate ``n_sims`` two-arm experiments, recording the test statistics after each day."""
    rng = np.random.default_rng(seed)
    x_c = rng.binomial(n_per_arm_per_day, p_control, size=(n_sims, days)).cumsum(axis=1)
    x_t = rng.binomial(n_per_arm_per_day, p_treatment, size=(n_sims, days)).cumsum(axis=1)
    n = n_per_arm_per_day * np.arange(1, days + 1)

    p_c, p_t = x_c / n, x_t / n
    pooled = (x_c + x_t) / (2 * n)
    z = (p_t - p_c) / np.sqrt(pooled * (1 - pooled) * 2 / n)

    # Posterior of each rate is Beta(1 + successes, 1 + failures); the difference is close to normal.
    a_c, b_c = 1 + x_c, 1 + n - x_c
    a_t, b_t = 1 + x_t, 1 + n - x_t
    mean_diff = a_t / (a_t + b_t) - a_c / (a_c + b_c)
    var_c = a_c * b_c / ((a_c + b_c) ** 2 * (a_c + b_c + 1))
    var_t = a_t * b_t / ((a_t + b_t) ** 2 * (a_t + b_t + 1))
    prob_better = stats.norm.cdf(mean_diff / np.sqrt(var_c + var_t))
    return SimulatedPaths(z=z, prob_better=prob_better)


def obf_boundaries(days: int, c: float) -> np.ndarray:
    """O'Brien-Fleming-shaped boundaries: very strict early, close to the usual 1.96 at the end."""
    k = np.arange(1, days + 1)
    return c * np.sqrt(days / k)


def calibrate_obf(days: int, alpha: float = 0.05, n_sims: int = 20_000, seed: int | None = 0) -> float:
    """Find the constant ``c`` so that stopping when |z| crosses the boundary on any
    day gives an overall two-sided false-positive rate of ``alpha``.

    Calibrated by simulation under no effect, using the fact that the cumulative
    z-statistic behaves like a scaled random walk.
    """
    rng = np.random.default_rng(seed)
    increments = rng.normal(size=(n_sims, days)).cumsum(axis=1)
    z = increments / np.sqrt(np.arange(1, days + 1))
    scaled = np.abs(z) / np.sqrt(days / np.arange(1, days + 1))
    return float(np.quantile(scaled.max(axis=1), 1 - alpha))


@dataclass(frozen=True)
class StoppingResult:
    share_stopped: float   # share of experiments that declared a winner (or any effect)
    mean_stop_day: float   # average day of stopping, counting non-stopped experiments at the final day


def apply_rule(stat: np.ndarray, crossed: Callable[[np.ndarray], np.ndarray]) -> StoppingResult:
    """Stop each experiment the first day ``crossed(stat)`` is true."""
    hits = crossed(stat)
    stopped = hits.any(axis=1)
    first = np.where(stopped, hits.argmax(axis=1) + 1, stat.shape[1])
    return StoppingResult(float(stopped.mean()), float(first.mean()))
