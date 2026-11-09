import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression, LogisticRegression

from expt.causal import (
    aipw_ate,
    cross_fit,
    ipw_ate,
    naive_difference,
    outcome_regression_ate,
    overlap_share,
)


def _confounded(n=60_000, seed=0, effect=1.0):
    """Treatment is more likely for customers with high x, and x also raises y."""
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    e = 1 / (1 + np.exp(-1.2 * x))
    t = (rng.random(n) < e).astype(int)
    y = 2.0 * x + effect * t + rng.normal(size=n)
    return pd.DataFrame({"x": x}), t, y


def _nuisance(X, t, y):
    return cross_fit(X, t, y, lambda: LogisticRegression(), LinearRegression, n_folds=3)


def test_naive_difference_is_biased_upwards():
    X, t, y = _confounded()
    assert naive_difference(y, t) > 1.5


def test_corrections_recover_the_true_effect():
    X, t, y = _confounded()
    nu = _nuisance(X, t, y)
    assert outcome_regression_ate(nu) == pytest.approx(1.0, abs=0.05)
    assert ipw_ate(y, t, nu.propensity) == pytest.approx(1.0, abs=0.1)
    res = aipw_ate(y, t, nu)
    assert res.estimate == pytest.approx(1.0, abs=0.05)
    assert res.ci_low < 1.0 < res.ci_high


def test_aipw_interval_coverage():
    covered = 0
    for seed in range(40):
        X, t, y = _confounded(n=8_000, seed=seed)
        res = aipw_ate(y, t, _nuisance(X, t, y))
        covered += res.ci_low <= 1.0 <= res.ci_high
    assert covered >= 34  # nominal 95% of 40 = 38; allow for simulation noise


def test_overlap_share():
    e = np.array([0.01, 0.2, 0.5, 0.97, 0.6])
    assert overlap_share(e) == pytest.approx(0.4)
