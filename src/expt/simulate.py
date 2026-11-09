"""A simulated food-delivery coupon experiment with a known ground truth.

Loosely modelled on large-scale coupon tests run by delivery apps (such as the
MT-LIFT setting): users are randomly assigned one of several coupon levels,
and outcomes follow the funnel impression -> click -> order. Because the
probabilities are set here, the true effect of every coupon, for every user,
is known, so any analysis method can be checked against it.

How the simulated world works
-----------------------------
* Each user has a hidden purchase **intent** and may be **price-sensitive**.
* Coupons raise the chance of clicking, more for price-sensitive users. Extra
  clicks come disproportionately from low-intent users, so "orders per click"
  can fall even when orders per user rise (the ratio-metric trap).
* Once a user has clicked, whether they order depends on their intent (the
  ``order_effect`` parameter can add a coupon effect at this step too).
* The platform earns a commission on each order and pays its share of the
  coupon on **every** order that uses it, including orders that would have
  happened anyway.
* Observable features (past orders, coupon history, new user, city tier) are
  noisy signals of intent and price sensitivity.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CouponWorld:
    coupon_values: tuple[float, ...] = (0.0, 3.0, 5.0, 8.0, 12.0)  # yuan; level 0 = no coupon
    share_price_sensitive: float = 0.35
    click_effect: float = 0.30           # log-odds increase in clicking per unit of coupon "strength"
    sensitivity_multiplier: float = 4.0  # price-sensitive users respond this much more
    order_effect: float = 0.0            # log-odds increase in ordering after a click (0: intent decides)
    order_value_mean: float = 52.0       # yuan
    order_value_sd: float = 22.0
    commission: float = 0.20             # platform's share of the order value
    platform_coupon_share: float = 0.5   # platform pays this share of the coupon; merchants the rest
    days: int = 14
    extra: dict = field(default_factory=dict)

    def strength(self, value: np.ndarray | float) -> np.ndarray:
        """Diminishing returns: the 12-yuan coupon is not four times the 3-yuan one."""
        return np.log1p(np.asarray(value, dtype=float) / 4.0)


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _logit(p):
    return np.log(p / (1 - p))


def make_users(n: int, world: CouponWorld = CouponWorld(), seed: int | None = 0) -> pd.DataFrame:
    """Users with hidden traits (intent, price sensitivity) and observable features."""
    rng = np.random.default_rng(seed)
    intent = rng.beta(2.0, 9.0, n)
    sensitive = rng.random(n) < world.share_price_sensitive
    new_user = rng.random(n) < 0.2
    city_tier = rng.choice([1, 2, 3], size=n, p=[0.3, 0.45, 0.25])
    past_orders = rng.poisson(1 + 25 * intent * np.where(new_user, 0.3, 1.0))
    coupon_history = rng.binomial(10, np.where(sensitive, 0.45, 0.12))  # past coupons redeemed out of 10 offers
    return pd.DataFrame({
        "past_orders": past_orders,
        "coupon_history": coupon_history,
        "new_user": new_user.astype(int),
        "city_tier": city_tier,
        "intent": intent,              # hidden
        "price_sensitive": sensitive.astype(int),  # hidden
        "arrival_day": rng.integers(1, world.days + 1, n),
    })


def outcome_probabilities(users: pd.DataFrame, coupon_value: float, world: CouponWorld = CouponWorld()) -> dict:
    """True click, order and profit expectations for every user under one coupon value."""
    intent = users["intent"].to_numpy()
    sens = users["price_sensitive"].to_numpy()
    s = world.strength(coupon_value)
    response = 1 + (world.sensitivity_multiplier - 1) * sens

    base_click = 0.08 + 0.9 * intent
    p_click = _sigmoid(_logit(base_click) + world.click_effect * s * response)

    base_order = 0.04 + 0.7 * intent
    p_order_given_click = _sigmoid(_logit(base_order) + world.order_effect * s * response)

    p_order = p_click * p_order_given_click
    margin_per_order = world.commission * world.order_value_mean - world.platform_coupon_share * coupon_value
    return {
        "p_click": p_click,
        "p_order_given_click": p_order_given_click,
        "p_order": p_order,
        "expected_profit": p_order * margin_per_order,
    }


def true_arm_values(users: pd.DataFrame, world: CouponWorld = CouponWorld()) -> pd.DataFrame:
    """Population averages under each coupon level: the ground truth an experiment estimates."""
    rows = []
    for level, value in enumerate(world.coupon_values):
        p = outcome_probabilities(users, value, world)
        rows.append({
            "level": level,
            "coupon": value,
            "click_rate": p["p_click"].mean(),
            "order_rate": p["p_order"].mean(),
            "orders_per_click": p["p_order"].sum() / p["p_click"].sum(),
            "profit_per_user": p["expected_profit"].mean(),
        })
    return pd.DataFrame(rows).set_index("level")


def simulate_experiment(
    n_per_arm: int = 100_000,
    world: CouponWorld = CouponWorld(),
    seed: int | None = 0,
) -> pd.DataFrame:
    """One randomised experiment: equal arms, outcomes drawn from the true probabilities."""
    n_arms = len(world.coupon_values)
    users = make_users(n_per_arm * n_arms, world, seed)
    rng = np.random.default_rng(None if seed is None else seed + 1)
    level = rng.permutation(np.repeat(np.arange(n_arms), n_per_arm))
    coupon = np.asarray(world.coupon_values)[level]

    p_click = np.empty(len(users))
    p_ogc = np.empty(len(users))
    for lv, value in enumerate(world.coupon_values):
        mask = level == lv
        probs = outcome_probabilities(users[mask], value, world)
        p_click[mask], p_ogc[mask] = probs["p_click"], probs["p_order_given_click"]

    click = rng.random(len(users)) < p_click
    order = click & (rng.random(len(users)) < p_ogc)
    order_value = np.where(order, np.maximum(rng.normal(world.order_value_mean, world.order_value_sd, len(users)), 10.0), 0.0)
    profit = np.where(order, world.commission * order_value - world.platform_coupon_share * coupon, 0.0)

    out = users.copy()
    out["level"] = level
    out["coupon"] = coupon
    out["click"] = click.astype(int)
    out["order"] = order.astype(int)
    out["order_value"] = order_value
    out["profit"] = profit
    return out
