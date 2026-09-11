#!/usr/bin/env python3
"""Build self-contained local plugins from the canonical source files."""

import argparse
import json
from pathlib import Path
import shutil
import sys

SOURCE_ROOT = Path(__file__).resolve().parents[1]
SHARED_FILES = (
    "LICENSE",
    "SECURITY.md",
    "skills/own-the-change/SKILL.md",
    "skills/own-the-change/agents/openai.yaml",
    "docs/protocol/understanding-protocol.md",
    "docs/protocol/status-definitions.md",
    "docs/protocol/output-schema.md",
    "docs/research/learning-principles.md",
    "templates/understanding-record.md",
    "scripts/resolve_context.py",
    "scripts/validate_record.py",
    "scripts/prepare_demo.py",
    "scripts/doctor.py",
    "scripts/prepare_question.py",
    "scripts/read_protocol.py",
)
ASSET_FILES = {
    f"tests/fixtures/host-smoke/{name}": f"assets/demo/{name}"
    for name in ("before/display_name.py", "after/display_name.py", "after/test_display_name.py")
}
CODEX_FILES = tuple(
    f"skills/{name}/{relative}"
    for name in ("own-change-debrief", "own-plan-check", "own-understanding-check", "own-demo", "own-doctor")
    for relative in ("SKILL.md", "agents/openai.yaml")
)
MARKETPLACE_TEMPLATE = "templates/claude-marketplace.json"
HOST_FILES = {
    "claude-code": (
        ".claude-plugin/plugin.json",
        "commands/own-plan-check.md",
        "commands/own-change-debrief.md",
        "commands/own-understanding-check.md",
        "commands/own-demo.md",
        "commands/own-doctor.md",
        "hooks/hooks.json",
        "hooks/suggest-debrief.sh",
    ),
    "codex": (".codex-plugin/plugin.json",),
}
EXECUTABLE_FILES = frozenset({
    "hooks/suggest-debrief.sh",
    "scripts/resolve_context.py",
    "scripts/validate_record.py",
})


def copy_package_file(original, destination, executable=False):
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Copy content only: source permissions and extended metadata are not releases.
    shutil.copyfile(original, destination, follow_symlinks=True)
    destination.chmod(0o755 if executable else 0o644)


def build_plugins(output, source=SOURCE_ROOT):
    source = Path(source).resolve()
    output = Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Output already exists; choose a new --output directory")

    # An explicit file list excludes private records, Git data, and incidental files.
    plans = {}
    versions = set()
    for host, files in HOST_FILES.items():
        adapter = source / "adapters" / host
        plans[host] = [(source / path, path) for path in SHARED_FILES]
        plans[host] += [(source / original, destination) for original, destination in ASSET_FILES.items()]
        if host == "codex":
            plans[host] += [(source / path, path) for path in CODEX_FILES]
        plans[host] += [(adapter / path, path) for path in files]
        for original, relative in plans[host]:
            if not original.is_file() or not original.resolve().is_relative_to(source):
                raise ValueError(f"Missing or external package input: {relative}")
        manifest = json.loads((adapter / files[0]).read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or manifest.get("name") != "own-the-change":
            raise ValueError(f"Unexpected {host} plugin name")
        version = manifest.get("version")
        if not isinstance(version, str) or not version:
            raise ValueError(f"Missing {host} plugin version")
        versions.add(version)
    if len(versions) != 1 or None in versions:
        raise ValueError("Host manifests must have the same version")

    marketplace_path = source / MARKETPLACE_TEMPLATE
    if not marketplace_path.is_file() or not marketplace_path.resolve().is_relative_to(source):
        raise ValueError("Missing or external Claude marketplace template")
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    if not isinstance(marketplace, dict) or marketplace.get("name") != "own-the-change":
        raise ValueError("Unexpected Claude marketplace name")
    entries = marketplace.get("plugins")
    if (not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict)
            or entries[0].get("name") != "own-the-change" or entries[0].get("source") != "./own-the-change"):
        raise ValueError("Claude marketplace must reference the generated local package")

    output.mkdir(parents=True, exist_ok=False)
    packages = {}
    for host, files in plans.items():
        package = output / host / "own-the-change"
        for original, relative in files:
            destination = package / relative
            copy_package_file(original, destination, relative in EXECUTABLE_FILES)
        packages[host] = str(package)
    destination = output / "claude-code/.claude-plugin/marketplace.json"
    copy_package_file(marketplace_path, destination)
    # Normalize only this new output, never the source or existing parent folders.
    for directory in output.rglob("*"):
        if directory.is_dir():
            directory.chmod(0o755)
    output.chmod(0o755)
    return packages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SOURCE_ROOT / "dist")
    args = parser.parse_args()
    try:
        print(json.dumps(build_plugins(args.output), indent=2))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
