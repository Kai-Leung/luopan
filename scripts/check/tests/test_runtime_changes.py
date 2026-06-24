from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.check.runtime_changes import (
    ZERO_SHA,
    changed_paths,
    runtime_changed,
)


class RuntimePathTests(unittest.TestCase):
    def test_backend_python_change_deploys(self):
        self.assertTrue(runtime_changed(["services/api/app/main.py"]))

    def test_h5_tsx_change_deploys(self):
        self.assertTrue(runtime_changed(["apps/h5/src/App.tsx"]))

    def test_pc_ts_change_deploys(self):
        self.assertTrue(runtime_changed(["apps/pc/src/api.ts"]))

    def test_package_type_change_deploys(self):
        self.assertTrue(runtime_changed(["packages/shared-types/src/index.ts"]))

    def test_root_readme_does_not_deploy(self):
        self.assertFalse(runtime_changed(["README.md"]))

    def test_nested_h5_readme_does_not_deploy(self):
        self.assertFalse(runtime_changed(["apps/h5/src/modules/README.md"]))

    def test_docs_change_does_not_deploy(self):
        self.assertFalse(runtime_changed(["docs/deployment/README.md"]))

    def test_mixed_code_and_markdown_deploys(self):
        self.assertTrue(
            runtime_changed(["README.md", "services/api/app/main.py"])
        )

    def test_workflow_change_deploys(self):
        self.assertTrue(runtime_changed([".github/workflows/deploy.yml"]))


class RuntimeGitRangeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self._git("init", "-q")
        self._git("config", "user.name", "Runtime Test")
        self._git("config", "user.email", "runtime@example.test")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _commit(self, message: str) -> str:
        self._git("add", ".")
        self._git("commit", "-q", "-m", message)
        return self._git("rev-parse", "HEAD")

    def test_multi_commit_range_keeps_earlier_code_change(self):
        self._write("README.md", "baseline")
        base = self._commit("baseline")
        self._write("services/api/app/main.py", "runtime")
        self._commit("runtime")
        self._write("README.md", "docs only last")
        head = self._commit("docs")

        paths = changed_paths(self.repo, base_sha=base, head_sha=head)

        self.assertIn("services/api/app/main.py", paths)
        self.assertTrue(runtime_changed(paths))

    def test_root_commit_fallback_detects_runtime_tree(self):
        self._write("apps/h5/src/App.tsx", "runtime")
        head = self._commit("root")

        paths = changed_paths(self.repo, base_sha="", head_sha=head)

        self.assertTrue(runtime_changed(paths))

    def test_zero_before_sha_detects_runtime_tree(self):
        self._write("README.md", "docs")
        self._commit("root docs")
        self._write("apps/pc/src/api.ts", "runtime")
        head = self._commit("runtime")

        paths = changed_paths(self.repo, base_sha=ZERO_SHA, head_sha=head)

        self.assertIn("apps/pc/src/api.ts", paths)
        self.assertTrue(runtime_changed(paths))


if __name__ == "__main__":
    unittest.main()
