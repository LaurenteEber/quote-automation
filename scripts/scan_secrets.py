#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]

SUSPICIOUS_PATTERNS = {
    "OPENAI_API_KEY": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "GITHUB_TOKEN": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "PRIVATE_KEY_BLOCK": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS_ACCESS_KEY_ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GOOGLE_API_KEY": re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
}

BLOCKED_GLOB_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.p12",
    "*.pfx",
    "*.key",
    "*service-account*.json",
    "*credentials*.json",
    ".secrets/*",
    "secrets/*",
]

SKIP_PATH_PREFIXES = [
    ".git/",
    ".venv/",
    "venv/",
    "output/",
    "tmp/",
    "__pycache__/",
    ".pytest_cache/",
]



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan repository for likely secret leaks")
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Scan only staged files",
    )
    return parser.parse_args()



def main() -> int:
    args = parse_args()

    files = _git_staged_files() if args.staged else _git_tracked_files()

    violations: list[str] = []
    for rel in files:
        if _should_skip(rel):
            continue

        path = REPO_ROOT / rel
        if not path.exists() or path.is_dir():
            continue

        if _is_blocked_name(rel):
            violations.append(f"blocked-file: {rel}")

        text = _read_text(path)
        if not text:
            continue

        for code, pattern in SUSPICIOUS_PATTERNS.items():
            if pattern.search(text):
                violations.append(f"pattern-{code}: {rel}")

    if violations:
        print("Potential secret leaks detected:")
        for item in sorted(set(violations)):
            print(f"  - {item}")
        print("Fix before commit/push.")
        return 1

    print("No secret leak patterns detected.")
    return 0



def _git_tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return _lines_to_paths(result.stdout)



def _git_staged_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return _lines_to_paths(result.stdout)



def _lines_to_paths(stdout: str) -> list[Path]:
    return [Path(line.strip()) for line in stdout.splitlines() if line.strip()]



def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""



def _is_blocked_name(rel: Path) -> bool:
    rel_str = rel.as_posix()
    filename = rel.name
    for pattern in BLOCKED_GLOB_PATTERNS:
        if fnmatch.fnmatch(rel_str, pattern) or fnmatch.fnmatch(filename, pattern):
            if rel_str == ".env.example":
                return False
            return True
    return False



def _should_skip(rel: Path) -> bool:
    rel_str = rel.as_posix()
    return any(rel_str.startswith(prefix) for prefix in SKIP_PATH_PREFIXES)


if __name__ == "__main__":
    raise SystemExit(main())
