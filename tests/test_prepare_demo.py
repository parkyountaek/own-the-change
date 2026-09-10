import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prepare_demo", ROOT / "scripts/prepare_demo.py")
DEMO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEMO)


class PrepareDemoTests(unittest.TestCase):
    def test_inherited_git_overrides_cannot_redirect_setup(self):
        with tempfile.TemporaryDirectory() as directory:
            foreign_index = Path(directory) / "foreign-index"
            foreign_index.write_text("Keep this index untouched", encoding="utf-8")
            foreign_git = Path(directory) / "foreign-git"
            with mock.patch.dict(os.environ, {"GIT_INDEX_FILE": str(foreign_index),
                                              "GIT_DIR": str(foreign_git)}):
                target = DEMO.prepare_demo(Path(directory) / "demo")
            self.assertEqual(foreign_index.read_text(), "Keep this index untouched")
            self.assertFalse(foreign_git.exists())
            self.assertTrue((target / ".git/index").is_file())

    def test_fixture_has_an_index_baseline_and_visible_change_without_a_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            target = DEMO.prepare_demo(Path(directory) / "demo with spaces")
            baseline = subprocess.run(["git", "show", ":display_name.py"], cwd=target,
                                      check=True, capture_output=True)
            self.assertEqual(baseline.stdout, (DEMO.FIXTURE / "before/display_name.py").read_bytes())
            head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=target, capture_output=True)
            self.assertNotEqual(head.returncode, 0)
            diff = subprocess.run(["git", "diff", "--name-only"], cwd=target,
                                  check=True, capture_output=True, text=True)
            self.assertEqual(set(diff.stdout.splitlines()), {"display_name.py", "test_display_name.py"})
            tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
                                   cwd=target, capture_output=True, text=True)
            self.assertEqual(tests.returncode, 0, tests.stderr)
            self.assertIn("Ran 4 tests", tests.stderr)
            ignored = subprocess.run(["git", "check-ignore", "docs/ai-understanding/2099-01-01/demo.md"],
                                     cwd=target, capture_output=True)
            self.assertEqual(ignored.returncode, 0)
            self.assertFalse((target / "docs/ai-understanding").exists())

    def test_existing_files_directories_and_links_are_preserved(self):
        for kind in ("file", "directory", "link"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "existing"
                if kind == "file":
                    target.write_text("Keep this content", encoding="utf-8")
                elif kind == "directory":
                    target.mkdir()
                else:
                    target.symlink_to(Path(directory) / "missing")
                with self.assertRaisesRegex(ValueError, "Output already exists"):
                    DEMO.prepare_demo(target)
                if kind == "file":
                    self.assertEqual(target.read_text(), "Keep this content")
                elif kind == "directory":
                    self.assertEqual(list(target.iterdir()), [])
                else:
                    self.assertTrue(target.is_symlink())


if __name__ == "__main__":
    unittest.main()
