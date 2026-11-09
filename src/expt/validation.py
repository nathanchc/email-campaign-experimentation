"""Checks that an experiment can be trusted before its outcomes are read.

* ``srm_test``: sample-ratio mismatch, i.e. are the group sizes what the
  random assignment should produce?
* ``standardized_mean_difference`` and ``balance_table``: do the groups look
  alike on characteristics measured before the treatment?
* ``covariate_tests``: one significance test per covariate, with a Holm
  adjustment, because many tests produce some small p-values by chance.
* ``joint_balance_test``: a single test of whether the covariates, taken
  together, predict group membership.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests


@dataclass(frozen=True)
class SRMResult:
    observed: pd.Series
    expected: pd.Series
    chi2: float
    p_value: float

    def passed(self, threshold: float = 0.001) -> bool:
        """SRM is usually flagged only at a strict threshold such as p < 0.001."""
        return self.p_value >= threshold


def srm_test(
    observed: Mapping[str, int] | pd.Series,
    expected_shares: Mapping[str, float] | None = None,
) -> SRMResult:
    """Chi-square goodness-of-fit test of group sizes against the planned split.

    ``expected_shares`` defaults to an equal split across the observed groups.
    """
    obs = pd.Series(observed, dtype=float)
    if expected_shares is None:
        shares = pd.Series(1 / len(obs), index=obs.index)
    else:
        shares = pd.Series(expected_shares, dtype=float).reindex(obs.index)
        if shares.isna().any():
            raise ValueError("expected_shares must cover every observed group")
        shares = shares / shares.sum()
    expected = shares * obs.sum()
    chi2, p_value = stats.chisquare(obs.values, expected.values)
    return SRMResult(obs.astype(int), expected, float(chi2), float(p_value))


def standardized_mean_difference(treated: Sequence[float], control: Sequence[float]) -> float:
    """Difference in means divided by the pooled standard deviation.

    A common rule of thumb treats |SMD| < 0.1 as negligible imbalance. Unlike a
    p-value, the SMD does not shrink towards "significant" as samples grow.
    """
    t = np.asarray(treated, dtype=float)
    c = np.asarray(control, dtype=float)
    pooled_sd = np.sqrt((t.var(ddof=1) + c.var(ddof=1)) / 2)
    if pooled_sd == 0:
        return 0.0
    return float((t.mean() - c.mean()) / pooled_sd)


def _group_order(groups: pd.Series) -> list:
    """Category order for categorical columns, order of appearance otherwise."""
    if isinstance(groups.dtype, pd.CategoricalDtype):
        return [g for g in groups.cat.categories if (groups == g).any()]
    return list(pd.unique(groups))


def _expand(df: pd.DataFrame, covariates: Sequence[str], categorical: Sequence[str]) -> pd.DataFrame:
    """Numeric covariates as they are; categorical ones as 0/1 columns, one per level."""
    parts = []
    for col in covariates:
        if col in categorical:
            dummies = pd.get_dummies(df[col], prefix=col, prefix_sep=" = ", dtype=float)
            parts.append(dummies)
        else:
            parts.append(df[[col]].astype(float))
    return pd.concat(parts, axis=1)


def balance_table(
    df: pd.DataFrame,
    group_col: str,
    control: str,
    covariates: Sequence[str],
    categorical: Sequence[str] = (),
) -> pd.DataFrame:
    """Mean of every covariate (share, for categories) per group, and the SMD of each
    treatment group against the control."""
    expanded = _expand(df, covariates, categorical)
    groups = [g for g in _group_order(df[group_col]) if g != control]
    is_control = (df[group_col] == control).to_numpy()
    table = pd.DataFrame(index=expanded.columns)
    table[control] = expanded[is_control].mean()
    for g in groups:
        mask = (df[group_col] == g).to_numpy()
        table[g] = expanded[mask].mean()
    for g in groups:
        mask = (df[group_col] == g).to_numpy()
        table[f"SMD {g}"] = [
            standardized_mean_difference(expanded.loc[mask, c], expanded.loc[is_control, c])
            for c in expanded.columns
        ]
    table.index.name = "covariate"
    return table


def covariate_tests(
    df: pd.DataFrame,
    group_col: str,
    covariates: Sequence[str],
    categorical: Sequence[str] = (),
) -> pd.DataFrame:
    """One test per covariate across all groups, with raw and Holm-adjusted p-values.

    Categorical and binary covariates use a chi-square test of independence;
    numeric covariates use the Kruskal-Wallis test, which does not assume normality.
    """
    rows = []
    for col in covariates:
        values = df[col]
        if col in categorical or values.nunique() <= 2:
            _, p, _, _ = stats.chi2_contingency(pd.crosstab(values, df[group_col]))
            test = "chi-square"
        else:
            samples = [values[df[group_col] == g] for g in pd.unique(df[group_col])]
            _, p = stats.kruskal(*samples)
            test = "Kruskal-Wallis"
        rows.append({"covariate": col, "test": test, "p_value": p})
    out = pd.DataFrame(rows).set_index("covariate")
    out["p_holm"] = multipletests(out["p_value"], method="holm")[1]
    return out


@dataclass(frozen=True)
class JointTestResult:
    lr_stat: float
    df: int
    p_value: float


def joint_balance_test(
    df: pd.DataFrame,
    group_col: str,
    control: str,
    treatment: str,
    covariates: Sequence[str],
    categorical: Sequence[str] = (),
) -> JointTestResult:
    """Likelihood-ratio test that the covariates jointly predict treatment vs control.

    Fits a logistic regression of "in the treatment group" on all covariates and
    compares it with an intercept-only model. Under successful randomisation the
    covariates should carry no information about group membership.
    """
    sub = df[df[group_col].isin([control, treatment])]
    y = (sub[group_col] == treatment).astype(float).to_numpy()
    parts = []
    for col in covariates:
        if col in categorical:
            parts.append(pd.get_dummies(sub[col], prefix=col, drop_first=True, dtype=float))
        else:
            parts.append(sub[[col]].astype(float))
    X = sm.add_constant(pd.concat(parts, axis=1), has_constant="add")
    model = sm.Logit(y, X).fit(disp=0)
    return JointTestResult(float(model.llr), int(model.df_model), float(model.llr_pvalue))
