"""Compute the next release version from the last tag and a bump decision.

Usage:
    python scripts/compute_next_version.py --last-tag v0.3.0 --lines-changed 42 \
        [--threshold 200] [--breaking] [--override auto|major|minor|patch]

Prints the next bare version (e.g. "0.4.0", no "v" prefix) to stdout.
"""

from __future__ import annotations

import argparse
import re

_TAG_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def parse_tag(tag: str) -> tuple[int, int, int]:
    m = _TAG_RE.match(tag.strip())
    if not m:
        raise ValueError(f"Tag {tag!r} doesn't look like [v]MAJOR.MINOR.PATCH")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def decide_bump(lines_changed: int, threshold: int, is_breaking: bool) -> str:
    """Pick a bump type from the change-size heuristic (see issue #60)."""
    if is_breaking:
        return "major"
    if lines_changed >= threshold:
        return "minor"
    return "patch"


def next_version(last_tag: str, bump: str) -> str:
    major, minor, patch = parse_tag(last_tag)
    if bump == "major":
        major, minor, patch = major + 1, 0, 0
    elif bump == "minor":
        minor, patch = minor + 1, 0
    elif bump == "patch":
        patch += 1
    else:
        raise ValueError(f"Unknown bump type {bump!r}")
    return f"{major}.{minor}.{patch}"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--last-tag", required=True)
    p.add_argument("--lines-changed", type=int, required=True)
    p.add_argument("--threshold", type=int, default=200)
    p.add_argument("--breaking", action="store_true")
    p.add_argument("--override", choices=["auto", "major", "minor", "patch"], default="auto")
    args = p.parse_args()

    bump = (
        args.override
        if args.override != "auto"
        else decide_bump(args.lines_changed, args.threshold, args.breaking)
    )
    print(next_version(args.last_tag, bump))


if __name__ == "__main__":
    main()
