# Does email cause sales?

**My end-to-end A/B testing project:** measuring how much revenue an email campaign actually causes, using a randomised experiment with 64,000 customers, from the analysis plan to a recommendation with money attached.

`Python` · `experiment design` · `power analysis` · `causal inference` · `uplift modelling` · `sequential testing`

---

## The question

Email reports usually credit a campaign with every purchase by anyone who received it, including customers who would have bought anyway. I wanted to answer the question a sceptical finance lead would ask: **how much revenue does the email actually *cause*, and is it worth what it costs?** That takes a randomised experiment with a holdout group that gets no email.

## What I found

- **Both emails cause extra purchases.** The men's email more than doubled the purchase rate (**+119%**); the women's raised it by half (**+54%**).
- **They pay for themselves many times over.** The men's email adds **$0.77 of revenue per email** against a break-even of $0.056, about **$183,000 of net margin per send** to a 640,000-customer file (under my stated cost and margin assumptions).
- **Send the men's email to everyone.** It wins overall, and no targeting rule or machine-learning model I tried did better.

![Incremental revenue per email against break-even](images/revenue_vs_breakeven.png)

## How I did it

**[Read the full report →](REPORT.md)** (about 15 minutes, with charts)

I treated the 2008 experiment as if I were planning it: I wrote the analysis plan, with metrics, power analysis and decision rules, **before looking at any outcome**.

| Step | The question at this stage | What I found |
|---|---|---|
| [1. The question](REPORT.md#1-the-question) | What should the experiment answer, and what is a sale worth? | Only a holdout separates caused sales from sales that would have happened anyway |
| [2. Analysis plan](REPORT.md#2-analysis-plan) | What lift is worth having, and can the test see it? | Break-even is +11% purchases, but the test can only reliably detect +47%, so I defined "not significant" as inconclusive in advance |
| [3. Data validation](REPORT.md#3-data-validation) | Can I trust the data and the randomisation? | Randomisation worked; only online purchases are recorded and spend is capped, so results are conservative |
| [4. Results](REPORT.md#4-results) | Did the emails work, and are they worth it? | Both emails clear break-even 7–14× over; the men's email wins |
| [5. Targeting](REPORT.md#5-targeting) | Does targeting beat sending to everyone? | No: the women's email only works for women's buyers, and models don't beat a blanket send |
| [6. Recommendation](REPORT.md#6-recommendation) | What should the business do? | Roll out and keep a long-term holdout; the decision holds even if 93% of the lift were pulled forward |

**Two extensions** cover what the main case cannot:

- **[A. Without randomisation](REPORT.md#extension-a-what-goes-wrong-without-randomisation)** (real Lazada data): a voucher's effect estimated from targeted data was **13× too large**, and statistical corrections couldn't fully fix it.
- **[B. A five-arm coupon test](REPORT.md#extension-b-a-five-arm-coupon-test-and-the-danger-of-peeking)** (simulation with a known truth): the coupon that maximises orders **loses the most money**, and checking results daily turns 5% false alarms into **22%**.

## Methods

| Area | What I used |
|---|---|
| **Experiment design** | Metric choice from a revenue decomposition, pre-registration, break-even analysis, power and minimum detectable effect, holdout sizing |
| **Validation** | Sample-ratio mismatch test, covariate balance (standardised differences, joint tests), data-quality checks |
| **Analysis** | Proportion tests, Holm and Dunnett corrections, bootstrap and delta-method intervals, regression adjustment and CUPED |
| **Causal inference and ML** | Uplift modelling (T- and S-learners, Qini curves), policy evaluation by inverse propensity weighting, IPW and doubly robust estimation |
| **Monitoring** | A/A tests, peeking simulations, O'Brien–Fleming sequential boundaries, Bayesian stopping rules |
| **Engineering** | A tested Python package (`src/expt`, 50 unit tests), reproducible pipeline (`make all`), checksum-verified data downloads |

## Repository guide

| If you want... | Go to |
|---|---|
| The story and the results | [`REPORT.md`](REPORT.md) |
| My working document for each step: brief, plan, validation, results, targeting, recommendation | [`docs/`](docs/) |
| The analysis behind each step | [`notebooks/`](notebooks/): `ch2_…` to `ch6_…` for the main case, `extA_…` and `extB…` for the extensions |
| The reusable code | [`src/expt/`](src/expt/), tested in [`tests/`](tests/) |

```
.
├── REPORT.md     # the full story, start here
├── docs/         # project brief, analysis plan, data validation, results, targeting, recommendation
├── notebooks/    # analysis, numbered by report section
├── src/expt/     # toolkit: power, validation, inference, uplift, policy, causal, simulate, sequential
├── tests/        # unit tests for the toolkit
├── images/       # charts used in this README and the report
├── scripts/      # data download, preparation and figure export
└── Makefile      # make all: data, tests and every notebook
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make all        # downloads and verifies the data, runs the tests, executes every notebook (about 10 minutes)
```

Executed notebooks are written to `runs/`, leaving the published ones untouched. To use a specific interpreter: `make all PYTHON=/path/to/python`.

## Data and credits

- **Hillstrom** (main case): Hillstrom, K. (2008). *The MineThatData E-Mail Analytics and Data Mining Challenge.* [blog.minethatdata.com](https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html). The download script only accepts a file whose SHA-256 checksum matches the original.
- **Lazada** (extension A): Zhong, K. et al. (2022). *DESCN: Deep Entire Space Cross Networks for Individual Treatment Effect Estimation.* KDD 2022. [github.com/kailiang-zhong/DESCN](https://github.com/kailiang-zhong/DESCN). Distributed by Alibaba Group under a BSD-style license.
- **Coupon simulation** (extension B): simulated in [`src/expt/simulate.py`](src/expt/simulate.py), loosely modelled on large-scale coupon tests such as Meituan's MT-LIFT.

The data and results are real; costs, margins and file size are my assumptions, listed in the [project brief](docs/1_project_brief.md). No data is committed to this repository. Code is MIT-licensed.

## Author

**Nathan Chen**
