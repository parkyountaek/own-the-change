#!/usr/bin/env python3
"""Refresh or check tracked Claude and Codex marketplaces from canonical inputs."""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

try:
    from .build_plugins import SOURCE_ROOT, build_plugins, copy_package_file
except ImportError:
    from build_plugins import SOURCE_ROOT, build_plugins, copy_package_file

CATALOG = Path(".claude-plugin/marketplace.json")
PACKAGE = Path("plugins/claude-code/own-the-change")
CODEX_CATALOG = Path(".agents/plugins/marketplace.json")
CODEX_TEMPLATE = Path("templates/codex-marketplace.json")
HOST_PACKAGES = {"claude-code": PACKAGE, "codex": Path("plugins/own-the-change")}


def sync_marketplace(source=SOURCE_ROOT, *, check=False):
    source = Path(source).resolve()
    with tempfile.TemporaryDirectory(prefix="own-change-marketplace-") as directory:
        build = Path(directory) / "build"
        packages = build_plugins(build, source=source)
        catalog = build / "claude-code/.claude-plugin/marketplace.json"
        metadata = json.loads(catalog.read_text(encoding="utf-8"))
        metadata["plugins"][0]["source"] = f"./{PACKAGE.as_posix()}"
        catalog.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        expected = {CATALOG: catalog}
        codex_catalog = source / CODEX_TEMPLATE
        if not codex_catalog.is_file() or not codex_catalog.resolve().is_relative_to(source):
            raise ValueError("Missing or external Codex marketplace template")
        codex_metadata = json.loads(codex_catalog.read_text(encoding="utf-8"))
        if (not isinstance(codex_metadata, dict) or codex_metadata.get("name") != "own-the-change"
                or codex_metadata.get("plugins") != [{
                    "name": "own-the-change",
                    "source": {"source": "local", "path": "./plugins/own-the-change"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Productivity",
                }]):
            raise ValueError("Codex marketplace must reference the generated local package with default policies")
        expected[CODEX_CATALOG] = codex_catalog
        for host, destination in HOST_PACKAGES.items():
            package = Path(packages[host])
            expected.update({destination / path.relative_to(package): path
                             for path in package.rglob("*") if path.is_file()})
        directories = {parent for path in expected for parent in path.parents
                       if parent != Path(".")}

        # Reject unexpected files and links before updating any generated content.
        # Removed build inputs need an explicit, reviewed deletion by the maintainer.
        for relative in sorted(directories):
            path = source / relative
            if path.is_symlink() or (path.exists() and not path.is_dir()):
                raise ValueError(f"Unsafe marketplace directory: {relative}")
        for root in (CATALOG.parent, CODEX_CATALOG.parent, *HOST_PACKAGES.values()):
            for path in (source / root).rglob("*"):
                relative = path.relative_to(source)
                if path.is_symlink() or relative not in expected.keys() | directories:
                    raise ValueError(f"Unexpected marketplace path: {relative}")
                if relative in expected and not path.is_file():
                    raise ValueError(f"Expected a marketplace file: {relative}")

        stale = []
        for relative, original in expected.items():
            destination = source / relative
            executable = bool(original.stat().st_mode & 0o111)
            if (not destination.is_file() or destination.read_bytes() != original.read_bytes()
                    or (os.name == "posix"
                        and bool(destination.stat().st_mode & 0o111) != executable)):
                stale.append(relative)
        if check and stale:
            names = ", ".join(str(path) for path in sorted(stale))
            raise ValueError(f"Marketplace is out of date: {names}. Run python3 scripts/sync_marketplace.py")
        if not check:
            for relative in stale:
                original = expected[relative]
                copy_package_file(original, source / relative, bool(original.stat().st_mode & 0o111))
        return len(stale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on stale files without changing them")
    args = parser.parse_args()
    try:
        count = sync_marketplace(check=args.check)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Marketplace is current" if args.check else f"Updated {count} marketplace files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
