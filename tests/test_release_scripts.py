"""Tests for the release-automation helper scripts (scripts/), not the visigit
package itself -- these back the auto-versioning/breaking-change-gate design
in issue #60."""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

import pytest

from scripts.compute_next_version import decide_bump, next_version, parse_tag
from scripts.detect_breaking_cli_changes import (
    _flags_from_source,
    diff_flags,
    diff_refs,
)


class TestParseTag:
    def test_parses_v_prefixed(self) -> None:
        assert parse_tag("v1.2.3") == (1, 2, 3)

    def test_parses_bare(self) -> None:
        assert parse_tag("1.2.3") == (1, 2, 3)

    def test_rejects_malformed(self) -> None:
        with pytest.raises(ValueError):
            parse_tag("not-a-version")


class TestDecideBump:
    def test_breaking_always_wins_major(self) -> None:
        assert decide_bump(lines_changed=1, threshold=200, is_breaking=True) == "major"

    def test_over_threshold_is_minor(self) -> None:
        assert decide_bump(lines_changed=200, threshold=200, is_breaking=False) == "minor"
        assert decide_bump(lines_changed=500, threshold=200, is_breaking=False) == "minor"

    def test_under_threshold_is_patch(self) -> None:
        assert decide_bump(lines_changed=199, threshold=200, is_breaking=False) == "patch"
        assert decide_bump(lines_changed=0, threshold=200, is_breaking=False) == "patch"


class TestNextVersion:
    def test_patch_bump(self) -> None:
        assert next_version("v0.3.0", "patch") == "0.3.1"

    def test_minor_bump_resets_patch(self) -> None:
        assert next_version("v0.3.5", "minor") == "0.4.0"

    def test_major_bump_resets_minor_and_patch(self) -> None:
        assert next_version("v1.4.5", "major") == "2.0.0"

    def test_unknown_bump_raises(self) -> None:
        with pytest.raises(ValueError):
            next_version("v0.3.0", "sideways")


class TestFlagsFromSource:
    def test_extracts_simple_flag(self) -> None:
        src = textwrap.dedent(
            """
            parser.add_argument("--mode", choices=["a", "b"], default="a")
            """
        )
        flags = _flags_from_source(src)
        assert flags["--mode"]["choices"] == ["a", "b"]

    def test_extracts_store_true_action(self) -> None:
        src = 'parser.add_argument("--monitor", action="store_true")'
        flags = _flags_from_source(src)
        assert flags["--monitor"]["action"] == "store_true"

    def test_extracts_type_and_required(self) -> None:
        src = 'parser.add_argument("--depth", type=int, required=True)'
        flags = _flags_from_source(src)
        assert flags["--depth"]["type"] == "int"
        assert flags["--depth"]["required"] is True

    def test_canonical_name_prefers_long_form(self) -> None:
        src = 'parser.add_argument("-m", "--mode")'
        flags = _flags_from_source(src)
        assert "--mode" in flags
        assert "-m" not in flags

    def test_positional_only_uses_its_own_name(self) -> None:
        src = 'parser.add_argument("path")'
        flags = _flags_from_source(src)
        assert "path" in flags

    def test_ignores_unrelated_calls(self) -> None:
        src = 'parser.add_argument("--mode")\nsome_other_call("--not-a-flag")'
        flags = _flags_from_source(src)
        assert list(flags) == ["--mode"]


class TestDiffFlags:
    def test_no_changes_is_silent(self) -> None:
        flags = {"--mode": {"choices": ["a", "b"]}}
        assert diff_flags(flags, dict(flags)) == []

    def test_removed_flag_is_flagged(self) -> None:
        old = {"--mode": {}, "--verbose": {}}
        new = {"--mode": {}}
        problems = diff_flags(old, new)
        assert any("REMOVED: --verbose" in p for p in problems)

    def test_added_flag_is_not_flagged(self) -> None:
        old = {"--mode": {}}
        new = {"--mode": {}, "--new-thing": {}}
        assert diff_flags(old, new) == []

    def test_narrowed_choices_is_flagged(self) -> None:
        old = {"--mode": {"choices": ["a", "b", "c"]}}
        new = {"--mode": {"choices": ["a", "b"]}}
        problems = diff_flags(old, new)
        assert any("CHOICES NARROWED" in p and "'c'" in p for p in problems)

    def test_widened_choices_is_not_flagged(self) -> None:
        old = {"--mode": {"choices": ["a", "b"]}}
        new = {"--mode": {"choices": ["a", "b", "c"]}}
        assert diff_flags(old, new) == []

    def test_becoming_required_is_flagged(self) -> None:
        old = {"--path": {"required": False}}
        new = {"--path": {"required": True}}
        problems = diff_flags(old, new)
        assert any("NOW REQUIRED" in p for p in problems)

    def test_becoming_optional_is_not_flagged(self) -> None:
        old = {"--path": {"required": True}}
        new = {"--path": {"required": False}}
        assert diff_flags(old, new) == []

    def test_type_change_is_flagged(self) -> None:
        old = {"--depth": {"type": "int"}}
        new = {"--depth": {"type": "str"}}
        problems = diff_flags(old, new)
        assert any("TYPE CHANGED" in p for p in problems)

    def test_action_change_is_flagged(self) -> None:
        old = {"--monitor": {"action": "store_true"}}
        new = {"--monitor": {"action": "store_false"}}
        problems = diff_flags(old, new)
        assert any("ACTION CHANGED" in p for p in problems)


class TestDiffRefsIntegration:
    """Exercises the git-plumbing wrapper against a real temp repo."""

    def _init_repo(self, tmp_path: Path) -> Path:
        repo = tmp_path / "r"
        repo.mkdir()
        subprocess.check_call(["git", "init", "-q", "-b", "main"], cwd=repo)
        subprocess.check_call(["git", "config", "user.email", "a@b.c"], cwd=repo)
        subprocess.check_call(["git", "config", "user.name", "t"], cwd=repo)
        return repo

    def _commit(self, repo: Path, path: str, content: str, msg: str) -> str:
        full = repo / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        subprocess.check_call(["git", "add", "-A"], cwd=repo)
        subprocess.check_call(["git", "commit", "-q", "-m", msg], cwd=repo)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

    def test_no_change_between_refs(self, tmp_path: Path) -> None:
        repo = self._init_repo(tmp_path)
        old = self._commit(repo, "cli.py", 'parser.add_argument("--mode")', "v1")
        new = self._commit(repo, "cli.py", 'parser.add_argument("--mode")  # comment', "v2")
        assert diff_refs(old, new, path="cli.py", cwd=str(repo)) == []

    def test_removed_flag_between_refs(self, tmp_path: Path) -> None:
        repo = self._init_repo(tmp_path)
        old = self._commit(
            repo, "cli.py", 'parser.add_argument("--mode")\nparser.add_argument("--old")', "v1"
        )
        new = self._commit(repo, "cli.py", 'parser.add_argument("--mode")', "v2")
        problems = diff_refs(old, new, path="cli.py", cwd=str(repo))
        assert any("REMOVED: --old" in p for p in problems)

    def test_file_missing_at_old_ref_is_not_flagged(self, tmp_path: Path) -> None:
        repo = self._init_repo(tmp_path)
        old = self._commit(repo, "other.py", "x = 1", "v1")
        new = self._commit(repo, "cli.py", 'parser.add_argument("--mode")', "v2")
        assert diff_refs(old, new, path="cli.py", cwd=str(repo)) == []
