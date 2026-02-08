"""Small env check for local bootstrap."""

REQUIRED_IMPORTS = [
    "openpyxl",
    "pandas",
    "numpy",
    "dotenv",
    "gspread",
    "googleapiclient",
    "pydantic",
    "yaml",
    "rich",
    "reportlab",
    "pdfplumber",
    "pypdf",
]


def main() -> int:
    failed = []
    for module in REQUIRED_IMPORTS:
        try:
            __import__(module)
        except Exception:
            failed.append(module)
    if failed:
        print("Missing modules:", ", ".join(failed))
        return 1
    print("Environment OK: all required modules import successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
