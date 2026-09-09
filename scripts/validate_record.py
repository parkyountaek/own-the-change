#!/usr/bin/env python3
"""Check record structure and consistency, never the quality of an explanation."""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

STATUSES = {"confirmed", "needs_follow_up", "not_confirmed", "unknown"}
RISK_LEVELS = {"low", "medium", "high"}
FIELDS = {
    "task_id", "date", "record_kind", "understanding_status", "risk_level",
    "user_response_status", "evidence_status", "diff_scope", "follow_up_at",
    "follow_up_reason", "execution_metadata",
}
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


def scalar(value):
    """Read the documented YAML string subset; reject ambiguous YAML constructs."""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except ValueError:
            fail("invalid double-quoted scalar")
        if not isinstance(parsed, str):
            fail("expected a string scalar")
        return parsed
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            fail("invalid single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if (not value or value[0] in "[]{},&*!|>#%@`" or value in {"-", "?", ":"}
            or value.startswith(("- ", "? ", ": ")) or ": " in value or " #" in value):
        fail("use a quoted scalar for special YAML characters")
    return value


def parse_front_matter(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("YAML front matter must start and end with ---")
    lines = match.group(1).splitlines()
    data, metadata, current = {}, {}, None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = re.fullmatch(r"  ([a-z_]+):\s*(.*)", line)
        item = re.fullmatch(r"  -\s+(.+)", line)
        top = re.fullmatch(r"([a-z_]+):\s*(.*)", line)
        if nested and current == "execution_metadata":
            key, value = nested.groups()
            if key not in METADATA_KEYS or key in metadata:
                fail(f"unknown or duplicate execution_metadata key: {key}")
            metadata[key] = scalar(value.strip())
        elif item and current == "follow_up_at":
            data["follow_up_at"].append(scalar(item.group(1).strip()))
        elif top:
            key, value = top.groups()
            if key not in FIELDS or key in data:
                fail(f"unknown or duplicate front matter key: {key}")
            value, current = value.strip(), key
            if key == "execution_metadata":
                if value:
                    fail("execution_metadata must be an indented mapping")
                data[key] = metadata
            elif key == "follow_up_at":
                if value not in ("", "[]"):
                    fail("follow_up_at must be [] or an indented date list")
                data[key] = []
                if value == "[]":
                    current = None
            else:
                data[key] = scalar(value)
        else:
            fail(f"unrecognized front matter line: {line}")
    return data, text[match.end():]


def calendar_date(value, field):
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError:
        fail(f"{field} must use a valid YYYY-MM-DD date")
    if str(parsed) != value:
        fail(f"{field} must use YYYY-MM-DD")
    return parsed


def sections_in(body):
    """Ignore headings in fenced evidence snippets and reject duplicate sections."""
    sections, current, fence = {}, None, None
    for line in body.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, rest = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
                fence = None
            if current:
                sections[current].append(line)
            continue
        heading = re.fullmatch(r"##\s+(.+?)\s*", line) if fence is None else None
        if heading:
            current = heading.group(1)
            if current in sections:
                fail(f"duplicate section: {current}")
            sections[current] = []
        elif current:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def is_placeholder(value):
    cleaned = value.strip().strip("- *`.").strip().lower()
    return cleaned in {"", "todo", "tbd", "replace me"}


def validate(path):
    path = Path(path)
    if path.suffix != ".md":
        fail("record path must end in .md")
    text = path.read_text(encoding="utf-8")
    data, body = parse_front_matter(text)

    for key in sorted(FIELDS):
        if key not in data:
            fail(f"missing required front matter key: {key}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["task_id"]):
        fail("task_id must use short kebab-case")
    if path.stem != data["task_id"]:
        fail("task_id must match the record filename")
    parsed_date = calendar_date(data["date"], "date")
    if path.parent.name != data["date"]:
        fail("date must match the YYYY-MM-DD parent directory")
    if data["understanding_status"] not in STATUSES:
        fail("understanding_status must be one of: " + ", ".join(sorted(STATUSES)))
    if data["risk_level"] not in RISK_LEVELS:
        fail("risk_level must be one of: " + ", ".join(sorted(RISK_LEVELS)))
    if data["record_kind"] not in {"actual", "example"}:
        fail("record_kind must be actual or example")
    locations = [path.absolute(), path.resolve()]
    if data["record_kind"] == "example" and any("ai-understanding" in location.parts for location in locations):
        fail("example records must not be stored in the actual-record directory")
    if data["record_kind"] == "actual" and any(
        ancestor.parts[-3:] == ("docs", "examples", "records")
        for location in locations for ancestor in location.parents
    ):
        fail("actual records must not be stored in the public example directory")
    if data["user_response_status"] not in {"answered", "not_answered"}:
        fail("user_response_status must be answered or not_answered")
    if data["evidence_status"] not in {"available", "unavailable"}:
        fail("evidence_status must be available or unavailable")
    if data["understanding_status"] in {"confirmed", "needs_follow_up"}:
        if data["user_response_status"] != "answered":
            fail("confirmed and needs_follow_up require an answered user response")
        if data["evidence_status"] != "available":
            fail("confirmed and needs_follow_up require available change evidence")
    if data["evidence_status"] == "available" and (data["diff_scope"].lower() == "unknown" or is_placeholder(data["diff_scope"])):
        fail("available evidence requires a known diff_scope")
    follow_up = [calendar_date(value, "follow_up_at") for value in data["follow_up_at"]]
    if len(set(follow_up)) != len(follow_up):
        fail("follow_up_at must not contain duplicate dates")
    if any(value <= parsed_date for value in follow_up):
        fail("follow_up_at dates must be after the work date")
    if data["risk_level"] == "high":
        try:
            expected = {parsed_date + dt.timedelta(days=1), parsed_date + dt.timedelta(days=7)}
        except OverflowError:
            fail("work date cannot represent the required follow-up dates")
        if not expected.issubset(follow_up):
            fail("high-risk records require next-day and one-week follow_up_at dates")
    if follow_up:
        if data["follow_up_reason"].lower() in {"none", "unknown"} or is_placeholder(data["follow_up_reason"]):
            fail("follow-up dates require a concrete follow_up_reason")
    elif data["follow_up_reason"] != "none":
        fail("use follow_up_reason: none when there are no follow-up dates")
    for key in METADATA_KEYS:
        if key not in data["execution_metadata"] or not data["execution_metadata"][key]:
            fail(f"missing execution_metadata.{key}; use unknown when unavailable")

    sections = sections_in(body)
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            fail(f"missing required section: {section}")
        if is_placeholder(sections[section]):
            fail(f"empty or placeholder section: {section}")
    response = sections["User Response"].strip().strip("- *`.").strip()
    no_response = response.lower() == "no response"
    if data["user_response_status"] == "not_answered" and not no_response:
        fail("not_answered requires the User Response marker: No response.")
    if data["user_response_status"] == "answered" and no_response:
        fail("answered requires a user response, not the No response marker")
    body_status = re.match(r"^\s*(?:-\s+)?`?([a-z_]+)`?(?=[:\s.\-\u2013\u2014]|$)", sections["Understanding Status"])
    if not body_status or body_status.group(1) != data["understanding_status"]:
        fail("Understanding Status must begin with the same status as front matter")
    if data["record_kind"] == "example" and "Fictional example" not in body:
        fail("example records must visibly identify themselves as a Fictional example")
    return f"VALID {path}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    args = parser.parse_args(argv)
    errors = []
    for path in args.records:
        try:
            print(validate(path))
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"INVALID {path}: {exc}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
