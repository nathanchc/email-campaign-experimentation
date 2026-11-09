import numpy as np
import pandas as pd
import pytest
from scipy import stats

from expt.data import clean_hillstrom
from expt.validation import (
    balance_table,
    covariate_tests,
    joint_balance_test,
    srm_test,
    standardized_mean_difference,
)


def test_srm_matches_scipy_and_passes_for_balanced_groups():
    counts = {"a": 21_306, "b": 21_307, "c": 21_387}
    result = srm_test(counts)
    chi2, p = stats.chisquare(list(counts.values()))
    assert result.chi2 == pytest.approx(chi2)
    assert result.p_value == pytest.approx(p)
    assert result.passed()


def test_srm_flags_a_broken_split():
    result = srm_test({"control": 20_000, "treatment": 21_000})
    assert not result.passed()


def test_srm_respects_unequal_planned_split():
    result = srm_test({"control": 10_000, "treatment": 90_000}, {"control": 0.1, "treatment": 0.9})
    assert result.p_value == pytest.approx(1.0)


def test_smd_known_value():
    treated = [2.0, 4.0, 6.0]   # mean 4, var 4
    control = [1.0, 3.0, 5.0]   # mean 3, var 4
    assert standardized_mean_difference(treated, control) == pytest.approx(0.5)


def _randomised_frame(n=6_000, confounded=False, seed=1):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    cat = rng.choice(["u", "v", "w"], size=n)
    if confounded:
        prob = 1 / (1 + np.exp(-1.5 * x))
        group = np.where(rng.random(n) < prob, "treat", "ctrl")
    else:
        group = rng.choice(["ctrl", "treat"], size=n)
    return pd.DataFrame({"x": x, "cat": cat, "group": group})


def test_balance_table_expands_categories_and_computes_smd():
    df = _randomised_frame()
    table = balance_table(df, "group", "ctrl", ["x", "cat"], categorical=["cat"])
    assert list(table.index) == ["x", "cat = u", "cat = v", "cat = w"]
    assert table["SMD treat"].abs().max() < 0.1


def test_joint_test_detects_confounding_but_not_randomisation():
    assert joint_balance_test(_randomised_frame(), "group", "ctrl", "treat", ["x", "cat"], ["cat"]).p_value > 0.01
    assert joint_balance_test(
        _randomised_frame(confounded=True), "group", "ctrl", "treat", ["x", "cat"], ["cat"]
    ).p_value < 1e-6


def test_covariate_tests_returns_holm_adjusted_p_values():
    df = _randomised_frame()
    out = covariate_tests(df, "group", ["x", "cat"], categorical=["cat"])
    assert set(out["test"]) == {"Kruskal-Wallis", "chi-square"}
    assert (out["p_holm"] >= out["p_value"]).all()


def test_clean_hillstrom_fixes_labels_and_orders_categories():
    raw = pd.DataFrame({
        "recency": [1, 2],
        "history_segment": ["2) $100 - $200", "1) $0 - $100"],
        "history": [150.0, 50.0],
        "mens": [1, 0], "womens": [0, 1],
        "zip_code": ["Surburban", "Urban"],
        "newbie": [0, 1],
        "channel": ["Web", "Phone"],
        "segment": ["Mens E-Mail", "No E-Mail"],
        "visit": [1, 0], "conversion": [0, 0], "spend": [0.0, 0.0],
    })
    df = clean_hillstrom(raw)
    assert list(df["zip_code"]) == ["Suburban", "Urban"]
    assert list(df["arm"]) == ["mens", "control"]
    assert df["segment"].cat.categories[0] == "No E-Mail"
    assert df["history_segment"].cat.ordered
