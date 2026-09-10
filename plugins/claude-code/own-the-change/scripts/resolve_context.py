#!/usr/bin/env python3
"""Resolve local plugin resources and the target Git root without writing files."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def resolve_context(target, record=None):
    source = Path(__file__).resolve().parents[1]
    resources = {
        "protocol": source / "docs/protocol/understanding-protocol.md",
        "template": source / "templates/understanding-record.md",
        "validator": source / "scripts/validate_record.py",
    }
    for name, path in resources.items():
        if not path.is_file():
            raise ValueError(f"Missing {name}; use a complete Own The Change checkout or built package")
    result = subprocess.run(
        ["git", "-C", str(Path(target).resolve()), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError("Target must be a directory inside a Git working tree")
    root = Path(result.stdout.strip()).resolve()
    record_root = root / "docs/ai-understanding"
    if not record_root.resolve().is_relative_to(root):
        raise ValueError("Record directory resolves outside the target repository; inspect its symbolic links")
    for directory in [root / "docs", record_root]:
        if directory.exists() and not directory.is_dir():
            raise ValueError(f"Record path component is not a directory: {directory}")
    context = {
        "source_root": str(source),
        "target_root": str(root),
        **{name: str(path) for name, path in resources.items()},
        "record_root": str(record_root),
    }
    if record is not None:
        record = Path(record)
        if not record.is_absolute():
            raise ValueError("The --record path must be absolute")
        # Normalize parent-directory notation without discarding the requested alias.
        record = Path(os.path.abspath(record))
        root_alias = next((parent for parent in record.parents if parent.resolve() == root), None)
        if root_alias is not None:
            record = root / record.relative_to(root_alias)
        resolved = record.resolve()
        if not record.is_relative_to(record_root) or not resolved.is_relative_to(root):
            raise ValueError("Record path must stay inside the target record directory and repository")
        if any(parent.parts[-3:] == ("docs", "examples", "records") for parent in resolved.parents):
            raise ValueError("Record path must not resolve into the public example directory")
        if record.suffix != ".md" or (record.exists() and not record.is_file()):
            raise ValueError("Record path must name a Markdown file")
        if any(parent.exists() and not parent.is_dir() for parent in record.parents if parent.is_relative_to(root)):
            raise ValueError("Record path has a non-directory parent")
        tracked, ignored = [], []
        for candidate in {record, resolved}:
            relative = str(candidate.relative_to(root))
            tracked.append(subprocess.run(
                ["git", "--literal-pathspecs", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
                capture_output=True, text=True, check=False,
            ).returncode)
            ignored.append(subprocess.run(
                ["git", "-C", str(root), "check-ignore", "--no-index", "--quiet", "--", relative],
                capture_output=True, text=True, check=False,
            ).returncode)
        # A tracked link target or an unignored physical path must not look private.
        tracking_state = "tracked" if 0 in tracked else "untracked" if all(code == 1 for code in tracked) else "unknown"
        ignore_state = "not_ignored" if 1 in ignored else "ignored" if all(code == 0 for code in ignored) else "unknown"
        context.update({
            "record_path": str(record),
            "record_resolved_path": str(resolved),
            "record_exists": record.exists() or record.is_symlink(),
            "record_tracked": tracking_state,
            "record_ignore_match": ignore_state,
        })
    return context


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--record", type=Path, help="Check an exact absolute record path and its Git tracking/ignore state")
    args = parser.parse_args()
    try:
        print(json.dumps(resolve_context(args.target, args.record), indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
