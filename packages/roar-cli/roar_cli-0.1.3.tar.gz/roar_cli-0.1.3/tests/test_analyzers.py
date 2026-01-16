"""Tests for roar analyzers module."""

from roar.analyzers import get_analyzers, run_analyzers
from roar.analyzers.experiment_trackers import ExperimentTrackerAnalyzer


class TestAnalyzerRegistry:
    """Tests for analyzer registration."""

    def test_experiment_tracker_is_registered(self):
        analyzers = get_analyzers()
        names = [a.name for a in [cls() for cls in analyzers]]
        assert "experiment_tracking" in names

    def test_get_analyzers_returns_copy(self):
        a1 = get_analyzers()
        a2 = get_analyzers()
        assert a1 is not a2


class TestRunAnalyzers:
    """Tests for run_analyzers function."""

    def test_run_analyzers_empty_context(self):
        context = {
            "written_files": [],
            "read_files": [],
            "env": {},
            "processes": [],
        }
        results = run_analyzers(context)
        # No trackers detected, should be empty
        assert results == {}

    def test_run_analyzers_respects_config_disable(self):
        context = {
            "written_files": ["wandb/run-123/files/config.yaml"],
            "read_files": [],
            "env": {},
            "processes": [],
        }
        config = {"analyzers": {"experiment_tracking": False}}
        results = run_analyzers(context, config=config)
        assert "experiment_tracking" not in results

    def test_run_analyzers_respects_config_enable(self):
        context = {
            "written_files": ["wandb/run-123/files/config.yaml"],
            "read_files": [],
            "env": {},
            "processes": [],
        }
        config = {"analyzers": {"experiment_tracking": True}}
        results = run_analyzers(context, config=config)
        # Should run (though may not find actual files)
        assert "experiment_tracking" in results


class TestExperimentTrackerAnalyzer:
    """Tests for ExperimentTrackerAnalyzer."""

    def test_relevant_no_tracker_files(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {"written_files": ["/home/user/model.pt", "/home/user/data.csv"]}
        assert analyzer.relevant(context) is False

    def test_relevant_wandb_files(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {"written_files": ["wandb/run-123/files/config.yaml"]}
        assert analyzer.relevant(context) is True

    def test_relevant_mlflow_files(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {"written_files": ["mlruns/0/abc123/metrics/loss"]}
        assert analyzer.relevant(context) is True

    def test_relevant_neptune_files(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {"written_files": [".neptune/async/run-123/data.json"]}
        assert analyzer.relevant(context) is True

    def test_analyze_detects_wandb(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": ["wandb/run-20231201_120000-abc123/files/config.yaml"],
            "env": {},
        }
        result = analyzer.analyze(context)

        assert result is not None
        assert "wandb" in result["trackers_detected"]
        assert "wandb/*" in result["ignore_patterns"]

    def test_analyze_detects_mlflow(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": ["mlruns/0/abc123def456/metrics/loss"],
            "env": {},
        }
        result = analyzer.analyze(context)

        assert result is not None
        assert "mlflow" in result["trackers_detected"]
        assert "mlruns/*" in result["ignore_patterns"]

    def test_analyze_detects_multiple_trackers(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": [
                "wandb/run-123/files/config.yaml",
                "mlruns/0/abc123/metrics/loss",
            ],
            "env": {},
        }
        result = analyzer.analyze(context)

        assert result is not None
        assert "wandb" in result["trackers_detected"]
        assert "mlflow" in result["trackers_detected"]

    def test_analyze_returns_none_when_no_trackers(self):
        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": ["/home/user/output.txt"],
            "env": {},
        }
        # relevant() would return False, but if called anyway:
        result = analyzer.analyze(context)
        assert result is None


class TestExperimentTrackerWithStubs:
    """Tests using stub/mock tracker directories."""

    def test_wandb_metadata_extraction(self, temp_dir):
        """Test W&B metadata extraction with stub files."""
        # Create stub wandb directory structure
        wandb_dir = temp_dir / "wandb"
        run_dir = wandb_dir / "run-20231201_120000-abc123xyz"
        files_dir = run_dir / "files"
        files_dir.mkdir(parents=True)

        # Create stub metadata file
        import json

        metadata = {
            "run_id": "abc123xyz",
            "project": "my-project",
            "entity": "my-team",
        }
        (files_dir / "wandb-metadata.json").write_text(json.dumps(metadata))

        # Create latest-run symlink
        latest_run = wandb_dir / "latest-run"
        latest_run.symlink_to(run_dir)

        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": [str(files_dir / "wandb-metadata.json")],
            "env": {},
        }
        result = analyzer.analyze(context)

        assert result is not None
        assert "wandb" in result["trackers_detected"]
        assert len(result["runs"]) == 1

        run_info = result["runs"][0]
        assert run_info["tracker"] == "wandb"
        assert run_info["run_id"] == "abc123xyz"
        assert run_info["project"] == "my-project"
        assert run_info["entity"] == "my-team"
        assert "url" in run_info
        assert "wandb.ai" in run_info["url"]

    def test_mlflow_run_extraction(self, temp_dir):
        """Test MLflow run extraction with stub files."""
        # Create stub mlruns directory structure
        mlruns = temp_dir / "mlruns"
        exp_dir = mlruns / "0"
        run_dir = exp_dir / "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"  # 32 hex chars
        run_dir.mkdir(parents=True)

        analyzer = ExperimentTrackerAnalyzer()
        context = {
            "written_files": [str(run_dir / "metrics" / "loss")],
            "env": {"MLFLOW_TRACKING_URI": "http://localhost:5000"},
        }
        result = analyzer.analyze(context)

        assert result is not None
        assert "mlflow" in result["trackers_detected"]
        assert len(result["runs"]) == 1

        run_info = result["runs"][0]
        assert run_info["tracker"] == "mlflow"
        assert run_info["experiment_id"] == "0"
        assert run_info["run_id"] == "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
        assert "url" in run_info
        assert "localhost:5000" in run_info["url"]
