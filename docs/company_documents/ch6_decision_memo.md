# Chapter 6 · Decision memo

> A company document from **Chapter 6** of the [case study](../../CASE_STUDY.md#6-the-recommendation). The data is real; the people and business figures are an invented scenario. Analysis: [`ch6_recommendation.ipynb`](../../notebooks/ch6_recommendation.ipynb).

**To:** CFO; Head of E-mail Marketing
**From:** Nathan Chen, Data Science
**Subject:** Spring e-mail test: approve the programme and roll out the men's campaign

## Decision requested

1. Approve next year's e-mail budget.
2. Send the **men's campaign** to the full active file (640,000 customers).
3. Approve a **long-term holdout** of 5% of the file for one quarter.

## Recommendation in brief

- **The emails cause sales that would not otherwise happen.** In a randomised test of 64,000 customers, the men's email more than doubled online purchases compared with sending nothing (+119%); the women's email raised them by about half (+54%).
- **They pay for themselves many times over.** The men's email brought in **$0.77 of extra revenue per email** against a break-even of $0.056: about **$183,000 of net margin per send** to the full file, after creative and sending costs (plausible range $113,000–$257,000).
- **Send the men's email to everyone.** It beat the women's email overall and was at least as good for every customer group. A targeting model added nothing measurable.

## Why we can trust this

- The test was designed and its decision rules signed off **before launch** ([design doc](ch2_experiment_design_doc.md)), and results were read only after the data and randomisation passed all checks ([validation report](ch3_validation_report.md)).
- Customers were assigned to email or no email **at random**, so the difference measures what the email caused, not who happened to receive it. That is the CFO's original concern, addressed directly.
- Both emails cleared every pre-registered rule ([readout](ch4_results_readout.md)).

## How robust is the money?

The figures depend on things the two-week test could not measure. The decision holds under any reasonable assumption:

| If... | Net margin per send (men's) |
|---|---|
| As measured (40% margin, all extra sales are new) | about $183,000 |
| Half the extra sales were only pulled forward from later weeks | about $84,000 |
| Margin is 30% and a quarter of sales were pulled forward | about $96,000 |
| **Break-even point** | More than **93%** of the extra sales would have to be pulled forward, or future campaigns would have to achieve under **7%** of this effect |

Two measurement gaps make the true effect likely *larger*: only online purchases were recorded, and individual spend was capped at $499.

## Risks and how we manage them

| Risk | Mitigation |
|---|---|
| Extra sales partly pulled forward in time | Long-term holdout (below) measures the effect over a full quarter |
| Customers tire of frequent emails; unsubscribes rise | E-mail Operations reports unsubscribes and complaints per send; the holdout shows any long-run decline |
| Future campaigns perform worse than this one | Each new creative is tested against the men's email before full rollout |
| Phone orders not measured | Operations to add phone orders to the data feed |

## What we will do next

| Next step | Size | What it tells us |
|---|---|---|
| **Long-term holdout:** 5% of the file receives no campaigns for one quarter | 32,000 customers; about $9,000 of margin per send | Whether the programme adds sales over time, net of pull-forward and fatigue. Detects a change of about 23% in the purchase rate |
| **Creative tests:** each new campaign vs the men's email, on visit rate | About 24,000 customers per arm for a 1-point visit difference | Which creative brings more customers in; revenue per customer as a guardrail. (Detecting a $0.10 revenue difference would need about 355,000 per arm) |
| **Data fixes:** phone orders, pre-period visits and purchases, customer IDs, unsubscribes per group | No cost | Complete measurement, and roughly a third more statistical power per test from pre-period data |

## Sign-off

| Role | Decision |
|---|---|
| CFO | |
| Head of E-mail Marketing | |

---

This memo closes the case. The full story is in the [case study](../../CASE_STUDY.md).
