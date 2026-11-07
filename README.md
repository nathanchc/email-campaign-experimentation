# Coupon Experimentation and Uplift Modeling

An end-to-end experimentation case study built on a recent, large-scale randomized coupon experiment from a food-delivery app, paired with a simulated experiment where the ground truth is known.

The goal is not just to compute a p-value. It is to practise the full discipline a business data scientist follows: understand the business context, define metrics before looking at outcomes, validate the randomisation, compare many treatment arms correctly, avoid the funnel-metric traps, and decide which users should receive which coupon, and whether a coupon pays for itself.

## The experiment

**Dataset:** MT-LIFT, released by Meituan in 2024 alongside the paper *Entire Chain Uplift Modeling with Context-Enhanced Learning for Intelligent Marketing* (WWW 2024 Companion).

**Business setting:** coupon marketing for food delivery inside the Meituan app, collected over two months. Users were randomly assigned to one of five treatment levels, coded `0`–`4`, one of which serves as the control. The outcome is tracked along the full funnel:

```
impression  ──►  click  ──►  conversion (order)
```

| Item | Value |
|------|-------|
| Rows | ~5.54 million |
| Features | 99 anonymised pre-treatment features (`f0`–`f98`) |
| Treatment | `treatment` ∈ {0, 1, 2, 3, 4}, randomly assigned |
| Outcomes | `click`, `conversion` (binary) |
| Split | `train.csv` / `test.csv` (the last week is held out as test) |
| Reported averages | click rate 33.5%, conversion rate 6.8% |

**What the data does not tell us**, and how this project deals with it:

- *What each treatment level means.* The levels are not documented. Lesson 02 identifies the control arm empirically and tests whether the effects behave like an ordered "dose" (for example increasing coupon value).
- *Order value and coupon cost.* There is no revenue or cost column, so we cannot compute profit directly. Lessons 07 and 08 make explicit, clearly labelled assumptions and test how sensitive the decisions are to them.
- *Feature meanings.* All features are anonymised. They are still valid pre-treatment covariates for balance checks, variance reduction and uplift modelling.

**Why this one?** Five arms instead of two, a two-step funnel where a naive conversion-given-click metric is biased, effects that are large on average but likely very uneven across users, and a real cost trade-off: a bigger coupon may lift orders more while losing more money per order.

## The business question

> Coupons cost money on every order they touch, including orders the user would have placed anyway. **Which coupon level, if any, produces enough incremental orders to justify its cost, and for which users?**

## Learning path

Each notebook is one lesson. Reusable code lives in `src/expt` and is tested in `tests/`.

| # | Notebook | What you learn |
|---|----------|----------------|
| 01 | `01_context_and_design.ipynb` | Business context, the metric tree for a coupon funnel, primary / secondary / guardrail metrics, minimum detectable effect and power for a multi-arm test, written as a pre-registration |
| 02 | `02_data_validation.ipynb` | Identifying the control arm, sample-ratio mismatch across five arms, covariate balance across 99 features (and the multiple-testing trap inside balance checks), the train / test time split |
| 03 | `03_average_effects.ipynb` | Click and conversion effects for each arm against control: proportion tests, confidence intervals, multiple-comparison correction (Holm, Dunnett), and dose-response across coupon levels |
| 04 | `04_funnel_and_ratio_metrics.ipynb` | Why conversion-given-click is biased when the treatment changes who clicks; delta method for ratio metrics; decomposing the effect along the funnel |
| 05 | `05_variance_reduction.ipynb` | CUPED and regression adjustment with pre-treatment features; how much sample size you save |
| 06 | `06_heterogeneity_and_uplift.ipynb` | Segment effects and the post-hoc slicing trap; multi-treatment uplift models (T-, S- and X-learners) evaluated with Qini / AUUC on the out-of-time test week |
| 07 | `07_coupon_allocation.ipynb` | Turning uplift scores into a coupon policy under a budget, with explicit cost assumptions and a sensitivity analysis |
| 08 | `08_simulated_experiment.ipynb` | A simulator modelled on MT-LIFT where the truth is known, adding order value and coupon cost: A/A tests, false-positive rate under peeking, sequential testing, Bayesian analysis, and checking whether uplift models recover the true effects |
| 09 | `09_decision_memo.ipynb` | Turning the analysis into a recommendation a marketing lead can act on |

## Repository layout

```
.
├── data/
│   ├── raw/            # original CSVs (downloaded, never committed)
│   └── processed/      # compact parquet files
├── notebooks/          # numbered lessons, run in order
├── scripts/
│   ├── download_data.py
│   └── prepare_data.py
├── src/expt/           # reusable experimentation toolkit
│   ├── power.py        # sample size / MDE for multi-arm tests
│   ├── validation.py   # SRM and covariate balance checks
│   ├── inference.py    # proportions, corrections, delta method, CUPED
│   ├── uplift.py       # multi-treatment uplift models, Qini / AUUC
│   ├── policy.py       # budget-constrained coupon allocation
│   └── simulate.py     # synthetic experiment generator
├── tests/              # unit tests for the toolkit
├── reports/            # decision memo and figures
├── requirements.txt
└── Makefile
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make data        # downloads MT-LIFT into data/raw/
make prepare     # converts the CSVs to compact parquet in data/processed/
jupyter lab
```

The raw CSVs are several gigabytes. `make prepare` downcasts types so the full dataset fits comfortably in memory.

If the automatic download fails, download manually from either mirror and place `train.csv` and `test.csv` in `data/raw/`:

- Google Drive: https://drive.google.com/file/d/1dslFa9EGrVVoO_040ZYM16cIH-SKDuss/view
- Baidu Drive (百度网盘): https://pan.baidu.com/s/1YmE5g-Y71ULNptiWqpToPA (extraction code `06nb`)

## Data source and citation

Huang, Y., Wang, S., Gao, M., Wei, X., Li, C., Luo, C., Zhu, Y., Xiao, X., and Luo, Y. (2024). *Entire Chain Uplift Modeling with Context-Enhanced Learning for Intelligent Marketing.* Companion Proceedings of the ACM Web Conference 2024, 226–234. arXiv:2402.03379. Dataset: https://github.com/MTDJDSP/MT-LIFT

The dataset is not redistributed in this repository. The MIT license below covers this project's code only.

## Author

Nathan Chen
