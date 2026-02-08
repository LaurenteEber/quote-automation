from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json


@dataclass(frozen=True)
class FormulaIssue:
    sheet: str
    cell: str
    code: str
    detail: str


@dataclass
class FormulaValidationReport:
    workbook_path: str
    total_formulas: int
    issues: list[FormulaIssue]

    @property
    def has_errors(self) -> bool:
        return len(self.issues) > 0

    def to_dict(self) -> dict[str, object]:
        return {
            "workbook_path": self.workbook_path,
            "total_formulas": self.total_formulas,
            "issue_count": len(self.issues),
            "issues": [asdict(issue) for issue in self.issues],
        }


@dataclass(frozen=True)
class QuotePayload:
    quote_id: str
    engine_type: str
    customer_name: str
    part_number: str
    total_cost: float
    total_price: float
    margin_pct: float
    lead_time_weeks: float
    moq: int
    pdf_ready_flag: bool
    generated_at_utc: str

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=True, indent=2)
