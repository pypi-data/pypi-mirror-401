"""
Pydantic models for roar.

This package provides typed, validated models for all roar data structures.
All models use Pydantic v2 with strict validation.
"""

# Base models
# Core domain models
from .artifact import Artifact, ArtifactHash
from .base import ImmutableModel, RoarBaseModel
from .command import CommandContext, CommandResult

# Configuration models
from .config import (
    AnalyzersConfig,
    CleanupConfig,
    FiltersConfig,
    HashConfig,
    LaasConfig,
    LoggingConfig,
    OutputConfig,
    RoarConfig,
    SyncConfig,
)
from .job import Job, JobInput, JobOutput

# LaaS API models
from .laas import (
    ArtifactDagResponse,
    ArtifactHashRequest,
    ArtifactResponse,
    CheckTagRequest,
    CheckTagResponse,
    CompleteLiveJobRequest,
    CreateDagRequest,
    CreateLiveJobRequest,
    DagResponse,
    IOEntry,
    JobResponse,
    LineageResponse,
    LiveJobResponse,
    RecordTagRequest,
    RegisterArtifactRequest,
    RegisterArtifactsBatchRequest,
    RegisterJobRequest,
    RegisterJobsBatchRequest,
    RegisterSessionRequest,
    SessionResponse,
    UpdateLiveJobRequest,
)

# Provenance models
from .provenance import (
    ContainerInfo,
    FileClassification,
    FilteredFiles,
    GitInfo,
    HardwareInfo,
    PackageInfo,
    ProvenanceContext,
    PythonInjectData,
    RuntimeInfo,
    TracerData,
)

# Run/execution models
from .run import (
    ResolvedStep,
    RunArguments,
    RunContext,
    RunResult,
    TracerResult,
)

# Session models
from .session import Session

# Sync models
from .sync import SyncManagerState, SyncState

# Telemetry models
from .telemetry import TelemetryRunInfo

# VCS models
from .vcs import VCSInfo

__all__ = [
    "AnalyzersConfig",
    # Artifact
    "Artifact",
    "ArtifactDagResponse",
    "ArtifactHash",
    # LaaS API
    "ArtifactHashRequest",
    "ArtifactResponse",
    "CheckTagRequest",
    "CheckTagResponse",
    "CleanupConfig",
    # Command
    "CommandContext",
    "CommandResult",
    "CompleteLiveJobRequest",
    "ContainerInfo",
    "CreateDagRequest",
    "CreateLiveJobRequest",
    "DagResponse",
    "FileClassification",
    "FilteredFiles",
    "FiltersConfig",
    "GitInfo",
    "HardwareInfo",
    "HashConfig",
    "IOEntry",
    "ImmutableModel",
    # Job
    "Job",
    "JobInput",
    "JobOutput",
    "JobResponse",
    "LaasConfig",
    "LineageResponse",
    "LiveJobResponse",
    "LoggingConfig",
    "OutputConfig",
    "PackageInfo",
    "ProvenanceContext",
    "PythonInjectData",
    "RecordTagRequest",
    "RegisterArtifactRequest",
    "RegisterArtifactsBatchRequest",
    "RegisterJobRequest",
    "RegisterJobsBatchRequest",
    "RegisterSessionRequest",
    "ResolvedStep",
    # Base
    "RoarBaseModel",
    # Config
    "RoarConfig",
    # Run
    "RunArguments",
    "RunContext",
    "RunResult",
    "RuntimeInfo",
    # Session
    "Session",
    "SessionResponse",
    "SyncConfig",
    "SyncManagerState",
    # Sync
    "SyncState",
    # Telemetry
    "TelemetryRunInfo",
    # Provenance
    "TracerData",
    "TracerResult",
    "UpdateLiveJobRequest",
    # VCS
    "VCSInfo",
]
