"""Uplift modelling: predicting who responds to a treatment, and checking it.

* ``t_learner`` and ``s_learner``: two standard ways to predict each
  customer's incremental outcome from a randomised experiment.
* ``qini_curve`` and ``qini_coefficient``: evaluate any ranking of customers
  (model scores or a business rule) on randomised data the model has not seen.
"""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd


def t_learner(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    treated_train: np.ndarray,
    X_score: pd.DataFrame,
    make_model: Callable[[], object],
) -> np.ndarray:
    """Fit one outcome model on treated and one on control customers; the
    predicted uplift is the difference of their predictions."""
    t = np.asarray(treated_train).astype(bool)
    y = np.asarray(y_train, dtype=float)
    m1 = make_model().fit(X_train[t], y[t])
    m0 = make_model().fit(X_train[~t], y[~t])
    return m1.predict(X_score) - m0.predict(X_score)


def s_learner(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    treated_train: np.ndarray,
    X_score: pd.DataFrame,
    make_model: Callable[[], object],
) -> np.ndarray:
    """Fit a single model with the treatment flag as a feature; the predicted
    uplift is the prediction with the flag on minus the prediction with it off."""
    Xt = X_train.assign(_treated=np.asarray(treated_train, dtype=float))
    model = make_model().fit(Xt, np.asarray(y_train, dtype=float))
    on = model.predict(X_score.assign(_treated=1.0))
    off = model.predict(X_score.assign(_treated=0.0))
    return on - off


def qini_curve(y: np.ndarray, treated: np.ndarray, score: np.ndarray, n_points: int = 101) -> pd.DataFrame:
    """Cumulative incremental outcome when treating customers in order of ``score``.

    At each fraction of customers targeted (highest scores first), the gain is
    the treated customers' total outcome minus the control customers' total
    scaled to the same number of treated customers, divided by the total number
    of customers. The ``random`` column is the straight line a random ordering
    would give. Ties in ``score`` are broken at random.
    """
    y = np.asarray(y, dtype=float)
    t = np.asarray(treated).astype(bool)
    s = np.asarray(score, dtype=float)
    rng = np.random.default_rng(0)
    order = np.lexsort((rng.random(len(s)), -s))
    y, t = y[order], t[order]
    cum_y_t = np.cumsum(y * t)
    cum_y_c = np.cumsum(y * ~t)
    cum_n_t = np.cumsum(t)
    cum_n_c = np.cumsum(~t)
    with np.errstate(divide="ignore", invalid="ignore"):
        gain = np.where(cum_n_c > 0, cum_y_t - cum_y_c * cum_n_t / cum_n_c, 0.0) / len(y)
    idx = np.unique(np.linspace(0, len(y) - 1, n_points).round().astype(int))
    fraction = (idx + 1) / len(y)
    total = gain[-1]
    return pd.DataFrame({"fraction": fraction, "gain": gain[idx], "random": fraction * total})


def qini_coefficient(y: np.ndarray, treated: np.ndarray, score: np.ndarray) -> float:
    """Area between the Qini curve and the random line.

    Positive: the ranking puts responsive customers first. Around zero: no
    better than random. Negative: worse than random, typically a model that
    learned noise. In units of outcome per customer.
    """
    curve = qini_curve(y, treated, score, n_points=1001)
    return float(np.trapezoid(curve["gain"] - curve["random"], curve["fraction"]))
