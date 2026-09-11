import unittest

import test_validate_record as fixtures


class RuntimeLanguageTests(unittest.TestCase):
    def test_localized_choice_response_preserves_selection_mode(self):
        answer = "2\ubc88"
        content = fixtures.record(response_status="answered", response=answer, response_mode="multiple_choice")
        result = fixtures.ValidateRecordTests().run_validator(content)
        self.assertEqual(result.returncode, 0, result.stderr)
        invalid = content.replace("not_confirmed", "confirmed")
        result = fixtures.ValidateRecordTests().run_validator(invalid)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not multiple_choice alone", result.stderr)

    def test_localized_prose_and_original_answer_are_accepted(self):
        # Unicode escapes keep the maintained fixture English while exercising Korean text.
        answer = "\uc774 \ubcc0\uacbd\uc740 \uc624\ub958\ub97c \ub9c9\uace0 \uc785\ub825\uc5d0 \uc601\ud5a5\uc744 \uc90d\ub2c8\ub2e4."
        content = fixtures.record(status="confirmed", response_status="answered", response=answer)
        content = content.replace("- Understand a small change.", "- " + answer)
        result = fixtures.ValidateRecordTests().run_validator(content)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_localized_follow_up_reason_with_stable_no_answer_marker(self):
        reason = "\ubcc0\uacbd \uc774\uc720\uc640 \uc704\ud5d8 \ubcf5\uc2b5"
        content = fixtures.record(risk="high", dates=["2026-09-10", "2026-09-16"], reason=reason)
        result = fixtures.ValidateRecordTests().run_validator(content)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
