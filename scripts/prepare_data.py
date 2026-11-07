"""Convert the MT-LIFT CSVs into compact parquet files in data/processed/.

Labels and treatment are stored as int8 and features as float32, which
roughly halves memory use compared with pandas' default float64.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

LABELS = ["click", "conversion", "treatment"]


def find_csv(name: str) -> Path:
    matches = sorted(RAW_DIR.rglob(name))
    if not matches:
        raise FileNotFoundError(f"{name} not found under {RAW_DIR}. Run `make data` first.")
    return matches[0]


def convert(name: str) -> None:
    src = find_csv(f"{name}.csv")
    header = pd.read_csv(src, nrows=0).columns
    dtypes = {col: ("int8" if col in LABELS else "float32") for col in header}
    df = pd.read_csv(src, dtype=dtypes)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / f"{name}.parquet"
    df.to_parquet(dest, index=False)
    print(f"{src.name}: {len(df):,} rows x {df.shape[1]} cols -> {dest}")


def main() -> None:
    for name in ("train", "test"):
        convert(name)


if __name__ == "__main__":
    main()
