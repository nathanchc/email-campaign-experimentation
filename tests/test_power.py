import math

import numpy as np
import pytest

from expt.power import (
    mde_mean,
    mde_proportion,
    power_proportions,
    sample_size_mean,
    sample_size_proportions,
    zero_inflated_sd,
)


def test_sample_size_proportions_matches_textbook_formula():
    # Classic two-sample formula (pooled under H0, unpooled under H1), equal groups.
    p1, p2, alpha, power = 0.10, 0.12, 0.05, 0.8
    z_a, z_b = 1.959963984540054, 0.8416212335729143
    p_bar = (p1 + p2) / 2
    expected = (
        z_a * math.sqrt(2 * p_bar * (1 - p_bar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2 / (p2 - p1) ** 2
    n_c, n_t = sample_size_proportions(p1, p2, alpha, power)
    assert n_c == n_t == math.ceil(expected)


def test_sample_size_proportions_close_to_statsmodels():
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize

    h = proportion_effectsize(0.12, 0.10)
    reference = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.8)
    n_c, _ = sample_size_proportions(0.10, 0.12)
    assert n_c == pytest.approx(reference, rel=0.01)


def test_mde_proportion_inverts_sample_size():
    n_c, n_t = 21_333, 21_333
    mde = mde_proportion(0.05, n_c, n_t, alpha=0.025)
    needed_c, _ = sample_size_proportions(0.05, 0.05 + mde, alpha=0.025)
    assert needed_c == pytest.approx(n_c, abs=2)


def test_power_at_mde_is_requested_power():
    mde = mde_proportion(0.05, 8_000, 8_000, alpha=0.05, power=0.8)
    assert power_proportions(0.05, 0.05 + mde, 8_000, 8_000, alpha=0.05) == pytest.approx(0.8, abs=1e-6)


def test_power_grows_with_effect_size():
    small = power_proportions(0.05, 0.055, 10_000, 10_000)
    large = power_proportions(0.05, 0.065, 10_000, 10_000)
    assert 0 < small < large < 1


def test_unequal_groups_need_more_customers_in_total():
    equal = sum(sample_size_proportions(0.05, 0.06, ratio=1))
    unequal = sum(sample_size_proportions(0.05, 0.06, ratio=4))
    assert unequal > equal


def test_mde_shrinks_with_sample_size():
    small = mde_proportion(0.05, 1_000, 1_000)
    large = mde_proportion(0.05, 10_000, 10_000)
    assert large < small


def test_mean_functions_are_inverse():
    sd, n = 10.0, 5_000
    delta = mde_mean(sd, n, n)
    n_c, n_t = sample_size_mean(sd, delta)
    assert n_c == pytest.approx(n, abs=1)
    assert n_t == n_c


def test_zero_inflated_sd_matches_simulation():
    rng = np.random.default_rng(0)
    n, p, mean, sd = 2_000_000, 0.01, 100.0, 80.0
    buys = rng.random(n) < p
    spend = np.where(buys, rng.normal(mean, sd, n), 0.0)
    assert zero_inflated_sd(p, mean, sd) == pytest.approx(spend.std(), rel=0.02)


@pytest.mark.parametrize("bad", [0, 1, -0.1, 1.5])
def test_invalid_proportions_raise(bad):
    with pytest.raises(ValueError):
        mde_proportion(bad, 100, 100)
