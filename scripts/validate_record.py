#!/usr/bin/env python3
"""Validate Own The Change Markdown records without judging user understanding."""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

STATUSES = {"confirmed", "needs_follow_up", "not_confirmed", "unknown"}
RISK_LEVELS = {"low", "medium", "high"}
METADATA_KEYS = ("provider", "model", "turn", "token", "cost")
REQUIRED_SECTIONS = (
    "Goal",
    "Changed Files",
    "Test Evidence",
    "Key Explanation",
    "User Response",
    "Understanding Status",
    "Remaining Risks",
    "Next Check",
)


def fail(message):
    raise ValueError(message)


def parse_front_matter(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("YAML front matter must start and end with ---")
    lines = match.group(1).splitlines()
    data, metadata, in_metadata = {}, {}, False
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = re.match(r"^  ([a-z_]+):\s*(.*)$", line)
        top = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if nested and in_metadata:
            metadata[nested.group(1)] = nested.group(2).strip()
        elif top:
            key, value = top.groups()
            data[key] = value.strip()
            in_metadata = key == "execution_metadata"
        else:
            fail(f"unrecognized front matter line: {line}")
    data["execution_metadata"] = metadata
    return data, text[match.end():]


def validate(path):
    path = Path(path)
    if path.suffix != ".md":
        fail("record path must end in .md")
    text = path.read_text(encoding="utf-8")
    data, body = parse_front_matter(text)

    for key in ("task_id", "date", "understanding_status", "risk_level", "follow_up_at"):
        if not data.get(key):
            fail(f"missing required front matter key: {key}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["task_id"]):
        fail("task_id must use short kebab-case")
    try:
        parsed_date = dt.date.fromisoformat(data["date"])
    except ValueError:
        fail("date must use YYYY-MM-DD")
    if str(parsed_date) != data["date"]:
        fail("date must use YYYY-MM-DD")
    if path.parent.name != data["date"]:
        fail("date must match the YYYY-MM-DD parent directory")
    if data["understanding_status"] not in STATUSES:
        fail("understanding_status must be one of: " + ", ".join(sorted(STATUSES)))
    if data["risk_level"] not in RISK_LEVELS:
        fail("risk_level must be one of: " + ", ".join(sorted(RISK_LEVELS)))
    for key in METADATA_KEYS:
        if key not in data["execution_metadata"] or not data["execution_metadata"][key]:
            fail(f"missing execution_metadata.{key}; use unknown when unavailable")

    headings = set(re.findall(r"^##\s+(.+?)\s*$", body, re.MULTILINE))
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            fail(f"missing required section: {section}")
    return f"VALID {path}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    args = parser.parse_args(argv)
    errors = []
    for path in args.records:
        try:
            print(validate(path))
        except (OSError, ValueError) as exc:
            errors.append(f"INVALID {path}: {exc}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
