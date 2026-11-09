"""Download the project datasets into data/raw/ and verify their integrity.

    python scripts/download_data.py            # Hillstrom (main case)
    python scripts/download_data.py --lazada   # Lazada (extension A)
    python scripts/download_data.py --all      # both

Every file is checked against a known SHA-256 checksum, so a mirror is only
accepted if it is byte-for-byte identical to the original.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


@dataclass(frozen=True)
class RemoteFile:
    local_name: str
    sha256: str
    urls: tuple[str, ...]  # tried in order until one passes the checksum


HILLSTROM = [
    RemoteFile(
        local_name="hillstrom.csv",
        # Checksum of the original MineThatData file, as recorded by libuplift.
        sha256="0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece",
        urls=(
            "http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv",
            "https://raw.githubusercontent.com/HarshGakare/uplift-project/main/data/hillstrom.csv",
            "https://raw.githubusercontent.com/yadavabhaykumar905-creator/Uplifting-model/main/hillstrom.csv",
        ),
    ),
]

_LAZADA_BASE = "https://github.com/jszymon/uplift_sklearn_data/releases/download/Lazada"
LAZADA = [
    RemoteFile(
        "lazada_train.csv.gz",
        "5a46ec368f9e8397267e818447ea7f3d239a671731ca98c0ae9f17c19ab5a469",
        (f"{_LAZADA_BASE}/Lazada_trainset.csv.gz",),
    ),
    RemoteFile(
        "lazada_test.csv.gz",
        "a6d8832a71e8f0b6d4e8858d91ce7de9d8e0f2f58aa7208c78b1e0f7d6ba9c94",
        (f"{_LAZADA_BASE}/Lazada_testset.csv.gz",),
    ),
    RemoteFile(
        "LICENSE_lazada",
        "3ae95b8e3fa8f3cae1af3c44274586179e7dda9f3cddba6bc7565d249c7cc7a3",
        (f"{_LAZADA_BASE}/Lazada_LICENSE",),
    ),
]


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(file: RemoteFile) -> None:
    dest = RAW_DIR / file.local_name
    if dest.exists() and sha256_of(dest) == file.sha256:
        print(f"Already present and verified: {dest.name}")
        return

    tmp = dest.with_name(dest.name + ".part")
    for url in file.urls:
        print(f"Downloading {dest.name} from {url}")
        try:
            urllib.request.urlretrieve(url, tmp)
        except Exception as exc:  # network errors, HTTP errors, blocked hosts
            print(f"  failed: {exc}")
            continue
        if sha256_of(tmp) == file.sha256:
            tmp.replace(dest)
            print(f"  verified ({dest.stat().st_size / 1e6:.1f} MB)")
            return
        print("  checksum mismatch, trying next source")
    if tmp.exists():
        tmp.unlink()
    raise RuntimeError(f"Could not download a verified copy of {dest.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lazada", action="store_true", help="download only the Lazada dataset (extension A)")
    group.add_argument("--all", action="store_true", help="download all datasets")
    args = parser.parse_args()

    files = LAZADA if args.lazada else HILLSTROM + LAZADA if args.all else HILLSTROM
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for file in files:
        fetch(file)
    print(f"Done. Files are in {RAW_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
