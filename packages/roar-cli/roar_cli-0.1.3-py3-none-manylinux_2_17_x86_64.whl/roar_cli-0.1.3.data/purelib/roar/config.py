"""Configuration loading and management for roar."""

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


DEFAULT_CONFIG = {
    "output": {
        "track_repo_files": False,  # Include list of repo files read in provenance
        "quiet": False,  # Suppress written files report
    },
    "analyzers": {
        "experiment_tracking": True,  # Detect experiment trackers (W&B, MLflow, etc.)
    },
    "filters": {
        "ignore_system_reads": True,  # Ignore /sys, /etc, /sbin reads (system introspection)
        "ignore_package_reads": True,  # Ignore reads from installed packages (in dependency list)
        "ignore_torch_cache": True,  # Ignore torchinductor/triton cache reads
        "ignore_tmp_files": True,  # Ignore /tmp files entirely (overridden by strict mode)
    },
    "cleanup": {
        "delete_tmp_writes": False,  # Delete /tmp files written during run (strict mode)
    },
    "laas": {
        "url": None,  # LaaS server URL
        "key": None,  # SSH private key path (defaults to ~/.ssh/id_ed25519 etc.)
    },
    "sync": {
        "enabled": False,  # Live sync to LaaS during roar run
    },
    "hash": {
        "primary": "blake3",  # Primary hash algorithm, always computed
        "get": ["sha256"],  # Additional algorithms for roar get (external data verification)
        "put": [],  # Additional algorithms for roar put/upload
        "run": [],  # Additional algorithms for roar run
    },
    "logging": {
        "level": "warning",  # Log level: debug, info, warning, error
        "console": False,  # Output logs to stderr
        "file": True,  # Output logs to ~/.roar/roar.log
    },
}

# Valid hash algorithms
VALID_HASH_ALGORITHMS = {"blake3", "sha256", "sha512", "md5"}

# Config keys that can be set via `roar config`
CONFIGURABLE_KEYS = {
    "output.track_repo_files": {
        "type": bool,
        "default": False,
        "description": "Include list of repo files read in provenance output",
    },
    "analyzers.experiment_tracking": {
        "type": bool,
        "default": True,
        "description": "Detect experiment trackers (W&B, MLflow, Neptune)",
    },
    "filters.ignore_system_reads": {
        "type": bool,
        "default": True,
        "description": "Ignore system file reads (/sys, /etc, /sbin)",
    },
    "filters.ignore_package_reads": {
        "type": bool,
        "default": True,
        "description": "Ignore reads from installed packages (already in dependency list)",
    },
    "filters.ignore_torch_cache": {
        "type": bool,
        "default": True,
        "description": "Ignore torch/triton cache reads (/tmp/torchinductor_*, etc.)",
    },
    "filters.ignore_tmp_files": {
        "type": bool,
        "default": True,
        "description": "Ignore /tmp files entirely (overridden by strict mode)",
    },
    "output.quiet": {
        "type": bool,
        "default": False,
        "description": "Suppress written files report after run",
    },
    "cleanup.delete_tmp_writes": {
        "type": bool,
        "default": False,
        "description": "Delete /tmp files written during run (strict mode)",
    },
    "laas.url": {
        "type": str,
        "default": None,
        "description": "LaaS server URL (e.g., https://laas.example.com)",
    },
    "laas.key": {
        "type": str,
        "default": None,
        "description": "Path to SSH private key for LaaS authentication",
    },
    "sync.enabled": {
        "type": bool,
        "default": False,
        "description": "Enable live sync to LaaS server during roar run",
    },
    "hash.primary": {
        "type": str,
        "default": "blake3",
        "description": "Primary hash algorithm (blake3, sha256, sha512, md5)",
    },
    "hash.get": {
        "type": list,
        "default": ["sha256"],
        "description": "Additional algorithms for roar get (comma-separated)",
    },
    "hash.put": {
        "type": list,
        "default": [],
        "description": "Additional algorithms for roar put/upload (comma-separated)",
    },
    "hash.run": {
        "type": list,
        "default": [],
        "description": "Additional algorithms for roar run (comma-separated)",
    },
    "logging.level": {
        "type": str,
        "default": "warning",
        "description": "Log level (debug, info, warning, error)",
    },
    "logging.console": {
        "type": bool,
        "default": False,
        "description": "Output debug logs to stderr",
    },
    "logging.file": {
        "type": bool,
        "default": True,
        "description": "Output debug logs to ~/.roar/roar.log",
    },
}


