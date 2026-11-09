import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from expt.policy import compare_policies, policy_value
from expt.uplift import qini_coefficient, qini_curve, s_learner, t_learner


def _rct(n=40_000, seed=0):
    """Randomised experiment where the treatment only helps customers with x > 0."""
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    t = rng.integers(0, 2, n)
    tau = np.where(x > 0, 1.0, 0.0)
    y = 0.5 * x + tau * t + rng.normal(size=n)
    return pd.DataFrame({"x": x, "x_pos": (x > 0).astype(float)}), t, y, tau


def test_learners_recover_heterogeneous_effect():
    X, t, y, tau = _rct()
    tree = lambda: DecisionTreeRegressor(min_samples_leaf=1_000, random_state=0)
    for learner, make_model in [(t_learner, LinearRegression), (t_learner, tree), (s_learner, tree)]:
        pred = learner(X, y, t, X, make_model)
        assert np.corrcoef(pred, tau)[0, 1] > 0.8


def test_linear_s_learner_cannot_see_heterogeneity():
    # Without an interaction term, a linear S-learner predicts the same uplift for everyone.
    X, t, y, tau = _rct()
    pred = s_learner(X, y, t, X, LinearRegression)
    assert np.ptp(pred) == pytest.approx(0, abs=1e-9)


def test_qini_positive_for_good_ranking_and_near_zero_for_random():
    X, t, y, tau = _rct(seed=1)
    good = qini_coefficient(y, t, tau + 1e-9 * X["x"].to_numpy())
    rand = qini_coefficient(y, t, np.random.default_rng(2).random(len(y)))
    # Perfect ranking here has a theoretical Qini area of 0.0625 (half the customers respond, effect 1).
    assert good == pytest.approx(0.0625, abs=0.01)
    assert abs(rand) < 0.01


def test_qini_curve_ends_at_total_effect():
    X, t, y, tau = _rct(seed=3)
    curve = qini_curve(y, t, X["x"].to_numpy())
    total = (y[t == 1].sum() - y[t == 0].sum() * (t == 1).sum() / (t == 0).sum()) / len(y)
    assert curve["gain"].iloc[-1] == pytest.approx(total)
    assert curve["random"].iloc[-1] == pytest.approx(total)


def test_policy_value_of_treating_everyone_is_treated_mean():
    rng = np.random.default_rng(4)
    assigned = rng.choice(["a", "b", "c"], size=30_000)
    y = (assigned == "b") * 2.0 + rng.normal(size=30_000)
    everyone_b = np.full(30_000, "b")
    value = policy_value(y, assigned, everyone_b, {"a": 1 / 3, "b": 1 / 3, "c": 1 / 3})
    assert value == pytest.approx(y[assigned == "b"].mean())


def test_ips_recovers_value_of_a_targeted_policy():
    rng = np.random.default_rng(5)
    n = 200_000
    x = rng.normal(size=n)
    assigned = rng.choice(["control", "treat"], size=n)
    effect = np.where(x > 0, 1.0, -0.5)
    y = x + effect * (assigned == "treat") + rng.normal(size=n)
    policy = np.where(x > 0, "treat", "control")
    true_value = np.mean(x + effect * (policy == "treat"))
    est = policy_value(y, assigned, policy, {"control": 0.5, "treat": 0.5})
    assert est == pytest.approx(true_value, abs=0.02)


def test_compare_policies_reports_differences_with_intervals():
    rng = np.random.default_rng(6)
    n = 20_000
    assigned = rng.choice(["control", "treat"], size=n)
    y = (assigned == "treat") * 1.0 + rng.normal(size=n)
    out = compare_policies(
        y, assigned,
        {"nobody": np.full(n, "control"), "everyone": np.full(n, "treat")},
        {"control": 0.5, "treat": 0.5}, baseline="nobody", n_boot=200,
    )
    assert out.loc["everyone", "diff_low"] > 0.9 - 0.1
    assert out.loc["nobody", "diff_vs_nobody"] == 0
