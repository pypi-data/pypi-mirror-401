"""Live sync functionality for roar run."""

import logging
import threading
import time
from collections.abc import Callable

from .laas_client import LaasClient, get_laas_url

logger = logging.getLogger(__name__)


class SyncThread:
    """Background thread for syncing job state to LaaS."""

    def __init__(
        self,
        job_uid: str,
        session_hash: str,
        laas_client: LaasClient,
        get_inputs: Callable[[], list],
        get_outputs: Callable[[], list],
        get_telemetry: Callable[[], str | None] | None = None,
        sync_interval: float = 15.0,
        heartbeat_interval: float = 60.0,
    ):
        """
        Initialize sync thread.

        Args:
            job_uid: The job's unique identifier
            session_hash: The session/DAG hash
            laas_client: LaaS client for API calls
            get_inputs: Callable returning current list of input paths
            get_outputs: Callable returning current list of output paths
            get_telemetry: Callable returning telemetry JSON string (optional)
            sync_interval: Seconds between full syncs (default 15)
            heartbeat_interval: Seconds between heartbeats (default 60)
        """
        self.job_uid = job_uid
        self.session_hash = session_hash
        self.client = laas_client
        self.get_inputs = get_inputs
        self.get_outputs = get_outputs
        self.get_telemetry = get_telemetry
        self.sync_interval = sync_interval
        self.heartbeat_interval = heartbeat_interval

        self.start_time = time.time()
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

        # Track what we've sent to avoid redundant updates
        # Use -1 to force first update
        self._last_input_count = -1
        self._last_output_count = -1
        self._last_telemetry = None

    def start(self):
        """Start the sync thread."""
        if self.thread is not None:
            return

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the sync thread."""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=2.0)

    def _run(self):
        """Main sync loop."""
        last_sync = 0
        last_heartbeat = 0

        # Initial sync immediately
        self._sync_job_state()
        last_sync = time.time()
        last_heartbeat = last_sync

        while not self.stop_event.wait(timeout=1.0):
            now = time.time()

            # Sync every sync_interval seconds
            if now - last_sync >= self.sync_interval:
                self._sync_job_state()
                last_sync = now
                last_heartbeat = now  # sync counts as heartbeat

            # Heartbeat every heartbeat_interval seconds (if no sync)
            elif now - last_heartbeat >= self.heartbeat_interval:
                self._send_heartbeat()
                last_heartbeat = now

    def _sync_job_state(self):
        """Sync current job state to LaaS."""
        try:
            inputs = self.get_inputs()
            outputs = self.get_outputs()

            # Build I/O lists with paths only (hashes computed at job completion)
            input_list = [{"path": path} for path in inputs]
            output_list = [{"path": path} for path in outputs]

            elapsed = time.time() - self.start_time

            # Get telemetry if callback provided
            telemetry = None
            if self.get_telemetry:
                telemetry = self.get_telemetry()

            # Check if there are any changes to send
            io_changed = (
                len(input_list) != self._last_input_count
                or len(output_list) != self._last_output_count
            )
            telemetry_changed = telemetry and telemetry != self._last_telemetry

            # Only send update if there are changes
            if io_changed or telemetry_changed:
                _result, error = self.client.update_live_job(
                    self.job_uid,
                    inputs=input_list,
                    outputs=output_list,
                    elapsed_seconds=elapsed,
                    telemetry=telemetry if telemetry_changed else None,
                )

                if error:
                    logger.warning(f"Sync failed: {error}")
                else:
                    self._last_input_count = len(input_list)
                    self._last_output_count = len(output_list)
                    if telemetry:
                        self._last_telemetry = telemetry

        except Exception as e:
            logger.warning(f"Sync error: {e}")

    def _send_heartbeat(self):
        """Send heartbeat to LaaS."""
        try:
            _result, error = self.client.heartbeat_job(self.job_uid)
            if error:
                logger.warning(f"Heartbeat failed: {error}")
        except Exception as e:
            logger.warning(f"Heartbeat error: {e}")


class SyncManager:
    """Manager for live sync during roar run."""

    def __init__(self):
        self.client: LaasClient | None = None
        self.session_hash: str | None = None
        self.session_url: str | None = None
        self.sync_thread: SyncThread | None = None
        self.enabled = False

    def initialize(
        self,
        session_hash: str,
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
    ) -> tuple[bool, str | None, str | None]:
        """
        Initialize sync manager and register session.

        Returns (success, session_url, error_message).
        """
        from .config import config_get

        # Check if sync is enabled
        if not config_get("sync.enabled"):
            return True, None, None

        laas_url = get_laas_url()
        if not laas_url:
            return True, None, None  # Silently skip if no LaaS configured

        self.client = LaasClient(laas_url)
        self.session_hash = session_hash

        # Register session
        result, error = self.client.register_session(
            session_hash,
            git_repo=git_repo,
            git_commit=git_commit,
            git_branch=git_branch,
        )

        if error:
            # Log warning but don't fail the run
            logger.warning(f"Failed to register session: {error}")
            return True, None, error

        self.session_url = result.get("url") if result else None
        if not self.session_url and laas_url:
            self.session_url = f"{laas_url.rstrip('/')}/sessions/{session_hash}"

        self.enabled = True
        return True, self.session_url, None

    def start_job(
        self,
        job_uid: str,
        command: str,
        step_number: int | None = None,
        job_type: str = "run",
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
        get_inputs: Callable[[], list] | None = None,
        get_outputs: Callable[[], list] | None = None,
        get_telemetry: Callable[[], str | None] | None = None,
    ) -> tuple[bool, str | None]:
        """
        Start tracking a live job.

        Returns (success, error_message).
        """
        if not self.enabled or not self.client or not self.session_hash:
            return True, None

        started_at = time.time()

        # Create live job on server
        _result, error = self.client.create_live_job(
            job_uid=job_uid,
            session_hash=self.session_hash,
            command=command,
            step_number=step_number,
            job_type=job_type,
            git_repo=git_repo,
            git_commit=git_commit,
            git_branch=git_branch,
            started_at=started_at,
        )

        if error:
            logger.warning(f"Failed to create live job: {error}")
            return True, error

        # Start sync thread if we have I/O callbacks
        if get_inputs and get_outputs:
            self.sync_thread = SyncThread(
                job_uid=job_uid,
                session_hash=self.session_hash,
                laas_client=self.client,
                get_inputs=get_inputs,
                get_outputs=get_outputs,
                get_telemetry=get_telemetry,
            )
            self.sync_thread.start()

        return True, None

    def complete_job(
        self,
        job_uid: str,
        exit_code: int,
        duration_seconds: float | None = None,
        inputs: list | None = None,
        outputs: list | None = None,
    ) -> tuple[bool, str | None]:
        """
        Mark a job as completed.

        Returns (success, error_message).
        """
        # Stop sync thread first
        if self.sync_thread:
            self.sync_thread.stop()
            self.sync_thread = None

        if not self.enabled or not self.client:
            return True, None

        _result, error = self.client.complete_live_job(
            job_uid=job_uid,
            exit_code=exit_code,
            duration_seconds=duration_seconds,
            inputs=inputs,
            outputs=outputs,
        )

        if error:
            logger.warning(f"Failed to complete live job: {error}")
            return True, error

        return True, None

    def shutdown(self):
        """Shutdown sync manager."""
        if self.sync_thread:
            self.sync_thread.stop()
            self.sync_thread = None


# Global sync manager instance
_sync_manager: SyncManager | None = None


def get_sync_manager() -> SyncManager:
    """Get or create the global sync manager."""
    global _sync_manager
    if _sync_manager is None:
        _sync_manager = SyncManager()
    return _sync_manager
