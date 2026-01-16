"""
Log command - Show recent jobs.

Usage: roar log [-n NUM] [-v]
"""

from datetime import datetime
from pathlib import Path

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


def format_timestamp(ts: float) -> str:
    """Format a timestamp for display."""
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: float | None) -> str:
    """Format duration in human-readable format."""
    if seconds is None:
        return "?"
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


class LogCommand(BaseCommand):
    """
    Show recent jobs.

    Displays the most recent jobs with their status, duration, and command.
    """

    @property
    def name(self) -> str:
        return "log"

    @property
    def help_text(self) -> str:
        return "Show recent jobs"

    @property
    def usage(self) -> str:
        return "roar log [-n NUM] [-v]"

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the log command."""
        # Check for help flag
        if self.has_flag(ctx, "-h", "--help"):
            self.print(self.get_help())
            return self.success()

        # Parse options
        limit = int(self.get_flag_value(ctx, "-n", "--limit", default="10") or "10")
        verbose = self.has_flag(ctx, "-v", "--verbose")

        with create_database_context(ctx.roar_dir) as ctx_db:
            jobs = ctx_db.jobs.get_recent(limit=limit)

            if not jobs:
                self.print("No jobs recorded yet.")
                self.print("")
                self.print("Run a command with: roar run <command>")
                return self.success()

            self.print(f"Recent jobs ({len(jobs)} shown):")
            self.print("")

            for job in jobs:
                self._print_job(job, ctx_db, ctx.cwd, verbose)

        return self.success()

    def _print_job(self, job: dict, ctx_db, cwd: Path, verbose: bool) -> None:
        """Print a single job entry."""
        job_id = job["id"]
        ts = format_timestamp(job["timestamp"])
        duration = format_duration(job.get("duration_seconds"))
        exit_code = job.get("exit_code", "?")
        command = job["command"]
        git_commit = job.get("git_commit", "")[:8] if job.get("git_commit") else ""

        # Truncate command if too long
        max_cmd_len = 60
        if len(command) > max_cmd_len:
            command = command[: max_cmd_len - 3] + "..."

        # Status indicator
        if exit_code == 0:
            status = "✓"
        elif exit_code is None or exit_code == "?":
            status = "?"
        else:
            status = "✗"

        self.print(f"[{job_id}] {status} {ts}  {duration:>8}  {command}")

        if git_commit:
            self.print(f"      commit: {git_commit}")

        if verbose:
            outputs = ctx_db.jobs.get_outputs(job_id, ctx_db.artifacts)
            inputs = ctx_db.jobs.get_inputs(job_id, ctx_db.artifacts)

            if outputs:
                self.print(f"      outputs: {len(outputs)} file(s)")
                for out in outputs[:3]:  # Show first 3
                    path = out["path"]
                    try:
                        rel_path = str(Path(path).relative_to(cwd))
                    except ValueError:
                        rel_path = path
                    self.print(f"        - {rel_path}")
                if len(outputs) > 3:
                    self.print(f"        ... and {len(outputs) - 3} more")

            if inputs:
                self.print(f"      inputs: {len(inputs)} file(s)")

            self.print("")

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar log [-n NUM] [-v]

Show recent jobs.

Options:
  -n, --limit NUM  Number of jobs to show (default: 10)
  -v, --verbose    Show more details including inputs/outputs
  -h, --help       Show this help message
"""
