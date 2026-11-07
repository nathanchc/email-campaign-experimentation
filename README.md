# Coupon Experimentation and Uplift Modeling

An end-to-end experimentation case study in two parts:

1. **A real voucher experiment** from Lazada, Alibaba Group's e-commerce platform in Southeast Asia, released in 2022.
2. **A simulated coupon experiment** with five coupon levels and a click-to-order funnel, where the ground truth is known.

The goal is not just to compute a p-value. It is to practise the full discipline a business data scientist follows: understand the business context, define metrics before looking at outcomes, validate the randomisation, see how badly non-randomised data can mislead, and decide which users should receive a voucher, and whether a voucher pays for itself.

## Part 1: the Lazada voucher experiment

**Source:** released by Alibaba Group alongside the paper *DESCN: Deep Entire Space Cross Networks for Individual Treatment Effect Estimation* (KDD 2022). The public files are a sample of the production dataset used in the paper.

**Business setting:** voucher distribution on Lazada. A voucher is a discount offer. Vouchers cost money on every order they touch, so the platform targets them: the paper's example is giving vouchers to inactive users to improve retention while withholding them from active users to save cost.

**What makes this dataset special:** it contains two very different kinds of data about the same treatment.

| Split | How the voucher was assigned | Rows | Treated share |
|-------|------------------------------|------|---------------|
| `train` | By Lazada's targeting policy (not random, so biased) | 926,669 | ~22% |
| `test` | At random (a randomised experiment) | 181,669 | ~52% |

| Item | Value |
|------|-------|
| Treatment | `is_treat` (1 = received a voucher, 0 = did not) |
| Outcome | `label` (binary; the paper does not define it, most likely a purchase) |
| Features | 83 anonymised pre-treatment features (`f0`–`f82`) |

The randomised test set tells us the true average effect of a voucher. The targeted training set looks like the data most companies actually have. Comparing the two shows, with real numbers, how much a naive analysis of targeted data gets wrong, and whether statistical corrections can recover the truth.

**What the data does not tell us**, and how this project deals with it:

- *The meaning of the outcome and the features.* Everything is anonymised. Features remain valid pre-treatment covariates for balance checks, variance reduction and uplift modelling.
- *Voucher value, voucher cost and order value.* There is no money in the data. Lesson 07 makes explicit, clearly labelled cost assumptions and tests how sensitive the decisions are to them.
- *The intended treatment ratio of the experiment.* Lesson 02 tests the observed split and discusses what we can and cannot conclude.

## Part 2: the simulated coupon experiment

A simulator modelled on a typical food-delivery coupon campaign: users are randomly assigned to one of **five coupon levels** (one of them no coupon), and outcomes are tracked along the funnel

```
impression  ──►  click  ──►  order
```

with an order value and a coupon cost per order. Because we set the true effects ourselves, we can check whether each analysis method recovers them. This part covers what the real data cannot: comparing many arms, the conversion-given-click trap, profit per arm, peeking and sequential testing.

## The business question

> **Does a voucher produce enough incremental purchases to justify its cost, and for which users?**

## Learning path

Each notebook is one lesson. Reusable code lives in `src/expt` and is tested in `tests/`.

| # | Notebook | What you learn |
|---|----------|----------------|
| 01 | `01_context_and_design.ipynb` | Business context, the metric tree for a voucher, primary / secondary / guardrail metrics, minimum detectable effect and power, written as a pre-registration |
| 02 | `02_data_validation.ipynb` | Sample-ratio mismatch, covariate balance across 83 features (and the multiple-testing trap inside balance checks); why the targeted training set fails these checks and the randomised test set passes |
| 03 | `03_average_effect.ipynb` | The voucher's average effect on the randomised data: proportion test, confidence interval, relative lift; then the naive estimate on targeted data and how far off it is |
| 04 | `04_correcting_selection_bias.ipynb` | Trying to recover the true effect from targeted data: regression adjustment, propensity-score weighting, matching, doubly robust estimation, all checked against the randomised answer |
| 05 | `05_variance_reduction.ipynb` | CUPED and regression adjustment with pre-treatment features; how much tighter the confidence interval gets and what sample size that saves |
| 06 | `06_heterogeneity_and_uplift.ipynb` | Segment effects and the post-hoc slicing trap; uplift models (S-, T- and X-learners, with and without propensity correction) trained on targeted data and evaluated with Qini / AUUC on randomised data |
| 07 | `07_voucher_targeting_policy.ipynb` | Turning uplift scores into a targeting policy under a budget, with explicit cost assumptions and a sensitivity analysis |
| 08 | `08_simulated_multi_arm_funnel.ipynb` | The five-level coupon simulator: multi-arm comparisons with multiple-testing correction (Holm, Dunnett), dose-response, the biased conversion-given-click metric and the delta method, profit per arm |
| 09 | `09_simulated_monitoring.ipynb` | A/A tests, the false-positive rate under peeking, sequential testing, Bayesian analysis, and whether uplift models recover the true effects |
| 10 | `10_decision_memo.ipynb` | Turning the analysis into a recommendation a marketing lead can act on |

## Repository layout

```
.
├── data/
│   ├── raw/            # downloaded CSVs (never committed)
│   └── processed/      # compact parquet files
├── notebooks/          # numbered lessons, run in order
├── scripts/
│   ├── download_data.py
│   └── prepare_data.py
├── src/expt/           # reusable experimentation toolkit
│   ├── power.py        # sample size / MDE
│   ├── validation.py   # SRM and covariate balance checks
│   ├── inference.py    # proportions, corrections, delta method, CUPED
│   ├── causal.py       # propensity scores, weighting, doubly robust estimation
│   ├── uplift.py       # uplift models, Qini / AUUC
│   ├── policy.py       # budget-constrained targeting
│   └── simulate.py     # five-level coupon experiment generator
├── tests/              # unit tests for the toolkit
├── reports/            # decision memo and figures
├── requirements.txt
└── Makefile
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make data        # downloads the Lazada dataset (~93 MB) into data/raw/
make prepare     # converts it to compact parquet in data/processed/
jupyter lab
```

## Data source and citation

Zhong, K., Xiao, F., Ren, Y., Liang, Y., Yao, W., Yang, X., and Cen, L. (2022). *DESCN: Deep Entire Space Cross Networks for Individual Treatment Effect Estimation.* Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. arXiv:2207.09920. Original code and data: https://github.com/kailiang-zhong/DESCN

The download script fetches the files from the mirror maintained for the `libuplift` package (https://github.com/jszymon/uplift_sklearn_data). The dataset is distributed by Alibaba Group under a BSD-style license, which the script saves as `data/raw/LICENSE_lazada`. The data is not committed to this repository; the MIT license below covers this project's code only.

## Author

Nathan Chen
