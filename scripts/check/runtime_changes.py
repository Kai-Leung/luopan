"""Detect whether a Git range contains deployable runtime changes."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Iterable


ZERO_SHA = "0" * 40
RUNTIME_PREFIXES = (
    "services/api/",
    "apps/h5/",
    "apps/pc/",
    "apps/mobile-shell/",
    "packages/",
    "scripts/check/",
)
RUNTIME_FILES = {
    "package.json",
    "package-lock.json",
    "services/api/requirements.txt",
    ".github/workflows/ci.yml",
    ".github/workflows/deploy.yml",
}
DOCUMENTATION_PREFIXES = (
    "docs/",
    ".github/ISSUE_TEMPLATE/",
)


def is_documentation_path(path: str) -> bool:
    normalized = _normalize_path(path)
    return (
        normalized.lower().endswith(".md")
        or normalized.startswith(DOCUMENTATION_PREFIXES)
    )


def is_runtime_path(path: str) -> bool:
    normalized = _normalize_path(path)
    if not normalized or is_documentation_path(normalized):
        return False
    return normalized in RUNTIME_FILES or normalized.startswith(RUNTIME_PREFIXES)


def runtime_changed(paths: Iterable[str]) -> bool:
    return any(is_runtime_path(path) for path in paths)


def _normalize_path(path: str) -> str:
    normalized = path.strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def git_lines(repo: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def commit_exists(repo: Path, sha: str) -> bool:
    if not sha or sha == ZERO_SHA:
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def changed_paths(repo: Path, *, base_sha: str, head_sha: str) -> list[str]:
    if not commit_exists(repo, head_sha):
        raise ValueError(f"head SHA is not a commit: {head_sha}")
    if commit_exists(repo, base_sha):
        return git_lines(repo, "diff", "--name-only", base_sha, head_sha)
    # Branch creation, all-zero before SHA, missing base, and root commits all
    # need the complete target tree rather than only the final commit delta.
    return git_lines(repo, "ls-tree", "-r", "--name-only", head_sha)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    paths = changed_paths(
        args.repo.resolve(),
        base_sha=args.base,
        head_sha=args.head,
    )
    result = "true" if runtime_changed(paths) else "false"
    print(result)
    if args.github_output is not None:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"runtime_changed={result}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
