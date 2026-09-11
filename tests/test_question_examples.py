"""Check example answer evidence, not the quality of arbitrary generated prose."""

import ast
from pathlib import Path
import re
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/examples/multiple-choice-check.md"
RECORDS = ROOT / "docs/examples/records/2026-09-11"
FIXTURE = ROOT / "tests/fixtures/host-smoke"


def options(document):
    # Parse numbered example data; do not assert exact question or feedback wording.
    entries = re.findall(r"^(?:> |  )([1-5])\. (.+)$", document, re.MULTILINE)
    if len(entries) % 5:
        raise ValueError("An example choice group is incomplete")
    groups = [entries[index:index + 5] for index in range(0, len(entries), 5)]
    if any([number for number, _ in group] != list("12345") for group in groups):
        raise ValueError("Example choices must be ordered from 1 to 5")
    return [[text for _, text in group] for group in groups]


class QuestionExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = staticmethod(runpy.run_path(str(FIXTURE / "before/display_name.py"))["display_name"])
        cls.after = staticmethod(runpy.run_path(str(FIXTURE / "after/display_name.py"))["display_name"])
        cls.guide = GUIDE.read_text()
        cls.groups = options(cls.guide)

    def test_reason_options_isolate_one_case_that_needs_the_change(self):
        self.assertEqual(len(self.groups), 2)
        requires_change = []
        for position, choice in enumerate(self.groups[0][:4], 1):
            literals = re.findall(r"`([^`]+)`", choice)
            self.assertEqual(len(literals), 2)
            value, expected = map(ast.literal_eval, literals)
            self.assertIsInstance(value, str)
            self.assertIsInstance(expected, str)
            self.assertEqual(self.after(value), expected)
            if self.before(value) != expected:
                requires_change.append(position)
        self.assertEqual(requires_change, [2])

    def test_prediction_options_distinguish_three_near_miss_behaviors(self):
        inputs = re.findall(r"`display_name\(([^`]+)\)`", self.guide)
        self.assertEqual(len(inputs), 1)
        value = ast.literal_eval(inputs[0])
        outputs = [ast.literal_eval(re.findall(r"`([^`]+)`", choice)[0])
                   for choice in self.groups[1][:4]]
        self.assertEqual(len(set(outputs)), 4)
        self.assertEqual(outputs, [self.after(value), re.sub(r"\s+", " ", value), value.strip(" "), value])
        self.assertEqual([index for index, output in enumerate(outputs, 1) if output == self.after(value)], [1])

    def test_complete_unsure_and_stopped_records_preserve_the_example_mapping(self):
        for name, count in (("whitespace-choice", 2), ("whitespace-unsure", 2), ("whitespace-stopped", 1)):
            with self.subTest(record=name):
                document = (RECORDS / f"{name}.md").read_text()
                self.assertEqual(options(document), self.groups[:count])
                self.assertEqual(re.findall(r"Expected answer: ([1-4])\.", document), list("21")[:count])


if __name__ == "__main__":
    unittest.main()
