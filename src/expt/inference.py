"""Estimating treatment effects and their uncertainty.

* ``compare_proportions``: absolute and relative lift of a rate, with a z-test.
* ``compare_means``: difference in means with Welch's standard error.
* ``bootstrap_diff_in_means``: a resampling confidence interval that does not
  rely on the normal approximation (useful for skewed, mostly-zero revenue).
* ``holm``: Holm's adjustment of p-values for several comparisons.
* ``regression_adjusted_effect``: a more precise effect estimate that uses
  pre-treatment covariates (Lin's interacted regression).
* ``cuped``: the CUPED adjustment of a metric with one pre-treatment covariate.
* ``ratio_delta_method``: standard error of a ratio of two means.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests


def _z(alpha: float) -> float:
    return float(stats.norm.ppf(1 - alpha / 2))


@dataclass(frozen=True)
class ProportionComparison:
    n_control: int
    n_treatment: int
    rate_control: float
    rate_treatment: float
    diff: float
    diff_low: float
    diff_high: float
    lift: float
    lift_low: float
    lift_high: float
    z: float
    p_value: float

    def to_dict(self) -> dict:
        return asdict(self)


def compare_proportions(
    successes_treatment: int,
    n_treatment: int,
    successes_control: int,
    n_control: int,
    alpha: float = 0.05,
) -> ProportionComparison:
    """Treatment vs control on a rate.

    The p-value uses the pooled-variance z-test (the usual test of "no
    difference"). The confidence interval for the absolute difference uses
    the unpooled standard error. The relative lift ``rate_t / rate_c - 1``
    gets its interval from the delta method on the log of the ratio.
    """
    p_t = successes_treatment / n_treatment
    p_c = successes_control / n_control
    diff = p_t - p_c

    p_pool = (successes_treatment + successes_control) / (n_treatment + n_control)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_treatment + 1 / n_control))
    z = diff / se_pool
    p_value = 2 * stats.norm.sf(abs(z))

    zc = _z(alpha)
    se_diff = np.sqrt(p_t * (1 - p_t) / n_treatment + p_c * (1 - p_c) / n_control)

    if successes_treatment > 0 and successes_control > 0:
        log_ratio = np.log(p_t / p_c)
        se_log = np.sqrt((1 - p_t) / successes_treatment + (1 - p_c) / successes_control)
        lift_low, lift_high = np.exp(log_ratio - zc * se_log) - 1, np.exp(log_ratio + zc * se_log) - 1
    else:
        lift_low = lift_high = np.nan

    return ProportionComparison(
        n_control=int(n_control),
        n_treatment=int(n_treatment),
        rate_control=p_c,
        rate_treatment=p_t,
        diff=diff,
        diff_low=diff - zc * se_diff,
        diff_high=diff + zc * se_diff,
        lift=p_t / p_c - 1 if p_c > 0 else np.nan,
        lift_low=float(lift_low),
        lift_high=float(lift_high),
        z=float(z),
        p_value=float(p_value),
    )


@dataclass(frozen=True)
class MeanComparison:
    mean_control: float
    mean_treatment: float
    diff: float
    se: float
    diff_low: float
    diff_high: float
    p_value: float

    def to_dict(self) -> dict:
        return asdict(self)


def compare_means(treatment: Sequence[float], control: Sequence[float], alpha: float = 0.05) -> MeanComparison:
    """Difference in means with Welch's (unequal-variance) standard error."""
    t = np.asarray(treatment, dtype=float)
    c = np.asarray(control, dtype=float)
    diff = t.mean() - c.mean()
    se = np.sqrt(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c))
    _, p_value = stats.ttest_ind(t, c, equal_var=False)
    zc = _z(alpha)
    return MeanComparison(c.mean(), t.mean(), diff, se, diff - zc * se, diff + zc * se, float(p_value))


@dataclass(frozen=True)
class BootstrapResult:
    diff: float
    diff_low: float
    diff_high: float
    draws: np.ndarray


def bootstrap_diff_in_means(
    treatment: Sequence[float],
    control: Sequence[float],
    n_boot: int = 2_000,
    alpha: float = 0.05,
    seed: int | None = 0,
) -> BootstrapResult:
    """Percentile bootstrap interval for the difference in means.

    Each draw resamples customers with replacement within each group. The loop
    keeps memory small, which matters for large groups.
    """
    t = np.asarray(treatment, dtype=float)
    c = np.asarray(control, dtype=float)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot)
    for b in range(n_boot):
        draws[b] = t[rng.integers(0, len(t), len(t))].mean() - c[rng.integers(0, len(c), len(c))].mean()
    low, high = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return BootstrapResult(float(t.mean() - c.mean()), float(low), float(high), draws)


def holm(p_values: Sequence[float]) -> np.ndarray:
    """Holm-adjusted p-values: control the chance of any false positive across tests."""
    return multipletests(np.asarray(p_values, dtype=float), method="holm")[1]


@dataclass(frozen=True)
class AdjustedEffect:
    estimate: float
    se: float
    ci_low: float
    ci_high: float
    p_value: float


def regression_adjusted_effect(
    y: Sequence[float],
    treated: Sequence[int],
    covariates: pd.DataFrame | None = None,
    alpha: float = 0.05,
) -> AdjustedEffect:
    """Treatment effect from OLS with centred covariates and their interactions
    with treatment (Lin, 2013), using HC2 robust standard errors.

    In a randomised experiment this stays unbiased for the average effect, and
    it is never less precise than the simple difference in means asymptotically.
    With ``covariates=None`` it reduces to the difference in means.
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(treated, dtype=float)
    parts = [pd.Series(d, name="treated")]
    if covariates is not None and covariates.shape[1] > 0:
        x = covariates.reset_index(drop=True).astype(float)
        x = x - x.mean()
        inter = x.mul(d, axis=0).add_prefix("treated_x_")
        parts += [x, inter]
    X = sm.add_constant(pd.concat(parts, axis=1), has_constant="add")
    fit = sm.OLS(y, X).fit(cov_type="HC2")
    est, se = fit.params["treated"], fit.bse["treated"]
    zc = _z(alpha)
    return AdjustedEffect(float(est), float(se), float(est - zc * se), float(est + zc * se), float(fit.pvalues["treated"]))


def cuped(y: Sequence[float], x: Sequence[float]) -> tuple[np.ndarray, float]:
    """CUPED-adjusted metric ``y - theta * (x - mean(x))`` and theta.

    ``x`` must be measured before treatment. theta is estimated on the pooled
    data, so the adjustment does not depend on group membership.
    """
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    theta = np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1)
    return y - theta * (x - x.mean()), float(theta)


def ratio_delta_method(numerator: Sequence[float], denominator: Sequence[float]) -> tuple[float, float]:
    """Ratio of means sum(num) / sum(den) and its delta-method standard error.

    Use it for metrics such as "orders per click" where both parts are
    measured per user and the user is the unit of randomisation.
    """
    a = np.asarray(numerator, dtype=float)
    b = np.asarray(denominator, dtype=float)
    n = len(a)
    ma, mb = a.mean(), b.mean()
    ratio = ma / mb
    va, vb = a.var(ddof=1), b.var(ddof=1)
    cov = np.cov(a, b, ddof=1)[0, 1]
    var_ratio = (va / mb**2 - 2 * ma * cov / mb**3 + ma**2 * vb / mb**4) / n
    return float(ratio), float(np.sqrt(var_ratio))
