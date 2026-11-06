# Email Campaign Experimentation

An end-to-end experimentation case study built around a real multi-arm email marketing test, paired with a simulated experiment where the ground truth is known.

The goal is not just to compute a p-value, but to practise the full discipline of running an experiment the way a business data scientist would: define metrics up front, size the test, validate the randomisation, analyse binary and heavy-tailed revenue outcomes correctly, resist post-hoc slicing, and decide who should receive which treatment.

## The experiment

**Dataset:** Kevin Hillstrom's MineThatData e-mail analytics challenge (2008). 64,000 customers who purchased in the previous 12 months were randomly assigned to one of three arms:

| Arm | Treatment |
|-----|-----------|
| `No E-Mail` | Control — received nothing |
| `Mens E-Mail` | Campaign featuring men's merchandise |
| `Womens E-Mail` | Campaign featuring women's merchandise |

Outcomes were tracked for two weeks after the send:

- `visit` — did the customer visit the site? (binary)
- `conversion` — did the customer purchase? (binary)
- `spend` — how much did they spend? (continuous, zero-inflated, heavy-tailed)

Pre-treatment covariates: recency, purchase history, channel, segment (newbie / men's / women's buyer), zip-code type.

**Why this one?** Three arms instead of two, a revenue metric that breaks the naive t-test, rich covariates for variance reduction and heterogeneity, and it is the standard benchmark for uplift modelling. It is a step up from the usual two-arm, one-binary-metric tutorial.

## Learning path

Each notebook is one lesson. Reusable code lives in `src/expt` and is tested in `tests/`.

| # | Notebook | What you learn |
|---|----------|----------------|
| 01 | `01_design_and_metrics.ipynb` | Writing an experiment plan before looking at outcomes: hypotheses, primary / secondary / guardrail metrics, minimum detectable effect, power and sample size |
| 02 | `02_data_validation.ipynb` | Sample-ratio mismatch, covariate balance across arms, A/A-style sanity checks — trusting the randomisation before trusting the result |
| 03 | `03_binary_metrics.ipynb` | Conversion and visit rates: two-proportion z-test, chi-square, confidence intervals, and multiple-comparison correction for three arms |
| 04 | `04_revenue_metric.ipynb` | Spend per customer: why the t-test misbehaves on zero-inflated heavy tails; bootstrap CIs, Mann–Whitney, delta method, and decomposing revenue into conversion × order value |
| 05 | `05_variance_reduction.ipynb` | CUPED and regression adjustment with pre-treatment covariates; how much sample you save |
| 06 | `06_heterogeneity_and_uplift.ipynb` | Segment effects and the post-hoc slicing trap; uplift modelling (two-model, class transformation, uplift trees) with Qini / AUUC evaluation; a targeting policy |
| 07 | `07_simulated_experiment.ipynb` | A simulator with a known true lift: validating the whole pipeline with A/A tests, measuring false-positive rate under peeking, and comparing frequentist, Bayesian and sequential analyses against the truth |
| 08 | `08_decision_memo.ipynb` | Turning the analysis into a recommendation a marketing lead can act on |

## Repository layout

```
.
├── data/
│   ├── raw/            # original dataset (downloaded by scripts, not committed)
│   └── processed/      # cleaned parquet files
├── notebooks/          # numbered lessons, run in order
├── src/expt/           # reusable experimentation toolkit
│   ├── power.py        # sample size / MDE calculations
│   ├── validation.py   # SRM and balance checks
│   ├── inference.py    # proportions, bootstrap, CUPED, corrections
│   ├── uplift.py       # uplift models and Qini curves
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
make data        # downloads the Hillstrom dataset into data/raw/
jupyter lab
```

## Data source

Hillstrom, K. (2008). *The MineThatData E-Mail Analytics And Data Mining Challenge.* https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html

## Author

Nathan Chen
