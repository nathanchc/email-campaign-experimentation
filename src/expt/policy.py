"""Evaluating targeting policies on randomised data.

A policy assigns each customer an arm (for example "no email", "men's
email" or "women's email"). In a randomised experiment we can estimate what
the outcome would have been under any policy, without running it, by looking
at customers whose random assignment happens to match what the policy would
have chosen (inverse propensity weighting).
"""
from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd


def _weights(assigned: np.ndarray, policy: np.ndarray, propensity: Mapping[str, float]) -> np.ndarray:
    match = assigned == policy
    p = np.array([propensity[a] for a in assigned], dtype=float)
    return match / p


def policy_value(
    y: np.ndarray,
    assigned: np.ndarray,
    policy: np.ndarray,
    propensity: Mapping[str, float],
) -> float:
    """Estimated mean outcome per customer if everyone were treated as ``policy`` says.

    Uses the self-normalised (Hajek) inverse-propensity estimator.
    """
    y = np.asarray(y, dtype=float)
    w = _weights(np.asarray(assigned), np.asarray(policy), propensity)
    if w.sum() == 0:
        raise ValueError("no customer's assignment matches the policy")
    return float((w * y).sum() / w.sum())


def compare_policies(
    y: np.ndarray,
    assigned: np.ndarray,
    policies: Mapping[str, np.ndarray],
    propensity: Mapping[str, float],
    baseline: str,
    n_boot: int = 1_000,
    alpha: float = 0.05,
    seed: int | None = 0,
) -> pd.DataFrame:
    """Value of each policy and its difference from ``baseline``, with paired
    bootstrap confidence intervals (the same resampled customers for every policy)."""
    y = np.asarray(y, dtype=float)
    assigned = np.asarray(assigned)
    pol = {name: np.asarray(p) for name, p in policies.items()}
    point = {name: policy_value(y, assigned, p, propensity) for name, p in pol.items()}

    rng = np.random.default_rng(seed)
    n = len(y)
    boot = {name: np.empty(n_boot) for name in pol}
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        for name, p in pol.items():
            boot[name][b] = policy_value(y[idx], assigned[idx], p[idx], propensity)

    lo, hi = alpha / 2, 1 - alpha / 2
    rows = []
    for name in pol:
        diff = boot[name] - boot[baseline]
        rows.append({
            "policy": name,
            "value": point[name],
            "value_low": np.quantile(boot[name], lo),
            "value_high": np.quantile(boot[name], hi),
            f"diff_vs_{baseline}": point[name] - point[baseline],
            "diff_low": np.quantile(diff, lo),
            "diff_high": np.quantile(diff, hi),
        })
    return pd.DataFrame(rows).set_index("policy")
