"""Tests for argument parsing and top-level CLI orchestration."""

from __future__ import annotations

import pytest

from visigit import cli
from visigit.renderer import Renderer

from .conftest import RepoTools


class TestParseArgs:
    def test_defaults(self) -> None:
        args = cli._parse_args([])
        assert args.repo_path == "."
        assert args.mode == "normal"
        assert args.output_format == "svg"
        assert args.output_path is None
        assert args.rank_direction is None
        assert args.max_commit_depth is None
        assert args.exclude_remotes is False
        assert args.commit_details is False
        assert args.no_open is False
        assert args.viewer == "html"
        assert args.monitor is False
        assert args.verbose_log is False

    def test_custom_values(self) -> None:
        args = cli._parse_args(
            [
                "--repo-path",
                "/tmp/repo",
                "--mode",
                "verbose",
                "--output-format",
                "mermaid",
                "--output-path",
                "out.md",
                "--rank-direction",
                "LR",
                "--max-commit-depth",
                "5",
                "--exclude-remotes",
                "--commit-details",
                "--no-open",
                "--viewer",
                "none",
                "--monitor",
                "--verbose-log",
            ]
        )
        assert args.repo_path == "/tmp/repo"
        assert args.mode == "verbose"
        assert args.output_format == "mermaid"
        assert args.output_path == "out.md"
        assert args.rank_direction == "LR"
        assert args.max_commit_depth == 5
        assert args.exclude_remotes is True
        assert args.commit_details is True
        assert args.no_open is True
        assert args.viewer == "none"
        assert args.monitor is True
        assert args.verbose_log is True

    def test_version_flag_exits_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as exc:
            cli._parse_args(["--version"])
        assert exc.value.code == 0
        assert "visigit" in capsys.readouterr().out

    def test_invalid_mode_exits_nonzero(self) -> None:
        with pytest.raises(SystemExit) as exc:
            cli._parse_args(["--mode", "bogus"])
        assert exc.value.code != 0


class TestRenderOnce:
    def test_normal_mode_returns_node_ids_and_writes_file(self, repo: RepoTools, tmp_path) -> None:
        repo.write("a.txt")
        sha = repo.commit("initial")
        out_path = tmp_path / "out.svg"
        args = cli._parse_args(
            ["--repo-path", str(repo.path), "--viewer", "none", "--output-path", str(out_path)]
        )
        renderer = Renderer(output_path=str(out_path), output_format="svg", viewer="none")

        node_ids = cli._render_once(args, renderer)

        assert sha in node_ids
        assert out_path.exists()

    def test_verbose_mode_includes_object_graph(self, repo: RepoTools, tmp_path) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"
        args = cli._parse_args(
            [
                "--repo-path",
                str(repo.path),
                "--mode",
                "verbose",
                "--viewer",
                "none",
                "--output-path",
                str(out_path),
            ]
        )
        renderer = Renderer(output_path=str(out_path), output_format="svg", viewer="none")

        node_ids = cli._render_once(args, renderer)

        assert node_ids  # commit + tree + blob nodes
        assert out_path.exists()

    def test_branch_mode_defaults_to_lr(self, repo: RepoTools, tmp_path) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"
        args = cli._parse_args(
            [
                "--repo-path",
                str(repo.path),
                "--mode",
                "branch",
                "--viewer",
                "none",
                "--output-path",
                str(out_path),
            ]
        )
        renderer = Renderer(output_path=str(out_path), output_format="svg", viewer="none")

        node_ids = cli._render_once(args, renderer)

        assert "main" in node_ids
        assert out_path.exists()

    def test_explicit_rank_direction_overrides_mode_default(
        self, repo: RepoTools, tmp_path
    ) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"
        args = cli._parse_args(
            [
                "--repo-path",
                str(repo.path),
                "--rank-direction",
                "TB",
                "--viewer",
                "none",
                "--output-path",
                str(out_path),
            ]
        )
        renderer = Renderer(output_path=str(out_path), output_format="svg", viewer="none")

        cli._render_once(args, renderer)

        assert out_path.exists()

    def test_max_commit_depth_and_exclude_remotes_wired_through(
        self, repo: RepoTools, tmp_path
    ) -> None:
        repo.write("a.txt")
        repo.commit("first")
        repo.write("b.txt")
        repo.commit("second")
        out_path = tmp_path / "out.svg"
        args = cli._parse_args(
            [
                "--repo-path",
                str(repo.path),
                "--max-commit-depth",
                "1",
                "--exclude-remotes",
                "--commit-details",
                "--viewer",
                "none",
                "--output-path",
                str(out_path),
            ]
        )
        renderer = Renderer(output_path=str(out_path), output_format="svg", viewer="none")

        node_ids = cli._render_once(args, renderer)

        assert node_ids
        assert out_path.exists()


