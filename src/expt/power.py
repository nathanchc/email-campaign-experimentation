"""Sample size and minimum detectable effect (MDE) for A/B tests.

Two kinds of metric are covered:

* proportions (visit rate, conversion rate), using the normal approximation
  with the pooled variance under H0 and unpooled variance under H1;
* means (spend per customer), using a known or assumed standard deviation.

All functions allow unequal group sizes, because business tests often keep the
control (holdout) group small to limit the cost of not treating people.
"""
from __future__ import annotations

import math

from scipy.optimize import brentq
from scipy.stats import norm


def _z_values(alpha: float, power: float, two_sided: bool) -> tuple[float, float]:
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if not 0 < power < 1:
        raise ValueError("power must be between 0 and 1")
    z_alpha = norm.ppf(1 - alpha / 2) if two_sided else norm.ppf(1 - alpha)
    return z_alpha, norm.ppf(power)


def _proportion_z_gap(
    p_control: float,
    p_treatment: float,
    n_control: float,
    n_treatment: float,
    alpha: float,
    power: float,
    two_sided: bool,
) -> float:
    """Zero when (n_control, n_treatment) give exactly the requested power."""
    z_alpha, z_beta = _z_values(alpha, power, two_sided)
    delta = abs(p_treatment - p_control)
    p_bar = (n_control * p_control + n_treatment * p_treatment) / (n_control + n_treatment)
    se_null = math.sqrt(p_bar * (1 - p_bar) * (1 / n_control + 1 / n_treatment))
    se_alt = math.sqrt(
        p_control * (1 - p_control) / n_control + p_treatment * (1 - p_treatment) / n_treatment
    )
    return delta - (z_alpha * se_null + z_beta * se_alt)


def sample_size_proportions(
    p_control: float,
    p_treatment: float,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    two_sided: bool = True,
) -> tuple[int, int]:
    """Customers needed in (control, treatment) to detect p_control -> p_treatment.

    ``ratio`` is n_treatment / n_control; 1.0 means equal groups.
    """
    if not (0 < p_control < 1 and 0 < p_treatment < 1):
        raise ValueError("proportions must be strictly between 0 and 1")
    if p_control == p_treatment:
        raise ValueError("p_control and p_treatment must differ")
    if ratio <= 0:
        raise ValueError("ratio must be positive")

    def gap(n_c: float) -> float:
        return _proportion_z_gap(p_control, p_treatment, n_c, ratio * n_c, alpha, power, two_sided)

    hi = 10.0
    while gap(hi) < 0:
        hi *= 2
    n_control = brentq(gap, 2.0, hi)
    return math.ceil(n_control), math.ceil(ratio * n_control)


def mde_proportion(
    p_control: float,
    n_control: int,
    n_treatment: int,
    alpha: float = 0.05,
    power: float = 0.8,
    two_sided: bool = True,
) -> float:
    """Smallest absolute increase over ``p_control`` detectable with the given groups."""
    if not 0 < p_control < 1:
        raise ValueError("p_control must be strictly between 0 and 1")

    def gap(delta: float) -> float:
        return _proportion_z_gap(
            p_control, p_control + delta, n_control, n_treatment, alpha, power, two_sided
        )

    upper = 1 - p_control - 1e-12
    if gap(upper) < 0:
        raise ValueError("groups too small to detect any increase at this power")
    return brentq(gap, 1e-12, upper)


def power_proportions(
    p_control: float,
    p_treatment: float,
    n_control: int,
    n_treatment: int,
    alpha: float = 0.05,
    two_sided: bool = True,
) -> float:
    """Probability of detecting the change p_control -> p_treatment with these groups."""
    if not (0 < p_control < 1 and 0 < p_treatment < 1):
        raise ValueError("proportions must be strictly between 0 and 1")
    z_alpha = norm.ppf(1 - alpha / 2) if two_sided else norm.ppf(1 - alpha)
    delta = abs(p_treatment - p_control)
    p_bar = (n_control * p_control + n_treatment * p_treatment) / (n_control + n_treatment)
    se_null = math.sqrt(p_bar * (1 - p_bar) * (1 / n_control + 1 / n_treatment))
    se_alt = math.sqrt(
        p_control * (1 - p_control) / n_control + p_treatment * (1 - p_treatment) / n_treatment
    )
    return float(norm.cdf((delta - z_alpha * se_null) / se_alt))


def mde_mean(
    sd: float,
    n_control: int,
    n_treatment: int,
    alpha: float = 0.05,
    power: float = 0.8,
    two_sided: bool = True,
) -> float:
    """Smallest absolute difference in means detectable, for a metric with this SD."""
    if sd <= 0:
        raise ValueError("sd must be positive")
    z_alpha, z_beta = _z_values(alpha, power, two_sided)
    return (z_alpha + z_beta) * sd * math.sqrt(1 / n_control + 1 / n_treatment)


def sample_size_mean(
    sd: float,
    delta: float,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    two_sided: bool = True,
) -> tuple[int, int]:
    """Customers needed in (control, treatment) to detect a difference ``delta`` in means."""
    if sd <= 0 or delta == 0:
        raise ValueError("sd must be positive and delta non-zero")
    if ratio <= 0:
        raise ValueError("ratio must be positive")
    z_alpha, z_beta = _z_values(alpha, power, two_sided)
    n_control = ((z_alpha + z_beta) * sd / abs(delta)) ** 2 * (1 + 1 / ratio)
    return math.ceil(n_control), math.ceil(ratio * n_control)


def zero_inflated_sd(conversion_rate: float, order_mean: float, order_sd: float) -> float:
    """SD of spend per customer when most customers spend nothing.

    Spend = 0 with probability 1 - p, and an order value with mean ``order_mean``
    and SD ``order_sd`` with probability p. Then
    Var(spend) = p * (order_sd**2 + order_mean**2) - (p * order_mean)**2.
    """
    if not 0 < conversion_rate < 1:
        raise ValueError("conversion_rate must be strictly between 0 and 1")
    p = conversion_rate
    variance = p * (order_sd**2 + order_mean**2) - (p * order_mean) ** 2
    return math.sqrt(variance)
