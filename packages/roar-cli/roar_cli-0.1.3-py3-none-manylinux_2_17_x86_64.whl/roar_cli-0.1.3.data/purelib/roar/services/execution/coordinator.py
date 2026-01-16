"""
Run coordinator service - main orchestrator for run/build execution.

Coordinates all services to execute commands with provenance tracking.
Follows SRP: coordinates, doesn't implement details.
"""

import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from ...core.interfaces.logger import ILogger
from ...core.interfaces.presenter import IPresenter
from ...core.interfaces.run import RunContext, RunResult
from .signal_handler import ProcessSignalHandler
from .tracer import TracerService


def _collect_telemetry(
    repo_root: str, start_time: float, end_time: float, allow_incomplete: bool = False
):
    """Collect telemetry from registered providers."""
    from ...core.container import get_container

    telemetry_data = {}
    try:
        container = get_container()
        providers = container.get_all_telemetry_providers()
        for name, provider in providers.items():
            if provider.is_available():
                runs = provider.detect_runs(repo_root, start_time, end_time)
                if runs:
                    urls = [run.url for run in runs if run.url]
                    if urls:
                        telemetry_data[name] = urls[0] if len(urls) == 1 else urls
    except Exception:
        pass  # Telemetry is best-effort

    return telemetry_data if telemetry_data else None


def _read_live_io(tracer_log_file: str) -> tuple:
    """Read current inputs/outputs from tracer log file."""
    from ...filters import filter_reads, filter_writes

    inputs = set()
    outputs = set()

    try:
        if not os.path.exists(tracer_log_file):
            return [], []

        with open(tracer_log_file) as f:
            content = f.read()
            if content.strip():
                try:
                    data = json.loads(content)
                    inputs = set(data.get("read_files", []))
                    outputs = set(data.get("written_files", []))
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass

    return filter_reads(list(inputs)), filter_writes(list(outputs))


