import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

from test_validate_record import record

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_plugins", ROOT / "scripts/build_plugins.py")
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class BuildPluginsTests(unittest.TestCase):
    def copy_source_inputs(self, workspace):
        source = workspace / "source"
        inputs = [*BUILD.SHARED_FILES, BUILD.MARKETPLACE_TEMPLATE]
        for host, paths in BUILD.HOST_FILES.items():
            inputs.extend(f"adapters/{host}/{path}" for path in paths)
        for relative in inputs:
            destination = source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        return source

    @unittest.skipUnless(os.name == "posix", "POSIX distribution permissions")
    def test_package_modes_are_portable_without_changing_source_or_parent(self):
        with tempfile.TemporaryDirectory(prefix="own-change-modes-") as directory:
            workspace = Path(directory)
            source = self.copy_source_inputs(workspace)
            source_modes = {}
            for path in source.rglob("*"):
                if path.is_file():
                    mode = 0o700 if path.suffix in {".py", ".sh"} else 0o600
                    # An incidental source execute bit must not make data executable.
                    if path.name == "LICENSE":
                        mode = 0o777
                    path.chmod(mode)
                    source_modes[path] = mode
            parent = workspace / "private-parent"
            parent.mkdir(mode=0o700)
            output = parent / "build"
            previous_umask = os.umask(0o077)
            try:
                BUILD.build_plugins(output, source=source)
            finally:
                os.umask(previous_umask)

            executables = {"hooks/suggest-debrief.sh", "scripts/resolve_context.py", "scripts/validate_record.py"}
            for path in [output, *output.rglob("*")]:
                with self.subTest(path=str(path.relative_to(output))):
                    executable = any(path == output / host / "own-the-change" / name
                                     for host in BUILD.HOST_FILES for name in executables)
                    expected = 0o755 if path.is_dir() or executable else 0o644
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), expected)
            self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o700)
            for path, original_mode in source_modes.items():
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), original_mode)

    def test_host_manifests_link_to_the_public_project(self):
        for host, paths in BUILD.HOST_FILES.items():
            with self.subTest(host=host):
                manifest = json.loads((ROOT / "adapters" / host / paths[0]).read_text())
                self.assertEqual(manifest["homepage"], "https://github.com/parkyountaek/own-the-change")
                self.assertEqual(manifest["repository"], "https://github.com/parkyountaek/own-the-change")

    def test_packages_work_after_their_source_snapshot_is_removed(self):
        with tempfile.TemporaryDirectory(prefix="own-change-package-") as directory:
            workspace = Path(directory).resolve()
            source = self.copy_source_inputs(workspace)
            private = source / "docs/ai-understanding/private.md"
            private.parent.mkdir(parents=True)
            private.write_text("Private test sentinel", encoding="utf-8")
            (source / ".env").write_text("Private test sentinel", encoding="utf-8")
            host_config = source / ".claude"
            host_config.mkdir()
            for name in [".credentials.json", "settings.json", "session.jsonl"]:
                (host_config / name).write_text("Private host test sentinel", encoding="utf-8")

            packages = BUILD.build_plugins(workspace / "build", source=source)
            marketplace_root = workspace / "build/claude-code"
            marketplace = json.loads((marketplace_root / ".claude-plugin/marketplace.json").read_text())
            self.assertEqual(marketplace["name"], "own-the-change")
            self.assertEqual(len(marketplace["plugins"]), 1)
            entry = marketplace["plugins"][0]
            self.assertEqual((marketplace_root / entry["source"]).resolve(), Path(packages["claude-code"]))
            expected_protocol = (source / "docs/protocol/understanding-protocol.md").read_bytes()
            source.rename(workspace / "source-unavailable")
            target = workspace / "target project"
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(target)], check=True, capture_output=True)
            nested = target / "src/nested"
            nested.mkdir(parents=True)

            for host, package_path in packages.items():
                with self.subTest(host=host):
                    package = Path(package_path)
                    self.assertEqual(package.name, "own-the-change")
                    self.assertFalse(any(path.is_symlink() for path in package.rglob("*")))
                    self.assertFalse((package / ".env").exists())
                    self.assertFalse((package / "docs/ai-understanding").exists())
                    self.assertFalse((package / ".git").exists())
                    self.assertFalse((package / ".claude").exists())
                    self.assertTrue((package / "SECURITY.md").is_file())
                    self.assertEqual((package / "docs/protocol/understanding-protocol.md").read_bytes(), expected_protocol)
                    result = subprocess.run(
                        [sys.executable, str(package / "scripts/resolve_context.py"), "--target", str(nested)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    context = json.loads(result.stdout)
                    self.assertEqual(Path(context["source_root"]), package)
                    self.assertEqual(Path(context["target_root"]), target)
                    for key in ["protocol", "template", "validator"]:
                        self.assertTrue(Path(context[key]).is_relative_to(package))
                        self.assertTrue(Path(context[key]).is_file())
                    destination = Path(context["record_root"]) / "2026-09-09/sample-change.md"
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(record(), encoding="utf-8")
                    validation = subprocess.run([sys.executable, context["validator"], str(destination)],
                                                cwd=nested, capture_output=True, text=True, check=False)
                    self.assertEqual(validation.returncode, 0, validation.stderr)
                    if host == "claude-code":
                        hook = subprocess.run([str(package / "hooks/suggest-debrief.sh")], input="{}",
                                              capture_output=True, text=True, check=False)
                        self.assertEqual(hook.returncode, 0, hook.stderr)
                        self.assertIn("systemMessage", json.loads(hook.stdout))
                        for command in (package / "commands").glob("*.md"):
                            self.assertNotIn("$CLAUDE_PLUGIN_ROOT", command.read_text())
                            self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/resolve_context.py", command.read_text())

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory(prefix="own-change-output-") as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("Keep this file", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Output already exists"):
                BUILD.build_plugins(output)
            self.assertEqual(sentinel.read_text(), "Keep this file")

    def test_broken_output_link_is_preserved(self):
        with tempfile.TemporaryDirectory(prefix="own-change-output-link-") as directory:
            output = Path(directory) / "link"
            output.symlink_to(Path(directory) / "missing")
            with self.assertRaisesRegex(ValueError, "Output already exists"):
                BUILD.build_plugins(output)
            self.assertTrue(output.is_symlink())

    def test_missing_source_input_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory(prefix="own-change-incomplete-") as directory:
            output = Path(directory) / "output"
            with self.assertRaisesRegex(ValueError, "Missing or external package input"):
                BUILD.build_plugins(output, source=Path(directory) / "missing-source")
            self.assertFalse(output.exists())

    def test_external_source_link_is_rejected_before_building(self):
        with tempfile.TemporaryDirectory(prefix="own-change-external-input-") as directory:
            source = Path(directory) / "source"
            source.mkdir()
            external = Path(directory) / "external.txt"
            external.write_text("External test sentinel", encoding="utf-8")
            (source / "LICENSE").symlink_to(external)
            output = Path(directory) / "output"
            with self.assertRaisesRegex(ValueError, "external package input: LICENSE"):
                BUILD.build_plugins(output, source=source)
            self.assertFalse(output.exists())

    def test_mismatched_host_versions_fail_before_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source = self.copy_source_inputs(workspace)
            manifest_path = source / "adapters/codex/.codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["version"] = "99.0.0"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "same version"):
                BUILD.build_plugins(workspace / "output", source=source)
            self.assertFalse((workspace / "output").exists())

    def test_marketplace_cannot_reference_the_incomplete_source_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source = self.copy_source_inputs(workspace)
            template = source / BUILD.MARKETPLACE_TEMPLATE
            marketplace = json.loads(template.read_text())
            marketplace["plugins"][0]["source"] = "./"
            template.write_text(json.dumps(marketplace), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "generated local package"):
                BUILD.build_plugins(workspace / "output", source=source)
            self.assertFalse((workspace / "output").exists())


if __name__ == "__main__":
    unittest.main()
