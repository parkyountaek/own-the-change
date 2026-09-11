import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/doctor.py"
SPEC = importlib.util.spec_from_file_location("doctor", SCRIPT)
DOCTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCTOR)


class DoctorTests(unittest.TestCase):
    def test_default_runs_outside_git_without_writes_or_target_inspection(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT)], cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            checks = json.loads(result.stdout)["checks"]
            self.assertNotIn("target", {check["name"] for check in checks})
            self.assertFalse(any(check["status"] == "error" for check in checks))
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_missing_resources_and_git_and_old_python_report_failures(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(DOCTOR.shutil, "which", return_value=None), \
                mock.patch.object(DOCTOR.sys, "version_info", (3, 10)):
            result = DOCTOR.diagnose(root=Path(directory), target=Path(directory))
            statuses = {check["name"]: check["status"] for check in result["checks"]}
            self.assertEqual(statuses["python"], "error")
            self.assertEqual(statuses["git"], "error")
            self.assertEqual(statuses["resources"], "error")
            self.assertEqual(statuses["target"], "warning")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_unverified_platform_and_git_timeout_are_not_passes(self):
        with mock.patch.object(DOCTOR.platform, "system", return_value="Linux"), \
                mock.patch.object(DOCTOR.platform, "release", return_value="microsoft-standard-WSL2"), \
                mock.patch.object(DOCTOR.shutil, "which", return_value="/synthetic/git"), \
                mock.patch.object(DOCTOR.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 10)):
            result = DOCTOR.diagnose()
            statuses = {check["name"]: check["status"] for check in result["checks"]}
            self.assertEqual(statuses["git"], "error")
            self.assertEqual(statuses["platform"], "warning")

    def test_optional_exact_record_context_reports_risk_without_reading_or_writing_content(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
            destination = target / "docs/ai-understanding/2026-09-11/sample.md"
            result = DOCTOR.diagnose(target=target, record=destination)
            check = next(check for check in result["checks"] if check["name"] == "target")
            self.assertEqual(check["status"], "warning")
            self.assertEqual(check["detail"]["record_tracked"], "untracked")
            self.assertEqual(check["detail"]["record_ignore_match"], "not_ignored")
            self.assertFalse(destination.parent.exists())

    def test_invalid_record_usage_and_non_git_target_are_distinguished(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--record", "/unused/sample.md"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        with tempfile.TemporaryDirectory() as directory:
            result = DOCTOR.diagnose(target=Path(directory))
            check = next(check for check in result["checks"] if check["name"] == "target")
            self.assertEqual(check["status"], "warning")
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