def find_config_file(start_dir: str | None = None) -> Path | None:
    """
    Find .roar/config.toml by walking up from start_dir (or cwd).

    Returns:
        Path to config file, or None if not found.
    """
    start = Path(start_dir) if start_dir else Path.cwd()

    for parent in [start, *list(start.parents)]:
        # Check for .roar/config.toml
        config_path = parent / ".roar" / "config.toml"
        if config_path.exists():
            return config_path

        # Also check for pyproject.toml with [tool.roar] section
        pyproject = parent / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                if "tool" in data and "roar" in data["tool"]:
                    return pyproject
            except Exception:
                pass

    return None


def _deep_copy_defaults():
    """Deep copy default config to avoid mutation."""
    import copy

    return copy.deepcopy(DEFAULT_CONFIG)


def _get_nested(d: dict, key: str, default=None):
    """Get a nested key like 'output.track_repo_files'."""
    parts = key.split(".")
    for part in parts:
        if isinstance(d, dict) and part in d:
            d = d[part]
        else:
            return default
    return d


def _set_nested(d: dict, key: str, value):
    """Set a nested key like 'output.track_repo_files'."""
    parts = key.split(".")
    for part in parts[:-1]:
        if part not in d:
            d[part] = {}
        d = d[part]
    d[parts[-1]] = value


def load_config(config_path: Path | None = None, start_dir: str | None = None) -> dict:
    """
    Load configuration from file.

    Args:
        config_path: Explicit path to config file
        start_dir: Directory to start searching from (if config_path not given)

    Returns:
        Configuration dict with defaults applied
    """
    config = _deep_copy_defaults()

    if config_path is None:
        config_path = find_config_file(start_dir)

    if config_path is None:
        return config

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        # Handle pyproject.toml vs .roar.toml
        if config_path.name == "pyproject.toml":
            data = data.get("tool", {}).get("roar", {})

        # Merge with defaults
        if "output" in data:
            config["output"].update(data["output"])
        if "analyzers" in data:
            config["analyzers"].update(data["analyzers"])
        if "filters" in data:
            config["filters"].update(data["filters"])
        if "cleanup" in data:
            config["cleanup"].update(data["cleanup"])
        if "laas" in data:
            if "laas" not in config:
                config["laas"] = {}
            config["laas"].update(data["laas"])
        if "sync" in data:
            config["sync"].update(data["sync"])
        if "hash" in data:
            config["hash"].update(data["hash"])
        if "logging" in data:
            config["logging"].update(data["logging"])

        # Store where we loaded from
        config["_config_file"] = str(config_path)

    except Exception as e:
        # Config errors shouldn't break roar
        config["_config_error"] = str(e)

    return config


def get_roar_dir(start_dir: str | None = None) -> Path:
    """
    Get the .roar directory path, creating it if needed.

    Returns:
        Path to .roar directory in start_dir or cwd.
    """
    base = Path(start_dir) if start_dir else Path.cwd()
    roar_dir = base / ".roar"
    roar_dir.mkdir(exist_ok=True)
    return roar_dir


def get_config_path_for_write(start_dir: str | None = None) -> Path:
    """
    Get the path where config should be written.

    Prefers existing .roar/config.toml, otherwise creates one in start_dir or cwd.
    """
    existing = find_config_file(start_dir)
    if existing and existing.name == "config.toml":
        return existing

    # Create new .roar/config.toml in start_dir or cwd
    roar_dir = get_roar_dir(start_dir)
    return roar_dir / "config.toml"


