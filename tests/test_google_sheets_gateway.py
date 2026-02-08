from __future__ import annotations

from pathlib import Path

import pytest

from staff_quoter.google_sheets import GoogleSheetsGateway


def test_gateway_requires_spreadsheet_id_and_credentials() -> None:
    with pytest.raises(ValueError):
        GoogleSheetsGateway(spreadsheet_id="", credentials_file="/tmp/cred.json")

    with pytest.raises(ValueError):
        GoogleSheetsGateway(spreadsheet_id="abc", credentials_file="")


def test_gateway_requires_existing_credentials_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        GoogleSheetsGateway(spreadsheet_id="abc", credentials_file=str(missing))
