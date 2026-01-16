"""
Status command - Show tracked artifacts.

Usage: roar status [-a] [--build]
"""

from pathlib import Path

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from ..presenters.console import format_size
from .base import BaseCommand


class StatusCommand(BaseCommand):
    """
    Show files created under roar supervision.

    Displays tracked artifacts with their hashes, sizes, and paths.
    """

    @property
    def name(self) -> str:
        return "status"

    @property
    def aliases(self) -> list:
        return ["st"]

    @property
    def help_text(self) -> str:
        return "Show tracked artifacts"

    @property
    def usage(self) -> str:
        return "roar status [-a] [--build]"

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the status command."""
        # Check for help flag
        if self.has_flag(ctx, "-h", "--help"):
            self.print(self.get_help())
            return self.success()

        # Parse options
        show_all = self.has_flag(ctx, "-a", "--all")
        show_build = self.has_flag(ctx, "--build")

        with create_database_context(ctx.roar_dir) as ctx_db:
            # Show DAG summary first
            self._show_dag_summary(ctx_db)

            # Get artifacts based on options
            if show_build:
                artifacts = ctx_db.artifacts.get_recent_outputs(limit=50, job_type="build")
                artifact_label = "Build artifacts"
            elif show_all:
                artifacts = ctx_db.artifacts.get_all(limit=100)
                artifact_label = "Tracked artifacts"
            else:
                # Default: exclude build artifacts
                artifacts = ctx_db.artifacts.get_recent_outputs(limit=50, job_type="run")
                artifact_label = "Tracked artifacts"

            # Count build artifacts for the hint
            build_count = ctx_db.artifacts.count_build_outputs() if not show_build else 0

            if not artifacts:
                if show_build:
                    self.print("No build artifacts tracked.")
                else:
                    self.print("No artifacts tracked yet.")
                    self.print("")
                    self.print("Run a command with: roar run <command>")
                return self.success()

            self.print(f"{artifact_label} ({len(artifacts)} shown):")
            self.print("")

            # Group by existence
            existing, missing = self._group_by_existence(artifacts, ctx.cwd)

            if existing:
                self.print("Present:")
                self._print_artifacts(existing, ctx.cwd)
                self.print("")

            if missing:
                self.print("Missing:")
                self._print_artifacts(missing, ctx.cwd)
                self.print("")

            # Summary
            self.print(f"Total: {len(existing)} present, {len(missing)} missing")

            # Hint about build artifacts
            if build_count > 0:
                self.print(f"\n({build_count} build artifact(s) hidden, use --build to show)")

        return self.success()

    def _show_dag_summary(self, ctx_db) -> None:
        """Show DAG summary."""
        pipeline = ctx_db.sessions.get_active()
        if pipeline:
            summary = ctx_db.sessions.get_summary(pipeline["id"], ctx_db.jobs)
            if summary:
                build_steps = [s for s in summary.get("steps", []) if s.get("job_type") == "build"]
                run_steps = [s for s in summary.get("steps", []) if s.get("job_type") != "build"]

                self.print("DAG:")
                if build_steps:
                    self.print(f"  Build steps: {len(build_steps)}")
                self.print(f"  Run steps:   {len(run_steps)}")
                self.print("")
        else:
            self.print("DAG: (none)")
            self.print("")

    def _group_by_existence(self, artifacts: list, cwd: Path) -> tuple:
        """Group artifacts by file existence."""
        existing = []
        missing = []

        for art in artifacts:
            path = art.get("path") or art.get("first_seen_path")
            if path and Path(path).exists():
                existing.append(art)
            else:
                missing.append(art)

        return existing, missing

    def _print_artifacts(self, artifacts: list, cwd: Path) -> None:
        """Print artifact list."""
        for art in artifacts:
            path = art.get("path") or art.get("first_seen_path") or "(unknown)"
            # Get first hash from hashes array (prefer blake3)
            hashes = art.get("hashes", [])
            hash_digest = None
            for h in hashes:
                if h.get("algorithm") == "blake3":
                    hash_digest = h.get("digest")
                    break
            if not hash_digest and hashes:
                hash_digest = hashes[0].get("digest", "")
            hash_short = (hash_digest or "")[:12]
            size = format_size(art.get("size"))

            # Try to make path relative
            try:
                rel_path = str(Path(path).relative_to(cwd))
                if not rel_path.startswith(".."):
                    path = rel_path
            except ValueError:
                pass

            self.print(f"  {hash_short}  {size:>8}  {path}")

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar status [-a] [--build]

Show files created under roar supervision.

Options:
  -a, --all    Show all artifacts, not just recent outputs
  --build      Show build artifacts (excluded by default)
  -h, --help   Show this help message
"""
