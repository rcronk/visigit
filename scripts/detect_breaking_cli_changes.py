"""Diff visigit/cli.py's argparse surface between two git refs.

Flags a possible breaking change if, between ``old_ref`` and ``new_ref``, a
flag was removed, became required when it previously wasn't, had its
``choices`` narrowed, or changed ``type``/``action``. Adding a new flag, or
widening an existing one (e.g. adding a choice), is never flagged.

This is a heuristic, not a guarantee: it only looks at ``_parse_args``'s
``add_argument`` calls, not at what the rest of the program actually does
with a flag's value. It exists to catch your attention on the release PR
gate and in the publish job's safety net, not to make the versioning
decision unsupervised -- see docs/curriculum or issue #60 for the full
design.

Usage:
    python scripts/detect_breaking_cli_changes.py <old-ref> <new-ref> [path]

Exit code 1 (and a human-readable report on stdout) if something looks
breaking; exit code 0 otherwise.
"""

from __future__ import annotations

import ast
import subprocess
import sys

DEFAULT_PATH = "visigit/cli.py"


def _flags_from_source(source: str) -> dict[str, dict]:
    """Return {canonical_flag_name: {choices, type, required, action}} from
    every ``parser.add_argument(...)`` call found in source."""
    tree = ast.parse(source)
    flags: dict[str, dict] = {}
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_argument"
        ):
            continue
        names = [
            arg.value
            for arg in node.args
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str)
        ]
        if not names:
            continue

        info: dict = {}
        for kw in node.keywords:
            if kw.arg == "choices" and isinstance(kw.value, (ast.List, ast.Tuple)):
                info["choices"] = sorted(
                    elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)
                )
            elif kw.arg == "type":
                info["type"] = ast.unparse(kw.value)
            elif kw.arg == "required" and isinstance(kw.value, ast.Constant):
                info["required"] = kw.value.value
            elif kw.arg == "action" and isinstance(kw.value, ast.Constant):
                info["action"] = kw.value.value

        # A flag's canonical name is its first long-form spelling (--foo), or
        # its only spelling if it's positional/short-only.
        key = next((n for n in names if n.startswith("--")), names[0])
        flags[key] = info
    return flags


def diff_flags(old_flags: dict[str, dict], new_flags: dict[str, dict]) -> list[str]:
    """Return a list of human-readable problems; empty if nothing looks breaking."""
    problems: list[str] = []
    for name, old_info in old_flags.items():
        if name not in new_flags:
            problems.append(f"REMOVED: {name}")
            continue
        new_info = new_flags[name]

        if old_info.get("required") is not True and new_info.get("required") is True:
            problems.append(f"NOW REQUIRED: {name} (was optional)")

        old_choices = old_info.get("choices")
        if old_choices is not None:
            missing = set(old_choices) - set(new_info.get("choices") or [])
            if missing:
                problems.append(f"CHOICES NARROWED: {name} lost {sorted(missing)}")

        old_type, new_type = old_info.get("type"), new_info.get("type")
        if old_type and old_type != new_type:
            problems.append(f"TYPE CHANGED: {name} ({old_type} -> {new_type})")

        old_action, new_action = old_info.get("action"), new_info.get("action")
        if (old_action or new_action) and old_action != new_action:
            problems.append(f"ACTION CHANGED: {name} ({old_action} -> {new_action})")
    return problems


def _source_at(ref: str, path: str, cwd: str | None = None) -> str | None:
    """Return the file's content at ref, or None if it didn't exist there."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}"], text=True, stderr=subprocess.DEVNULL, cwd=cwd
        )
    except subprocess.CalledProcessError:
        return None


def diff_refs(
    old_ref: str, new_ref: str, path: str = DEFAULT_PATH, cwd: str | None = None
) -> list[str]:
    old_src = _source_at(old_ref, path, cwd=cwd)
    if old_src is None:
        return []  # nothing to compare against
    new_src = _source_at(new_ref, path, cwd=cwd)
    if new_src is None:
        return [f"REMOVED FILE: {path}"]
    return diff_flags(_flags_from_source(old_src), _flags_from_source(new_src))


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    old_ref, new_ref = argv[0], argv[1]
    path = argv[2] if len(argv) == 3 else DEFAULT_PATH

    problems = diff_refs(old_ref, new_ref, path)
    if problems:
        print(f"Possible breaking CLI changes detected ({old_ref} -> {new_ref}):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"No breaking CLI changes detected ({old_ref} -> {new_ref}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
