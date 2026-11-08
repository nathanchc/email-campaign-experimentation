# Pre-registration: Hillstrom e-mail experiment

**Status:** draft v0.1, metric choices to be confirmed
**Written:** before any outcome data (`visit`, `conversion`, `spend`) was examined
**Supporting analysis:** `notebooks/01_context_and_design.ipynb`

## 1. Business question

Recent customers often buy without being prompted. Does a campaign email cause additional visits, purchases and revenue compared with sending nothing, which of the two emails works better, and which customers should receive which email?

## 2. Design

| Item | Value |
|---|---|
| Unit of randomisation and analysis | Customer |
| Population | 64,000 customers who purchased in the last 12 months |
| Arms | No e-mail (control), Men's e-mail, Women's e-mail |
| Allocation | Random, one third per arm (planned 21,333 per arm) |
| Observation window | Two weeks after the send |

## 3. Metrics

| Role | Metric | Definition |
|---|---|---|
| **Primary** | Conversion rate | Share of customers with `conversion = 1` |
| Secondary | Visit rate | Share of customers with `visit = 1` |
| Secondary | Spend per customer | Mean of `spend`, including zeros |
| Descriptive only | P(purchase \| visit), spend per buyer | Conditional on post-treatment behaviour, so not randomised comparisons |
| Guardrail (not available) | Unsubscribes, complaints, returns, margin | Reported as a limitation |
| Validity | Sample-ratio mismatch, covariate balance | Checked before outcomes are read |

## 4. Hypotheses

- **H1:** the men's e-mail changes the conversion rate compared with no e-mail.
- **H2:** the women's e-mail changes the conversion rate compared with no e-mail.

Two-sided tests. Family-wise error rate controlled at 5% across H1 and H2 using the Holm correction. Men's vs women's is a secondary comparison, reported with a confidence interval.

## 5. Power analysis

Planning assumptions (no historical data available; this experiment's control group was not used):

| Assumption | Value |
|---|---|
| Visit rate without email | 10% |
| Conversion rate without email | 0.5% |
| Order value | mean $100, SD $90 |
| Implied spend per customer | mean $0.50, SD $9.50 |

With 21,333 customers per arm, α = 0.025 per comparison (Bonferroni planning for two comparisons) and 80% power:

| Metric | Minimum detectable effect |
|---|---|
| Visit rate | +0.91 points (about +9% relative) |
| **Conversion rate** | **+0.23 points (about +47% relative)** |
| Spend per customer | +$0.28 (about +57% relative) |

The experiment is well powered for visits but only for large effects on purchases and revenue. A non-significant conversion result would therefore not show that the email has no effect, only that any effect is smaller than about 47%. If the true baseline conversion is 1%, the MDE falls to about 32%; if it is 0.3%, it rises above 60%.

## 6. Decision rules

1. **Validity first.** If the sample-ratio test gives p < 0.001 or pre-treatment covariates are clearly imbalanced, stop and investigate before reading outcomes.
2. **An email works** if its conversion lift over the control is positive and significant at family-wise α = 0.05 (Holm).
3. **Secondary metrics explain, they do not decide.** Visit and spend lifts are reported with 95% confidence intervals. A significant visit lift without a significant conversion lift is reported as "brings traffic; purchase effect not shown".
4. **Choosing between emails** uses incremental spend per email sent, with a confidence interval. If the intervals overlap heavily, no winner is declared and targeting is considered instead.
5. **Segments** not listed in this document are exploratory and require a new test to confirm.

## 7. Known limitations

- No unsubscribe, complaint, return or margin data: long-term costs of emailing cannot be assessed.
- Two-week window only: effects that appear later, or purchases merely pulled forward in time, are not captured.
- `spend` is gross revenue, not profit.
