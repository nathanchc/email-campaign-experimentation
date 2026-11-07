"""Download the MT-LIFT dataset (Meituan, 2024) into data/raw/.

Tries the Google Drive mirror with gdown. If that fails, prints manual
download instructions for the Google Drive and Baidu Drive mirrors.
"""
from pathlib import Path
import sys
import tarfile
import zipfile

GDRIVE_FILE_ID = "1dslFa9EGrVVoO_040ZYM16cIH-SKDuss"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
EXPECTED = ("train.csv", "test.csv")

MANUAL_INSTRUCTIONS = """
Automatic download failed. Download MT-LIFT manually from either mirror and
place train.csv and test.csv in data/raw/:

  Google Drive: https://drive.google.com/file/d/1dslFa9EGrVVoO_040ZYM16cIH-SKDuss/view
  Baidu Drive:  https://pan.baidu.com/s/1YmE5g-Y71ULNptiWqpToPA  (extraction code: 06nb)
"""


def already_present() -> bool:
    return all(any(RAW_DIR.rglob(name)) for name in EXPECTED)


def extract(archive: Path) -> None:
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(RAW_DIR)
    elif tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tf:
            tf.extractall(RAW_DIR, filter="data")
    else:
        return
    archive.unlink()


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if already_present():
        print(f"MT-LIFT already present in {RAW_DIR}")
        return 0

    try:
        import gdown
    except ImportError:
        print("gdown is not installed (pip install gdown).")
        print(MANUAL_INSTRUCTIONS)
        return 1

    target = RAW_DIR / "mt_lift_download"
    out = gdown.download(id=GDRIVE_FILE_ID, output=str(target), quiet=False)
    if out is None:
        print(MANUAL_INSTRUCTIONS)
        return 1

    extract(target)
    if not already_present():
        print(f"Downloaded to {target}, but train.csv / test.csv were not found.")
        print(MANUAL_INSTRUCTIONS)
        return 1

    print(f"MT-LIFT ready in {RAW_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
