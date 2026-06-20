"""Fail CI when repository governance invariants are violated."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_PARTS = {
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".vite",
    ".vercel",
    "playwright-report",
    "test-results",
    "__MACOSX",
}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".log", ".tsbuildinfo"}
FORBIDDEN_ROOTS = {"工作记录及报告", "05_reports"}


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    errors: list[str] = []
    tracked = git_lines("ls-files")
    present_tracked = [path for path in tracked if (ROOT / path).exists()]

    if not (ROOT / "README.md").is_file():
        errors.append("README.md must exist")
    if not (ROOT / "AGENTS.md").is_file():
        errors.append("AGENTS.md must exist")
    if os.getenv("CI") == "true" and "README.md" not in tracked:
        errors.append("README.md must be tracked")
    if os.getenv("CI") == "true" and "AGENTS.md" not in tracked:
        errors.append("AGENTS.md must be tracked")

    nested_locks = sorted(
        str(path.relative_to(ROOT))
        for base in ("apps", "packages")
        for path in (ROOT / base).rglob("package-lock.json")
    )
    if nested_locks:
        errors.append(f"nested package-lock.json files: {', '.join(nested_locks)}")

    forbidden_tracked = []
    for path_text in present_tracked:
        path = Path(path_text)
        if path.parts and path.parts[0] in FORBIDDEN_ROOTS:
            forbidden_tracked.append(path_text)
            continue
        if any(part in FORBIDDEN_PARTS for part in path.parts):
            forbidden_tracked.append(path_text)
            continue
        if path.suffix in FORBIDDEN_SUFFIXES:
            forbidden_tracked.append(path_text)
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            forbidden_tracked.append(path_text)

    if forbidden_tracked:
        errors.append("forbidden tracked files: " + ", ".join(forbidden_tracked))

    deploy_path = ROOT / ".github" / "workflows" / "deploy.yml"
    if deploy_path.exists():
        deploy_text = deploy_path.read_text(encoding="utf-8")
        trigger_block = deploy_text.split("jobs:", 1)[0]
        if "workflow_dispatch:" not in trigger_block:
            errors.append("deploy workflow must support workflow_dispatch")
        if "\n  push:" in trigger_block:
            errors.append("deploy workflow must not run on push")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"repository policy passed: {len(present_tracked)} present tracked paths checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