def save_config(config: dict, config_path: Path):
    """
    Save configuration to a .roar.toml file.

    Only saves non-default values.
    """
    # Build TOML content manually (to avoid adding tomlkit dependency)
    lines = []

    defaults = _deep_copy_defaults()

    # Output section
    output_lines = []
    for key, val in config.get("output", {}).items():
        default_val = defaults.get("output", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                output_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                output_lines.append(f'{key} = "{val}"')
            else:
                output_lines.append(f"{key} = {val}")

    if output_lines:
        lines.append("[output]")
        lines.extend(output_lines)
        lines.append("")

    # Analyzers section
    analyzers_lines = []
    for key, val in config.get("analyzers", {}).items():
        default_val = defaults.get("analyzers", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                analyzers_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                analyzers_lines.append(f'{key} = "{val}"')
            else:
                analyzers_lines.append(f"{key} = {val}")

    if analyzers_lines:
        lines.append("[analyzers]")
        lines.extend(analyzers_lines)
        lines.append("")

    # Filters section
    filters_lines = []
    for key, val in config.get("filters", {}).items():
        default_val = defaults.get("filters", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                filters_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                filters_lines.append(f'{key} = "{val}"')
            else:
                filters_lines.append(f"{key} = {val}")

    if filters_lines:
        lines.append("[filters]")
        lines.extend(filters_lines)
        lines.append("")

    # Cleanup section
    cleanup_lines = []
    for key, val in config.get("cleanup", {}).items():
        default_val = defaults.get("cleanup", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                cleanup_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                cleanup_lines.append(f'{key} = "{val}"')
            else:
                cleanup_lines.append(f"{key} = {val}")

    if cleanup_lines:
        lines.append("[cleanup]")
        lines.extend(cleanup_lines)
        lines.append("")

    # LaaS section
    laas_lines = []
    for key, val in config.get("laas", {}).items():
        default_val = defaults.get("laas", {}).get(key)
        if val != default_val and val is not None:
            if isinstance(val, bool):
                laas_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                laas_lines.append(f'{key} = "{val}"')
            else:
                laas_lines.append(f"{key} = {val}")

    if laas_lines:
        lines.append("[laas]")
        lines.extend(laas_lines)
        lines.append("")

    # Sync section
    sync_lines = []
    for key, val in config.get("sync", {}).items():
        default_val = defaults.get("sync", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                sync_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                sync_lines.append(f'{key} = "{val}"')
            else:
                sync_lines.append(f"{key} = {val}")

    if sync_lines:
        lines.append("[sync]")
        lines.extend(sync_lines)
        lines.append("")

    # Hash section
    hash_lines = []
    for key, val in config.get("hash", {}).items():
        default_val = defaults.get("hash", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                hash_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                hash_lines.append(f'{key} = "{val}"')
            elif isinstance(val, list):
                # Format as TOML array
                items = ", ".join(f'"{v}"' for v in val)
                hash_lines.append(f"{key} = [{items}]")
            else:
                hash_lines.append(f"{key} = {val}")

    if hash_lines:
        lines.append("[hash]")
        lines.extend(hash_lines)
        lines.append("")

    # Logging section
    logging_lines = []
    for key, val in config.get("logging", {}).items():
        default_val = defaults.get("logging", {}).get(key)
        if val != default_val:
            if isinstance(val, bool):
                logging_lines.append(f"{key} = {str(val).lower()}")
            elif isinstance(val, str):
                logging_lines.append(f'{key} = "{val}"')
            else:
                logging_lines.append(f"{key} = {val}")

    if logging_lines:
        lines.append("[logging]")
        lines.extend(logging_lines)
        lines.append("")

    config_path.write_text("\n".join(lines))


def config_get(key: str, start_dir: str | None = None):
    """Get a config value."""
    config = load_config(start_dir=start_dir)
    return _get_nested(config, key)


def config_set(key: str, value: str, start_dir: str | None = None):
    """Set a config value and save to .roar.toml."""
    from typing import Any

    if key not in CONFIGURABLE_KEYS:
        raise ValueError(
            f"Unknown config key: {key}. Valid keys: {', '.join(CONFIGURABLE_KEYS.keys())}"
        )

    key_info = CONFIGURABLE_KEYS[key]
    typed_value: Any

    # Parse value to correct type
    if key_info["type"] is bool:  # type: ignore[index]
        if value.lower() in ("true", "1", "yes", "on"):
            typed_value = True
        elif value.lower() in ("false", "0", "no", "off"):
            typed_value = False
        else:
            raise ValueError(f"Invalid boolean value: {value}")
    elif key_info["type"] is list:  # type: ignore[index]
        # Parse comma-separated list
        if value.strip() == "":
            typed_value = []
        else:
            typed_value = [v.strip() for v in value.split(",")]
        # Validate hash algorithms if this is a hash config key
        if key.startswith("hash."):
            for algo in typed_value:
                if algo not in VALID_HASH_ALGORITHMS:
                    raise ValueError(
                        f"Invalid hash algorithm: {algo}. "
                        f"Valid algorithms: {', '.join(sorted(VALID_HASH_ALGORITHMS))}"
                    )
    elif key.startswith("hash.") and key_info["type"] is str:  # type: ignore[index]
        # Validate single hash algorithm
        if value not in VALID_HASH_ALGORITHMS:
            raise ValueError(
                f"Invalid hash algorithm: {value}. "
                f"Valid algorithms: {', '.join(sorted(VALID_HASH_ALGORITHMS))}"
            )
        typed_value = value
    else:
        typed_value = value

    # Load existing config, update, and save
    config = load_config(start_dir=start_dir)
    _set_nested(config, key, typed_value)

    config_path = get_config_path_for_write(start_dir)
    save_config(config, config_path)

    return config_path, typed_value


def config_list():
    """List all configurable keys with descriptions."""
    return CONFIGURABLE_KEYS


def get_hash_algorithms(
    operation: str,
    cli_algorithms: list | None = None,
    hash_only: bool = False,
    start_dir: str | None = None,
) -> list:
    """
    Get the list of hash algorithms to use for an operation.

    Args:
        operation: One of 'get', 'put', 'run'
        cli_algorithms: Algorithms specified via --hash or --hash-only CLI option
        hash_only: If True, use only cli_algorithms (skip primary and config)
        start_dir: Directory to load config from

    Returns:
        List of algorithm names to compute, deduplicated, primary first (unless hash_only)
    """
    if hash_only and cli_algorithms:
        # Validate and return only CLI-specified algorithms
        for algo in cli_algorithms:
            if algo not in VALID_HASH_ALGORITHMS:
                raise ValueError(
                    f"Invalid hash algorithm: {algo}. "
                    f"Valid algorithms: {', '.join(sorted(VALID_HASH_ALGORITHMS))}"
                )
        return cli_algorithms

    config = load_config(start_dir=start_dir)

    # Start with primary algorithm
    primary = config.get("hash", {}).get("primary", "blake3")
    algorithms = [primary]

    # Add operation-specific algorithms from config
    config_algos = config.get("hash", {}).get(operation, [])
    for algo in config_algos:
        if algo not in algorithms:
            algorithms.append(algo)

    # Add CLI-specified algorithms
    if cli_algorithms:
        for algo in cli_algorithms:
            if algo not in VALID_HASH_ALGORITHMS:
                raise ValueError(
                    f"Invalid hash algorithm: {algo}. "
                    f"Valid algorithms: {', '.join(sorted(VALID_HASH_ALGORITHMS))}"
                )
            if algo not in algorithms:
                algorithms.append(algo)

    return algorithms
