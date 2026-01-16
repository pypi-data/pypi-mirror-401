"""Tests for roar provenance module."""

from roar.services.execution.provenance.process_summarizer import ProcessSummarizerService

# Create a module-level helper function to match the old test interface
_summarizer = ProcessSummarizerService()


def _summarize_process_tree(processes):
    """Helper to match old function interface."""
    return _summarizer.summarize(processes)


class TestSummarizeProcessTree:
    """Tests for process tree summarization."""

    def test_empty_list(self):
        result = _summarize_process_tree([])
        assert result == []

    def test_single_process(self):
        processes = [{"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]}]
        result = _summarize_process_tree(processes)
        assert result == [{"command": ["python", "train.py"]}]

    def test_fork_only_collapsed(self):
        """Fork-only children (same command) should be collapsed to fork_count."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]},
            {"pid": 1001, "parent_pid": 1000, "command": ["python", "train.py"]},
            {"pid": 1002, "parent_pid": 1000, "command": ["python", "train.py"]},
            {"pid": 1003, "parent_pid": 1000, "command": ["python", "train.py"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["python", "train.py"]
        assert result[0]["fork_count"] == 3
        assert "children" not in result[0]

    def test_exec_children_preserved(self):
        """Children that exec'd different commands should be in children list."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]},
            {"pid": 1001, "parent_pid": 1000, "command": ["nvidia-smi", "-q"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["python", "train.py"]
        assert "fork_count" not in result[0]
        assert len(result[0]["children"]) == 1
        assert result[0]["children"][0]["command"] == ["nvidia-smi", "-q"]

    def test_mixed_fork_and_exec(self):
        """Mix of fork-only and exec'd children."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]},
            # Fork-only workers
            {"pid": 1001, "parent_pid": 1000, "command": ["python", "train.py"]},
            {"pid": 1002, "parent_pid": 1000, "command": ["python", "train.py"]},
            # Exec'd child
            {"pid": 1003, "parent_pid": 1000, "command": ["nvidia-smi"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["python", "train.py"]
        assert result[0]["fork_count"] == 2
        assert len(result[0]["children"]) == 1
        assert result[0]["children"][0]["command"] == ["nvidia-smi"]

    def test_many_forks_collapsed(self):
        """Many fork-only children (like PyTorch workers) should collapse to one count."""
        # Simulate 22,000+ PyTorch data loader workers
        processes = [{"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]}]
        for i in range(22000):
            processes.append(
                {"pid": 1001 + i, "parent_pid": 1000, "command": ["python", "train.py"]}
            )

        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["python", "train.py"]
        assert result[0]["fork_count"] == 22000
        assert "children" not in result[0]

    def test_nested_exec(self):
        """Child execs, then grandchild execs."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["bash", "run.sh"]},
            {"pid": 1001, "parent_pid": 1000, "command": ["python", "train.py"]},
            {"pid": 1002, "parent_pid": 1001, "command": ["nvidia-smi"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["bash", "run.sh"]
        assert len(result[0]["children"]) == 1
        child = result[0]["children"][0]
        assert child["command"] == ["python", "train.py"]
        assert len(child["children"]) == 1
        assert child["children"][0]["command"] == ["nvidia-smi"]

    def test_fork_then_exec_grandchild(self):
        """Fork-only child that has an exec'd grandchild."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]},
            # Fork-only child
            {"pid": 1001, "parent_pid": 1000, "command": ["python", "train.py"]},
            # Grandchild that exec'd
            {"pid": 1002, "parent_pid": 1001, "command": ["nvidia-smi"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["python", "train.py"]
        assert result[0]["fork_count"] == 1
        # The nvidia-smi grandchild should be promoted to children
        assert len(result[0]["children"]) == 1
        assert result[0]["children"][0]["command"] == ["nvidia-smi"]

    def test_shell_script_tree(self):
        """Realistic shell script that runs multiple commands."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["bash", "train.sh"]},
            {"pid": 1001, "parent_pid": 1000, "command": ["python", "preprocess.py"]},
            {"pid": 1002, "parent_pid": 1000, "command": ["python", "train.py"]},
            {"pid": 1003, "parent_pid": 1000, "command": ["python", "evaluate.py"]},
        ]
        result = _summarize_process_tree(processes)
        assert len(result) == 1
        assert result[0]["command"] == ["bash", "train.sh"]
        assert len(result[0]["children"]) == 3
        commands = [c["command"] for c in result[0]["children"]]
        assert ["python", "preprocess.py"] in commands
        assert ["python", "train.py"] in commands
        assert ["python", "evaluate.py"] in commands

    def test_pids_not_in_output(self):
        """PIDs should not appear in the summarized output."""
        processes = [
            {"pid": 1000, "parent_pid": None, "command": ["python", "train.py"]},
            {"pid": 1001, "parent_pid": 1000, "command": ["nvidia-smi"]},
        ]
        result = _summarize_process_tree(processes)

        # Check recursively that no PIDs
        def check_no_pids(node):
            assert "pid" not in node
            assert "parent_pid" not in node
            for child in node.get("children", []):
                check_no_pids(child)

        for node in result:
            check_no_pids(node)


from roar.core.models.provenance import PythonInjectData  # noqa: E402


class TestPythonInjectDataValidation:
    """Tests for PythonInjectData model validation."""

    def test_used_packages_accepts_none_values(self):
        """used_packages should accept None values for packages without version metadata.

        This reproduces the real-world scenario where sitecustomize.py sets None
        for packages installed via 'maturin develop' or similar tools that don't
        have proper metadata.
        """
        # This should NOT raise a ValidationError
        data = PythonInjectData(used_packages={"numpy": "1.24.0", "typing_extensions": None})
        assert data.used_packages == {"numpy": "1.24.0", "typing_extensions": None}
