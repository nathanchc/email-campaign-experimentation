"""Export the charts used in the README and case study to images/.

Chart cells in the notebooks start with a comment such as
``# figure: revenue_vs_breakeven``. This script finds those cells in the
executed notebooks and saves their image output as images/<name>.png.

    python scripts/export_figures.py              # from notebooks/ (as published)
    python scripts/export_figures.py --from runs  # from a fresh `make notebooks` run
"""
from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = re.compile(r"^#\s*figure:\s*([\w-]+)", re.MULTILINE)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="source", default="notebooks", help="folder with executed notebooks")
    args = parser.parse_args()

    out = ROOT / "images"
    out.mkdir(exist_ok=True)
    count = 0
    for nb_path in sorted((ROOT / args.source).glob("*.ipynb")):
        nb = json.loads(nb_path.read_text())
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                continue
            match = TAG.search("".join(cell["source"]))
            if not match:
                continue
            images = [o["data"]["image/png"] for o in cell.get("outputs", []) if "image/png" in o.get("data", {})]
            if not images:
                raise SystemExit(f"{nb_path.name}: cell tagged '{match.group(1)}' has no image output; run the notebook first")
            (out / f"{match.group(1)}.png").write_bytes(base64.b64decode(images[0]))
            count += 1
    print(f"Exported {count} figures to {out.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
