"""Convert the Lazada CSVs into compact parquet files in data/processed/.

The outcome and treatment are stored as int8 and features as float32,
roughly halving memory use compared with pandas' default float64.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

INT_COLUMNS = {"label", "is_treat"}


def convert(split: str) -> None:
    src = RAW_DIR / f"lazada_{split}.csv.gz"
    if not src.exists():
        raise FileNotFoundError(f"{src} not found. Run `make data` first.")
    header = pd.read_csv(src, nrows=0).columns
    dtypes = {col: ("int8" if col in INT_COLUMNS else "float32") for col in header}
    df = pd.read_csv(src, dtype=dtypes)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / f"lazada_{split}.parquet"
    df.to_parquet(dest, index=False)
    print(f"{src.name}: {len(df):,} rows x {df.shape[1]} cols -> {dest.relative_to(ROOT)}")


def main() -> None:
    for split in ("train", "test"):
        convert(split)


if __name__ == "__main__":
    main()
