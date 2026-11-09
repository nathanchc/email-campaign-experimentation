"""Estimating a treatment effect from non-randomised (targeted) data.

When treatment was given by a targeting rule rather than at random, treated
and untreated customers differ, and a naive comparison mixes the treatment
effect with those differences. The usual corrections:

* outcome regression: model the outcome with and without treatment and
  average the predicted difference;
* inverse propensity weighting (IPW): reweight customers by the inverse of
  their probability of receiving the treatment they got;
* augmented IPW (AIPW, "doubly robust"): combine both; consistent if either
  model is right.

All rely on "no unmeasured confounding" and on overlap (every kind of
customer had some chance of each treatment). ``cross_fit`` produces the model
predictions out-of-fold, so no customer is scored by a model trained on them.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import KFold


@dataclass(frozen=True)
class Nuisance:
    propensity: np.ndarray   # P(treated | X)
    mu0: np.ndarray          # E[y | X, untreated]
    mu1: np.ndarray          # E[y | X, treated]


def _predict(model, X) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.predict(X)


def cross_fit(
    X: pd.DataFrame,
    treated: np.ndarray,
    y: np.ndarray,
    make_propensity_model: Callable[[], object],
    make_outcome_model: Callable[[], object],
    n_folds: int = 3,
    seed: int = 0,
) -> Nuisance:
    """Out-of-fold propensity scores and outcome predictions."""
    t = np.asarray(treated).astype(int)
    y = np.asarray(y, dtype=float)
    e, mu0, mu1 = np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))
    for train, score in KFold(n_folds, shuffle=True, random_state=seed).split(X):
        Xa, ta, ya = X.iloc[train], t[train], y[train]
        e[score] = _predict(make_propensity_model().fit(Xa, ta), X.iloc[score])
        mu1[score] = _predict(make_outcome_model().fit(Xa[ta == 1], ya[ta == 1]), X.iloc[score])
        mu0[score] = _predict(make_outcome_model().fit(Xa[ta == 0], ya[ta == 0]), X.iloc[score])
    return Nuisance(e, mu0, mu1)


def naive_difference(y: np.ndarray, treated: np.ndarray) -> float:
    y, t = np.asarray(y, dtype=float), np.asarray(treated).astype(bool)
    return float(y[t].mean() - y[~t].mean())


def outcome_regression_ate(nuisance: Nuisance) -> float:
    return float(np.mean(nuisance.mu1 - nuisance.mu0))


def ipw_ate(y: np.ndarray, treated: np.ndarray, propensity: np.ndarray, clip: float = 0.01) -> float:
    """Self-normalised (Hajek) IPW estimate. Propensities are clipped to
    [clip, 1 - clip] to stop a few customers from getting enormous weights."""
    y, t = np.asarray(y, dtype=float), np.asarray(treated).astype(float)
    e = np.clip(propensity, clip, 1 - clip)
    w1, w0 = t / e, (1 - t) / (1 - e)
    return float((w1 * y).sum() / w1.sum() - (w0 * y).sum() / w0.sum())


@dataclass(frozen=True)
class AIPWResult:
    estimate: float
    se: float
    ci_low: float
    ci_high: float


def aipw_ate(
    y: np.ndarray,
    treated: np.ndarray,
    nuisance: Nuisance,
    clip: float = 0.01,
    alpha: float = 0.05,
) -> AIPWResult:
    """Doubly robust estimate with an influence-function standard error."""
    y, t = np.asarray(y, dtype=float), np.asarray(treated).astype(float)
    e = np.clip(nuisance.propensity, clip, 1 - clip)
    psi = (nuisance.mu1 - nuisance.mu0
           + t * (y - nuisance.mu1) / e
           - (1 - t) * (y - nuisance.mu0) / (1 - e))
    est = psi.mean()
    se = psi.std(ddof=1) / np.sqrt(len(psi))
    z = stats.norm.ppf(1 - alpha / 2)
    return AIPWResult(float(est), float(se), float(est - z * se), float(est + z * se))


def overlap_share(propensity: np.ndarray, low: float = 0.05, high: float = 0.95) -> float:
    """Share of customers whose propensity is outside [low, high]: customers who
    were almost always or almost never treated, for whom there is barely anyone
    comparable in the other group."""
    e = np.asarray(propensity)
    return float(((e < low) | (e > high)).mean())
