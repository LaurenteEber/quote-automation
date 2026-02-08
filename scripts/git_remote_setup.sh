#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <remote_url> [branch_name]"
  exit 1
fi

REMOTE_URL="$1"
BRANCH_NAME="${2:-$(git rev-parse --abbrev-ref HEAD)}"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

git remote -v

echo "Pushing branch: $BRANCH_NAME"
git push -u origin "$BRANCH_NAME"
