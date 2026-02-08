#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from staff_quoter.config import get_settings
from staff_quoter.google_sheets import GoogleSheetsGateway


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync CSV files to Google Sheets tabs")
    parser.add_argument(
        "--csv-dir",
        default="../artifacts/rebuild_template_csv",
        help="Directory containing one CSV file per tab",
    )
    parser.add_argument(
        "--tabs",
        nargs="*",
        default=[],
        help="Specific tabs to sync (defaults to all CSV files found)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = get_settings()

    gateway = GoogleSheetsGateway(
        spreadsheet_id=settings.google_sheets_id,
        credentials_file=settings.google_credentials_file,
    )

    csv_dir = Path(args.csv_dir).expanduser().resolve()
    if not csv_dir.exists():
        raise FileNotFoundError(f"CSV directory not found: {csv_dir}")

    csv_files = sorted(csv_dir.glob("*.csv"))
    if args.tabs:
        wanted = set(args.tabs)
        csv_files = [p for p in csv_files if p.stem in wanted]

    synced = 0
    for csv_file in csv_files:
        rows = _read_csv_dicts(csv_file)
        tab_name = csv_file.stem
        gateway.write_records(tab_name, rows, clear_first=True)
        print(f"synced tab={tab_name} rows={len(rows)} source={csv_file}")
        synced += 1

    print(f"done. synced_tabs={synced}")
    return 0


def _read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


if __name__ == "__main__":
    raise SystemExit(main())
