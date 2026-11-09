"""Convert the raw datasets in data/raw/ into parquet files in data/processed/.

Values are kept exactly as in the source files (including known quirks such
as the "Surburban" spelling in Hillstrom); cleaning is explained in chapter 3.
Only the storage types are made compact.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

HILLSTROM_DTYPES = {
    "recency": "int8",
    "history_segment": "category",
    "history": "float64",
    "mens": "int8",
    "womens": "int8",
    "zip_code": "category",
    "newbie": "int8",
    "channel": "category",
    "segment": "category",
    "visit": "int8",
    "conversion": "int8",
    "spend": "float64",
}


def save(df: pd.DataFrame, name: str, src: Path) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUT_DIR / f"{name}.parquet"
    df.to_parquet(dest, index=False)
    print(f"{src.name}: {len(df):,} rows x {df.shape[1]} cols -> {dest.relative_to(ROOT)}")


def prepare_hillstrom() -> None:
    src = RAW_DIR / "hillstrom.csv"
    if not src.exists():
        raise FileNotFoundError(f"{src} not found. Run `make data` first.")
    save(pd.read_csv(src, dtype=HILLSTROM_DTYPES), "hillstrom", src)


def prepare_lazada() -> None:
    for split in ("train", "test"):
        src = RAW_DIR / f"lazada_{split}.csv.gz"
        if not src.exists():
            print(f"Skipping Lazada ({src.name} not found; run `make data-lazada` for extension A).")
            return
        header = pd.read_csv(src, nrows=0).columns
        dtypes = {col: ("int8" if col in {"label", "is_treat"} else "float32") for col in header}
        save(pd.read_csv(src, dtype=dtypes), f"lazada_{split}", src)


def main() -> None:
    prepare_hillstrom()
    prepare_lazada()


if __name__ == "__main__":
    main()
