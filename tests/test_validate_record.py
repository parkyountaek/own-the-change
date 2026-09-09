import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_record.py"


def record(*, date="2026-09-09", status="not_confirmed", include_tests=True,
           response_status="not_answered", evidence="available", risk="low",
           dates=(), reason="none", response=None):
    tests = "## Test Evidence\n- `python3 -m unittest` was run.\n" if include_tests else ""
    follow_up = "\n" + "\n".join("  - " + item for item in dates) if dates else " []"
    response = response if response is not None else "No response."
    diff_scope = "HEAD and current working-tree changes" if evidence == "available" else "unknown"
    return f"""---
task_id: sample-change
date: {date}
record_kind: actual
understanding_status: {status}
risk_level: {risk}
user_response_status: {response_status}
evidence_status: {evidence}
diff_scope: {diff_scope}
follow_up_at:{follow_up}
follow_up_reason: {reason}
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# Understanding record: sample-change

## Goal
- Understand a small change.

## Changed Files
- `src/example.py`

{tests}## Key Explanation
- It accepts input and returns a result.

## User Response
{response}

## Understanding Status
- {status}: structural test fixture, not an actual assessment.

## Remaining Risks
- The production environment was not checked.

## Next Check
- Explain it again if needed.
"""


class ValidateRecordTests(unittest.TestCase):
    def run_validator(self, content, filename="sample-change.md", directory_date="2026-09-09"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / directory_date / filename
            path.parent.mkdir()
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_accepts_complete_record_and_unknown_metadata(self):
        result = self.run_validator(record())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_rejects_unknown_status(self):
        result = self.run_validator(record(status="passed"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("understanding_status", result.stderr)

    def test_rejects_missing_required_section(self):
        result = self.run_validator(record(include_tests=False))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Test Evidence", result.stderr)

    def test_rejects_invalid_or_mismatched_date(self):
        for date in ["09-09-2026", "2026-02-30", "2026-09-10"]:
            with self.subTest(date=date):
                result = self.run_validator(record(date=date))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("date", result.stderr)

    def assert_invalid(self, content, message):
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def test_answer_and_evidence_are_required_for_assessed_statuses(self):
        for status in ["confirmed", "needs_follow_up"]:
            with self.subTest(status=status):
                self.assert_invalid(record(status=status), "require an answered user response")
                self.assert_invalid(record(status=status, response_status="answered", response="A supplied answer.", evidence="unavailable"), "require available change evidence")

    def test_structurally_supported_statuses_do_not_grade_the_answer(self):
        for status in ["confirmed", "needs_follow_up"]:
            result = self.run_validator(record(status=status, response_status="answered", response="A supplied test answer whose correctness is not judged."))
            self.assertEqual(result.returncode, 0, result.stderr)
        for status in ["not_confirmed", "unknown"]:
            result = self.run_validator(record(status=status, evidence="unavailable"))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_body_status_must_agree_with_front_matter(self):
        content = record().replace("- not_confirmed: structural", "- confirmed: structural")
        self.assert_invalid(content, "same status as front matter")

    def test_status_accepts_common_dash_separators_without_accepting_a_different_value(self):
        for separator in ["-", "\u2013", "\u2014"]:
            with self.subTest(separator=separator):
                content = record().replace("- not_confirmed: structural", f"- not_confirmed{separator}structural")
                result = self.run_validator(content)
                self.assertEqual(result.returncode, 0, result.stderr)
        for suffix in ["ness", "_extra", "123"]:
            content = record().replace("- not_confirmed: structural", f"- not_confirmed{suffix}: structural")
            self.assert_invalid(content, "same status as front matter")

    def test_response_marker_must_agree_with_response_status(self):
        self.assert_invalid(record(response_status="answered"), "not the No response marker")
        self.assert_invalid(record(response="An answer that was not marked answered."), "not_answered requires")

    def test_available_evidence_requires_a_diff_scope(self):
        for scope in ["unknown", '""', "TODO"]:
            with self.subTest(scope=scope):
                self.assert_invalid(record().replace("HEAD and current working-tree changes", scope), "known diff_scope")

    def test_empty_and_placeholder_sections_are_rejected(self):
        for content in ["", "- ", "TODO", "- TBD"]:
            self.assert_invalid(record().replace("- Understand a small change.", content), "empty or placeholder section: Goal")

    def test_duplicate_keys_and_sections_are_rejected(self):
        cases = [
            (record().replace("risk_level: low", "risk_level: low\nrisk_level: high"), "duplicate front matter key"),
            (record().replace("  model: unknown", "  model: unknown\n  model: another-model"), "duplicate execution_metadata key"),
            (record() + "\n## Goal\nAnother goal.\n", "duplicate section"),
        ]
        for content, message in cases:
            self.assert_invalid(content, message)

    def test_headings_inside_fenced_evidence_do_not_supply_sections(self):
        self.assert_invalid(record(include_tests=False) + "\n```md\n## Test Evidence\nFake section.\n```\n", "missing required section: Test Evidence")

    def test_mismatched_task_filename_is_rejected(self):
        result = self.run_validator(record(), filename="another-task.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("record filename", result.stderr)

    def test_required_structured_fields_and_metadata_are_checked(self):
        for line, message in [
            ("record_kind: actual\n", "record_kind"),
            ("user_response_status: not_answered\n", "user_response_status"),
            ("  cost: unknown\n", "execution_metadata.cost"),
        ]:
            self.assert_invalid(record().replace(line, ""), message)
        self.assert_invalid(record().replace("record_kind: actual", "record_kind: real"), "record_kind must be")
        self.assert_invalid(record().replace("evidence_status: available", "evidence_status: maybe"), "evidence_status must be")
        self.assert_invalid(record().replace("risk_level: low", "risk_level: low\nextra: value"), "unknown or duplicate")

    def test_high_risk_requires_both_follow_up_dates(self):
        self.assert_invalid(record(risk="high"), "next-day and one-week")
        self.assert_invalid(record(risk="high", dates=["2026-09-10"], reason="Recall the boundary"), "next-day and one-week")
        result = self.run_validator(record(risk="high", dates=["2026-09-10", "2026-09-16"], reason="Recall the boundary"))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_follow_up_calendar_boundaries(self):
        for work_date, dates in [
            ("2026-12-31", ["2027-01-01", "2027-01-07"]),
            ("2028-02-28", ["2028-02-29", "2028-03-06"]),
        ]:
            result = self.run_validator(record(date=work_date, risk="high", dates=dates, reason="Recall the boundary"), directory_date=work_date)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_duplicate_past_and_unexplained_follow_up_dates(self):
        for dates, reason, message in [
            (["2026-99-99"], "Recall", "valid YYYY-MM-DD"),
            (["2026-09-10", "2026-09-10"], "Recall", "duplicate dates"),
            (["2026-09-09"], "Recall", "after the work date"),
            (["2026-09-10"], "none", "concrete follow_up_reason"),
            ([], "Recall", "follow_up_reason: none"),
        ]:
            self.assert_invalid(record(dates=dates, reason=reason), message)

    def test_legacy_follow_up_scalars_fail_with_migration_guidance(self):
        self.assert_invalid(record().replace("follow_up_at: []", "follow_up_at: none"), "indented date list")

    def test_quoted_scalar_with_colon_is_supported(self):
        content = record().replace("HEAD and current working-tree changes", '"baseline: HEAD and working tree"')
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_yaml_scalars_are_rejected(self):
        for value in ["'a'b'", "'unterminated", "# not a value", "- list item", "? map key", "`reserved"]:
            with self.subTest(value=value):
                self.assert_invalid(record().replace("HEAD and current working-tree changes", value), "scalar")

    def test_escaped_single_quotes_are_supported(self):
        content = record().replace("HEAD and current working-tree changes", "'the user''s requested diff'")
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_actual_records_cannot_be_put_in_the_public_example_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "docs/examples/records/2026-09-09/sample-change.md"
            path.parent.mkdir(parents=True)
            path.write_text(record(), encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("public example directory", result.stderr)

    def test_example_path_checks_follow_directory_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            actual = Path(directory) / "docs/ai-understanding/2026-09-09"
            actual.mkdir(parents=True)
            alias = Path(directory) / "2026-09-09"
            alias.symlink_to(actual, target_is_directory=True)
            path = alias / "sample-change.md"
            path.write_text(record().replace("record_kind: actual", "record_kind: example") + "\nFictional example.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("actual-record directory", result.stderr)

    def test_examples_require_a_visible_label_and_cannot_be_actual_records(self):
        content = record().replace("record_kind: actual", "record_kind: example")
        self.assert_invalid(content, "Fictional example")
        result = self.run_validator(content + "\nFictional example.\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "docs/ai-understanding/2026-09-09/sample-change.md"
            path.parent.mkdir(parents=True)
            path.write_text(content + "\nFictional example.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("actual-record directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
