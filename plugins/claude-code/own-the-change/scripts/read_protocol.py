#!/usr/bin/env python3
"""Print the relevant sections of the canonical protocol without copying its rules."""

import argparse
from pathlib import Path
import re
import sys

PROTOCOL = Path(__file__).resolve().parents[1] / "docs/protocol/understanding-protocol.md"
COMMON = (
    "Purpose and scope", "Runtime language", "Evidence collection", "Efficient execution",
    "Record choice", "Status", "Privacy and safety",
)
MODES = {
    "plan": (*COMMON, "Before work: Plan Check"),
    "debrief": (*COMMON, "After work: Change Debrief"),
    "understanding": (*COMMON, "Understanding Check"),
    "demo": ("Runtime language", "Demo and environment diagnosis", "Privacy and safety"),
    "doctor": ("Runtime language", "Demo and environment diagnosis", "Privacy and safety"),
    "record": ("Runtime language", "Record choice", "Record contract", "Follow-up", "Privacy and safety"),
    "research": ("Research and readable output",),
}


def select_sections(document, mode):
    if mode == "all":
        return document
    parts = re.split(r"(?=^## )", document, flags=re.MULTILINE)
    sections = {}
    for part in parts[1:]:
        title = part.splitlines()[0][3:]
        if title in sections:
            raise ValueError("Duplicate protocol section")
        sections[title] = part
    expected = {title for titles in MODES.values() for title in titles}
    if set(sections) != expected:
        raise ValueError("Protocol section map is stale; read the complete canonical protocol")
    requested = set(MODES[mode])
    return parts[0] + "".join(section for title, section in sections.items() if title in requested)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=[*MODES, "all"], required=True)
    args = parser.parse_args()
    try:
        print(select_sections(PROTOCOL.read_text(encoding="utf-8"), args.mode), end="")
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
