# Step 6: Targeting analysis

> **Scenario note.** The data and results are real (Hillstrom, 2008); margin and cost figures are the invented scenario. Analysis: [`notebooks/06_targeting.ipynb`](../notebooks/06_targeting.ipynb).

| | |
|---|---|
| **Question** | Who should receive which email? (Marketing's third question in the [request](01_request.md)) |
| **Author** | Nathan Chen, Data Science |
| **Status** | Final. **Exploratory**, as classed in the [design doc](03_experiment_design_doc.md): findings here are hypotheses for future tests, not confirmed results |

## TL;DR

- **Send the men's email to everyone.** No targeting policy we tried earns more.
- **Nobody should be excluded:** the men's email lifts visits by about 7 points in every customer group, and an email costs about two cents.
- **The women's email works only for women's buyers**, a real pattern, but even for them it is merely *as good as* the men's email.
- **Machine-learning uplift models are not worth deploying here.** They rank visits only slightly better than a one-line business rule, are unstable for revenue, and the policies built from them earned less than "men's to everyone" on held-out customers.

## 1. Slicing by segment mostly finds noise

Cutting the revenue lift of each email by 18 customer segments gives 36 comparisons. Both emails work almost everywhere, so most are positive, but the *differences between segments* are where the trap lies. For example, the women's email shows negative estimates in the $200–$500 past-spend segments and its biggest estimate in the smallest segment ($1,000+). With 36 comparisons and wide intervals, such patterns are expected by chance and have no business explanation. They were not used.

## 2. One pattern with a reason: merchandise match

We tested one specific hypothesis with a business rationale: an email works better when its merchandise matches what the customer buys.

| Bought last year | Men's e-mail: visit lift | Women's e-mail: visit lift |
|---|---|---|
| Men's merchandise only | +6.9 points | **+1.1 points** |
| Women's merchandise only | +7.1 points | +7.4 points |
| Both | +13.4 points | +7.1 points |

The women's email barely moves men's-only buyers. The difference in its effect between women's-only and men's-only buyers is **+6.3 points (95% CI +5.0 to +7.6)**, far beyond chance. The men's email works for everyone, including women's-only buyers.

## 3. Uplift models

T-learner and S-learner models (gradient-boosted trees), trained on 70% of customers and evaluated with Qini curves on the other 30%, repeated over 10 random splits:

| Outcome | Model vs simple rule ("women's-only buyers first") |
|---|---|
| Visits | Model slightly better on average; both consistently better than random |
| Purchases, revenue | Too few buyers (578 in total): the model's performance swings from worse than random to better than random depending on the split |

## 4. Which policy earns the most?

Estimated net margin per customer (40% of revenue minus $0.0225 per email) on held-out customers, using inverse propensity weighting:

| Policy | Net margin per customer | Difference vs "men's to all" (95% CI) |
|---|---|---|
| No e-mail | $0.19 | −$0.39 (−$0.60 to −$0.20) |
| **Men's e-mail to all** | **$0.58** | |
| Women's e-mail to all | $0.37 | −$0.21 (−$0.43 to −$0.00) |
| Match rule (women's-only buyers get the women's e-mail) | $0.55 | −$0.03 (−$0.16 to +$0.11) |
| Model choosing the e-mail by predicted visit uplift | $0.48 | −$0.09 (−$0.24 to +$0.04) |
| Model choosing by predicted revenue uplift (or no e-mail below break-even) | $0.45 | −$0.13 (−$0.29 to +$0.03) |

On all 64,000 customers, the match rule and "men's to all" differ by less than a cent per customer.

## 5. Recommendation

1. **Roll out the men's email to the full active file**, with no targeting.
2. **Do not build a targeting model** for this campaign type: it adds complexity and risk without measurable gain.
3. **Use the merchandise-match finding in creative development**, for example a women's email designed to also appeal to men's buyers, and test it against the men's email (see the [decision memo](07_decision_memo.md) for the test design).

---

**Next:** [Step 7: decision memo](07_decision_memo.md) (lesson 07).
