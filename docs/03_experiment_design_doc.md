# Step 3: Experiment design doc

> **Scenario note.** The data in this project is real (Hillstrom, 2008). The business figures and sign-offs are invented, taken from the [request](01_request.md) and [kickoff notes](02_kickoff_notes.md). All calculations are in the appendix notebook, [`notebooks/01_experiment_design.ipynb`](../notebooks/01_experiment_design.ipynb).

| | |
|---|---|
| **Experiment** | Spring e-mail campaigns: incrementality test |
| **Author** | Nathan Chen, Data Science |
| **Reviewers** | Head of E-mail Marketing; Finance Business Partner (for the CFO); E-mail Operations Manager |
| **Status** | Approved for launch |
| **Written** | Before launch. No outcome data has been seen. |

## TL;DR

- We will send the men's email to one third of a random 64,000 customers, the women's email to another third, and nothing to the last third, then compare purchases over two weeks.
- **A campaign pays for itself if it lifts purchases by about 11%.** Marketing expects about 30%.
- **The test is small for this question.** With 64,000 customers it reliably detects only lifts of about 47% or more, and has a 42% chance of detecting a true 30% lift. A larger test was not possible this spring. So a "not significant" result on purchases will mean *inconclusive*, not *no effect*, and the decision rules below say so in advance.

## 1. Background

Our e-mail report credits campaigns with every purchase made by anyone who received an email: about $1.2M last quarter. Recipients are our most recent customers, and many would have bought anyway, so that figure overstates what email causes. The CFO will approve next year's e-mail budget (about $192,000 in creative) only with evidence of **incremental** purchases that cover the cost.

## 2. Hypotheses

- **H1:** sending the men's email increases the share of customers who purchase within two weeks, compared with sending nothing.
- **H2:** the same for the women's email.

The comparison between the two emails is secondary.

## 3. Design

| Item | Decision | Why |
|---|---|---|
| Population | Active file: bought in the last 12 months | Who the campaigns are for. Lapsed customers behave differently. |
| Sample | Random 64,000 customers (10% of the file) | The rest of the file is in the spring catalogue test. |
| Groups | No email / Men's email / Women's email | A holdout is the only way to measure incremental sales. |
| Split | Equal thirds: 21,333 per group | See section 6. |
| Assignment | Random, by customer ID, in the e-mail platform | Groups differ only by chance. |
| Window | Two weeks after the send | Captures most of the response; closes before the next campaign (day 15). |
| Analysis | By assigned group (intent-to-treat) | Comparing by "opened the email" would compare different kinds of customers. |

## 4. Metrics

| Role | Metric | Definition |
|---|---|---|
| **Primary** | **Purchase rate** | Share of customers with at least one purchase in the window |
| Secondary | Visit rate | Share of customers who visited the website |
| Secondary | Revenue per customer | Revenue in the window divided by all customers in the group, including non-buyers |
| Descriptive only | Purchase rate among visitors; revenue per buyer | The email changes who visits and buys, so these are not like-for-like comparisons |
| Guardrails | Unsubscribe rate, spam complaints | Reported by E-mail Operations from the platform (not in the analysis dataset) |
| Validity | Group sizes (sample-ratio check), balance of customer characteristics | Checked before any outcome is read |

**Why purchases, not visits, as primary:** Finance's decision depends on purchases. A campaign can drive visits without sales; it cannot fake purchases. Visits are the more sensitive metric, so they are kept as the key secondary metric that shows whether the email worked as intended.

## 5. What success is worth: the break-even lift

Each email sent at full rollout costs the sending fee plus its share of the creative cost:

| | Value |
|---|---|
| Sending cost per email | $0.010 |
| Creative cost per email ($8,000 / 640,000) | $0.0125 |
| **Total cost per email** | **$0.0225** |
| Gross margin | 40% |
| **Break-even incremental revenue per email** ($0.0225 / 0.40) | **$0.056** |

At an average order of $100, that is 0.056 extra purchases per 100 customers. On a baseline of 0.5%, **a lift of about 11% in purchases pays for the campaign.**

## 6. Sample size and power

Planning baselines from Operations: visit rate 10%, purchase rate 0.5% in a normal fortnight. Two confirmatory comparisons, so α = 0.025 each (Bonferroni for planning; the analysis uses Holm). Power 80%.

**What 21,333 customers per group can detect:**

| Metric | Smallest lift reliably detected |
|---|---|
| Visit rate | +0.91 points (+9%) |
| **Purchase rate** | **+0.23 points (+47%)** |
| Revenue per customer | +$0.28 (+57%) |

