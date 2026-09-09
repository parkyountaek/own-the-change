from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryContentTests(unittest.TestCase):
    def maintained_files(self):
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT, check=True, capture_output=True,
        )
        for name in set(result.stdout.decode().split("\0")) - {""}:
            path = ROOT / name
            if path.is_file() and not path.is_symlink() and not name.startswith(("docs/ai-understanding/", "dist/")):
                yield path

    def test_maintained_text_keeps_localization_data_escaped(self):
        # This script guard catches accidental CJK prose, not every non-English word.
        # It deliberately excludes ignored local records and generated packages.
        cjk = re.compile(r"[\u1100-\u11ff\u3000-\u30ff\u3130-\u318f\u3400-\u9fff\uac00-\ud7af]")
        for path in self.maintained_files():
            if path.suffix not in {".md", ".py", ".sh", ".json", ".yml", ".yaml"}:
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(cjk.search(path.read_text(encoding="utf-8")),
                                  "Keep maintained prose in English and localization fixtures Unicode-escaped")

    def test_local_markdown_links_point_to_existing_files(self):
        for path in self.maintained_files():
            if path.suffix != ".md":
                continue
            for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                with self.subTest(path=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue((path.parent / relative).exists())

    def test_synthetic_after_fixture_passes_its_four_tests(self):
        fixture = ROOT / "tests/fixtures/host-smoke/after"
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_display_name.py", "-v"],
            cwd=fixture, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 4 tests", result.stderr)


if __name__ == "__main__":
    unittest.main()
