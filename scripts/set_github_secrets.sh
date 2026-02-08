#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GOOGLE_SHEETS_ID:-}" ]; then
  echo "GOOGLE_SHEETS_ID env var is required"
  exit 1
fi

if [ -z "${GOOGLE_CREDENTIALS_FILE:-}" ]; then
  echo "GOOGLE_CREDENTIALS_FILE env var is required"
  exit 1
fi

if [ ! -f "$GOOGLE_CREDENTIALS_FILE" ]; then
  echo "Credentials file not found: $GOOGLE_CREDENTIALS_FILE"
  exit 1
fi

REPO="${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"

gh secret set GOOGLE_SHEETS_ID --repo "$REPO" --body "$GOOGLE_SHEETS_ID"
gh secret set GOOGLE_CREDENTIALS_JSON --repo "$REPO" < "$GOOGLE_CREDENTIALS_FILE"

echo "GitHub secrets set for $REPO: GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_JSON"
