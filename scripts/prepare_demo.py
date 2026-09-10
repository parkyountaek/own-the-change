#!/usr/bin/env python3
"""Prepare a fresh synthetic Git change for an Own The Change debrief."""

import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

FIXTURE = Path(__file__).resolve().parents[1] / "tests/fixtures/host-smoke"


def prepare_demo(output=None):
    inputs = ("before/display_name.py", "after/display_name.py", "after/test_display_name.py")
    if not all((FIXTURE / name).is_file() for name in inputs):
        raise ValueError("Demo fixtures are missing; run this script from a complete source checkout")
    if shutil.which("git") is None:
        raise ValueError("Git is required to prepare the demo")
    git_env = os.environ.copy()
    # A caller's repository/index override must not redirect synthetic setup.
    for key in ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        git_env.pop(key, None)
    if output is None:
        target = Path(tempfile.mkdtemp(prefix="own-change-demo-")).resolve()
    else:
        target = Path(output).absolute()
        if target.exists() or target.is_symlink():
            raise ValueError("Output already exists; choose a new --output directory")
        target.mkdir(parents=True, exist_ok=False)
        target = target.resolve()

    subprocess.run(["git", "init", "--quiet", "--template=", str(target)], check=True, env=git_env)
    # Only this newly created synthetic repository gets a local record exclusion.
    (target / ".git/info").mkdir(exist_ok=True)
    (target / ".git/info/exclude").write_text(
        "/docs/ai-understanding/\n__pycache__/\n*.pyc\n", encoding="utf-8"
    )
    shutil.copyfile(FIXTURE / "before/display_name.py", target / "display_name.py")
    subprocess.run(["git", "-C", str(target), "add", "--", "display_name.py"], check=True, env=git_env)
    for name in ("display_name.py", "test_display_name.py"):
        shutil.copyfile(FIXTURE / "after" / name, target / name)
    subprocess.run(["git", "-C", str(target), "add", "--intent-to-add", "--", "test_display_name.py"],
                   check=True, env=git_env)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New directory; defaults to a fresh temporary directory")
    args = parser.parse_args()
    try:
        target = prepare_demo(args.output)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Synthetic demo ready: {target}")
    print(f"cd {shlex.quote(str(target))}")
    print("git diff -- display_name.py test_display_name.py")
    print("python3 -m unittest discover -s . -p 'test_display_name.py' -v")
    print("Open your installed coding agent here. The Git index is the before baseline; there is no HEAD commit.")
    print("Claude: /own-the-change:own-change-debrief")
    print("Codex: /skills, then select Own The Change: Change Debrief and send the selection.")
    print("No agent was launched and no learning record was created. The demo directory remains for you to use.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
