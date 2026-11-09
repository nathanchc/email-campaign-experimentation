"""Loading the Hillstrom dataset in analysis-ready form.

The cleaning steps follow the data validation in docs/3_data_validation.md;
notebooks/ch3_data_checks.ipynb explains each of them.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_CSV = ROOT / "data" / "raw" / "hillstrom.csv"

CONTROL = "No E-Mail"
ARMS = [CONTROL, "Mens E-Mail", "Womens E-Mail"]
ARM_SHORT = {"No E-Mail": "control", "Mens E-Mail": "mens", "Womens E-Mail": "womens"}

PRE_TREATMENT = ["recency", "history", "history_segment", "mens", "womens", "zip_code", "newbie", "channel"]
CATEGORICAL = ["history_segment", "zip_code", "channel"]
OUTCOMES = ["visit", "conversion", "spend"]

HISTORY_SEGMENTS = [
    "1) $0 - $100",
    "2) $100 - $200",
    "3) $200 - $350",
    "4) $350 - $500",
    "5) $500 - $750",
    "6) $750 - $1,000",
    "7) $1,000 +",
]


def clean_hillstrom(raw: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning decided in the validation report.

    1. Fix the misspelled zip-code label "Surburban" -> "Suburban".
    2. Store categories with a meaningful order (control first, history buckets ascending).
    3. Add ``arm``, a short label for the experiment group.

    Values are otherwise unchanged; in particular ``spend`` keeps its apparent
    cap at $499, which is reported as a limitation rather than "fixed".
    """
    df = raw.copy()
    df["zip_code"] = df["zip_code"].replace({"Surburban": "Suburban"})
    df["segment"] = pd.Categorical(df["segment"], categories=ARMS, ordered=False)
    df["history_segment"] = pd.Categorical(df["history_segment"], categories=HISTORY_SEGMENTS, ordered=True)
    df["zip_code"] = pd.Categorical(df["zip_code"], categories=["Urban", "Suburban", "Rural"])
    df["channel"] = pd.Categorical(df["channel"], categories=["Web", "Phone", "Multichannel"])
    df["arm"] = pd.Categorical(df["segment"].map(ARM_SHORT), categories=list(ARM_SHORT.values()))
    if df["segment"].isna().any() or df["history_segment"].isna().any():
        raise ValueError("unexpected category labels in the raw data")
    return df


LAZADA_FEATURES = [f"f{i}" for i in range(83)]


def load_lazada(split: str) -> pd.DataFrame:
    """Load the Lazada voucher data (extension A). ``split`` is "train" (targeted)
    or "test" (randomised). Reads the compact parquet file if `make prepare`
    has been run, otherwise the raw CSV."""
    if split not in {"train", "test"}:
        raise ValueError('split must be "train" or "test"')
    parquet = ROOT / "data" / "processed" / f"lazada_{split}.parquet"
    if parquet.exists():
        return pd.read_parquet(parquet)
    csv = ROOT / "data" / "raw" / f"lazada_{split}.csv.gz"
    if not csv.exists():
        raise FileNotFoundError(f"{csv} not found. Run `make data-lazada` first.")
    dtypes = {"label": "int8", "is_treat": "int8", **{f: "float32" for f in LAZADA_FEATURES}}
    return pd.read_csv(csv, dtype=dtypes)


def load_hillstrom(path: Path | str = RAW_CSV) -> pd.DataFrame:
    """Read the raw CSV and return the cleaned, analysis-ready DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run `make data` first.")
    return clean_hillstrom(pd.read_csv(path))
