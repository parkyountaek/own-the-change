import importlib.util
import json
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLAUDE = ROOT / "adapters/claude-code"
CODEX_MANIFEST = ROOT / "adapters/codex/.codex-plugin/plugin.json"
MODULES = {}
for name in ("read_protocol", "build_plugins"):
    SPEC = importlib.util.spec_from_file_location(name, ROOT / f"scripts/{name}.py")
    MODULES[name] = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(MODULES[name])
READER, BUILD = MODULES["read_protocol"], MODULES["build_plugins"]
# Each named checkpoint is a Claude command and a Codex skill with the same name.
NAMED = {
    "own-plan-check": "plan",
    "own-change-debrief": "debrief",
    "own-understanding-check": "understanding",
    "own-demo": "demo",
    "own-doctor": "doctor",
}


def split_entry(path):
    _, front_matter, body = path.read_text(encoding="utf-8").split("---", 2)
    return front_matter, body


def reader_modes(body):
    return re.findall(r'read_protocol\.py"? --mode ([a-z]+)', body)


class HostParityTests(unittest.TestCase):
    def test_each_named_checkpoint_reads_the_same_mode_on_both_hosts(self):
        self.assertEqual({path.stem for path in (CLAUDE / "commands").glob("*.md")}, set(NAMED))
        for name, mode in NAMED.items():
            with self.subTest(name=name):
                self.assertIn(mode, READER.MODES)
                self.assertEqual(reader_modes(split_entry(CLAUDE / "commands" / f"{name}.md")[1]), [mode])
                self.assertEqual(reader_modes(split_entry(ROOT / "skills" / name / "SKILL.md")[1]), [mode])

    def test_shared_entry_offers_every_checkpoint_mode(self):
        body = split_entry(ROOT / "skills/own-the-change/SKILL.md")[1]
        listed = re.search(r"\(default ([a-z]+), or ([a-z/]+)\)", body)
        self.assertIsNotNone(listed)
        offered = {listed.group(1), *listed.group(2).split("/")}
        self.assertLessEqual(offered, set(READER.MODES))
        self.assertLessEqual({*NAMED.values(), "review"}, offered)

    def test_only_the_shared_skill_starts_without_an_explicit_request(self):
        # Named entries are explicit shortcuts on both hosts; implicit requests use
        # the shared skill, whose description is identical in both packages.
        for name in NAMED:
            with self.subTest(name=name):
                self.assertIn("\ndisable-model-invocation: true\n", split_entry(CLAUDE / "commands" / f"{name}.md")[0])
                metadata = (ROOT / "skills" / name / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertIn("\npolicy:\n  allow_implicit_invocation: false\n", metadata)
        shared = ROOT / "skills/own-the-change"
        self.assertNotIn("disable-model-invocation", split_entry(shared / "SKILL.md")[0])
        self.assertNotIn("allow_implicit_invocation", (shared / "agents/openai.yaml").read_text(encoding="utf-8"))

    def test_codex_metadata_points_at_existing_skills(self):
        manifest = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["skills"], "./skills/")
        for prompt in manifest["interface"]["defaultPrompt"]:
            with self.subTest(prompt=prompt):
                self.assertTrue((ROOT / "skills" / prompt.removeprefix("$own-the-change:") / "SKILL.md").is_file())
        for skill in (path for path in (ROOT / "skills").iterdir() if path.is_dir()):
            with self.subTest(skill=skill.name):
                self.assertIn(f"\nname: {skill.name}\n", split_entry(skill / "SKILL.md")[0])
                mention = "$own-the-change" + ("" if skill.name == "own-the-change" else f":{skill.name}")
                metadata = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertIn(f'default_prompt: "Use {mention} ', metadata)

    def test_stop_hook_registration_runs_the_packaged_script(self):
        hooks = json.loads((CLAUDE / "hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]
        self.assertEqual(set(hooks), {"Stop"})
        handlers = [hook for group in hooks["Stop"] for hook in group["hooks"]]
        self.assertEqual(handlers, [{"type": "command", "command": '"$CLAUDE_PLUGIN_ROOT"/hooks/suggest-debrief.sh'}])
        self.assertTrue(os.access(CLAUDE / "hooks/suggest-debrief.sh", os.X_OK))
        self.assertLessEqual({"hooks/hooks.json", "hooks/suggest-debrief.sh"}, set(BUILD.HOST_FILES["claude-code"]))
        self.assertIn("hooks/suggest-debrief.sh", BUILD.EXECUTABLE_FILES)


if __name__ == "__main__":
    unittest.main()
