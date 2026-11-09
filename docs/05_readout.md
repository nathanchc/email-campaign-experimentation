# Step 5: Results readout

> **Scenario note.** The data and results are real (Hillstrom, 2008). The business figures (margin, costs, file size) and the people are the invented scenario from the [request](01_request.md) and [kickoff](02_kickoff_notes.md). Analyses: [lesson 03](../notebooks/03_purchases_and_visits.ipynb) (purchases and visits), [lesson 04](../notebooks/04_revenue.ipynb) (revenue and business case), [lesson 05](../notebooks/05_variance_reduction.ipynb) (variance reduction).

| | |
|---|---|
| **Experiment** | Spring e-mail campaigns: incrementality test |
| **Author** | Nathan Chen, Data Science |
| **Audience** | Head of E-mail Marketing; CFO; E-mail Operations Manager |
| **Status** | Final. Analysed exactly as pre-registered in the [design doc](03_experiment_design_doc.md), after the [validation report](04_validation_report.md) gave a go |

## TL;DR

- **Both emails cause additional purchases, and both pay for themselves many times over.** The men's email more than doubles the purchase rate (+119%); the women's raises it by about half (+54%).
- **Incremental revenue per email:** men's **$0.77**, women's **$0.42**, against a break-even of **$0.056**. Even the low ends of the confidence intervals are far above break-even.
- **The men's email is the better campaign** on purchases, visits and revenue.
- **Recommendation:** approve the e-mail programme and roll out the men's campaign; the [targeting analysis](06_targeting_analysis.md) then checks whether some customers should get the women's email instead.
- **Caveats:** only online purchases are measured and spend is capped at $499 (both make these results conservative); a two-week window cannot rule out purchases merely pulled forward.

## 1. Results

**Primary metric: purchase rate** (two-week window, all customers in each group)

| Group | Purchase rate | Lift vs no e-mail | 95% CI of lift | Holm-adjusted p |
|---|---|---|---|---|
| No e-mail | 0.57% | | | |
| Men's e-mail | 1.25% | **+0.68 points (+119%)** | +77% to +171% | < 0.001 |
| Women's e-mail | 0.88% | **+0.31 points (+54%)** | +23% to +94% | < 0.001 |

**Secondary metrics**

| Metric | No e-mail | Men's e-mail | Women's e-mail |
|---|---|---|---|
| Visit rate | 10.6% | 18.3% (+72%) | 15.1% (+43%) |
| Revenue per customer | $0.65 | $1.42 (+$0.77) | $1.08 (+$0.42) |
| 95% CI of revenue lift (bootstrap) | | $0.50 to $1.06 | $0.16 to $0.68 |

The baseline came in close to plan (0.57% purchase rate vs 0.5% assumed; 10.6% visit rate vs 10%), so the test was as sensitive as designed. Both effects turned out much larger than the +47% it could reliably detect.

## 2. Is it worth the money?

| | Men's e-mail | Women's e-mail |
|---|---|---|
| Incremental revenue per email | $0.77 | $0.42 |
| Multiple of break-even ($0.056) | 14x | 7.5x |
| Net margin per email (40% margin minus $0.0225 cost) | $0.29 | $0.15 |
| **Net margin per send to the full file (640,000)** | **about $183,000** | **about $94,000** |
| Range from the confidence interval | $113,000 to $257,000 | $25,000 to $160,000 |

Against about $8,000 of creative per campaign, both campaigns pay back many times over.

## 3. Which campaign?

The men's email beats the women's on revenue by **$0.35 per email (95% CI $0.05 to $0.66)**. The interval excludes zero, so under the pre-registered rule **the men's email is the winner**. The margin is real but modest: the interval reaches down to a few cents. Whether some customers respond better to the women's email is a targeting question, answered in [step 6](06_targeting_analysis.md).

## 4. Decision against the pre-registered rules

| Rule (from the design doc) | Men's e-mail | Women's e-mail |
|---|---|---|
| Validity checks pass | Yes | Yes |
| Purchase lift significant after Holm | **Yes** | **Yes** |
| Incremental revenue per email ≥ $0.056 | **Yes** | **Yes** |
| Conclusion | Causes purchases and pays for itself: **roll out** | Causes purchases and pays for itself |
| Winner (CI of difference excludes zero) | **Yes** | |

## 5. What the results do not say

- **Online purchases only.** Every recorded purchase comes with a website visit, so phone orders are probably missing. If emails also prompt phone orders, the true effect is larger.
- **Spend capped at $499.** Large orders are understated, so revenue effects are conservative.
- **Two weeks only.** Some of these purchases may have happened later anyway (pulled forward rather than created). A longer holdout would measure that.
- **No guardrail data yet.** Unsubscribes and complaints come from the e-mail platform; Operations to report them before full rollout.
- **Why buyers' basket sizes are not compared.** Spend per buyer ($114 with no email, $114 men's, $122 women's) and purchases among visitors compare different sets of people once the email changes who visits and buys, so they describe, but do not measure, an effect. The revenue lift comes almost entirely from more buyers.

## 6. A lesson for the next test

The pre-registered regression adjustment confirmed the results but added almost no precision (under 3% more effective sample size). The customer characteristics in the extract explain only 0.2–3% of two-week outcomes. **Recommendation:** include each customer's visits and purchases in the comparable period *before* the send in future extracts. A pre-period metric with a correlation of 0.5 would be worth a third more customers at no cost. That matters, because the next question, whether smaller improvements to a campaign pay off, needs far more power than this test had.

---

**Next:** [Step 6: targeting analysis](06_targeting_analysis.md) (lesson 06).
