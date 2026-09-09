import subprocess
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install-local.sh"
SKILL = ROOT / "skills" / "own-the-change" / "SKILL.md"
PROJECT_LINK = ROOT / ".agents" / "skills" / "own-the-change"
CLAUDE_ADAPTER = ROOT / "adapters" / "claude-code"
CODEX_ADAPTER = ROOT / "adapters" / "codex"


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

    def test_adapter_entry_points_and_discovery_links_exist(self):
        self.assertTrue((CLAUDE_ADAPTER / ".claude-plugin" / "plugin.json").is_file())
        self.assertFalse((CLAUDE_ADAPTER / ".claude-plugin" / "marketplace.json").exists())
        self.assertTrue((ROOT / "templates/claude-marketplace.json").is_file())
        self.assertTrue((CODEX_ADAPTER / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue((CLAUDE_ADAPTER / "commands" / "own-plan-check.md").is_file())
        self.assertTrue((CLAUDE_ADAPTER / "hooks" / "hooks.json").is_file())
        self.assertTrue((ROOT / ".cursor" / "skills" / "own-the-change").is_symlink())
        self.assertEqual((ROOT / ".cursor" / "skills" / "own-the-change").resolve(), SKILL.parent.resolve())

    def test_discovery_aliases_resolve_to_complete_shared_resources(self):
        for entry in [PROJECT_LINK, ROOT / ".cursor/skills/own-the-change",
                      CLAUDE_ADAPTER / "skills/own-the-change", CODEX_ADAPTER / "skills/own-the-change"]:
            with self.subTest(entry=entry):
                source = (entry / "SKILL.md").resolve().parents[2]
                self.assertEqual(source, ROOT)
                for resource in ["docs/protocol/understanding-protocol.md", "templates/understanding-record.md", "scripts/validate_record.py"]:
                    self.assertTrue((source / resource).is_file())

    def test_claude_commands_have_discoverable_descriptions(self):
        for command in (CLAUDE_ADAPTER / "commands").glob("*.md"):
            with self.subTest(command=command.name):
                self.assertRegex(command.read_text(encoding="utf-8"), r"\A---\ndescription: [^\n]+\n---\n")

    def test_claude_project_hint_uses_the_launcher_without_a_reused_build_path(self):
        result = subprocess.run(
            [str(INSTALL), "claude-project"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('python3 "' + str(ROOT / "scripts/launch_claude.py") + '"', result.stdout)
        self.assertNotIn(str(ROOT / "dist"), result.stdout)

    def run_user_install(self, mode, directory):
        return subprocess.run([str(INSTALL), mode, "--skills-dir", str(directory)],
                              capture_output=True, text=True, check=False)

    def test_user_install_is_idempotent_and_removes_only_its_link(self):
        with tempfile.TemporaryDirectory(prefix="own-change-install-") as directory:
            skills = Path(directory) / "skills with spaces"
            for _ in range(2):
                result = self.run_user_install("codex-user", skills)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((skills / "own-the-change").resolve(), SKILL.parent)
            for _ in range(2):
                result = self.run_user_install("remove-codex-user", skills)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse((skills / "own-the-change").is_symlink())
            self.assertTrue(SKILL.is_file())

    def test_install_and_remove_preserve_foreign_destinations(self):
        for kind in ["file", "directory", "foreign_link", "broken_link"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(prefix="own-change-collision-") as directory:
                skills = Path(directory) / "skills"
                skills.mkdir()
                destination = skills / "own-the-change"
                foreign = Path(directory) / "foreign"
                if kind == "file":
                    destination.write_text("user content", encoding="utf-8")
                elif kind == "directory":
                    destination.mkdir()
                    (destination / "keep.txt").write_text("user content", encoding="utf-8")
                else:
                    if kind == "foreign_link":
                        foreign.mkdir()
                    destination.symlink_to(foreign)
                for mode in ["codex-user", "remove-codex-user"]:
                    result = self.run_user_install(mode, skills)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("not owned", result.stderr)
                if kind == "file":
                    self.assertEqual(destination.read_text(), "user content")
                elif kind == "directory":
                    self.assertEqual(list(destination.iterdir()), [destination / "keep.txt"])
                else:
                    self.assertTrue(destination.is_symlink())
                    self.assertEqual(destination.readlink(), foreign)

    def test_invalid_install_arguments_do_not_create_a_destination(self):
        result = self.run_user_install("codex-user", Path("relative-path"))
        self.assertEqual(result.returncode, 2)

    def test_stop_hook_emits_a_visible_nonblocking_message_and_valid_commands(self):
        hook = CLAUDE_ADAPTER / "hooks/suggest-debrief.sh"
        result = subprocess.run([str(hook)], input="{}", capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"systemMessage"})
        plugin = json.loads((CLAUDE_ADAPTER / ".claude-plugin/plugin.json").read_text())["name"]
        for command in ["own-change-debrief", "own-understanding-check"]:
            self.assertIn(f"/{plugin}:{command}", payload["systemMessage"])
            self.assertTrue((CLAUDE_ADAPTER / "commands" / (command + ".md")).is_file())


if __name__ == "__main__":
    unittest.main()
