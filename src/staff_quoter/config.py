from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    workspace_root: Path
    google_credentials_file: str
    google_sheets_id: str
    xlsx_recalc_script: Path
    default_workbook: Path
    output_json_dir: Path
    output_pdf_dir: Path



def _env_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    return Path(value).expanduser() if value else default



def get_settings() -> Settings:
    repo_root = Path(__file__).resolve().parents[2]
    workspace_root = repo_root.parent
    return Settings(
        workspace_root=workspace_root,
        google_credentials_file=os.getenv("GOOGLE_CREDENTIALS_FILE", ""),
        google_sheets_id=os.getenv("GOOGLE_SHEETS_ID", ""),
        xlsx_recalc_script=_env_path(
            "XLSX_RECALC_SCRIPT",
            Path.home() / ".codex" / "skills" / "xlsx" / "scripts" / "recalc.py",
        ),
        default_workbook=_env_path(
            "DEFAULT_WORKBOOK_PATH",
            workspace_root / "artifacts" / "workbooks" / "Staff_Quoter_Rebuild_Foundation_v1.xlsx",
        ),
        output_json_dir=_env_path("OUTPUT_JSON_DIR", repo_root / "output" / "json"),
        output_pdf_dir=_env_path("OUTPUT_PDF_DIR", repo_root / "output" / "pdf"),
    )
