# 6 · Recommendation

*Numbers: [`notebooks/ch6_recommendation.ipynb`](../notebooks/ch6_recommendation.ipynb). Money figures use the assumptions in the [project brief](1_project_brief.md).*

## Recommendation

1. **Keep the email programme.** Both emails cause purchases that would not otherwise happen and pay for themselves many times over.
2. **Send the men's campaign to the full active file.** It beat the women's email overall and was at least as good for every customer group; targeting added nothing measurable.
3. **Keep a long-term holdout** of 5% of customers for a quarter, to keep measuring what the programme adds over time.

## The money

The men's email brought in **$0.77 of extra revenue per email** against a break-even of $0.056. Sent to the full file of 640,000 customers, that is about **$183,000 of net margin per send** after creative and sending costs (range from the confidence interval: $113,000 to $257,000).

## How robust is it?

The two-week test cannot measure everything, and the margin is an assumption. The decision holds under any reasonable alternative:

| If... | Net margin per send (men's) |
|---|---|
| As measured (40% margin, all extra sales are new) | about $183,000 |
| Half the extra sales were only pulled forward from later weeks | about $84,000 |
| Margin is 30% and a quarter of sales were pulled forward | about $96,000 |
| **Break-even point** | More than **93%** of extra sales pulled forward, or future campaigns achieving under **7%** of this effect |

Two measurement gaps make the true effect likely *larger*: only online purchases were recorded, and spend is capped at $499.

## Risks

| Risk | How to manage it |
|---|---|
| Extra sales partly pulled forward | Long-term holdout measures the effect over a full quarter |
| Email fatigue, rising unsubscribes | Track unsubscribes and complaints per send; the holdout shows any long-run decline |
| Future campaigns perform worse | Test each new creative against the men's email before full rollout |
| Phone orders not measured | Add phone orders to the outcome data |

## Next experiments

| Experiment | Size | Purpose |
|---|---|---|
| Long-term holdout: 5% of customers get no campaigns for a quarter | 32,000 customers; about $9,000 of margin per send | Programme effect over time, net of pull-forward and fatigue; detects a change of about 23% in the purchase rate |
| New creative vs the men's email, with **visit rate** as the primary metric | About 24,000 per group for a 1-point difference | Which creative brings more customers in; revenue per customer as a guardrail. A $0.10 revenue difference would need about 355,000 per group |
| Data improvements: phone orders, pre-period behaviour, customer IDs, unsubscribes | No cost | Complete measurement, and about a third more precision per test |

The second experiment flips the metric choice I made for this one. When both groups get an email, the creative's job is to bring people in, and visits measure that precisely. The metric follows the decision.
