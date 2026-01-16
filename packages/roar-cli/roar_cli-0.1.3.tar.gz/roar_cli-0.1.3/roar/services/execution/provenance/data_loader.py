"""
Data loader service for provenance collection.

Loads tracer JSON output and Python inject data with proper error handling.
"""

import json
import os
import sys

from ....core.interfaces.provenance import PythonInjectData, TracerData


class DataLoaderService:
    """Loads tracer and Python inject data from JSON files."""

    def load_tracer_data(self, path: str) -> TracerData:
        """
        Load tracer JSON output.

        Args:
            path: Path to the tracer JSON file

        Returns:
            TracerData with parsed values

        Raises:
            FileNotFoundError: If the tracer file doesn't exist
            json.JSONDecodeError: If the file is not valid JSON
        """
        with open(path) as f:
            data = json.load(f)

        return TracerData(
            opened_files=data.get("opened_files", []),
            read_files=data.get("read_files", []),
            written_files=data.get("written_files", []),
            processes=data.get("processes", []),
            start_time=data.get("start_time", 0),
            end_time=data.get("end_time", 0),
        )

    def load_python_data(self, path: str | None) -> PythonInjectData:
        """
        Load Python inject JSON output (optional).

        Args:
            path: Path to the Python inject JSON file, or None

        Returns:
            PythonInjectData with parsed values (defaults if file missing/invalid)
        """
        if not path or not os.path.exists(path):
            return PythonInjectData(
                sys_prefix=sys.prefix,
                sys_base_prefix=sys.base_prefix,
            )

        try:
            with open(path) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return PythonInjectData(
                sys_prefix=sys.prefix,
                sys_base_prefix=sys.base_prefix,
            )

        return PythonInjectData(
            modules_files=data.get("modules_files", []),
            env_reads=data.get("env_reads", {}),
            sys_prefix=data.get("sys_prefix", sys.prefix),
            sys_base_prefix=data.get("sys_base_prefix", sys.base_prefix),
            roar_inject_dir=data.get("roar_inject_dir", ""),
            shared_libs=data.get("shared_libs", []),
            used_packages=data.get("used_packages", {}),
            installed_packages=data.get("installed_packages", {}),
        )
