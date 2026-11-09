# 4 · Results

*Analysed exactly as set out in the [analysis plan](2_analysis_plan.md), after the [data validation](3_data_validation.md) gave a go. Analysis: notebooks [4a purchases and visits](../notebooks/ch4a_purchases_and_visits.ipynb), [4b revenue](../notebooks/ch4b_revenue.ipynb), [4c variance reduction](../notebooks/ch4c_variance_reduction.ipynb).*

## Summary

- **Both emails cause additional purchases.** The men's email more than doubles the purchase rate (+119%); the women's raises it by about half (+54%).
- **Both pay for themselves many times over:** $0.77 (men's) and $0.42 (women's) of extra revenue per email, against a $0.056 break-even.
- **The men's email is the better campaign** on purchases, visits and revenue.

## Purchases (primary)

| Group | Purchase rate | Lift vs no e-mail | 95% interval of lift | Holm-adjusted p |
|---|---|---|---|---|
| No e-mail | 0.57% | | | |
| Men's e-mail | 1.25% | **+0.68 points (+119%)** | +77% to +171% | < 0.001 |
| Women's e-mail | 0.88% | **+0.31 points (+54%)** | +23% to +94% | < 0.001 |

The baseline came in close to the planning assumption (0.57% vs 0.5%), so the test was as sensitive as planned, and both effects are well above the +47% it could reliably detect.

## Visits and revenue (secondary)

| Metric | No e-mail | Men's e-mail | Women's e-mail |
|---|---|---|---|
| Visit rate | 10.6% | 18.3% (+72%) | 15.1% (+43%) |
| Revenue per customer | $0.65 | $1.42 (+$0.77) | $1.08 (+$0.42) |
| 95% interval of revenue lift (bootstrap) | | $0.50 to $1.06 | $0.16 to $0.68 |

Revenue per customer is over 99% zeros with a long tail, so I checked the normal-approximation interval against a bootstrap; they agree.

## Business value

| | Men's e-mail | Women's e-mail |
|---|---|---|
| Incremental revenue per email | $0.77 | $0.42 |
| Multiple of break-even ($0.056) | 14× | 7.5× |
| Low end of interval, as a multiple of break-even | about 9× | about 3× |
| Net margin per email (40% margin minus $0.0225) | $0.29 | $0.15 |
| Net margin per send to the full file (640,000) | about $183,000 | about $94,000 |

## Which campaign

The men's email beats the women's on revenue by **$0.35 per email (95% interval $0.05 to $0.66)**. The interval excludes zero, so under the plan's rule the men's email is the winner, by a real but modest margin.

## Against the decision rules

| Rule | Men's e-mail | Women's e-mail |
|---|---|---|
| Validity checks pass | Yes | Yes |
| Purchase lift significant after Holm | Yes | Yes |
| Revenue per email ≥ $0.056 | Yes | Yes |
| Winner | **Yes** | |

## What I checked and did not use

- **Purchases among visitors** (5.4% no e-mail, 6.9% men's, 5.8% women's) and **spend per buyer** ($114, $114, $122). Both compare different people once the email changes who visits and buys, so they describe but don't measure an effect. The revenue lift comes almost entirely from more buyers, not bigger baskets.
- **The Mann-Whitney test.** With 99% zeros it mostly tests how many people bought, not how much revenue came in.
- **Regression adjustment / CUPED.** It confirmed the estimates but added less than 3% precision, because the pre-treatment characteristics explain only 0.2–3% of two-week outcomes. Pre-period visits and purchases would help much more; a correlation of 0.5 is worth a third more customers.

## Caveats

- Online purchases only; spend capped at $499 (both make these results conservative).
- Two-week window: some purchases may only have been pulled forward.
- No unsubscribe or complaint data.
