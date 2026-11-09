# Notebooks

The analysis behind each section of the [report](../REPORT.md). Each notebook runs top to bottom (`make notebooks` from the repository root) and uses the tested functions in [`src/expt`](../src/expt/).

| Notebook | Report section | What it does |
|---|---|---|
| [`ch2_experiment_design`](ch2_experiment_design.ipynb) | 2. Analysis plan | Break-even lift, minimum detectable effect, power at a plausible lift, holdout sizing |
| [`ch3_data_checks`](ch3_data_checks.ipynb) | 3. Data validation | Data-quality findings, sample-ratio test, covariate balance, a placebo check on multiple testing |
| [`ch4a_purchases_and_visits`](ch4a_purchases_and_visits.ipynb) | 4. Results | Purchase and visit lifts with confidence intervals and Holm correction; why purchases per visitor misleads |
| [`ch4b_revenue`](ch4b_revenue.ipynb) | 4. Results | Revenue per customer: Welch vs bootstrap, why not Mann-Whitney, the business case against break-even |
| [`ch4c_variance_reduction`](ch4c_variance_reduction.ipynb) | 4. Results | Regression adjustment and CUPED: why they barely help here, and a simulation of when they do |
| [`ch5_targeting`](ch5_targeting.ipynb) | 5. Targeting | Segment slicing, the merchandise-match effect, uplift models with Qini curves, policy evaluation |
| [`ch6_recommendation`](ch6_recommendation.ipynb) | 6. Recommendation | Rollout value, break-even and sensitivity analysis, sizing the follow-up experiments |
| [`extA_selection_bias`](extA_selection_bias.ipynb) | Extension A | Lazada: targeted vs randomised data; outcome regression, IPW and doubly robust estimation |
| [`extB1_coupon_experiment`](extB1_coupon_experiment.ipynb) | Extension B | Simulated five-arm coupon test: Dunnett, the orders-per-click trap, profit vs orders, targeting |
| [`extB2_monitoring`](extB2_monitoring.ipynb) | Extension B | A/A tests, peeking, sequential boundaries, Bayesian stopping rules |

Section 1 (the question, data and business assumptions) has no notebook; it is in the [project brief](../docs/1_project_brief.md).
