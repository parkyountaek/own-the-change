import json
from pathlib import Path
import tempfile
import unittest
import shutil

from scripts import sync_marketplace as SYNC
import test_build_plugins


class SyncMarketplaceTests(unittest.TestCase):
    def source_snapshot(self, directory):
        source = test_build_plugins.BuildPluginsTests().copy_source_inputs(Path(directory)).resolve()
        shutil.copyfile(test_build_plugins.ROOT / SYNC.CODEX_TEMPLATE, source / SYNC.CODEX_TEMPLATE)
        return source

    def test_tracked_marketplace_matches_canonical_build(self):
        self.assertEqual(SYNC.sync_marketplace(check=True), 0)

    def test_generated_catalog_installs_only_the_complete_package(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.source_snapshot(directory)
            private = source / "docs/ai-understanding/private.md"
            private.parent.mkdir(parents=True)
            private.write_text("Private test sentinel", encoding="utf-8")
            (source / ".env").write_text("Private test sentinel", encoding="utf-8")
            SYNC.sync_marketplace(source)
            metadata = json.loads((source / SYNC.CATALOG).read_text())
            package = (source / metadata["plugins"][0]["source"]).resolve()
            self.assertEqual(package, source / SYNC.PACKAGE)
            self.assertTrue((package / ".claude-plugin/plugin.json").is_file())
            self.assertEqual({path.stem for path in (package / "commands").glob("*.md")},
                             {"own-plan-check", "own-change-debrief", "own-understanding-check",
                              "own-demo", "own-doctor"})
            self.assertTrue((package / "scripts/resolve_context.py").is_file())
            self.assertFalse((package / "docs/ai-understanding").exists())
            self.assertFalse((package / ".env").exists())
            codex_metadata = json.loads((source / SYNC.CODEX_CATALOG).read_text())
            codex_package = (source / codex_metadata["plugins"][0]["source"]["path"]).resolve()
            self.assertEqual(codex_package, source / SYNC.HOST_PACKAGES["codex"])
            self.assertTrue((codex_package / ".codex-plugin/plugin.json").is_file())
            self.assertFalse((codex_package / "commands").exists())
            self.assertFalse((codex_package / "hooks").exists())
            self.assertFalse((codex_package / "docs/ai-understanding").exists())
            self.assertFalse((codex_package / ".env").exists())
            self.assertEqual(SYNC.sync_marketplace(source), 0)

    def test_check_detects_stale_files_without_rewriting_them(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.source_snapshot(directory)
            SYNC.sync_marketplace(source)
            original = source / "adapters/claude-code/.claude-plugin/plugin.json"
            manifest = json.loads(original.read_text())
            manifest["description"] = "Updated plugin description"
            original.write_text(json.dumps(manifest), encoding="utf-8")
            installed = source / SYNC.PACKAGE / ".claude-plugin/plugin.json"
            before = installed.read_bytes()
            with self.assertRaisesRegex(ValueError, "out of date"):
                SYNC.sync_marketplace(source, check=True)
            self.assertEqual(installed.read_bytes(), before)
            self.assertEqual(SYNC.sync_marketplace(source), 1)
            self.assertEqual(installed.read_bytes(), original.read_bytes())
            self.assertEqual(SYNC.sync_marketplace(source, check=True), 0)

    def test_check_does_not_create_missing_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.source_snapshot(directory)
            with self.assertRaisesRegex(ValueError, "out of date"):
                SYNC.sync_marketplace(source, check=True)
            self.assertFalse((source / "plugins").exists())
            self.assertFalse((source / ".claude-plugin").exists())
            self.assertFalse((source / ".agents/plugins").exists())

    def test_unexpected_files_are_preserved_and_block_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.source_snapshot(directory)
            SYNC.sync_marketplace(source)
            extra = source / SYNC.PACKAGE / "private.md"
            extra.write_text("Keep this file", encoding="utf-8")
            for check in (True, False):
                with self.subTest(check=check), self.assertRaisesRegex(ValueError, "Unexpected"):
                    SYNC.sync_marketplace(source, check=check)
            self.assertEqual(extra.read_text(), "Keep this file")

    def test_links_cannot_redirect_distribution_writes(self):
        for relative in (Path("plugins"), SYNC.PACKAGE, SYNC.CATALOG,
                         Path(".agents"), SYNC.CODEX_CATALOG, SYNC.HOST_PACKAGES["codex"]):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as directory:
                source = self.source_snapshot(directory)
                external = Path(directory) / "external"
                external.mkdir()
                destination = source / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.symlink_to(external)
                with self.assertRaisesRegex(ValueError, "Unsafe|Unexpected"):
                    SYNC.sync_marketplace(source)
                self.assertEqual(list(external.iterdir()), [])
                self.assertTrue(destination.is_symlink())

    def test_codex_catalog_cannot_install_the_source_adapter(self):
        with tempfile.TemporaryDirectory() as directory:
            source = self.source_snapshot(directory)
            template = source / SYNC.CODEX_TEMPLATE
            metadata = json.loads(template.read_text())
            metadata["plugins"][0]["source"]["path"] = "./adapters/codex"
            template.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "generated local package"):
                SYNC.sync_marketplace(source)
            self.assertFalse((source / "plugins").exists())


if __name__ == "__main__":
    unittest.main()
