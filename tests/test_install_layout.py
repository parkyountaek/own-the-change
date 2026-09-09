import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install-local.sh"
SKILL = ROOT / "skills" / "own-the-change" / "SKILL.md"
PROJECT_LINK = ROOT / ".agents" / "skills" / "own-the-change"


class InstallLayoutTests(unittest.TestCase):
    def test_project_scope_uses_the_tracked_canonical_skill(self):
        before = PROJECT_LINK.resolve()
        result = subprocess.run(
            [str(INSTALL), "codex-project"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(PROJECT_LINK.resolve(), SKILL.parent.resolve())
        self.assertEqual(before, SKILL.parent.resolve())
        self.assertIn("already available", result.stdout)

    def test_root_entry_points_and_discovery_links_exist(self):
        self.assertTrue((ROOT / ".claude-plugin" / "plugin.json").is_file())
        self.assertTrue((ROOT / ".claude-plugin" / "marketplace.json").is_file())
        self.assertTrue((ROOT / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue((ROOT / "commands" / "own-plan-check.md").is_file())
        self.assertTrue((ROOT / "hooks" / "hooks.json").is_file())
        self.assertTrue((ROOT / ".cursor" / "skills" / "own-the-change").is_symlink())
        self.assertEqual((ROOT / ".cursor" / "skills" / "own-the-change").resolve(), SKILL.parent.resolve())

    def test_shared_skill_has_no_claude_specific_path(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("$CLAUDE_PLUGIN_ROOT", content)
        self.assertIn("docs/protocol/understanding-protocol.md", content)

    def test_claude_project_command_uses_repository_root(self):
        result = subprocess.run(
            [str(INSTALL), "claude-project"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("claude --plugin-dir " + str(ROOT), result.stdout)
        self.assertNotIn("adapters/claude-code", result.stdout)


if __name__ == "__main__":
    unittest.main()
