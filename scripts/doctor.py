#!/usr/bin/env python3
"""Report local prerequisites without reading project source, credentials, or config files."""

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "docs/protocol/understanding-protocol.md", "templates/understanding-record.md",
    "scripts/resolve_context.py", "scripts/validate_record.py", "scripts/read_protocol.py",
    "scripts/prepare_demo.py", "scripts/prepare_question.py",
)


def diagnose(root=ROOT, target=None, record=None):
    checks = []

    def add(name, status, detail):
        checks.append({"name": name, "status": status, "detail": detail})

    supported_python = sys.version_info >= (3, 11)
    add("python", "ok" if supported_python else "error", platform.python_version() + "; requires 3.11+")
    git = shutil.which("git")
    if git:
        try:
            result = subprocess.run([git, "--version"], capture_output=True, text=True, timeout=10)
            add("git", "ok" if result.returncode == 0 else "error",
                result.stdout.strip() if result.returncode == 0 else "Git did not report its version")
        except (OSError, subprocess.TimeoutExpired):
            add("git", "error", "Git could not be executed")
    else:
        add("git", "error", "Install Git and make it available on PATH")
    add("shell", "ok" if os.name == "posix" and shutil.which("sh") else "warning",
        "POSIX shell required by shell entry points; native Windows is unverified")
    system = platform.system()
    wsl = "microsoft" in platform.release().lower()
    verified_platform = system in {"Darwin", "Linux"} and not wsl
    add("platform", "ok" if verified_platform else "warning",
        ("WSL" if wsl else system) + "; helper suite covers macOS/Linux; Windows and WSL unverified")
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    fixture = root / "assets/demo"
    if not fixture.is_dir():
        fixture = root / "tests/fixtures/host-smoke"
    for name in ("before/display_name.py", "after/display_name.py", "after/test_display_name.py"):
        if not (fixture / name).is_file():
            missing.append("demo/" + name)
    add("resources", "error" if missing else "ok", {"missing": missing})
    if target is not None:
        if not supported_python or not git or missing:
            add("target", "warning", "Target check unavailable until prerequisites are restored")
        else:
            command = [sys.executable, str(root / "scripts/resolve_context.py"), "--target", str(target)]
            if record is not None:
                command += ["--record", str(record)]
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    context = json.loads(result.stdout)
                    privacy_risk = record is not None and (
                        context.get("record_tracked") != "untracked"
                        or context.get("record_ignore_match") != "ignored")
                    add("target", "warning" if privacy_risk else "ok", context)
                else:
                    add("target", "warning", "Target/record context unavailable; run resolve_context for details")
            except (OSError, ValueError, subprocess.TimeoutExpired):
                add("target", "warning", "Target check unavailable")
    return {"checks": checks, "limits": "No model, authentication, network, test execution, or security audit was performed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, help="Optional project directory; source contents are not read")
    parser.add_argument("--record", type=Path, help="Optional exact record path; requires --target")
    args = parser.parse_args()
    if args.record is not None and args.target is None:
        parser.error("--record requires --target")
    result = diagnose(target=args.target, record=args.record)
    print(json.dumps(result, indent=2))
    return int(any(check["status"] == "error" for check in result["checks"]))


if __name__ == "__main__":
    sys.exit(main())
