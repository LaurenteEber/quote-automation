from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas

from .models import QuotePayload


class QuotePdfRenderer:
    def render(self, payload: QuotePayload, output_path: Path | str) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        canvas = Canvas(str(output_path), pagesize=LETTER)
        width, height = LETTER

        y = height - 72
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(72, y, "Staff Quoter - Quote Summary")

        y -= 26
        canvas.setFont("Helvetica", 10)
        canvas.drawString(72, y, f"Generated UTC: {payload.generated_at_utc}")

        y -= 28
        lines = [
            ("Quote ID", payload.quote_id),
            ("Engine", payload.engine_type),
            ("Customer", payload.customer_name),
            ("Part Number", payload.part_number),
            ("Total Cost", f"{payload.total_cost:,.2f}"),
            ("Total Price", f"{payload.total_price:,.2f}"),
            ("Margin %", f"{payload.margin_pct:.4f}"),
            ("Lead Time (weeks)", f"{payload.lead_time_weeks:.2f}"),
            ("MOQ", str(payload.moq)),
            ("PDF Ready", "TRUE" if payload.pdf_ready_flag else "FALSE"),
        ]

        canvas.setFont("Helvetica", 11)
        for label, value in lines:
            canvas.drawString(72, y, f"{label}: {value}")
            y -= 20

        canvas.showPage()
        canvas.save()
        return output_path
