import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("read_protocol", ROOT / "scripts/read_protocol.py")
READER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READER)


class ReadProtocolTests(unittest.TestCase):
    def test_entry_bodies_stay_within_the_requested_character_budget(self):
        entries = [*ROOT.glob("skills/*/SKILL.md"), *ROOT.glob("adapters/claude-code/commands/*.md")]
        self.assertEqual(len(entries), 11)
        for entry in entries:
            with self.subTest(entry=str(entry.relative_to(ROOT))):
                body = entry.read_text().split("---", 2)[2].strip()
                self.assertGreater(len(body), 0)
                self.assertLessEqual(len(body), 250)

    def test_modes_select_complete_verbatim_sections_from_one_source(self):
        document = READER.PROTOCOL.read_text()
        for mode, titles in READER.MODES.items():
            with self.subTest(mode=mode):
                selected = READER.select_sections(document, mode)
                self.assertLess(len(selected), len(document))
                for section in document.split("\n## ")[1:]:
                    title = section.splitlines()[0]
                    self.assertEqual("## " + section in selected, title in titles)
        self.assertEqual(READER.select_sections(document, "all"), document)

    def test_section_drift_fails_closed_instead_of_losing_rules(self):
        document = READER.PROTOCOL.read_text()
        for changed in (document + "\n## New rule\nDo something.\n",
                        document.replace("## Status\n", "## Renamed status\n"),
                        document + "\n## Status\nDuplicate.\n"):
            with self.assertRaises(ValueError):
                READER.select_sections(changed, "debrief")

    def test_debrief_does_not_load_question_and_record_schema_text(self):
        document = READER.PROTOCOL.read_text()
        selected = READER.select_sections(document, "debrief")
        for title in ("Understanding Check", "Record contract", "Before work: Plan Check"):
            self.assertNotIn("\n## " + title + "\n", selected)
        for title in ("Status", "Record choice", "Privacy and safety", "Evidence collection"):
            self.assertIn("\n## " + title + "\n", selected)

    def test_cli_returns_the_same_selection(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/read_protocol.py"), "--mode", "understanding"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, READER.select_sections(READER.PROTOCOL.read_text(), "understanding"))


if __name__ == "__main__":
    unittest.main()
