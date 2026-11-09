# 3 · Data validation

*Checked before comparing any outcome between groups. Analysis: [`notebooks/ch3_data_checks.ipynb`](../notebooks/ch3_data_checks.ipynb).*

## Summary

- **The randomisation worked**: group sizes match random thirds (p = 0.90), and the largest imbalance on any pre-treatment characteristic is 0.016 standard deviations (threshold 0.1).
- **The data is usable** after one label fix.
- **Two measurement gaps** make the results conservative: purchases appear to be recorded **online only**, and **spend is capped at $499**.

**Decision: go.** The results can be read as planned.

## Data

64,000 rows and 12 columns, no missing values, no customer ID. Outcome columns were checked only for structure and valid values, pooled across all groups.

## Findings

| # | Finding | Impact | Action |
|---|---|---|---|
| 1 | `zip_code` misspelled "Surburban" (28,776 rows) | Cosmetic | Recoded to "Suburban" |
| 2 | 6,562 identical rows; 99.5% are customers with past-year spend of exactly $29.99 and no activity; none are buyers | Identical customers, not repeated records (cannot be proven without an ID) | Kept |
| 3 | **Every purchase comes with a website visit**, although 44% of customers are phone-channel customers | Phone orders are probably missing: the measured effect is on **online** purchases and likely understates the total | Kept; stated with the results |
| 4 | **Spend tops out at exactly $499**, with 12 buyers at that value | Large orders appear capped: revenue effects are conservative | Kept as delivered; stated with the results |
| 5 | Past-spend buckets match past spend; every customer bought men's or women's merchandise | As expected | None |

The cleaning lives in one function, `expt.data.load_hillstrom()`, used by every later analysis.

## Sample ratio

| Group | Observed | Expected | Difference |
|---|---|---|---|
| No e-mail | 21,306 | 21,333 | −27 |
| Men's e-mail | 21,307 | 21,333 | −26 |
| Women's e-mail | 21,387 | 21,333 | +54 |

Chi-square = 0.20, p = 0.90. A mismatch would be flagged at p < 0.001.

## Balance

| Check | Result | Threshold |
|---|---|---|
| Largest standardised difference, 18 characteristics, both emails vs holdout | 0.016 | 0.1 |
| One test per characteristic (8 tests) | All p between 0.36 and 0.93 | Holm-adjusted p < 0.05 |
| Joint test: do the characteristics together predict group membership? | p = 0.70 (men's), 0.92 (women's) | p < 0.05 |

I don't rely on single p-values here: in a placebo check with randomly shuffled groups, at least one of the eight characteristics looked "significantly" imbalanced in 27% of perfectly random assignments. The decision rests on the size of differences and the joint test.
