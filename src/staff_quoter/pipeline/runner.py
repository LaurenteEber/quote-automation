from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import subprocess
import sys

from staff_quoter.config import Settings

from .formula_validator import WorkbookFormulaValidator
from .models import FormulaValidationReport
from .pdf_renderer import QuotePdfRenderer
from .quote_builder import QuotePayloadBuilder


@dataclass(frozen=True)
class PipelineResult:
    workbook_path: str
    formula_report: dict[str, object]
    json_output_path: str
    pdf_output_path: str
    recalc_output: dict[str, object] | None


class QuotePipeline:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._validator = WorkbookFormulaValidator()
        self._builder = QuotePayloadBuilder()
        self._pdf_renderer = QuotePdfRenderer()

    def run(
        self,
        workbook_path: Path | str,
        fail_on_formula_issues: bool = True,
        run_recalc: bool = False,
    ) -> PipelineResult:
        workbook_path = Path(workbook_path)
        recalc_output = self._run_recalc_if_requested(workbook_path, run_recalc)

        formula_report = self._validator.validate(workbook_path)
        if fail_on_formula_issues and formula_report.has_errors:
            raise ValueError(
                f"Formula validation failed with {len(formula_report.issues)} issues."
            )

        payload = self._builder.build_from_workbook(workbook_path)

        json_output_path = self._write_json(payload)
        pdf_output_path = self._write_pdf(payload)

        return PipelineResult(
            workbook_path=str(workbook_path),
            formula_report=formula_report.to_dict(),
            json_output_path=str(json_output_path),
            pdf_output_path=str(pdf_output_path),
            recalc_output=recalc_output,
        )

    def _write_json(self, payload: object) -> Path:
        data = payload.to_json()  # type: ignore[attr-defined]
        output_dir = self._settings.output_json_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{payload.quote_id}.json"  # type: ignore[attr-defined]
        output_path.write_text(data, encoding="utf-8")
        return output_path

    def _write_pdf(self, payload: object) -> Path:
        output_dir = self._settings.output_pdf_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{payload.quote_id}.pdf"  # type: ignore[attr-defined]
        return self._pdf_renderer.render(payload, output_path)

    def _run_recalc_if_requested(
        self,
        workbook_path: Path,
        run_recalc: bool,
    ) -> dict[str, object] | None:
        if not run_recalc:
            return None

        script_path = self._settings.xlsx_recalc_script
        if not script_path.exists():
            return {
                "status": "skipped",
                "reason": f"recalc script not found: {script_path}",
            }

        command = [
            sys.executable,
            str(script_path),
            str(workbook_path),
            "60",
        ]
        completed = subprocess.run(command, capture_output=True, text=True)

        parsed: dict[str, object] | None = _parse_json_output(completed.stdout)
        return {
            "status": "ok" if completed.returncode == 0 else "failed",
            "return_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "parsed": parsed,
        }


def _parse_json_output(stdout: str) -> dict[str, object] | None:
    text = stdout.strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue

    return None