**The gap between what matters and what we can see:**

| Lift in purchases | Chance this test detects it | Customers needed per group for 80% |
|---|---|---|
| +11% (break-even) | 7% | 315,627 (more than the whole file allows) |
| +30% (Marketing's expectation) | 42% | 48,301 |
| +47% | 80% | The size of this test |

We asked for about 145,000 customers to detect the expected 30% lift. The spring catalogue test made that impossible, so we proceed knowingly. Visits are well covered: an email that lifts visits by 10% would be detected 87% of the time.

**Why equal thirds.** A smaller holdout means emailing more customers during the test, but it costs detection power and saves almost nothing:

| Holdout share | Holdout / each email group | Smallest purchase lift detected | Chance to detect +30% | Margin lost in holdout if +30% is real |
|---|---|---|---|---|
| 10% | 6,400 / 28,800 | +73% | 17% | $384 |
| 20% | 12,800 / 25,600 | +54% | 32% | $768 |
| **33%** | **21,333 / 21,333** | **+47%** | **42%** | **$1,280** |

With two campaigns compared both against the holdout and against each other, equal groups give the most information. The cost of the largest holdout is about $1,280 of margin, against a $192,000 budget decision.

## 7. Analysis plan

1. **Validity checks first:** sample-ratio test on group sizes; balance of recency, past spend, channel, zip-code type, newbie flag and past men's/women's purchases across groups.
2. **Primary:** two-proportion z-tests of each email against the holdout on purchase rate; Holm correction across the two tests; 95% confidence intervals for the absolute and relative lift.
3. **Secondary:** visit rate tested the same way; revenue per customer with bootstrap confidence intervals, because revenue is mostly zeros with a long tail.
4. **Business value:** incremental revenue per email sent, with its confidence interval, compared with the $0.056 break-even.
5. **Precision:** a regression-adjusted estimate using pre-treatment customer characteristics, pre-specified here as a secondary analysis.
6. **Exploratory only:** segment differences and uplift models, to inform targeting.

## 8. Decision rules

Written before launch and applied as written:

| Result on purchases | Conclusion | Recommendation |
|---|---|---|
| Validity check fails (sample-ratio p < 0.001 or clear imbalance) | Results cannot be trusted | Stop, investigate, do not read outcomes |
| Significant lift, and incremental revenue per email at or above $0.056 | The campaign causes purchases and pays for itself | Roll out; approve the budget for that campaign |
| Significant lift, but below $0.056 | Real effect that does not cover its cost | Do not roll out as is; reduce cost or target better |
| Not significant | **Inconclusive**: the test could miss effects up to about +47% | Do not cut the budget on this evidence; re-test with a larger sample after the catalogue test |
| Visits up, purchases not significant | Email brings traffic; a purchase effect is not shown | As "not significant" |

**Choosing between the campaigns:** declare a winner only if the confidence interval for the difference in incremental revenue per email excludes zero. Otherwise, use targeting (who should get which email) rather than picking one.

**Guardrail:** if either email's unsubscribe rate is clearly above our usual campaign level, Marketing reviews before any rollout, whatever the purchase result.

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Test too small for the expected effect | Stated upfront; "not significant" is pre-defined as inconclusive |
| Visits tracked differently for emailed customers | Confirmed: visits matched by login and cookie for all groups |
| Overlap with the catalogue test or other campaigns | Separate customers; no other campaigns or catalogue mailings to the test sample during the window |
| Some emails not delivered or not opened | Analyse by assigned group; the estimate is the effect of *sending*, which is what the business controls |
| Purchases pulled forward rather than created | Two-week window cannot rule this out; stated as a limitation |
| Seasonality | A regular, non-holiday fortnight |
| Looking at results early and stopping when they look good | One analysis at the end of the window |

## 10. Pre-launch checklist

- [ ] Random assignment run by customer ID; group sizes within expected range
- [ ] Customer characteristics balanced across groups
- [ ] Seed emails received and rendered correctly
- [ ] Visit and purchase tracking verified for a few customers in each group
- [ ] No other campaigns scheduled to the test sample during the window
- [ ] Analysis code written and reviewed before the window closes

## 11. Sign-off

| Role | Decision |
|---|---|
| Head of E-mail Marketing | Approved |
| Finance Business Partner (for the CFO) | Approved. Finance accepts that a non-significant result is inconclusive and will not by itself cut the budget. |
| E-mail Operations Manager | Approved; assignment and tracking confirmed |

---

**Next:** [Step 4: validation report](04_validation_report.md) (lesson 02).
