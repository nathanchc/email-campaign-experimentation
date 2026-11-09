import numpy as np
import pytest

from expt.simulate import CouponWorld, make_users, simulate_experiment, true_arm_values


@pytest.fixture(scope="module")
def truth():
    return true_arm_values(make_users(200_000, seed=0))


def test_orders_rise_with_coupon_value(truth):
    assert truth["order_rate"].is_monotonic_increasing


def test_profit_peaks_at_a_small_coupon_and_the_largest_loses_money(truth):
    gain = truth["profit_per_user"] - truth["profit_per_user"].iloc[0]
    assert gain.idxmax() in (1, 2)
    assert gain.iloc[-1] < 0


def test_orders_per_click_fall_with_bigger_coupons(truth):
    assert truth["orders_per_click"].iloc[-1] < truth["orders_per_click"].iloc[0]


def test_only_price_sensitive_users_are_profitable_to_couponise():
    users = make_users(200_000, seed=1)
    for flag, expect_gain in [(1, True), (0, False)]:
        t = true_arm_values(users[users["price_sensitive"] == flag])
        best_gain = (t["profit_per_user"] - t["profit_per_user"].iloc[0]).iloc[1:].max()
        assert (best_gain > 0) == expect_gain


def test_simulated_experiment_matches_truth():
    sim = simulate_experiment(n_per_arm=60_000, seed=3)
    assert np.bincount(sim["level"]).tolist() == [60_000] * 5
    truth = true_arm_values(sim)
    observed = sim.groupby("level")["order"].mean()
    assert np.allclose(observed, truth["order_rate"], atol=0.004)
    assert (sim.loc[sim["order"] == 0, "profit"] == 0).all()


def test_world_is_configurable():
    w = CouponWorld(coupon_values=(0.0, 5.0))
    sim = simulate_experiment(n_per_arm=1_000, world=w, seed=0)
    assert set(sim["coupon"]) == {0.0, 5.0}
