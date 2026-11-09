# Email Campaign Experimentation

An end-to-end business A/B testing case study built on a real, randomised, three-arm email experiment, with two optional extensions: what goes wrong without randomisation (real data), and a modern multi-arm coupon test (simulated, with known ground truth).

The goal is not just to compute a p-value. It is to practise the full discipline a business data scientist follows: understand the business context, define metrics before looking at outcomes, size the test, validate the randomisation, analyse binary and heavy-tailed revenue outcomes correctly, resist post-hoc slicing, and decide who should receive which email.

| Part | Data | Status |
|------|------|--------|
| **1. The business A/B test** | Hillstrom e-mail experiment (real, randomised) | Core |
| 2. Without randomisation | Lazada voucher data (real, targeted vs randomised) | Optional |
| 3. A modern coupon test | Simulated five-arm coupon funnel (known truth) | Optional |

## The business context

The data comes from an unnamed US multichannel retailer selling men's and women's apparel through a website and a phone order line (customers ordering from a printed catalogue). It was released in 2008 by Kevin Hillstrom, a consultant to such retailers, as the *MineThatData E-Mail Analytics and Data Mining Challenge*.

At the time, email reports typically credited a campaign with every purchase made by anyone who received it. Hillstrom's point was that most of those customers would have bought anyway, so a campaign's true contribution can only be measured against a **holdout group that receives nothing**. That is why this experiment has a no-email control arm, and why it became a reference dataset for measuring incrementality.

## The experiment

64,000 customers who purchased within the last twelve months were randomly assigned to one of three arms, and their behaviour was tracked for the **two weeks** after the email was sent.

| Arm (`segment`) | Treatment | Customers |
|-----------------|-----------|-----------|
| `No E-Mail` | Control: received nothing | 21,306 |
| `Mens E-Mail` | Campaign featuring men's merchandise | 21,307 |
| `Womens E-Mail` | Campaign featuring women's merchandise | 21,387 |

The email labels describe the merchandise featured, not the customer's sex.

**Outcomes**, measured over the two weeks after the send:

| Column | Definition |
|--------|------------|
| `visit` | 1 if the customer visited the website |
| `conversion` | 1 if the customer purchased |
| `spend` | Dollars spent (zero for most customers, heavily skewed for buyers) |

**Pre-treatment covariates:**

| Column | Definition |
|--------|------------|
| `recency` | Months since last purchase |
| `history` | Dollars spent in the past year |
| `history_segment` | `history` in seven buckets |
| `mens` | 1 if the customer bought men's merchandise in the past year |
| `womens` | 1 if the customer bought women's merchandise in the past year |
| `zip_code` | Urban, suburban or rural |
| `newbie` | 1 if the customer was new in the past twelve months |
| `channel` | Channels purchased from in the past year: phone, web or multichannel |

## The business question

> **Did either email produce incremental visits, purchases and revenue beyond what would have happened anyway, which email worked better, and which customers should receive which email in the future?**

## Follow the case the way a company runs it

The case is told as it would happen inside the retailer, with you as the data scientist. The data is real; the people, messages and business figures are invented and labelled as a scenario.

| Step | Document | What happens |
|------|----------|--------------|
| 1 | [The request](docs/01_request.md) | E-mail Marketing asks for a test; the CFO doubts that email causes any sales |
| 2 | [Kickoff notes](docs/02_kickoff_notes.md) | The data scientist turns the request into a decision, a metric and constraints |
| 3 | [Experiment design doc](docs/03_experiment_design_doc.md) | Break-even lift, power, the holdout split and decision rules, signed off before launch ([numbers](notebooks/01_experiment_design.ipynb)) |
| 4 | [Validation report](docs/04_validation_report.md) | Go / no-go: data quality, sample ratio and covariate balance, checked before any result is read ([checks](notebooks/02_validation.ipynb)) |
| 5 | Results readout | Lessons 03–05 |
| 6 | Targeting and decision memo | Lessons 06–07 |

The headline of the design: **a campaign pays for itself at about +11% more purchases, but a 64,000-customer test can reliably detect only about +47%.** How a data scientist plans around that gap, and gets stakeholders to agree to it in advance, is the subject of lesson 01.

## Learning path

Each notebook is one lesson. Reusable code lives in `src/expt` and is tested in `tests/`.

### Part 1: the business A/B test (Hillstrom)

| # | Notebook | What you learn |
|---|----------|----------------|
| 01 | `01_experiment_design.ipynb` + [docs](docs/) | Designing the test the way a company does: from the request and kickoff to a signed design doc with metric roles, the break-even lift, power, the holdout split and decision rules, all before any outcome is seen |
| 02 | `02_validation.ipynb` | Data quality checks, sample-ratio mismatch, covariate balance and the multiple-testing trap inside balance checks, ending in a go / no-go before any result is read |
| 03 | `03_binary_metrics.ipynb` | Visit and conversion rates: proportion tests, confidence intervals, relative lift, and multiple-comparison correction for two treatments against one control |
| 04 | `04_revenue_metric.ipynb` | Spend per customer: why the t-test struggles with zero-inflated, heavy-tailed data; bootstrap confidence intervals; decomposing revenue into conversion × spend per buyer |
| 05 | `05_variance_reduction.ipynb` | CUPED and regression adjustment with pre-treatment covariates; how much tighter the estimates get |
| 06 | `06_heterogeneity_and_uplift.ipynb` | Segment effects and the post-hoc slicing trap; uplift models (S-, T- and X-learners) evaluated with Qini curves |
| 07 | `07_targeting_and_decision_memo.ipynb` | Which customers should get which email, the incremental revenue of that policy, and a recommendation a marketing lead can act on |

