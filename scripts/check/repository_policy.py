"""Fail CI when repository governance invariants are violated."""

from __future__ import annotations

import os
import re
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
    ci_path = ROOT / ".github" / "workflows" / "ci.yml"
    runtime_changes_path = ROOT / "scripts" / "check" / "runtime_changes.py"
    runtime_changes_test_path = (
        ROOT / "scripts" / "check" / "tests" / "test_runtime_changes.py"
    )
    if deploy_path.exists():
        deploy_text = deploy_path.read_text(encoding="utf-8")
        trigger_block = deploy_text.split("jobs:", 1)[0]
        if "workflow_dispatch:" not in trigger_block:
            errors.append("deploy workflow must support workflow_dispatch")
        if "workflow_call:" not in trigger_block:
            errors.append("deploy workflow must support workflow_call")
        if "\n  push:" in trigger_block:
            errors.append("deploy workflow must not run on push")
        if "cancel-in-progress: false" not in deploy_text:
            errors.append("deploy workflow must not cancel an in-progress production deployment")
        if "git merge --ff-only" not in deploy_text:
            errors.append("deploy workflow must use a fast-forward-only update")
        dirty_worktree_checks = (
            "git diff --quiet",
            "git diff --cached --quiet",
            "git ls-files --others --exclude-standard",
        )
        for check in dirty_worktree_checks:
            if check not in deploy_text:
                errors.append(f"deploy workflow missing dirty-worktree check: {check}")
        forbidden_cleanup_commands = (
            "git reset --hard",
            "git clean",
            "git checkout -f",
            "git stash",
        )
        for command in forbidden_cleanup_commands:
            if command in deploy_text:
                errors.append(f"deploy workflow must not use destructive cleanup: {command}")
        if 'git cat-file -e "${deploy_sha}^{commit}"' not in deploy_text:
            errors.append("deploy workflow must validate the target commit object")
        if 'actual_sha="$(git rev-parse HEAD)"' not in deploy_text:
            errors.append("deploy workflow must read the deployed HEAD")
        if '"$actual_sha" != "$deploy_sha"' not in deploy_text:
            errors.append("deploy workflow must compare HEAD with the deployment SHA")
        if "/health" not in deploy_text:
            errors.append("deploy workflow must perform a health check")

    if not ci_path.exists():
        errors.append("CI workflow must exist")
    else:
        ci_text = ci_path.read_text(encoding="utf-8")
        required_jobs = {
            "repository-policy",
            "frontend",
            "contracts",
            "backend",
            "integration",
            "detect-runtime-changes",
            "deploy-production",
        }
        declared_jobs = set(re.findall(r"^  ([a-z0-9-]+):$", ci_text, flags=re.MULTILINE))
        missing_jobs = sorted(required_jobs - declared_jobs)
        if missing_jobs:
            errors.append(f"CI workflow missing required jobs: {', '.join(missing_jobs)}")
        if "continue-on-error:" in ci_text:
            errors.append("CI workflow must not use continue-on-error")
        deploy_job = ci_text.split("\n  deploy-production:", 1)
        if len(deploy_job) != 2:
            errors.append("CI workflow must define deploy-production")
        else:
            deploy_text = deploy_job[1]
            for required_need in (
                "repository-policy",
                "frontend",
                "contracts",
                "backend",
                "integration",
                "detect-runtime-changes",
            ):
                if f"- {required_need}" not in deploy_text:
                    errors.append(f"deploy-production must depend on {required_need}")
            if "github.event_name == 'push'" not in deploy_text:
                errors.append("deploy-production must only run for push events")
            if "github.ref == 'refs/heads/main'" not in deploy_text:
                errors.append("deploy-production must only run on main")
            if "runtime_changed == 'true'" not in deploy_text:
                errors.append("deploy-production must require runtime changes")
            if "uses: ./.github/workflows/deploy.yml" not in deploy_text:
                errors.append("deploy-production must call the reusable deploy workflow")
        if "python3 scripts/check/runtime_changes.py" not in ci_text:
            errors.append("CI workflow must use the tested runtime change detector")
        if "python3 -m unittest scripts.check.tests.test_runtime_changes" not in ci_text:
            errors.append("CI workflow must run runtime change detector tests")

    if not runtime_changes_path.is_file():
        errors.append("runtime change detection script must exist")
    if not runtime_changes_test_path.is_file():
        errors.append("runtime change detection tests must exist")

    workflow_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ci_path, deploy_path)
        if path.exists()
    )
    if "[skip ci]" in workflow_text.lower():
        errors.append("CI and deploy workflows must not rely on [skip ci]")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"repository policy passed: {len(present_tracked)} present tracked paths checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