class RunCoordinator:
    """
    Orchestrates the complete run lifecycle.

    Follows SRP: coordinates, doesn't implement details.
    Follows DIP: depends on service abstractions.
    Follows OCP: new features added via new services.
    """

    def __init__(
        self,
        tracer_service: TracerService | None = None,
        presenter: IPresenter | None = None,
        logger: ILogger | None = None,
    ) -> None:
        """
        Initialize run coordinator.

        Args:
            tracer_service: Service for process tracing
            presenter: Presenter for output
            logger: Logger for internal diagnostics
        """
        self._tracer = tracer_service or TracerService()
        self._presenter = presenter
        self._logger = logger

    @property
    def presenter(self) -> IPresenter:
        """Get presenter, creating default if needed."""
        if self._presenter is None:
            from ...presenters.console import ConsolePresenter

            self._presenter = ConsolePresenter()
        return self._presenter

    @property
    def logger(self) -> ILogger:
        """Get logger, resolving from container or creating NullLogger."""
        if self._logger is None:
            from ...core.container import get_container
            from ...services.logging import NullLogger

            container = get_container()
            self._logger = container.try_resolve(ILogger)  # type: ignore[type-abstract]
            if self._logger is None:
                self._logger = NullLogger()
        return self._logger

    def execute(self, ctx: RunContext) -> RunResult:
        """
        Execute a complete run with all tracking.

        Args:
            ctx: Run context with command and configuration

        Returns:
            RunResult with execution details
        """
        from ...config import config_get, load_config
        from .provenance import ProvenanceService

        start_time = time.time()
        is_build = ctx.job_type == "build"

        # Initialize sync manager if enabled
        sync_manager = None
        session_url = None
        job_uid_for_sync = None

        if config_get("sync.enabled"):
            sync_manager, session_url, job_uid_for_sync = self._init_sync(ctx, start_time)

        # Create signal handler
        signal_handler = ProcessSignalHandler(
            on_first_interrupt=lambda: self.logger.info(
                "Interrupted. Recording run... (Ctrl-C again to abort)"
            ),
        )

        # Execute via tracer
        try:
            tracer_result = self._tracer.execute(
                ctx.command,
                ctx.roar_dir,
                signal_handler,
            )
        except RuntimeError as e:
            # Tracer not found
            self.presenter.print_error(str(e))
            return RunResult(
                exit_code=1,
                job_id=0,
                job_uid="",
                duration=0,
                inputs=[],
                outputs=[],
                interrupted=False,
                is_build=is_build,
            )

        time.time()

        # Check if we should abort (double Ctrl-C)
        if signal_handler.should_abort():
            if sync_manager:
                sync_manager.shutdown()
            self._cleanup_logs(tracer_result.tracer_log_path, tracer_result.inject_log_path)
            sys.exit(130)

        # Stop live sync thread (completion with hashes happens after provenance collection)
        if sync_manager and sync_manager.sync_thread:
            sync_manager.sync_thread.stop()
            sync_manager.sync_thread = None

        # Load configuration
        config = load_config(start_dir=ctx.repo_root)

        # Check if tracer log exists
        if not os.path.exists(tracer_result.tracer_log_path):
            self.logger.warning("Tracer log not found at %s", tracer_result.tracer_log_path)
            self.logger.warning("The tracer may have failed to start. Run was not recorded.")
            self._cleanup_logs(tracer_result.tracer_log_path, tracer_result.inject_log_path)
            return RunResult(
                exit_code=tracer_result.exit_code,
                job_id=0,
                job_uid="",
                duration=tracer_result.duration,
                inputs=[],
                outputs=[],
                interrupted=tracer_result.interrupted,
                is_build=is_build,
            )

        # Collect provenance
        inject_log = (
            tracer_result.inject_log_path if os.path.exists(tracer_result.inject_log_path) else None
        )
        provenance_service = ProvenanceService()
        prov = provenance_service.collect(
            ctx.repo_root,
            tracer_result.tracer_log_path,
            inject_log,
            config,
        )

        # Record in database
        job_id, job_uid, read_file_info, written_file_info, stale_upstream, stale_downstream = (
            self._record_job(ctx, prov, tracer_result, start_time, is_build)
        )

        # Warn about external inputs for build steps
        if is_build:
            self._warn_external_inputs(prov, ctx.repo_root)

        # Complete sync with final hashed I/O
        if sync_manager and sync_manager.enabled and job_uid_for_sync:
            self._complete_sync(
                sync_manager,
                job_uid_for_sync,
                tracer_result,
                read_file_info,
                written_file_info,
                prov,
            )

        # Cleanup temp files
        self._cleanup_logs(tracer_result.tracer_log_path, tracer_result.inject_log_path)

        return RunResult(
            exit_code=tracer_result.exit_code,
            job_id=job_id,
            job_uid=job_uid,
            duration=tracer_result.duration,
            inputs=read_file_info,
            outputs=written_file_info,
            interrupted=tracer_result.interrupted,
            is_build=is_build,
            session_url=session_url,
            stale_upstream=stale_upstream,
            stale_downstream=stale_downstream,
        )

    def _init_sync(self, ctx: RunContext, start_time: float) -> tuple:
        """Initialize live sync if enabled."""
        from ...db.context import create_database_context
        from ...sync import get_sync_manager

        sync_manager = get_sync_manager()
        session_url = None
        job_uid_for_sync = None

        # Get session hash from active session
        with create_database_context(ctx.roar_dir) as db_ctx:
            session = db_ctx.sessions.get_active()
            if not session:
                # Create a session if one doesn't exist
                db_ctx.sessions.create(
                    git_repo=ctx.git_repo,
                    git_commit=ctx.git_commit,
                    make_active=True,
                )
                session = db_ctx.sessions.get_active()

            if session:
                session_id_str = f"{ctx.roar_dir}:{session['id']}"
                session_hash = hashlib.sha256(session_id_str.encode()).hexdigest()
            else:
                session_hash = None

        if session_hash:
            _success, session_url, _sync_error = sync_manager.initialize(
                session_hash=session_hash,
                git_repo=ctx.git_repo,
                git_commit=ctx.git_commit,
                git_branch=ctx.git_branch,
            )

            if session_url:
                self.presenter.print(f"Session: {session_url}")
                self.presenter.print("")

            if sync_manager.enabled:
                job_uid_for_sync = uuid.uuid4().hex[:16]

                # Get step number from session
                with create_database_context(ctx.roar_dir) as db_ctx:
                    step_number = (
                        db_ctx.sessions.get_next_step_number(session["id"]) if session else None
                    )

                # Get tracer log path for live I/O
                tracer_log, _ = self._tracer.get_log_paths(ctx.roar_dir)

                # Create closures for live I/O callbacks
                def get_live_inputs():
                    inputs, _ = _read_live_io(tracer_log)
                    return inputs

                def get_live_outputs():
                    _, outputs = _read_live_io(tracer_log)
                    return outputs

                # Create closure for live telemetry with caching
                _cached_telemetry = [None]

                def get_live_telemetry():
                    if _cached_telemetry[0]:
                        return _cached_telemetry[0]
                    telemetry_data = _collect_telemetry(
                        ctx.repo_root, start_time, time.time(), allow_incomplete=True
                    )
                    if telemetry_data:
                        _cached_telemetry[0] = json.dumps(telemetry_data)
                    return _cached_telemetry[0]

                # Start live job
                sync_manager.start_job(
                    job_uid=job_uid_for_sync,
                    command=" ".join(ctx.command),
                    step_number=step_number,
                    job_type=ctx.job_type or "run",
                    git_repo=ctx.git_repo,
                    git_commit=ctx.git_commit,
                    git_branch=ctx.git_branch,
                    get_inputs=get_live_inputs,
                    get_outputs=get_live_outputs,
                    get_telemetry=get_live_telemetry,
                )

        return sync_manager, session_url, job_uid_for_sync

    def _record_job(
        self,
        ctx: RunContext,
        prov: dict[str, Any],
        tracer_result,
        start_time: float,
        is_build: bool,
    ) -> tuple:
        """Record job in database and return file info."""
        from ...db.context import create_database_context

        written_files = prov.get("data", {}).get("written_files", [])
        read_files = prov.get("data", {}).get("read_files", [])

        git_info = prov.get("executables", {}).get("code", {}).get("git", {})
        git_commit = git_info.get("commit")
        git_branch = git_info.get("branch")
        git_repo = git_info.get("remote_url")

        # Compute working directory relative to repo root
        cwd_relative = None
        try:
            cwd_relative = str(Path.cwd().relative_to(Path(ctx.repo_root)))
            if cwd_relative == ".":
                cwd_relative = ""
        except ValueError:
            pass

        # Build metadata from provenance
        metadata = {}
        if prov.get("executables", {}).get("packages"):
            metadata["packages"] = prov["executables"]["packages"]
        if prov.get("runtime"):
            metadata["runtime"] = prov["runtime"]
        if prov.get("analysis"):
            metadata["analysis"] = prov["analysis"]
        metadata["git"] = git_info
        if cwd_relative is not None:
            metadata["cwd"] = cwd_relative
        metadata_json = json.dumps(metadata) if metadata else None

        # Collect telemetry
        telemetry_data = _collect_telemetry(ctx.repo_root, start_time, time.time())
        telemetry_json = json.dumps(telemetry_data) if telemetry_data else None

        stale_upstream = []
        stale_downstream = []

        with create_database_context(ctx.roar_dir) as db_ctx:
            job_id, job_uid = db_ctx.job_recording.record_job(
                command=" ".join(ctx.command),
                timestamp=start_time,
                git_repo=git_repo,
                git_commit=git_commit,
                git_branch=git_branch,
                duration_seconds=tracer_result.duration,
                exit_code=tracer_result.exit_code,
                input_files=read_files,
                output_files=written_files,
                metadata=metadata_json,
                job_type=ctx.job_type,
                repo_root=ctx.repo_root,
                telemetry=telemetry_json,
                hash_algorithms=list(ctx.hash_algorithms),
            )

            # Get files with hashes for report
            written_file_info = db_ctx.jobs.get_outputs(job_id, db_ctx.artifacts)
            read_file_info = db_ctx.jobs.get_inputs(job_id, db_ctx.artifacts)

            # Check for stale steps
            session = db_ctx.sessions.get_active()
            if session:
                job = db_ctx.jobs.get(job_id)
                if job and job.get("step_number"):
                    step_num = job["step_number"]
                    stale = set(db_ctx.session_service.get_stale_steps(session["id"]))

                    # Check stale upstream
                    job_inputs = db_ctx.jobs.get_inputs(job_id, db_ctx.artifacts)
                    for inp in job_inputs:
                        artifact_hash = inp.get("artifact_hash")
                        if not artifact_hash:
                            continue
                        producer_jobs = db_ctx.artifacts.get_jobs(artifact_hash)
                        for pj in producer_jobs.get("produced_by", []):
                            producer_step = db_ctx.sessions.get_step_for_job(
                                session["id"], pj["id"]
                            )
                            if (
                                producer_step
                                and producer_step["step_number"] in stale
                                and producer_step["step_number"] not in stale_upstream
                            ):
                                stale_upstream.append(producer_step["step_number"])

                    # Check stale downstream
                    downstream = db_ctx.session_service.get_downstream_steps(
                        session["id"], step_num
                    )
                    stale_downstream = [s for s in downstream if s in stale]

        stale_upstream.sort()

        return job_id, job_uid, read_file_info, written_file_info, stale_upstream, stale_downstream

    def _warn_external_inputs(self, prov: dict[str, Any], repo_root: str) -> None:
        """Warn about external inputs for build steps."""
        read_files = prov.get("data", {}).get("read_files", [])
        if not read_files:
            return

        external_inputs = []
        for f in read_files:
            try:
                Path(f).relative_to(repo_root)
            except ValueError:
                external_inputs.append(f)

        if external_inputs:
            self.presenter.print("")
            self.presenter.print("Warning: Build step reads files outside the repository:")
            for f in external_inputs[:5]:
                self.presenter.print(f"  {f}")
            if len(external_inputs) > 5:
                self.presenter.print(f"  ... and {len(external_inputs) - 5} more")
            self.presenter.print("These files won't be available during reproduction.")
            self.presenter.print("")

    def _complete_sync(
        self,
        sync_manager,
        job_uid: str,
        tracer_result,
        read_file_info: list[dict],
        written_file_info: list[dict],
        prov: dict[str, Any],
    ) -> None:
        """Complete sync with final hashed I/O."""
        # Build I/O lists with hashes
        input_list = []
        for f in read_file_info:
            hashes = f.get("hashes", [])
            if not hashes and f.get("artifact_hash"):
                hashes = [{"algorithm": "blake3", "digest": f["artifact_hash"]}]
            input_list.append(
                {
                    "path": f["path"],
                    "hashes": hashes,
                    "size": f.get("size"),
                }
            )

        output_list = []
        for f in written_file_info:
            hashes = f.get("hashes", [])
            if not hashes and f.get("artifact_hash"):
                hashes = [{"algorithm": "blake3", "digest": f["artifact_hash"]}]
            output_list.append(
                {
                    "path": f["path"],
                    "hashes": hashes,
                    "size": f.get("size"),
                }
            )

        # Register all artifacts with LaaS
        all_artifacts = []
        for f in read_file_info + written_file_info:
            hashes = f.get("hashes", [])
            if not hashes and f.get("artifact_hash"):
                hashes = [{"algorithm": "blake3", "digest": f["artifact_hash"]}]
            if hashes and f.get("size"):
                all_artifacts.append(
                    {
                        "hashes": hashes,
                        "size": f["size"],
                    }
                )

        if all_artifacts:
            sync_manager.client.register_artifacts_batch(all_artifacts)

        # Build metadata
        git_info = prov.get("executables", {}).get("code", {}).get("git", {})
        metadata = {}
        if prov.get("executables", {}).get("packages"):
            metadata["packages"] = prov["executables"]["packages"]
        if prov.get("runtime"):
            metadata["runtime"] = prov["runtime"]
        if prov.get("analysis"):
            metadata["analysis"] = prov["analysis"]
        metadata["git"] = git_info
        metadata_json = json.dumps(metadata) if metadata else None

        # Get telemetry
        telemetry_data = _collect_telemetry(prov.get("repo_root", ""), 0, time.time())
        telemetry_json = json.dumps(telemetry_data) if telemetry_data else None

        # Complete the job
        sync_manager.client.complete_live_job(
            job_uid=job_uid,
            exit_code=tracer_result.exit_code,
            duration_seconds=tracer_result.duration,
            inputs=input_list,
            outputs=output_list,
            metadata=metadata_json,
            telemetry=telemetry_json,
        )

    def _cleanup_logs(self, tracer_log: str, inject_log: str) -> None:
        """Clean up temporary log files."""
        for log_file in [tracer_log, inject_log]:
            try:
                if log_file and os.path.exists(log_file):
                    os.remove(log_file)
            except OSError:
                pass
