# Step 4: Validation report (go / no-go)

> **Scenario note.** The data in this project is real (Hillstrom, 2008). The people, launch confirmations and sign-offs are invented to show how the step works in practice. All checks are computed in [`notebooks/02_validation.ipynb`](../notebooks/02_validation.ipynb).

| | |
|---|---|
| **Experiment** | Spring e-mail campaigns: incrementality test |
| **Author** | Nathan Chen, Data Science |
| **Reviewers** | E-mail Operations Manager; Head of E-mail Marketing |
| **Status** | **GO**: results may be read as pre-registered |
| **Written** | After the two-week window closed, **before any outcome was compared between groups** |

## TL;DR

- **The randomisation worked.** Group sizes match the planned thirds (p = 0.90), and the groups are alike on every customer characteristic: the largest difference is 0.016 standard deviations, against a 0.1 threshold.
- **The data is usable** after fixing one label.
- **Two caveats travel into the readout:** purchases appear to be recorded **online only**, and **spend is capped at $499**. Both make the measured effects conservative.

## 1. Launch checklist

From the [design doc](03_experiment_design_doc.md), confirmed at launch by E-mail Operations (scenario):

| Item | Status |
|---|---|
| Random assignment by customer ID; group sizes in expected range | Done |
| Customer characteristics balanced across groups | Done; re-checked below on the delivered data |
| Seed emails received and rendered correctly | Done |
| Visit and purchase tracking verified for sample customers in each group | Done |
| No other campaigns to the test sample during the window | Done |
| Analysis code written and reviewed before the window closed | Done |

## 2. Data received

- 64,000 rows and the 12 columns agreed in the data dictionary; no missing values.
- **No customer ID** in the extract (see finding 2).
- Outcome columns were checked only for structure and valid values, pooled across all groups, never compared between groups.

## 3. Data quality findings

| # | Finding | Impact | Action |
|---|---|---|---|
| 1 | `zip_code` label misspelled "Surburban" (28,776 rows) | Cosmetic; could break joins with other data | Recoded to "Suburban" |
| 2 | 6,562 identical rows. 99.5% of them are customers with past-year spend of exactly $29.99 who did nothing in the window; none are buyers | Identical customers, not repeated records. Cannot be proven without an ID | Kept. **Request customer IDs in future extracts** |
| 3 | **Every purchase comes with a website visit.** 44% of customers (28,021) are phone-channel customers | Purchases appear to be **online only**; email-prompted phone orders are probably missing. Measured effects are effects on online purchases and likely understate the total | Kept. **Operations to confirm** which order channels the extract covers. Stated in the readout |
| 4 | **Spend tops out at exactly $499**, with 12 buyers at that value (the 99th percentile) | Typical of top-coding: large orders are understated, so revenue effects are measured conservatively | Kept as delivered. Stated as a limitation |
| 5 | `history_segment` matches the `history` buckets; every customer bought men's or women's merchandise in the past year (6,448 bought both) | As expected from the population definition | None |
| 6 | 136 buyers spent exactly $29.99, the most common past-spend value | Most likely a popular price point | None |

The cleaning is implemented once in `expt.data.load_hillstrom()`, so every later analysis uses the same data.

## 4. Sample-ratio check

| Group | Observed | Expected | Difference |
|---|---|---|---|
| No e-mail | 21,306 | 21,333 | −27 |
| Men's e-mail | 21,307 | 21,333 | −26 |
| Women's e-mail | 21,387 | 21,333 | +54 |

Chi-square = 0.20, **p = 0.90**. The threshold for a mismatch is p < 0.001. **Pass.**

## 5. Covariate balance

| Check | Result | Threshold | Verdict |
|---|---|---|---|
| Size of imbalance: largest standardised mean difference across 18 characteristics, both emails vs holdout | 0.016 | 0.1 | Pass |
| One test per characteristic (8 tests) | All p between 0.36 and 0.93 | Holm-adjusted p < 0.05 | Pass |
| Joint test: can the characteristics together predict group membership? | p = 0.70 (men's), p = 0.92 (women's) | p < 0.05 | Pass |

**Why the decision does not rest on single p-values:** in a placebo exercise (group labels shuffled at random 300 times, so any imbalance is pure chance), at least one of the eight characteristics came out "significant" at p < 0.05 in **27%** of perfectly random assignments. A single small p-value is therefore expected now and then and is not evidence of a broken experiment. The verdict uses the size of imbalances, adjusted p-values and the joint test.

## 6. Decision

**GO.** The randomisation can be trusted and the data is fit for analysis. The readout proceeds exactly as pre-registered in the [design doc](03_experiment_design_doc.md).

**Carried into the readout:**

1. Effects are on **online** purchases and revenue only (pending confirmation from Operations).
2. Revenue per customer is computed on spend **capped at $499**.
3. Guardrail data (unsubscribes, complaints) comes from the e-mail platform and is not in this extract.

## 7. Sign-off

| Role | Decision |
|---|---|
| Data Science | GO |
| E-mail Operations Manager | Agreed; will confirm which order channels the extract covers |
| Head of E-mail Marketing | Agreed |

---

**Next:** [Step 5: results readout](05_readout.md) (lessons 03–05).