### Part 2 (optional): what goes wrong without randomisation (Lazada)

| # | Notebook | What you learn |
|---|----------|----------------|
| 08 | `08_selection_bias_lazada.ipynb` | Lazada released the same voucher treatment twice: assigned by its targeting system, and assigned at random. The targeted data suggests the voucher multiplies purchases about six-fold; the randomised data shows roughly +11%. We measure the bias and test whether propensity weighting and doubly robust estimation can recover the randomised answer |

### Part 3 (optional): a modern coupon test (simulated)

| # | Notebook | What you learn |
|---|----------|----------------|
| 09 | `09_simulated_coupon_experiment.ipynb` | A food-delivery coupon test with five coupon levels and an impression → click → order funnel, calibrated to published industry rates: multi-arm comparisons, dose-response, the biased conversion-given-click metric, profit per arm against a known truth |
| 10 | `10_simulated_monitoring.ipynb` | A/A tests, the false-positive rate under peeking, sequential testing and Bayesian analysis |

## Why this dataset

Before choosing, we compared the public datasets most often used for A/B testing and uplift modelling against what a business case needs:

| Dataset | Business context stated | Metrics defined | Randomised | User-level | Has money |
|---------|------------------------|-----------------|------------|------------|-----------|
| **Hillstrom** (2008, US retailer, email) | Yes | Yes: visit, purchase, spend | Yes | Yes | Yes |
| X5 RetailHero (2019, Russian grocer) | Partly | "A purchase afterward", no window | Not stated | Yes | Pre-period only |
| Lazada (2022, Alibaba) | Partly (vouchers) | No: the outcome is an undefined `label` | Test set only | Yes | No |
| MT-LIFT (2024, Meituan) | Partly (coupons) | Click, conversion | Disputed in the repo's issues | Yes | No; downloads no longer available |
| ASOS (2021, fashion) | Partly | No: "Metric 1–4" | Yes | Group totals only | Unknown |
| Upworthy (2013–15, media headlines) | Yes | Yes: clicks | 22% of tests flagged for randomisation problems | Group totals only | No |
| Kaggle tutorial datasets | Usually none | Varies | Unknown | Varies | Often synthetic, with no known truth |

Companies strip exactly what makes a dataset a business case: what the treatment was, what the outcome means, and anything involving money. Newer releases tend to be more anonymised, not less. Hillstrom is the only public dataset where every step of a business A/B test can be done honestly. Its age changes nothing about the methods, and measuring whether a campaign adds anything beyond what would have happened anyway is still the central question in marketing.

The other parts use each remaining source only for what it does well: Lazada for the selection-bias lesson (where the meaning of the outcome does not matter), and a simulation where we define the business, the metrics and the true effects ourselves.

## Repository layout

```
.
├── data/
│   ├── raw/            # downloaded files (never committed)
│   └── processed/      # compact parquet files
├── docs/               # the case as company documents: request, kickoff, design doc
├── notebooks/          # numbered lessons, run in order
├── scripts/
│   ├── download_data.py
│   └── prepare_data.py
├── src/expt/           # reusable experimentation toolkit
│   ├── power.py        # sample size / MDE
│   ├── validation.py   # SRM and covariate balance checks
│   ├── inference.py    # proportions, corrections, bootstrap, CUPED
│   ├── uplift.py       # uplift models, Qini
│   ├── policy.py       # targeting policies
│   ├── causal.py       # propensity scores, weighting, doubly robust (Part 2)
│   └── simulate.py     # coupon experiment generator (Part 3)
├── tests/              # unit tests for the toolkit
├── reports/            # decision memo and figures
├── requirements.txt
└── Makefile
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make data          # downloads the Hillstrom dataset (4 MB) and verifies its checksum
make prepare       # converts it to parquet in data/processed/
jupyter lab
```

For Part 2, `make data-lazada` downloads the Lazada dataset (93 MB); `make prepare` then converts it too.

The download script tries the original MineThatData URL first, then two GitHub mirrors, and only accepts a file whose SHA-256 checksum matches the original (`0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece`).

## Data sources and citations

**Hillstrom.** Hillstrom, K. (2008). *The MineThatData E-Mail Analytics And Data Mining Challenge.* https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html

**Lazada (Part 2).** Zhong, K., Xiao, F., Ren, Y., Liang, Y., Yao, W., Yang, X., and Cen, L. (2022). *DESCN: Deep Entire Space Cross Networks for Individual Treatment Effect Estimation.* KDD 2022. arXiv:2207.09920. https://github.com/kailiang-zhong/DESCN. Distributed by Alibaba Group under a BSD-style license, saved by the download script as `data/raw/LICENSE_lazada`.

No data is committed to this repository. The MIT license below covers this project's code only.

## Author

Nathan Chen
