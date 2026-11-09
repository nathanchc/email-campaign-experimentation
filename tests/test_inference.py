import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.proportion import proportions_ztest

from expt.inference import (
    bootstrap_diff_in_means,
    compare_means,
    compare_proportions,
    cuped,
    holm,
    ratio_delta_method,
    regression_adjusted_effect,
)


def test_compare_proportions_matches_statsmodels_ztest():
    res = compare_proportions(267, 21_307, 122, 21_306)
    z, p = proportions_ztest([267, 122], [21_307, 21_306])
    assert res.z == pytest.approx(z)
    assert res.p_value == pytest.approx(p)
    assert res.diff_low < res.diff < res.diff_high
    assert res.lift_low < res.lift < res.lift_high


def test_relative_lift_interval_covers_truth_in_simulation():
    rng = np.random.default_rng(3)
    p_c, p_t, n, covered = 0.02, 0.03, 20_000, 0
    for _ in range(400):
        r = compare_proportions(rng.binomial(n, p_t), n, rng.binomial(n, p_c), n)
        covered += r.lift_low <= p_t / p_c - 1 <= r.lift_high
    assert 0.92 <= covered / 400 <= 0.98


def test_compare_means_and_bootstrap_agree_on_normal_data():
    rng = np.random.default_rng(0)
    t, c = rng.normal(1.0, 2.0, 5_000), rng.normal(0.8, 2.0, 5_000)
    welch = compare_means(t, c)
    boot = bootstrap_diff_in_means(t, c, n_boot=1_000, seed=1)
    assert boot.diff == pytest.approx(welch.diff)
    assert boot.diff_low == pytest.approx(welch.diff_low, abs=0.02)
    assert boot.diff_high == pytest.approx(welch.diff_high, abs=0.02)


def test_holm_is_never_smaller_than_raw():
    raw = [0.01, 0.04, 0.03]
    adj = holm(raw)
    assert np.all(adj >= raw)
    assert adj[0] == pytest.approx(0.03)


def _experiment(n=20_000, effect=0.5, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    d = rng.integers(0, 2, n)
    y = 2.0 * x + effect * d + rng.normal(size=n)
    return x, d, y


def test_regression_adjustment_is_unbiased_and_more_precise():
    x, d, y = _experiment()
    plain = regression_adjusted_effect(y, d)
    adjusted = regression_adjusted_effect(y, d, pd.DataFrame({"x": x}))
    assert plain.estimate == pytest.approx(y[d == 1].mean() - y[d == 0].mean())
    assert adjusted.estimate == pytest.approx(0.5, abs=0.05)
    assert adjusted.se < 0.6 * plain.se


def test_cuped_reduces_variance_by_correlation_squared():
    x, d, y = _experiment(effect=0.0)
    y_adj, theta = cuped(y, x)
    rho = np.corrcoef(y, x)[0, 1]
    assert y_adj.var() == pytest.approx(y.var() * (1 - rho**2), rel=0.01)
    assert y_adj.mean() == pytest.approx(y.mean())


def test_ratio_delta_method_matches_simulation():
    rng = np.random.default_rng(5)
    ratios = []
    for _ in range(300):
        clicks = rng.binomial(1, 0.3, 4_000)
        orders = clicks * rng.binomial(1, 0.2, 4_000)
        ratios.append(orders.sum() / clicks.sum())
    clicks = rng.binomial(1, 0.3, 4_000)
    orders = clicks * rng.binomial(1, 0.2, 4_000)
    _, se = ratio_delta_method(orders, clicks)
    assert se == pytest.approx(np.std(ratios), rel=0.15)
