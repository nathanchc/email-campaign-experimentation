# Part 3: A simulated multi-arm coupon experiment

> **Data:** simulated, with a known ground truth. The simulated world (`expt.simulate`) is loosely modelled on large-scale food-delivery coupon tests such as Meituan's MT-LIFT: five coupon levels, an offer → click → order funnel, a 20% platform commission, and coupons co-funded 50/50 with merchants. Analyses: [lesson 09](../notebooks/09_simulated_coupon_experiment.ipynb) and [lesson 10](../notebooks/10_simulated_monitoring.ipynb).

## Why a simulation

No public dataset combines several treatment arms, a funnel, defined metrics and real costs (see [Why this dataset](../README.md#why-this-dataset)). A simulation fills that gap, and adds something real data can never give: the **true** effect of every treatment, so every method can be checked against it.

## Lesson 09: five arms, a funnel and the cost of coupons

One experiment with 200,000 users per arm (no coupon, ¥3, ¥5, ¥8, ¥12):

| Coupon | Order lift (estimate / truth) | Profit per user vs no coupon (estimate / truth) |
|---|---|---|
| ¥3 | +24% / +25% | **+¥0.032 / +¥0.035** |
| ¥5 | +37% / +37% | +¥0.027 / +¥0.020 |
| ¥8 | +49% / +50% | −¥0.035 / −¥0.037 |
| ¥12 | **+61% / +64%** | −¥0.151 / −¥0.155 |

- **The coupon that maximises orders loses the most money**, because coupons are paid on every order that uses them, including orders that would have happened anyway. The primary metric must be profit, not orders.
- **Orders per click fall** as coupons grow, while orders per user rise: coupons attract extra, less committed clickers. Never judge a funnel step on a conditional metric.
- **With several arms**, Holm and Dunnett corrections agree here; ¥3 and ¥5 cannot be separated with this sample (truth: ¥3 is better by ¥0.015).
- **Targeting pays when treatments are expensive.** A simple rule (¥5 only for users who redeemed 3+ past coupons) earns +¥0.047 per user, more than any blanket coupon, and about 80% of the best achievable (+¥0.058). An uplift model trained on profit earns only +¥0.030.

## Lesson 10: watching an experiment while it runs

10,000 simulated experiments per scenario, 14 daily looks:

| Monitoring rule | False positives with no real effect |
|---|---|
| One look at the end | 4.5% |
| Daily look, stop at the first p < 0.05 | **22%** |
| Daily look, calibrated O'Brien–Fleming boundary | 4.7% |
| Daily look, stop when "P(better) > 95%" (Bayesian) | **19%** |

With a real +5% lift, the sequential design keeps 94% power (95% for a single final look) and stops on average around day 9 instead of 14.

Simulated percentages depend slightly on the numpy version (different random draws from the same seed): on another machine they may differ by a few tenths of a point, for example 4.9% instead of 4.5%. The conclusions are the same.

## Lessons

- Pick the metric that matches the business goal; for costly treatments that is profit.
- Outcomes per user assigned, never per click or per visitor.
- Fix the horizon in advance, or plan a sequential design; swapping p-values for Bayesian probabilities does not remove the peeking problem.
- Monitor validity (sample ratio) and harm (guardrails) daily, but declare winners only by the pre-registered rule.
