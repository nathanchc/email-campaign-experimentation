import numpy as np
import pytest

from expt.sequential import apply_rule, calibrate_obf, obf_boundaries, simulate_daily_paths

Z = 1.959963984540054


@pytest.fixture(scope="module")
def aa_paths():
    return simulate_daily_paths(0.05, 0.05, 2_000, 14, 4_000, seed=1)


def test_single_final_look_has_nominal_false_positive_rate(aa_paths):
    fpr = (np.abs(aa_paths.z[:, -1]) > Z).mean()
    assert fpr == pytest.approx(0.05, abs=0.012)


def test_daily_peeking_inflates_false_positives(aa_paths):
    res = apply_rule(aa_paths.z, lambda z: np.abs(z) > Z)
    assert res.share_stopped > 0.15


def test_calibrated_obf_restores_the_error_rate(aa_paths):
    c = calibrate_obf(14, n_sims=20_000, seed=2)
    bounds = obf_boundaries(14, c)
    res = apply_rule(aa_paths.z, lambda z: np.abs(z) > bounds)
    assert res.share_stopped == pytest.approx(0.05, abs=0.012)
    assert bounds[0] > bounds[-1] > Z


def test_bayesian_probability_tracks_the_z_statistic(aa_paths):
    # With flat priors and large samples, P(better) is close to the one-sided normal CDF of z.
    from scipy import stats
    assert np.allclose(aa_paths.prob_better[:, -1], stats.norm.cdf(aa_paths.z[:, -1]), atol=0.02)


def test_real_effect_is_usually_detected():
    paths = simulate_daily_paths(0.05, 0.056, 2_000, 14, 2_000, seed=3)
    assert (np.abs(paths.z[:, -1]) > Z).mean() > 0.7
