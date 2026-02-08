from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from .models import QuotePayload


class QuotePayloadBuilder:
    def build_from_workbook(self, workbook_path: Path | str) -> QuotePayload:
        workbook_path = Path(workbook_path)
        wb = load_workbook(workbook_path, data_only=True, read_only=True)

        input_ws = wb["INPUT_QUOTE"]
        calc_ws = wb["CALC_OUTPUTS"]
        quote_ws = wb["QUOTE_OUTPUT"]

        quote_id = _to_text(input_ws["A2"].value) or "UNKNOWN"
        payload = QuotePayload(
            quote_id=quote_id,
            engine_type=_to_text(input_ws["C2"].value),
            customer_name=_to_text(input_ws["D2"].value),
            part_number=_to_text(input_ws["G2"].value),
            total_cost=_to_float(calc_ws["B2"].value),
            total_price=_to_float(calc_ws["C2"].value),
            margin_pct=_to_float(calc_ws["D2"].value),
            lead_time_weeks=_to_float(calc_ws["E2"].value),
            moq=_to_int(calc_ws["F2"].value),
            pdf_ready_flag=_to_bool(quote_ws["C2"].value),
            generated_at_utc=QuotePayload.now_iso(),
        )

        wb.close()
        return payload


def _to_text(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def _to_float(value: object) -> float:
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _to_int(value: object) -> int:
    if value is None or value == "":
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().upper() == "TRUE"
