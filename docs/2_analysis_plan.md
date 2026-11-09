# 2 · Analysis plan

*Written before looking at any outcome. All numbers are computed in [`notebooks/ch2_experiment_design.ipynb`](../notebooks/ch2_experiment_design.ipynb).*

## Summary

- **A campaign pays for itself if it lifts purchases by about 11%.**
- **This experiment can only reliably detect a lift of about 47%.** At a plausible +30% effect it has a 42% chance of a clear result.
- So I fix in advance that a non-significant result on purchases means **inconclusive, not "no effect"**, and I judge the business case on revenue against break-even, with confidence intervals.

## Hypotheses

- **H1:** the men's email changes the share of customers who purchase within two weeks, compared with no email.
- **H2:** the same for the women's email.

Both two-sided, with the family-wise error rate held at 5% across the two tests (Holm correction). Men's vs women's is a secondary comparison.

## Metrics

| Role | Metric | Why |
|---|---|---|
| **Primary** | **Purchase rate** (share of customers who buy within two weeks) | The first metric that proves money moved. A catchy subject line can raise visits without sales; it cannot fake purchases |
| Secondary | Visit rate | The mechanism: did the email bring people back? Most sensitive metric |
| Secondary | Revenue per customer (all customers, including non-buyers) | The business value; weakly powered |
| Descriptive only | Purchase rate among visitors, spend per buyer | The email changes who visits and buys, so these compare different people |
| Guardrail | Unsubscribes, complaints | Not in the data; recorded as a limitation |
| Validity | Group sizes, balance of pre-treatment characteristics | Checked before any outcome is read |

Following the revenue decomposition in the [brief](1_project_brief.md), I expect the clearest effect on visits and the weakest signal on revenue. I still chose purchases as primary because the decision is about money, and kept visits as the key secondary metric.

## Break-even

| | Value |
|---|---|
| Sending cost per email | $0.010 |
| Creative cost per email ($8,000 / 640,000) | $0.0125 |
| **Total cost per email** | **$0.0225** |
| Break-even incremental revenue per email ($0.0225 / 40% margin) | **$0.056** |
| Equivalent lift in purchases (at a $100 order, from a 0.5% baseline) | **about +11%** |

## What the experiment can detect

21,333 customers per group, α = 0.025 per comparison (Bonferroni, conservative for Holm), 80% power:

| Metric | Minimum detectable effect |
|---|---|
| Visit rate | +0.91 points (+9%) |
| **Purchase rate** | **+0.23 points (+47%)** |
| Revenue per customer | +$0.28 (+57%) |

| True lift in purchases | Chance this test detects it | Customers per group needed for 80% |
|---|---|---|
| +11% (break-even) | 7% | 315,627, more than the whole file |
| +30% (plausible campaign) | 42% | 48,301 |
| +47% | 80% | the size of this test |

Visits are well covered: a +10% visit lift would be detected 87% of the time.

## Is an equal three-way split right?

A smaller holdout would email more customers during the test, but costs detection power and saves little:

| Holdout share | Holdout / each email group | Smallest purchase lift detected | Chance to detect +30% | Margin lost in holdout if +30% is real |
|---|---|---|---|---|
| 10% | 6,400 / 28,800 | +73% | 17% | $384 |
| 20% | 12,800 / 25,600 | +54% | 32% | $768 |
| **33%** | **21,333 / 21,333** | **+47%** | **42%** | **$1,280** |

With two campaigns to compare against the holdout and against each other, equal groups give the most information for about $1,300 of margin. The design as run is the right one.

## Analysis steps

1. **Validity first:** sample-ratio test; balance of all pre-treatment characteristics.
2. **Primary:** two-proportion z-tests of each email vs the holdout on purchase rate; Holm correction; 95% intervals for absolute and relative lift.
3. **Secondary:** visit rate the same way; revenue per customer with bootstrap intervals (mostly zeros, long tail).
4. **Business value:** incremental revenue per email, with its interval, against the $0.056 break-even.
5. **Precision:** a regression-adjusted estimate using pre-treatment characteristics.
6. **Exploratory only:** segment differences and uplift models.

## Decision rules

| Result on purchases | Conclusion |
|---|---|
| Validity check fails (sample-ratio p < 0.001 or clear imbalance) | Stop; do not read outcomes |
| Significant lift, and revenue per email ≥ $0.056 | The campaign causes purchases and pays for itself: roll out |
| Significant lift, revenue per email < $0.056 | Real effect that does not cover its cost |
| Not significant | **Inconclusive**: the test could miss effects up to about +47%; re-test larger rather than cut |

**Choosing between campaigns:** declare a winner only if the interval for the difference in revenue per email excludes zero; otherwise consider targeting.

## Known limitations

- No unsubscribe, complaint, return or margin data.
- A two-week window cannot separate new purchases from purchases pulled forward in time.
- Spend is gross revenue, not profit.
