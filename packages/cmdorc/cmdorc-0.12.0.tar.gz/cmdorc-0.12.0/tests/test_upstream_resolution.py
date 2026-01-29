"""
Tests for upstream output resolution feature.

Tests the {{ command.output_file }} syntax for referencing outputs from
upstream commands in the trigger chain.
"""

from pathlib import Path

import pytest

from cmdorc import CommandConfig, CommandRuntime, RunResult, RunState
from cmdorc.exceptions import VariableResolutionError
from cmdorc.runtime_vars import resolve_runtime_vars


class TestRunRegistry:
    """Tests for CommandRuntime run_id index."""

    def test_get_run_by_id_found(self):
        """Can look up run by ID after completion."""
        runtime = CommandRuntime()
        config = CommandConfig(name="test", command="echo", triggers=[])
        runtime.register_command(config)

        result = RunResult(command_name="test")
        result.mark_running()
        result.mark_success()

        runtime.add_live_run(result)
        runtime.mark_run_complete(result)

        found = runtime.get_run_by_id(result.run_id)
        assert found is result

    def test_get_run_by_id_not_found(self):
        """Returns None for unknown run_id."""
        runtime = CommandRuntime()
        assert runtime.get_run_by_id("nonexistent") is None

    def test_get_run_by_id_evicted(self):
        """Returns None after run evicted from memory."""
        runtime = CommandRuntime()
        config = CommandConfig(name="test", command="echo", triggers=[], keep_in_memory=2)
        runtime.register_command(config)

        # Create 3 runs (limit is 2)
        results = []
        for _ in range(3):
            r = RunResult(command_name="test")
            r.mark_running()
            r.mark_success()
            runtime.add_live_run(r)
            runtime.mark_run_complete(r)
            results.append(r)

        # First run should be evicted
        assert runtime.get_run_by_id(results[0].run_id) is None
        # Later runs should still be available
        assert runtime.get_run_by_id(results[1].run_id) is results[1]
        assert runtime.get_run_by_id(results[2].run_id) is results[2]

    def test_run_index_cleaned_on_remove_command(self):
        """Run index entries cleaned when command removed."""
        runtime = CommandRuntime()
        config = CommandConfig(name="test", command="echo", triggers=[])
        runtime.register_command(config)

        result = RunResult(command_name="test")
        result.mark_running()
        result.mark_success()
        runtime.add_live_run(result)
        runtime.mark_run_complete(result)

        # Should be in index
        assert runtime.get_run_by_id(result.run_id) is result

        # Remove command
        runtime.remove_command("test")

        # Should no longer be in index
        assert runtime.get_run_by_id(result.run_id) is None

    def test_run_index_stats(self):
        """Run index count in stats."""
        runtime = CommandRuntime()
        config = CommandConfig(name="test", command="echo", triggers=[])
        runtime.register_command(config)

        # No runs yet
        stats = runtime.get_stats()
        assert stats["runs_in_index"] == 0

        # Add a run
        result = RunResult(command_name="test")
        result.mark_running()
        result.mark_success()
        runtime.add_live_run(result)
        runtime.mark_run_complete(result)

        stats = runtime.get_stats()
        assert stats["runs_in_index"] == 1


class TestUpstreamResolution:
    """Tests for {{ command.output_file }} resolution."""

    def test_resolve_from_trigger_chain(self):
        """Resolution from trigger chain."""
        upstream = RunResult(command_name="generate")
        upstream.state = RunState.SUCCESS
        upstream.output_file = Path("/tmp/output.txt")

        result = resolve_runtime_vars(
            "process {{ generate.output_file }}",
            {},
            trigger_chain_runs={"generate": upstream},
        )
        assert result == "process /tmp/output.txt"

    def test_missing_command_error(self):
        """Error when command not in chain and no fallback."""
        with pytest.raises(VariableResolutionError) as exc:
            resolve_runtime_vars(
                "{{ unknown.output_file }}",
                {},
                trigger_chain_runs={},
            )
        assert "not in trigger chain" in str(exc.value)

    def test_unsupported_field_error(self):
        """Error for unsupported field names."""
        upstream = RunResult(command_name="test")
        upstream.state = RunState.SUCCESS

        with pytest.raises(VariableResolutionError) as exc:
            resolve_runtime_vars(
                "{{ test.unknown_field }}",
                {},
                trigger_chain_runs={"test": upstream},
            )
        assert "Unknown field" in str(exc.value)

    def test_resolve_from_failed_command(self):
        """Can access output_file from failed command."""
        upstream = RunResult(command_name="build")
        upstream.state = RunState.FAILED
        upstream.output_file = Path("/tmp/error.log")

        result = resolve_runtime_vars(
            "notify {{ build.output_file }}",
            {},
            trigger_chain_runs={"build": upstream},
        )
        assert result == "notify /tmp/error.log"

    def test_no_output_file_error(self):
        """Error when output_storage disabled."""
        upstream = RunResult(command_name="test")
        upstream.state = RunState.SUCCESS
        upstream.output_file = None

        with pytest.raises(VariableResolutionError) as exc:
            resolve_runtime_vars(
                "{{ test.output_file }}",
                {},
                trigger_chain_runs={"test": upstream},
            )
        assert "output_storage" in str(exc.value)

    def test_mixed_vars_and_upstream(self):
        """Mix of regular vars and upstream refs."""
        upstream = RunResult(command_name="lint")
        upstream.state = RunState.SUCCESS
        upstream.output_file = Path("/tmp/lint.out")

        result = resolve_runtime_vars(
            "{{ tool }} {{ lint.output_file }} --config={{ config }}",
            {"tool": "mypy", "config": "setup.cfg"},
            trigger_chain_runs={"lint": upstream},
        )
        assert result == "mypy /tmp/lint.out --config=setup.cfg"

    def test_fallback_to_latest(self):
        """Falls back to latest result for manual runs."""
        runtime = CommandRuntime()
        config = CommandConfig(name="generate", command="echo", triggers=[])
        runtime.register_command(config)

        # Create a completed run
        upstream = RunResult(command_name="generate")
        upstream.state = RunState.SUCCESS
        upstream.output_file = Path("/tmp/gen.txt")
        upstream.mark_running()
        upstream.mark_success()
        runtime.add_live_run(upstream)
        runtime.mark_run_complete(upstream)

        # Resolve with empty chain (manual run scenario)
        result = resolve_runtime_vars(
            "process {{ generate.output_file }}",
            {},
            trigger_chain_runs={},
            runtime=runtime,
        )
        assert result == "process /tmp/gen.txt"

    def test_multiple_upstream_refs(self):
        """Multiple upstream refs in same string."""
        upstream_a = RunResult(command_name="A")
        upstream_a.state = RunState.SUCCESS
        upstream_a.output_file = Path("/tmp/a.out")

        upstream_b = RunResult(command_name="B")
        upstream_b.state = RunState.SUCCESS
        upstream_b.output_file = Path("/tmp/b.out")

        result = resolve_runtime_vars(
            "diff {{ A.output_file }} {{ B.output_file }}",
            {},
            trigger_chain_runs={"A": upstream_a, "B": upstream_b},
        )
        assert result == "diff /tmp/a.out /tmp/b.out"


