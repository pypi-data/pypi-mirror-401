"""
Sync domain models.

Provides Pydantic models for live sync state management.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import RoarBaseModel


class SyncState(RoarBaseModel):
    """State tracking for sync thread.

    Tracks the current state of a running sync thread including
    job information and I/O counts.
    """

    job_uid: str
    session_hash: str
    start_time: Annotated[float, Field(gt=0)]
    last_input_count: int = -1
    last_output_count: int = -1
    last_telemetry: str | None = None
    sync_interval: Annotated[float, Field(ge=1.0)] = 15.0
    heartbeat_interval: Annotated[float, Field(ge=10.0)] = 60.0


class SyncManagerState(RoarBaseModel):
    """State for sync manager.

    Tracks the overall sync manager state including session information.
    """

    session_hash: str | None = None
    session_url: str | None = None
    enabled: bool = False
