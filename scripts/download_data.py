"""Download the Lazada voucher dataset (Alibaba Group, KDD 2022) into data/raw/.

Files come from the mirror maintained for the libuplift package:
https://github.com/jszymon/uplift_sklearn_data/releases/tag/Lazada
"""
from pathlib import Path
import sys
import urllib.request

BASE_URL = "https://github.com/jszymon/uplift_sklearn_data/releases/download/Lazada"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# remote file name -> (local file name, expected size in bytes)
FILES = {
    "Lazada_trainset.csv.gz": ("lazada_train.csv.gz", 75_748_426),
    "Lazada_testset.csv.gz": ("lazada_test.csv.gz", 17_076_799),
    "Lazada_LICENSE": ("LICENSE_lazada", 1_713),
}


def download(remote: str, local: Path, expected_size: int) -> None:
    if local.exists() and local.stat().st_size == expected_size:
        print(f"Already present: {local.name}")
        return
    tmp = local.with_suffix(local.suffix + ".part")
    print(f"Downloading {remote} ...")
    urllib.request.urlretrieve(f"{BASE_URL}/{remote}", tmp)
    size = tmp.stat().st_size
    if size != expected_size:
        tmp.unlink()
        raise RuntimeError(f"{remote}: expected {expected_size:,} bytes, got {size:,}")
    tmp.rename(local)
    print(f"Saved {local.name} ({size / 1e6:.1f} MB)")


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for remote, (local_name, size) in FILES.items():
        download(remote, RAW_DIR / local_name, size)
    print(f"Lazada dataset ready in {RAW_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
