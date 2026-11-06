"""Download the Hillstrom e-mail challenge dataset into data/raw/."""
from pathlib import Path
import urllib.request

URL = "http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv"
DEST = Path(__file__).resolve().parents[1] / "data" / "raw" / "hillstrom.csv"


def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Already present: {DEST}")
        return
    print(f"Downloading {URL} ...")
    urllib.request.urlretrieve(URL, DEST)
    print(f"Saved to {DEST}")


if __name__ == "__main__":
    main()
