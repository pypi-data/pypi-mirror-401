"""
Tracer service for process execution with file I/O tracking.

Handles tracer binary discovery and process execution via the tracer.
"""

import os
import subprocess
import time
from pathlib import Path

from ...core.interfaces.run import ISignalHandler, TracerResult


class TracerService:
    """
    Manages tracer discovery and execution.

    Follows SRP: only handles process tracing.
    Follows OCP: tracer discovery can be extended.
    """

    def __init__(self, package_path: Path | None = None) -> None:
        """
        Initialize tracer service.

        Args:
            package_path: Path to the roar package (for finding tracer binary)
        """
        # Go up 3 levels: execution -> services -> roar
        self._package_path = package_path or Path(__file__).parent.parent.parent

    def find_tracer(self) -> str | None:
        """
        Find the roar-tracer binary.

        Searches in:
        1. Development location (tracer/target/release/)
        2. Installed location (roar/bin/)
        3. System PATH

        Returns:
            Path to tracer binary, or None if not found
        """
        candidates = [
            # Development: relative to roar package
            self._package_path.parent / "tracer" / "target" / "release" / "roar-tracer",
            # Installed alongside roar package
            self._package_path / "bin" / "roar-tracer",
        ]

        for candidate in candidates:
            if candidate.exists():
                return str(candidate)

        # Check if it's in PATH
        result = subprocess.run(["which", "roar-tracer"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()

        return None

    def execute(
        self,
        command: list[str],
        roar_dir: Path,
        signal_handler: ISignalHandler,
    ) -> TracerResult:
        """
        Execute command with tracing.

        Args:
            command: Command and arguments to execute
            roar_dir: Path to .roar directory for log files
            signal_handler: Signal handler for interrupt management

        Returns:
            TracerResult with execution details

        Raises:
            RuntimeError: If tracer binary not found
        """
        tracer_path = self.find_tracer()
        if not tracer_path:
            raise RuntimeError(
                "roar-tracer binary not found. Please build it with:\n"
                "  cd roar/tracer && cargo build --release"
            )

        # Generate log file paths
        pid = os.getpid()
        tracer_log_file = str(roar_dir / f"run_{pid}_tracer.json")
        inject_log_file = str(roar_dir / f"run_{pid}_inject.json")

        # Update signal handler with log files for cleanup on abort
        signal_handler.set_log_files([tracer_log_file, inject_log_file])

        # Prepare environment for child process
        env = dict(os.environ)
        # inject/ is now in the same directory as this file
        inject_dir = str(Path(__file__).parent / "inject")
        env["PYTHONPATH"] = inject_dir + os.pathsep + env.get("PYTHONPATH", "")
        env["ROAR_LOG_FILE"] = inject_log_file

        # Build tracer command
        tracer_cmd = [tracer_path, tracer_log_file, *command]

        # Execute with signal handling
        start_time = time.time()
        signal_handler.install()

        try:
            proc = subprocess.Popen(tracer_cmd, env=env)
            exit_code = proc.wait()
        except KeyboardInterrupt:
            # This shouldn't happen since we handle SIGINT, but just in case
            exit_code = proc.wait()
        finally:
            signal_handler.restore()

        end_time = time.time()

        return TracerResult(
            exit_code=exit_code,
            duration=end_time - start_time,
            tracer_log_path=tracer_log_file,
            inject_log_path=inject_log_file,
            interrupted=signal_handler.is_interrupted(),
        )

    def get_log_paths(self, roar_dir: Path) -> tuple:
        """
        Get log file paths for a run.

        Args:
            roar_dir: Path to .roar directory

        Returns:
            Tuple of (tracer_log_path, inject_log_path)
        """
        pid = os.getpid()
        tracer_log = str(roar_dir / f"run_{pid}_tracer.json")
        inject_log = str(roar_dir / f"run_{pid}_inject.json")
        return tracer_log, inject_log
