# 1 · Project brief

## The question

Email reports usually credit a campaign with every purchase made by anyone who received it. For a list of recent customers that badly overstates what the email does, because many of them would have bought anyway. The question I wanted to answer is the one a sceptical finance lead would ask:

> **How much revenue does an email campaign actually *cause*, and is it worth what it costs?**

Answering it requires a randomised experiment with a **holdout**: customers chosen at random to receive nothing, whose behaviour shows what would have happened without the email.

## Why this project

I wanted to practise A/B testing the way it is done in a business, with real data, defined metrics and a decision that involves money, rather than computing a p-value on a tutorial dataset.

Finding the data was harder than expected. I first looked for a recent dataset, ideally from a large Chinese platform. Meituan's MT-LIFT coupon experiment (2024) was the best candidate, but its download links are no longer available. Lazada's voucher dataset (Alibaba, 2022) can be downloaded, but its outcome is an undefined `label`, and a business test is meaningless if you cannot say what the metric is. Most Kaggle A/B datasets are synthetic or of unknown origin.

I settled on the **Hillstrom e-mail experiment (2008)**: it is the only public dataset I found with a stated business context, defined metrics (visit, purchase, spend) and real randomisation. I then used the other sources for what they do well: Lazada to show what goes wrong without randomisation, and a simulation of a modern coupon test where the true effects are known. The full comparison is in the [report](../REPORT.md#why-i-chose-this-dataset).

## The data

A US apparel retailer selling online and through a phone line for catalogue customers. 64,000 customers who had bought in the past 12 months were randomly assigned to three groups:

| Group | Treatment |
|---|---|
| No e-mail | Holdout: received nothing |
| Men's e-mail | Campaign featuring men's merchandise |
| Women's e-mail | Campaign featuring women's merchandise |

Outcomes were recorded for the two weeks after the send: website **visit**, **purchase** and **spend**. Pre-treatment information includes recency, past-year spend, merchandise bought, channel, location and whether the customer is new.

## Questions

1. Does each email cause additional purchases and revenue, compared with sending nothing?
2. Which email works better?
3. Is the effect large enough to pay for the campaign?
4. Should different customers receive different emails, or none?

## Business assumptions

The dataset contains no costs or margins, so I set explicit assumptions to translate effects into money. They are typical for a mid-size apparel retailer; every money result scales with them, and the [recommendation](6_recommendation.md) tests how sensitive the decision is.

| Assumption | Value |
|---|---|
| Average order value | $100 (standard deviation about $90) |
| Gross margin | 40% |
| Sending cost | $0.01 per email |
| Creative production | $8,000 per campaign |
| Active customer file | 640,000 customers |
| Programme | Two campaigns a month (about $192,000 a year in creative) |

For planning I also assumed, *before* looking at any outcomes, that without email about 10% of customers visit and 0.5% buy in a two-week period, and that a good campaign might lift purchases by around 30%.

## Starting point for the metrics

My starting point was a simple decomposition of revenue:

```
revenue per customer = visit rate × purchase rate among visitors × spend per buyer
```

An email mainly works on the first factor, bringing people back to the site, so I expected the effect to be clearest on visits and most diluted on revenue. That decomposition shaped the choice of metrics in the [analysis plan](2_analysis_plan.md).

## How I approached it

The experiment ran in 2008, so I could not design it. Instead I treated it as if I were planning it: I wrote the analysis plan, including metrics, power analysis and decision rules, **before looking at any outcome**, then validated the data, analysed the results exactly as planned, and turned them into a recommendation.

| Step | Document | Analysis |
|---|---|---|
| Analysis plan | [2_analysis_plan.md](2_analysis_plan.md) | [notebook](../notebooks/ch2_experiment_design.ipynb) |
| Data validation | [3_data_validation.md](3_data_validation.md) | [notebook](../notebooks/ch3_data_checks.ipynb) |
| Results | [4_results.md](4_results.md) | notebooks [4a](../notebooks/ch4a_purchases_and_visits.ipynb), [4b](../notebooks/ch4b_revenue.ipynb), [4c](../notebooks/ch4c_variance_reduction.ipynb) |
| Targeting | [5_targeting.md](5_targeting.md) | [notebook](../notebooks/ch5_targeting.ipynb) |
| Recommendation | [6_recommendation.md](6_recommendation.md) | [notebook](../notebooks/ch6_recommendation.ipynb) |
