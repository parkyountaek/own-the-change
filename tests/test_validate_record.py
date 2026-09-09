import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_record.py"


def record(*, date="2026-09-09", status="not_confirmed", include_tests=True):
    tests = "## 테스트 근거\n- `python3 -m unittest`를 실행했다.\n" if include_tests else ""
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

# 이해 기록: sample-change

## 작업 목표
- 작은 변경을 이해한다.

## 변경 파일
- `src/example.py`

{tests}
## 핵심 설명
- 입력을 받아 결과를 돌려준다.

## 사용자 답변
- 답변하지 않음.

## 이해 상태
- not_confirmed: 사용자의 답변이 없다.

## 남은 위험
- 실제 운영 환경은 확인하지 않았다.

## 다음 확인 항목
- 필요하면 다시 설명한다.
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
        self.assertIn("테스트 근거", result.stderr)

    def test_rejects_invalid_or_mismatched_date(self):
        result = self.run_validator(record(date="09-09-2026"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("date", result.stderr)


if __name__ == "__main__":
    unittest.main()
