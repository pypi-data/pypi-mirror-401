"""
Configuration models.

Provides Pydantic models for roar configuration with validation.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field, field_validator

from .base import RoarBaseModel

# Type aliases
HashAlgorithm = Literal["blake3", "sha256", "sha512", "md5"]
LogLevel = Literal["debug", "info", "warning", "error"]


class OutputConfig(RoarBaseModel):
    """Output configuration section."""

    track_repo_files: bool = False
    quiet: bool = False


class AnalyzersConfig(RoarBaseModel):
    """Analyzers configuration section."""

    experiment_tracking: bool = True


class FiltersConfig(RoarBaseModel):
    """File filtering configuration section."""

    ignore_system_reads: bool = True
    ignore_package_reads: bool = True
    ignore_torch_cache: bool = True
    ignore_tmp_files: bool = True


class CleanupConfig(RoarBaseModel):
    """Cleanup configuration section."""

    delete_tmp_writes: bool = False


class LaasConfig(RoarBaseModel):
    """LaaS server configuration section."""

    url: Annotated[str, Field(max_length=2048)] | None = None

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        """Validate and normalize LaaS URL."""
        if v is None or v == "":
            return None
        if not v.startswith(("http://", "https://")):
            raise ValueError("LaaS URL must start with http:// or https://")
        return v.rstrip("/")


class SyncConfig(RoarBaseModel):
    """Sync configuration section."""

    enabled: bool = False


class HashConfig(RoarBaseModel):
    """Hash algorithm configuration section."""

    primary: HashAlgorithm = "blake3"
    get: list[HashAlgorithm] = Field(default_factory=lambda: ["sha256"])  # type: ignore[arg-type]
    put: list[HashAlgorithm] = Field(default_factory=list)
    run: list[HashAlgorithm] = Field(default_factory=list)

    @field_validator("get", "put", "run", mode="before")
    @classmethod
    def parse_comma_separated(cls, v: Any) -> list[str]:
        """Parse comma-separated string to list."""
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v if v else []


class LoggingConfig(RoarBaseModel):
    """Logging configuration section."""

    level: LogLevel = "warning"
    console: bool = False
    file: bool = True


class RoarConfig(RoarBaseModel):
    """Complete roar configuration.

    This model represents the full configuration with all sections.
    It can be loaded from TOML files or constructed programmatically.
    """

    model_config = RoarBaseModel.model_config.copy()
    model_config["extra"] = "ignore"

    output: OutputConfig = Field(default_factory=OutputConfig)
    analyzers: AnalyzersConfig = Field(default_factory=AnalyzersConfig)
    filters: FiltersConfig = Field(default_factory=FiltersConfig)
    cleanup: CleanupConfig = Field(default_factory=CleanupConfig)
    laas: LaasConfig = Field(default_factory=LaasConfig)
    sync: SyncConfig = Field(default_factory=SyncConfig)
    hash: HashConfig = Field(default_factory=HashConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot-notation key.

        Args:
            key: Dot-notation key (e.g., 'output.quiet')
            default: Default value if key not found

        Returns:
            Config value or default
        """
        parts = key.split(".")
        obj: Any = self
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return default
        return obj

    def set(self, key: str, value: Any) -> None:
        """Set config value by dot-notation key.

        Args:
            key: Dot-notation key (e.g., 'output.quiet')
            value: Value to set

        Raises:
            ValueError: If key path is invalid
        """
        parts = key.split(".")
        if len(parts) != 2:
            raise ValueError(f"Invalid config key: {key}")

        section, field = parts
        if not hasattr(self, section):
            raise ValueError(f"Unknown config section: {section}")

        section_obj = getattr(self, section)
        if not hasattr(section_obj, field):
            raise ValueError(f"Unknown config field: {key}")

        setattr(section_obj, field, value)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RoarConfig:
        """Create config from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            RoarConfig instance
        """
        return cls.model_validate(data)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary.

        Returns:
            Configuration as nested dict
        """
        return self.model_dump()
