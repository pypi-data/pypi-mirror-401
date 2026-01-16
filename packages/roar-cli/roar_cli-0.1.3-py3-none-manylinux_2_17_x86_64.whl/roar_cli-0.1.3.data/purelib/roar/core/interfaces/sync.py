"""
Sync service interface definitions.

Defines contracts for LaaS client and sync service operations.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class ILaasClient(ABC):
    """
    Interface for LaaS (Lineage-as-a-Service) server communication.

    Implementations handle HTTP communication with the LaaS server.
    """

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if LaaS is configured (URL and auth available)."""
        pass

    @abstractmethod
    def health_check(self) -> tuple[bool, str | None]:
        """
        Check server health.

        Returns:
            (healthy, error_message)
        """
        pass

    @abstractmethod
    def register_session(
        self,
        session_hash: str,
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Register a sync session with the server.

        Returns:
            (session_data, error_message)
        """
        pass

    @abstractmethod
    def create_live_job(
        self,
        session_hash: str,
        job_uid: str,
        command: str,
        timestamp: float,
        git_commit: str | None = None,
        git_branch: str | None = None,
        step_number: int | None = None,
        step_name: str | None = None,
        job_type: str | None = None,
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Create a live job on the server.

        Returns:
            (job_data, error_message)
        """
        pass

    @abstractmethod
    def complete_live_job(
        self,
        session_hash: str,
        job_uid: str,
        exit_code: int,
        duration_seconds: float,
        inputs: list[dict[str, Any]],
        outputs: list[dict[str, Any]],
        telemetry: str | None = None,
    ) -> tuple[dict[str, Any] | None, str | None]:
        """
        Mark a live job as complete.

        Returns:
            (result_data, error_message)
        """
        pass


class ISyncService(ABC):
    """
    Interface for sync management.

    Orchestrates synchronization of job data to LaaS server,
    including live monitoring and final upload.
    """

    @abstractmethod
    def initialize(
        self,
        session_hash: str,
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
    ) -> tuple[bool, str | None, str | None]:
        """
        Initialize sync.

        Args:
            session_hash: Unique session identifier
            git_repo: Optional git repository URL
            git_commit: Optional git commit hash
            git_branch: Optional git branch name

        Returns:
            (success, session_url, error)
        """
        pass

    @abstractmethod
    def start_job(
        self,
        job_uid: str,
        command: str,
        get_inputs: Callable[[], list[str]],
        get_outputs: Callable[[], list[str]],
        get_telemetry: Callable[[], str | None] | None = None,
        **kwargs: Any,
    ) -> tuple[bool, str | None]:
        """
        Start tracking a job.

        Args:
            job_uid: Unique job identifier
            command: Command being executed
            get_inputs: Callback to get current input files
            get_outputs: Callback to get current output files
            get_telemetry: Optional callback to get telemetry data
            **kwargs: Additional job metadata

        Returns:
            (success, error_message)
        """
        pass

    @abstractmethod
    def complete_job(
        self,
        job_uid: str,
        exit_code: int,
        **kwargs: Any,
    ) -> tuple[bool, str | None]:
        """
        Complete a job.

        Args:
            job_uid: Unique job identifier
            exit_code: Job exit code
            **kwargs: Additional completion data

        Returns:
            (success, error_message)
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown sync service and clean up resources."""
        pass
