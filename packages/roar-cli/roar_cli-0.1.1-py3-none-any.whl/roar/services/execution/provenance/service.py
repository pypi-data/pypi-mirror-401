"""
Provenance service orchestrator.

Coordinates all provenance collection services to produce the final output.
"""

from datetime import datetime, timezone
from typing import Any

from .... import analyzers
from ....core.container import get_container
from ....core.interfaces.provenance import (
    IDataLoader,
    IFileFilterService,
    IPackageCollector,
    IProcessSummarizer,
    IProvenanceAssembler,
    IRuntimeCollector,
    ProvenanceContext,
)
from ....filters import FileClassifier
from .assembler import ProvenanceAssemblerService
from .data_loader import DataLoaderService
from .file_filter import FileFilterService
from .package_collector import PackageCollectorService
from .process_summarizer import ProcessSummarizerService
from .runtime_collector import RuntimeCollectorService


class ProvenanceService:
    """
    Main orchestrator for provenance collection.

    Coordinates:
    - Loading tracer and Python-specific data
    - Running filters to classify files
    - Running analyzers for hygiene checks
    - Assembling the final provenance output
    """

    def __init__(
        self,
        data_loader: IDataLoader | None = None,
        file_filter: IFileFilterService | None = None,
        runtime_collector: IRuntimeCollector | None = None,
        process_summarizer: IProcessSummarizer | None = None,
        package_collector: IPackageCollector | None = None,
        assembler: IProvenanceAssembler | None = None,
    ):
        """
        Initialize the provenance service with optional dependencies.

        Args:
            data_loader: Service for loading JSON data (default: DataLoaderService)
            file_filter: Service for filtering files (default: FileFilterService)
            runtime_collector: Service for runtime info (default: RuntimeCollectorService)
            process_summarizer: Service for process tree (default: ProcessSummarizerService)
            package_collector: Service for packages (default: PackageCollectorService)
            assembler: Service for output assembly (default: ProvenanceAssemblerService)
        """
        self._data_loader = data_loader or DataLoaderService()
        self._file_filter = file_filter or FileFilterService()
        self._runtime_collector = runtime_collector or RuntimeCollectorService()
        self._process_summarizer = process_summarizer or ProcessSummarizerService()
        self._package_collector = package_collector or PackageCollectorService()
        self._assembler = assembler or ProvenanceAssemblerService()

    def collect(
        self,
        repo_root: str,
        tracer_log_path: str,
        python_log_path: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Collect provenance from tracer output and optional Python-specific log.

        Args:
            repo_root: Path to the git repository root
            tracer_log_path: Path to the Rust tracer's JSON output
            python_log_path: Optional path to Python sitecustomize.py output
            config: Optional configuration dict (from .roar.toml)

        Returns:
            Complete provenance dict
        """
        config = config or {}

        # 1. Load data
        tracer_data = self._data_loader.load_tracer_data(tracer_log_path)
        python_data = self._data_loader.load_python_data(python_log_path)

        # 2. Filter files
        filtered_files = self._file_filter.filter_files(tracer_data, python_data, config)

        # 3. Build timing info
        timing = self._build_timing(tracer_data.start_time, tracer_data.end_time)

        # 4. Collect runtime info
        runtime_info = self._runtime_collector.collect(python_data, tracer_data, timing)

        # 5. Summarize processes
        process_info = self._build_process_info(tracer_data.processes)
        process_summary = self._process_summarizer.summarize(process_info)

        # 6. Classify files (via FileClassifier)
        all_files = list(
            set(
                filtered_files.opened_files
                + filtered_files.read_files
                + filtered_files.modules_files
            )
        )
        classifier = FileClassifier(
            repo_root=repo_root,
            sys_prefix=python_data.sys_prefix,
            sys_base_prefix=python_data.sys_base_prefix,
            roar_inject_dir=python_data.roar_inject_dir,
        )
        classification = classifier.classify_all(all_files)

        # 7. Get git info (via VCS provider)
        git_info = self._get_git_info(repo_root)

        # 8. Collect packages
        packages: dict[str, dict[str, str | None]] = self._package_collector.collect(  # type: ignore[assignment]
            python_data,
            python_data.shared_libs,
            python_data.sys_prefix,
        )
        # Merge with classification packages if needed
        if not packages.get("pip") and classification.get("packages"):
            packages["pip"] = classification["packages"]

        # 9. Run analyzers
        analyzer_context = {
            "repo_root": repo_root,
            "written_files": filtered_files.written_files,
            "read_files": filtered_files.read_files,
            "env": python_data.env_reads or self._get_env_from_processes(tracer_data.processes),
            "processes": process_info,
            "tracer_data": {
                "opened_files": tracer_data.opened_files,
                "read_files": tracer_data.read_files,
                "written_files": tracer_data.written_files,
                "processes": tracer_data.processes,
                "start_time": tracer_data.start_time,
                "end_time": tracer_data.end_time,
            },
            "python_data": {
                "modules_files": python_data.modules_files,
                "env_reads": python_data.env_reads,
                "sys_prefix": python_data.sys_prefix,
                "sys_base_prefix": python_data.sys_base_prefix,
                "roar_inject_dir": python_data.roar_inject_dir,
                "shared_libs": python_data.shared_libs,
                "used_packages": python_data.used_packages,
                "installed_packages": python_data.installed_packages,
            },
        }
        analyzer_results = analyzers.run_analyzers(analyzer_context, config=config)

        # 10. Assemble output
        ctx = ProvenanceContext(
            repo_root=repo_root,
            tracer_data=tracer_data,
            python_data=python_data,
            filtered_files=filtered_files,
            runtime_info=runtime_info,
            process_summary=process_summary,
            classification=classification,
            git_info=git_info,
            packages=packages,
            analyzer_results=analyzer_results,
        )

        return self._assembler.assemble(ctx, config)

    def _build_timing(self, start_time: float, end_time: float) -> dict[str, Any]:
        """Build timing info dict from timestamps."""
        if not start_time or not end_time:
            return {}

        return {
            "start": datetime.fromtimestamp(start_time, tz=timezone.utc).isoformat(),
            "end": datetime.fromtimestamp(end_time, tz=timezone.utc).isoformat(),
            "duration_seconds": end_time - start_time,
        }

    def _build_process_info(self, processes: list) -> list:
        """Build process info list for summarization."""
        process_info = []
        for proc in processes:
            process_info.append(
                {
                    "pid": proc.get("pid"),
                    "parent_pid": proc.get("parent_pid"),
                    "command": proc.get("command", []),
                }
            )
        return process_info

    def _get_git_info(self, repo_root: str) -> dict[str, Any]:
        """Get git info via VCS provider."""
        vcs = get_container().get_vcs_provider("git")
        vcs_info = vcs.get_info(repo_root)

        return {
            "commit": vcs_info.commit,
            "branch": vcs_info.branch,
            "remote_url": vcs_info.remote_url,
            "clean": vcs_info.clean,
            "uncommitted_changes": vcs_info.uncommitted_changes if not vcs_info.clean else None,
            "commit_timestamp": vcs_info.commit_timestamp,
            "commit_message": vcs_info.commit_message,
        }

    def _get_env_from_processes(self, processes: list) -> dict[str, str]:
        """Get environment from root process if Python data unavailable."""
        if not processes:
            return {}

        root_proc = next((p for p in processes if p.get("parent_pid") is None), None)
        if root_proc:
            return root_proc.get("env", {})
        return {}
