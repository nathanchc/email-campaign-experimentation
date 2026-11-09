# Part 2: What goes wrong without randomisation

> **Data:** Lazada voucher dataset (Alibaba Group, released with the KDD 2022 paper *DESCN*). Real data; the outcome (`label`) and the 83 features are anonymised by Lazada. Analysis: [`notebooks/08_selection_bias_lazada.ipynb`](../notebooks/08_selection_bias_lazada.ipynb).

## Why this part exists

Part 1 answered "would they have bought anyway?" with a randomised holdout. Most companies estimate promotion effects from data where a targeting system decided who got the promotion. Lazada released the rare dataset that shows how far that can go wrong: the same voucher treatment, once **assigned by its targeting system** (926,669 customers) and once **assigned at random** (181,669 customers).

## Findings

| Method | Estimated effect of a voucher | vs the randomised answer |
|---|---|---|
| **Randomised experiment** | **+0.37 points (+11%), 95% CI +0.20 to +0.54** | |
| Naive comparison, targeted data | +4.72 points (six-fold outcome rate) | about 13x |
| Outcome regression (gradient-boosted trees) | +0.92 points | 2.5x |
| Inverse propensity weighting | +1.43 points | 3.8x |
| Doubly robust (AIPW) | +0.77 points, 95% CI +0.58 to +0.97 | 2.1x, and the interval excludes the truth |

*(Corrections estimated on a random 300,000 of the targeted customers.)*

## Why the corrections fall short

1. **The targeted groups were never comparable.** 67 of 83 features are imbalanced between customers who did and did not get vouchers (median standardised difference 0.41); in the randomised data, none are.
2. **No overlap.** The targeting is 94% predictable from the features: half the customers had a propensity below 5% or above 95%, so for them there is nobody comparable in the other group, and every correction extrapolates.
3. **Unmeasured reasons for targeting** cannot be adjusted for, and the data cannot reveal them.
4. **Different populations.** 55 of 83 features differ between the two files, and the no-voucher outcome rate is 0.94% in one and 3.33% in the other. Models trained on the targeted data predict a +1.21 point effect for the randomised customers, where the experiment measured +0.37.

## Lessons

- Targeted data can overstate an effect by an order of magnitude, because the people a system chooses are chosen for being likely to buy.
- Statistical corrections remove much of the bias but are no substitute for randomisation when targeting is strong.
- Their confidence intervals reflect sampling noise, not bias: a narrow interval around a wrong number.
- Validate against an experiment whenever possible. This is why the holdout in Part 1, and the long-term holdout in the [decision memo](07_decision_memo.md), are worth their cost.
