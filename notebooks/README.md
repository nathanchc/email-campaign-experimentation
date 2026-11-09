# Notebooks

The analysis behind each chapter of the [case study](../CASE_STUDY.md). Each notebook runs top to bottom (`make notebooks` from the repository root) and ends with questions to try yourself.

| Notebook | Chapter | What it does |
|---|---|---|
| [`ch2_experiment_design`](ch2_experiment_design.ipynb) | 2. Designing the test | Break-even lift, minimum detectable effect, power at the expected lift, holdout sizing |
| [`ch3_data_checks`](ch3_data_checks.ipynb) | 3. Checking the data | Data-quality findings, sample-ratio test, covariate balance, a placebo exercise on multiple testing |
| [`ch4a_purchases_and_visits`](ch4a_purchases_and_visits.ipynb) | 4. Results | Purchase and visit lifts with confidence intervals and Holm correction; the purchases-per-visitor trap |
| [`ch4b_revenue`](ch4b_revenue.ipynb) | 4. Results | Revenue per customer: Welch vs bootstrap, why not Mann-Whitney, the business case against break-even |
| [`ch4c_variance_reduction`](ch4c_variance_reduction.ipynb) | 4. Results | Regression adjustment and CUPED: why they barely help here, and a simulation of when they do |
| [`ch5_targeting`](ch5_targeting.ipynb) | 5. Who should get which email? | Segment slicing, the merchandise-match effect, uplift models with Qini curves, policy evaluation |
| [`ch6_recommendation`](ch6_recommendation.ipynb) | 6. The recommendation | Rollout value, break-even and sensitivity analysis, sizing the follow-up tests |
| [`extA_selection_bias`](extA_selection_bias.ipynb) | Extension A | Lazada: targeted vs randomised data; outcome regression, IPW and doubly robust estimation |
| [`extB1_coupon_experiment`](extB1_coupon_experiment.ipynb) | Extension B | Simulated five-arm coupon test: Dunnett, the orders-per-click trap, profit vs orders, targeting |
| [`extB2_monitoring`](extB2_monitoring.ipynb) | Extension B | A/A tests, peeking, sequential boundaries, Bayesian stopping rules |

Chapter 1 (the problem) has no notebook: it is the business scoping, in [`docs/company_documents`](../docs/company_documents/).
