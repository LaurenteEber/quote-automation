from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import gspread
from gspread import Spreadsheet, Worksheet

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsGateway:
    def __init__(
        self,
        spreadsheet_id: str,
        credentials_file: str,
        scopes: Sequence[str] | None = None,
    ) -> None:
        if not spreadsheet_id:
            raise ValueError("spreadsheet_id is required")
        if not credentials_file:
            raise ValueError("credentials_file is required")

        credentials_path = Path(credentials_file).expanduser()
        if not credentials_path.exists():
            raise FileNotFoundError(f"Google credentials file not found: {credentials_path}")

        self._spreadsheet_id = spreadsheet_id
        self._credentials_file = str(credentials_path)
        self._scopes = list(scopes or DEFAULT_SCOPES)
        self._client = gspread.service_account(filename=self._credentials_file, scopes=self._scopes)
        self._spreadsheet: Spreadsheet = self._client.open_by_key(self._spreadsheet_id)

    def worksheet(self, tab_name: str) -> Worksheet:
        return self._spreadsheet.worksheet(tab_name)

    def list_tabs(self) -> list[str]:
        return [ws.title for ws in self._spreadsheet.worksheets()]

    def read_records(self, tab_name: str) -> list[dict[str, Any]]:
        ws = self.worksheet(tab_name)
        return ws.get_all_records(default_blank="")

    def read_values(self, tab_name: str, range_a1: str | None = None) -> list[list[Any]]:
        ws = self.worksheet(tab_name)
        if range_a1:
            return ws.get(range_a1)
        return ws.get_all_values()

    def clear_tab(self, tab_name: str) -> None:
        self.worksheet(tab_name).clear()

    def write_records(self, tab_name: str, rows: Sequence[Mapping[str, Any]], clear_first: bool = True) -> int:
        ws = self.worksheet(tab_name)
        if clear_first:
            ws.clear()

        if not rows:
            return 0

        headers = list(rows[0].keys())
        values = [headers]
        for row in rows:
            values.append([_normalize_value(row.get(header)) for header in headers])

        ws.update(values, value_input_option="USER_ENTERED")
        return len(rows)


def _normalize_value(value: Any) -> Any:
    if value is None:
        return ""
    return value
