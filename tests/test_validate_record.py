import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_record.py"


def record(*, date="2026-09-09", status="not_confirmed", include_tests=True):
    tests = "## Test Evidence\n- `python3 -m unittest` was run.\n" if include_tests else ""
    return f"""---
task_id: sample-change
date: {date}
understanding_status: {status}
risk_level: low
follow_up_at: none
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
- No response.

## Understanding Status
- not_confirmed: there is no user response.

## Remaining Risks
- The production environment was not checked.

## Next Check
- Explain it again if needed.
"""


class ValidateRecordTests(unittest.TestCase):
    def run_validator(self, content, filename="sample-change.md"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "2026-09-09" / filename
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
        result = self.run_validator(record(date="09-09-2026"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("date", result.stderr)


if __name__ == "__main__":
    unittest.main()
