"""
History command - Show job history for a script.

Usage: roar history <script> [-n NUM]
"""

from datetime import datetime

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


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


class HistoryCommand(BaseCommand):
    """
    Show job history for a specific script.

    Examples:
      roar history train.py
      roar history scripts.pretrain
      roar history pretrain -n 20
    """

    @property
    def name(self) -> str:
        return "history"

    @property
    def help_text(self) -> str:
        return "Show job history for a script"

    @property
    def usage(self) -> str:
        return "roar history <script> [-n NUM]"

    def requires_init(self) -> bool:
        """History command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the history command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        script = args[0]
        limit = 20

        # Parse remaining options
        i = 1
        while i < len(args):
            if args[i] in ("-n", "--limit"):
                if i + 1 < len(args):
                    try:
                        limit = int(args[i + 1])
                    except ValueError:
                        self.print_error(f"Invalid number: {args[i + 1]}")
                        return self.failure("Invalid limit")
                    i += 2
                else:
                    self.print_error("-n requires a number")
                    return self.failure("-n requires a number")
            else:
                i += 1

        roar_dir = ctx.cwd / ".roar"
        with create_database_context(roar_dir) as ctx_db:
            jobs = ctx_db.jobs.get_by_script(script, limit=limit)

            if not jobs:
                self.print(f"No jobs found for '{script}'.")
                self.print("")
                self.print("Try:")
                self.print("  roar log        # Show all recent jobs")
                self.print("  roar history    # See usage examples")
                return self.success()

            self.print(f"Job history for '{script}' ({len(jobs)} found):")
            self.print("")

            # Group by date
            current_date = None
            for job in jobs:
                job_id = job["id"]
                ts = job["timestamp"]
                dt = datetime.fromtimestamp(ts)
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M:%S")

                if date_str != current_date:
                    if current_date is not None:
                        self.print("")
                    self.print(f"  {date_str}")
                    current_date = date_str

                duration = format_duration(job.get("duration_seconds"))
                exit_code = job.get("exit_code", "?")
                git_commit = job.get("git_commit", "")[:8] if job.get("git_commit") else "--------"

                # Status indicator
                if exit_code == 0:
                    status = "✓"
                elif exit_code is None or exit_code == "?":
                    status = "?"
                else:
                    status = "✗"

                # Count outputs
                outputs = ctx_db.jobs.get_outputs(job_id, ctx_db.artifacts)
                output_count = len(outputs) if outputs else 0

                self.print(
                    f"    [{job_id:3}] {status} {time_str}  {duration:>8}  {git_commit}  → {output_count} output(s)"
                )

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar history <script> [-n NUM]

Show job history for a specific script.

Examples:
  roar history train.py
  roar history scripts.pretrain
  roar history pretrain -n 20

Options:
  -n, --limit NUM  Number of jobs to show (default: 20)
"""
