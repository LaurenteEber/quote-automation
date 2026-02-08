#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from staff_quoter.config import get_settings
from staff_quoter.pipeline import QuotePipeline


def parse_args() -> argparse.Namespace:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Run quote pipeline: validate formulas + JSON/PDF outputs")
    parser.add_argument(
        "--workbook",
        default=str(settings.default_workbook),
        help="Path to workbook (.xlsx)",
    )
    parser.add_argument(
        "--run-recalc",
        action="store_true",
        help="Run LibreOffice recalc script before validation",
    )
    parser.add_argument(
        "--allow-formula-issues",
        action="store_true",
        help="Do not fail pipeline when formula issues are found",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workbook_path = Path(args.workbook).expanduser().resolve()

    settings = get_settings()
    pipeline = QuotePipeline(settings)

    result = pipeline.run(
        workbook_path=workbook_path,
        fail_on_formula_issues=not args.allow_formula_issues,
        run_recalc=args.run_recalc,
    )

    print(json.dumps(result.__dict__, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