class TestMain:
    def test_non_monitor_run_writes_output_and_returns(self, repo: RepoTools, tmp_path) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"

        cli.main(
            [
                "--repo-path",
                str(repo.path),
                "--output-path",
                str(out_path),
                "--viewer",
                "none",
            ]
        )

        assert out_path.exists()

    def test_default_output_path_depends_on_format(
        self, repo: RepoTools, tmp_path, monkeypatch
    ) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        monkeypatch.chdir(tmp_path)

        cli.main(["--repo-path", str(repo.path), "--output-format", "mermaid", "--viewer", "none"])

        assert (tmp_path / "visigit.md").exists()

    def test_no_open_forces_none_viewer(self, repo: RepoTools, tmp_path, monkeypatch) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"
        captured: dict = {}
        orig_init = Renderer.__init__

        def spy_init(self, **kwargs):
            captured.update(kwargs)
            orig_init(self, **kwargs)

        monkeypatch.setattr(Renderer, "__init__", spy_init)

        cli.main(
            [
                "--repo-path",
                str(repo.path),
                "--output-path",
                str(out_path),
                "--viewer",
                "html",
                "--no-open",
            ]
        )

        assert captured["viewer"] == "none"

    def test_verbose_log_flag_sets_debug_level(self, repo: RepoTools, tmp_path) -> None:
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"

        cli.main(
            [
                "--repo-path",
                str(repo.path),
                "--output-path",
                str(out_path),
                "--viewer",
                "none",
                "--verbose-log",
            ]
        )

        assert out_path.exists()

    def test_monitor_loop_runs_once_then_stops_on_keyboard_interrupt(
        self, repo: RepoTools, tmp_path, monkeypatch
    ) -> None:
        """A fake Monitor stands in for watchdog: no real filesystem watching is
        exercised (that's tests/test_monitor.py's job), just main()'s own
        start/wait/update/stop wiring and KeyboardInterrupt handling."""
        repo.write("a.txt")
        repo.commit("initial")
        out_path = tmp_path / "out.svg"

        class FakeMonitor:
            calls = {"start": 0, "wait": 0, "update": 0, "stop": 0}

            def __init__(self, repo_path, output_path) -> None:
                self.prev_node_ids: frozenset = frozenset()

            def start(self) -> None:
                FakeMonitor.calls["start"] += 1

            def wait(self) -> None:
                FakeMonitor.calls["wait"] += 1
                if FakeMonitor.calls["wait"] >= 2:
                    raise KeyboardInterrupt

            def update(self, node_ids) -> None:
                FakeMonitor.calls["update"] += 1
                self.prev_node_ids = node_ids

            def stop(self) -> None:
                FakeMonitor.calls["stop"] += 1

        monkeypatch.setattr(cli, "Monitor", FakeMonitor)

        cli.main(
            [
                "--repo-path",
                str(repo.path),
                "--output-path",
                str(out_path),
                "--viewer",
                "none",
                "--monitor",
            ]
        )

        assert FakeMonitor.calls["start"] == 1
        assert FakeMonitor.calls["wait"] == 2
        assert FakeMonitor.calls["update"] == 2  # once before the loop, once inside it
        assert FakeMonitor.calls["stop"] == 1
