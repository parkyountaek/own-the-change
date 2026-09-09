#!/usr/bin/env python3
"""Build a temporary plugin and start Claude Code in your project."""

import argparse
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

if __package__:
    from .build_plugins import build_plugins
else:
    from build_plugins import build_plugins


def launch(project):
    project = Path(project).resolve()
    if not project.exists():
        raise ValueError("Project directory does not exist")
    if not project.is_dir():
        raise ValueError("Project path is not a directory")
    claude = shutil.which("claude")
    if claude is None:
        raise ValueError("Claude Code is not installed or is not on PATH. Install it and sign in first.")
    if shutil.which("git") is None:
        raise ValueError("Git is not installed or is not on PATH")
    git = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
    )
    if git.returncode != 0:
        raise ValueError("Choose a directory inside a Git repository")

    with tempfile.TemporaryDirectory(prefix="own-change-session-") as directory:
        packages = build_plugins(Path(directory) / "plugins")
        print(f"Starting Claude Code in {project}", flush=True)
        print("Try /own-the-change:own-change-debrief after a code change.", flush=True)
        print("This loads the plugin for this session only; no marketplace is registered.", flush=True)
        # Ctrl+C belongs to Claude's interactive UI. A caught handler resets to
        # the default on exec, unlike SIG_IGN, which the child would inherit.
        previous_handler = signal.signal(signal.SIGINT, lambda _signum, _frame: None)
        try:
            result = subprocess.run(
                [claude, "--plugin-dir", packages["claude-code"]],
                cwd=project, check=False,
            )
        finally:
            signal.signal(signal.SIGINT, previous_handler)
        return result.returncode if result.returncode >= 0 else 128 - result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Path to the Git project you want to work on")
    args = parser.parse_args()
    try:
        return launch(args.project)
    except KeyboardInterrupt:
        return 130
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