class TestChainPropagation:
    """Tests for transitive ancestor access."""

    def test_access_grandparent(self):
        """C can access A through B's chain."""
        # A's result
        result_a = RunResult(command_name="A")
        result_a.state = RunState.SUCCESS
        result_a.output_file = Path("/tmp/a.out")

        # B's result (triggered by A)
        result_b = RunResult(command_name="B")
        result_b.state = RunState.SUCCESS
        result_b.upstream_run_ids = [("command_success:A", result_a.run_id)]

        # When C is triggered by B, chain propagation should include A
        # Simulated trigger_chain_runs after propagation:
        trigger_chain_runs = {"B": result_b, "A": result_a}

        result = resolve_runtime_vars(
            "{{ A.output_file }}",
            {},
            trigger_chain_runs=trigger_chain_runs,
        )
        assert result == "/tmp/a.out"


class TestUpstreamRunIdsSerialization:
    """Tests for upstream_run_ids persistence."""

    def test_to_toml(self):
        """upstream_run_ids serializes to TOML."""
        result = RunResult(command_name="test")
        result.upstream_run_ids = [
            ("command_success:A", "abc-123"),
            ("command_success:B", "def-456"),
        ]
        result.state = RunState.SUCCESS

        toml = result.to_toml()
        assert "[[upstream_run_ids]]" in toml
        assert 'event = "command_success:A"' in toml
        assert 'run_id = "abc-123"' in toml

    def test_to_dict(self):
        """upstream_run_ids serializes to dict."""
        result = RunResult(command_name="test")
        result.upstream_run_ids = [("event1", "id1"), ("event2", "id2")]

        d = result.to_dict()
        assert d["upstream_run_ids"] == [
            {"event": "event1", "run_id": "id1"},
            {"event": "event2", "run_id": "id2"},
        ]

    def test_empty_upstream_run_ids(self):
        """Empty upstream_run_ids handled correctly."""
        result = RunResult(command_name="test")
        result.upstream_run_ids = []

        # to_dict
        d = result.to_dict()
        assert d["upstream_run_ids"] == []

        # to_toml should not include upstream_run_ids section
        toml = result.to_toml()
        assert "[[upstream_run_ids]]" not in toml


class TestMetadataParserUpstreamRunIds:
    """Tests for parsing upstream_run_ids from TOML."""

    def test_parse_upstream_run_ids(self, tmp_path):
        """Parse upstream_run_ids from metadata file."""
        from cmdorc.metadata_parser import parse_metadata_file

        metadata_content = """
command_name = "test"
run_id = "test-run-123"
state = "success"
duration_str = "1.0s"

[[upstream_run_ids]]
event = "command_success:A"
run_id = "abc-123"

[[upstream_run_ids]]
event = "command_success:B"
run_id = "def-456"
"""
        metadata_file = tmp_path / "metadata.toml"
        metadata_file.write_text(metadata_content)

        result = parse_metadata_file(metadata_file)
        assert result is not None
        assert result.upstream_run_ids == [
            ("command_success:A", "abc-123"),
            ("command_success:B", "def-456"),
        ]

    def test_parse_no_upstream_run_ids(self, tmp_path):
        """Parse metadata without upstream_run_ids."""
        from cmdorc.metadata_parser import parse_metadata_file

        metadata_content = """
command_name = "test"
run_id = "test-run-123"
state = "success"
duration_str = "1.0s"
"""
        metadata_file = tmp_path / "metadata.toml"
        metadata_file.write_text(metadata_content)

        result = parse_metadata_file(metadata_file)
        assert result is not None
        assert result.upstream_run_ids == []
