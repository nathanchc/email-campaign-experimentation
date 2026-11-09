# 5 · Targeting

*Exploratory, as set out in the [analysis plan](2_analysis_plan.md): patterns here are hypotheses for a future test, not confirmed results. Analysis: [`notebooks/ch5_targeting.ipynb`](../notebooks/ch5_targeting.ipynb).*

## Summary

- **Send the men's email to everyone.** No targeting policy I tried earns more.
- **Nobody should be excluded:** the men's email lifts visits by about 7 points in every customer group, and an email costs about two cents.
- **The women's email only works for women's buyers**, a real pattern, but even for them it is only *as good as* the men's email.
- **Machine-learning uplift models aren't worth deploying here:** slightly better than a one-line rule for visits, unstable for revenue, and their policies earned less on held-out customers.

## Slicing by segment

Cutting the revenue lift by 18 customer segments gives 36 comparisons. Both emails work almost everywhere, so most are positive, but a few differences look striking, such as negative estimates for the women's email among $200–$500 customers. With 36 comparisons and wide intervals, such patterns are expected by chance, and none has a business explanation. I didn't use them.

## One hypothesis with a reason: merchandise match

| Bought last year | Men's e-mail: visit lift | Women's e-mail: visit lift |
|---|---|---|
| Men's merchandise only | +6.9 points | **+1.1 points** |
| Women's merchandise only | +7.1 points | +7.4 points |
| Both | +13.4 points | +7.1 points |

The women's email's effect differs between women's-only and men's-only buyers by **+6.3 points (95% interval +5.0 to +7.6)**. The men's email works for everyone.

## Uplift models

I trained T- and S-learners (gradient-boosted trees) on 70% of customers and evaluated them with Qini curves on the other 30%, repeating over 10 random splits:

| Outcome | Model vs a simple rule ("women's-only buyers first") |
|---|---|
| Visits | Model slightly better on average; both consistently better than random |
| Purchases, revenue | Too few buyers (578): performance swings from worse than random to better than random depending on the split |

## Which policy earns the most?

Estimated net margin per customer on held-out customers (40% of revenue minus $0.0225 per email), using inverse propensity weighting:

| Policy | Net margin per customer | vs "men's to all" (95% interval) |
|---|---|---|
| No e-mail | $0.19 | −$0.39 (−$0.60 to −$0.20) |
| **Men's e-mail to all** | **$0.58** | |
| Women's e-mail to all | $0.37 | −$0.21 (−$0.43 to −$0.00) |
| Match rule (women's-only buyers get the women's e-mail) | $0.55 | −$0.03 (−$0.16 to +$0.11) |
| Model choosing by predicted visit uplift | $0.48 | −$0.09 (−$0.24 to +$0.04) |
| Model choosing by predicted revenue uplift (no e-mail below break-even) | $0.45 | −$0.13 (−$0.29 to +$0.03) |

On all 64,000 customers, the match rule and "men's to all" differ by less than a cent per customer.

## Conclusion

Roll out the men's email to everyone, without a targeting model. The merchandise-match finding is useful for creative development, for example a women's email designed to also appeal to men's buyers, tested against the men's email.
