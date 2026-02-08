# Secrets Management Guide

## Rules
- Never commit `.env` or credential JSON files.
- Keep service-account files outside the repository path.
- Use GitHub Actions secrets for CI/CD access.
- Rotate credentials if a leak is suspected.

## Local setup
1. Create a local env file:
```bash
cp .env.example .env
chmod 600 .env
```
2. Fill values in `.env`:
- `GOOGLE_SHEETS_ID`
- `GOOGLE_CREDENTIALS_FILE` (absolute path outside repo)

## Install local commit protection
```bash
./scripts/setup_hooks.sh
```

This enables `.githooks/pre-commit`, which runs:
```bash
python3 scripts/scan_secrets.py --staged
```

## Manual secret scan
```bash
python3 scripts/scan_secrets.py
```

## Configure GitHub secrets safely
Required secrets:
- `GOOGLE_SHEETS_ID`
- `GOOGLE_CREDENTIALS_JSON`

Set from local machine without printing values:
```bash
export GOOGLE_SHEETS_ID='<sheet_id>'
export GOOGLE_CREDENTIALS_FILE='/absolute/path/outside/repo/service-account.json'
./scripts/set_github_secrets.sh
```

## Run first sync
```bash
source .venv/bin/activate
python scripts/sync_csv_to_gsheet.py --csv-dir ../artifacts/rebuild_template_csv
```
