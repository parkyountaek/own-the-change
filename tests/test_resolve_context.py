import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_validate_record import record

ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "scripts/resolve_context.py"


class ResolveContextTests(unittest.TestCase):
    def run_resolver(self, target, resolver=RESOLVER, record_path=None):
        arguments = [sys.executable, str(resolver), "--target", str(target)]
        if record_path is not None:
            arguments.extend(["--record", str(record_path)])
        return subprocess.run(arguments,
                              capture_output=True, text=True, check=False)

    def init_target(self, directory):
        target = Path(directory).resolve() / "target"
        target.mkdir()
        subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
        return target

    def test_exact_record_check_does_not_create_a_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.init_target(directory)
            destination = target / "docs/ai-understanding/2026-09-09/sample-change.md"
            result = self.run_resolver(target, record_path=destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)
            self.assertEqual(context["record_tracked"], "untracked")
            self.assertEqual(context["record_ignore_match"], "not_ignored")
            self.assertFalse(context["record_exists"])
            self.assertFalse((target / "docs").exists())
            alias = Path(directory) / "target-alias"
            alias.symlink_to(target, target_is_directory=True)
            result = self.run_resolver(alias, record_path=alias / destination.relative_to(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["record_path"], str(destination))

    def test_exact_record_reports_tracked_and_ignore_match_separately(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.init_target(directory)
            destination = target / "docs/ai-understanding/2026-09-09/sample-change.md"
            destination.parent.mkdir(parents=True)
            destination.write_text("Synthetic tracking fixture", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", str(destination)], check=True, capture_output=True)
            (target / ".gitignore").write_text("/docs/ai-understanding/\n", encoding="utf-8")
            context = json.loads(self.run_resolver(target, record_path=destination).stdout)
            self.assertEqual(context["record_tracked"], "tracked")
            self.assertEqual(context["record_ignore_match"], "ignored")
            self.assertTrue(context["record_exists"])
            untracked = destination.with_name("new-record.md")
            context = json.loads(self.run_resolver(target, record_path=untracked).stdout)
            self.assertEqual(context["record_tracked"], "untracked")
            self.assertEqual(context["record_ignore_match"], "ignored")

    def test_exact_record_rejects_external_date_or_file_alias(self):
        for kind in ["date", "file", "public"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                target = self.init_target(directory)
                destination = target / "docs/ai-understanding/2026-09-09/sample-change.md"
                external = Path(directory).resolve() / "external"
                external.mkdir()
                if kind == "date":
                    destination.parent.parent.mkdir(parents=True)
                    destination.parent.symlink_to(external, target_is_directory=True)
                elif kind == "file":
                    destination.parent.mkdir(parents=True)
                    destination.symlink_to(external / "sample-change.md")
                else:
                    public = target / "docs/examples/records/2026-09-09"
                    public.mkdir(parents=True)
                    destination.parent.parent.mkdir(parents=True)
                    destination.parent.symlink_to(public, target_is_directory=True)
                result = self.run_resolver(target, record_path=destination)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("Record path must", result.stderr)
                self.assertEqual(list(external.iterdir()), [])

    def test_exact_record_rejects_relative_and_outside_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.init_target(directory)
            for destination in [Path("record.md"), target / "other.md", target / "docs/ai-understanding/../../other.md"]:
                result = self.run_resolver(target, record_path=destination)
                self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertFalse((target / "other.md").exists())

    def test_record_alias_cannot_hide_a_tracked_physical_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.init_target(directory)
            physical = target / "existing-record.md"
            physical.write_text("Synthetic tracked record target", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", str(physical)], check=True, capture_output=True)
            destination = target / "docs/ai-understanding/2026-09-09/sample-change.md"
            destination.parent.mkdir(parents=True)
            destination.symlink_to(physical)
            (target / ".gitignore").write_text("/docs/ai-understanding/\n", encoding="utf-8")
            result = self.run_resolver(target, record_path=destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)
            self.assertEqual(context["record_tracked"], "tracked")
            self.assertEqual(context["record_ignore_match"], "not_ignored")
            self.assertEqual(physical.read_text(), "Synthetic tracked record target")

    def test_foreign_nested_target_uses_source_resources_and_target_record_root(self):
        with tempfile.TemporaryDirectory(prefix="own-change-context-") as directory:
            target = Path(directory).resolve() / "target project"
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
            nested = target / "src/nested"
            nested.mkdir(parents=True)
            source_alias = Path(directory) / "source alias"
            source_alias.symlink_to(ROOT, target_is_directory=True)
            result = self.run_resolver(nested, source_alias / "scripts/resolve_context.py")
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)
            self.assertEqual(context["source_root"], str(ROOT))
            self.assertEqual(context["target_root"], str(target))
            self.assertEqual(context["record_root"], str(target / "docs/ai-understanding"))
            self.assertFalse(Path(context["record_root"]).exists())
            self.assertFalse((nested / "docs").exists())
            for key in ["protocol", "template", "validator"]:
                self.assertTrue(Path(context[key]).is_file())
                self.assertTrue(Path(context[key]).is_relative_to(ROOT))

            # An explicitly fictional test fixture exercises writing/validation in a foreign target.
            destination = Path(context["record_root"]) / "2026-09-09/sample-change.md"
            destination.parent.mkdir(parents=True)
            destination.write_text(record(), encoding="utf-8")
            validated = subprocess.run([sys.executable, context["validator"], str(destination)],
                                       cwd=nested, capture_output=True, text=True, check=False)
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertFalse((nested / "docs").exists())

    def test_non_git_target_fails_without_creating_records(self):
        with tempfile.TemporaryDirectory(prefix="own-change-no-git-") as directory:
            result = self.run_resolver(directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("inside a Git working tree", result.stderr)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_missing_target_fails_without_creation(self):
        with tempfile.TemporaryDirectory(prefix="own-change-missing-") as directory:
            target = Path(directory) / "absent"
            result = self.run_resolver(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())

    def test_external_record_directory_links_are_rejected_without_writes(self):
        for component in ["docs", "docs/ai-understanding"]:
            with self.subTest(component=component), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "target"
                target.mkdir()
                subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
                external = Path(directory) / "external"
                external.mkdir()
                link = target / component
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(external, target_is_directory=True)
                result = self.run_resolver(target)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("outside the target repository", result.stderr)
                self.assertEqual(list(external.iterdir()), [])
                self.assertTrue(link.is_symlink())

    def test_file_in_record_directory_path_has_actionable_error(self):
        for component in ["docs", "docs/ai-understanding"]:
            with self.subTest(component=component), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "target"
                target.mkdir()
                subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
                conflict = target / component
                conflict.parent.mkdir(parents=True, exist_ok=True)
                conflict.write_text("Keep this file", encoding="utf-8")
                result = self.run_resolver(target)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("not a directory", result.stderr)
                self.assertEqual(conflict.read_text(), "Keep this file")


if __name__ == "__main__":
    unittest.main()
