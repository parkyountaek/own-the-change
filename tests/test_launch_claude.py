import importlib.util
from pathlib import Path
import subprocess
import signal
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("launch_claude", ROOT / "scripts/launch_claude.py")
LAUNCHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAUNCHER)


class LaunchClaudeTests(unittest.TestCase):
    def test_launch_builds_a_complete_temporary_plugin_and_preserves_project(self):
        with tempfile.TemporaryDirectory(prefix="own-change-launch-test-") as directory:
            project = Path(directory).resolve() / "project with spaces"
            project.mkdir()
            (project / "keep.txt").write_text("existing work", encoding="utf-8")
            packages = []

            def run(command, **kwargs):
                if command[0] == "git":
                    self.assertEqual(command, ["git", "-C", str(project), "rev-parse", "--show-toplevel"])
                    return subprocess.CompletedProcess(command, 0, str(project), "")
                self.assertEqual(command[:2], ["/test tools/claude", "--plugin-dir"])
                self.assertEqual(len(command), 3)
                self.assertEqual(kwargs["cwd"], project)
                self.assertTrue(callable(signal.getsignal(signal.SIGINT)))
                self.assertIsNone(signal.getsignal(signal.SIGINT)(signal.SIGINT, None))
                package = Path(command[2])
                packages.append(package)
                self.assertTrue((package / ".claude-plugin/plugin.json").is_file())
                self.assertTrue((package / "docs/protocol/understanding-protocol.md").is_file())
                self.assertFalse(any(path.is_symlink() for path in package.rglob("*")))
                return subprocess.CompletedProcess(command, 7)

            original_handler = signal.getsignal(signal.SIGINT)
            with patch.object(LAUNCHER.shutil, "which", return_value="/test tools/claude"), \
                    patch.object(LAUNCHER.subprocess, "run", side_effect=run):
                for _ in range(2):
                    self.assertEqual(LAUNCHER.launch(project), 7)
                    self.assertEqual(signal.getsignal(signal.SIGINT), original_handler)
            self.assertNotEqual(packages[0], packages[1])
            self.assertTrue(all(not package.exists() for package in packages))
            self.assertEqual(list(project.iterdir()), [project / "keep.txt"])
            self.assertEqual((project / "keep.txt").read_text(), "existing work")

    def test_missing_project_fails_before_build_or_host_start(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(LAUNCHER, "build_plugins") as build, \
                patch.object(LAUNCHER.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "does not exist"):
                LAUNCHER.launch(Path(directory) / "absent")
            build.assert_not_called()
            run.assert_not_called()

    def test_missing_tools_and_non_git_targets_fail_without_a_build(self):
        cases = [(None, "Git", "Claude Code"), ("claude", None, "Git is not"),
                 ("claude", "git", "inside a Git repository")]
        for claude, git, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory, \
                    patch.object(LAUNCHER.shutil, "which", side_effect=[claude, git]), \
                    patch.object(LAUNCHER.subprocess, "run", return_value=subprocess.CompletedProcess([], 128)), \
                    patch.object(LAUNCHER, "build_plugins") as build:
                with self.assertRaisesRegex(ValueError, message):
                    LAUNCHER.launch(directory)
                build.assert_not_called()

    def test_launch_error_or_interrupt_cleans_up_only_the_temporary_build(self):
        for error in [OSError("launch failed"), KeyboardInterrupt()]:
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as directory:
                packages = []

                def run(command, **kwargs):
                    if command[0] == "git":
                        return subprocess.CompletedProcess(command, 0, directory, "")
                    packages.append(Path(command[2]))
                    raise error

                with patch.object(LAUNCHER.shutil, "which", return_value="claude"), \
                        patch.object(LAUNCHER.subprocess, "run", side_effect=run):
                    with self.assertRaises(type(error)):
                        LAUNCHER.launch(directory)
                self.assertFalse(packages[0].exists())
                self.assertTrue(Path(directory).is_dir())

    def test_help_does_not_launch_a_session(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/launch_claude.py"), "--help"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("project", result.stdout)

    def test_module_invocation_is_supported(self):
        result = subprocess.run([sys.executable, "-m", "scripts.launch_claude", "--help"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("project", result.stdout)

    def test_file_target_has_an_accurate_error(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "not-a-directory"
            target.write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not a directory"):
                LAUNCHER.launch(target)
            self.assertEqual(target.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
