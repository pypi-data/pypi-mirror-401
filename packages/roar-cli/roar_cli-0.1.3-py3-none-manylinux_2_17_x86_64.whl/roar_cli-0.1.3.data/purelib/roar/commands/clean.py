"""
Clean command - Delete all written files.

Usage: roar clean [-y] [--db-only]
"""

import os

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


class CleanCommand(BaseCommand):
    """
    Delete all files that were written by tracked jobs.

    Options:
      -y         Skip confirmation prompt
      --db-only  Only clean database records for missing files (no file deletion)
    """

    @property
    def name(self) -> str:
        return "clean"

    @property
    def help_text(self) -> str:
        return "Delete all written files"

    @property
    def usage(self) -> str:
        return "roar clean [-y] [--db-only]"

    def requires_init(self) -> bool:
        """Clean command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the clean command."""
        args = ctx.args

        # Check for help
        if args and args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        skip_confirm = "-y" in args
        db_only = "--db-only" in args

        roar_dir = ctx.cwd / ".roar"

        with create_database_context(roar_dir) as ctx_db:
            written_files = ctx_db.jobs.get_all_written_files(ctx_db.artifacts)

            if not written_files:
                self.print("No written files to clean.")
                return self.success()

            # Separate existing and missing files
            existing_files = []
            missing_files = []
            for f in written_files:
                path = f["path"]
                if os.path.exists(path):
                    existing_files.append(f)
                else:
                    missing_files.append(f)

            # Handle --db-only mode: clean up records for missing files
            if db_only:
                if not missing_files:
                    self.print("No missing files to clean from database.")
                    return self.success()

                self.print(f"Database records to remove ({len(missing_files)}):")
                for f in missing_files[:20]:
                    path = f["path"]
                    try:
                        rel = os.path.relpath(path)
                        if not rel.startswith(".."):
                            path = rel
                    except ValueError:
                        pass
                    self.print(f"  {path}")

                if len(missing_files) > 20:
                    self.print(f"  ... and {len(missing_files) - 20} more")

                # Confirm
                if not skip_confirm and not self.confirm(
                    "\nRemove these database records?", default=False
                ):
                    self.print("Aborted.")
                    return self.success()

                # Clean up database records
                missing_artifact_ids = [f["artifact_id"] for f in missing_files]
                ctx_db.jobs.clear_output_records(missing_artifact_ids, ctx_db.artifacts)
                self.print(f"\nRemoved {len(missing_files)} database record(s).")
                return self.success()

            # Normal mode: delete existing files
            if not existing_files:
                self.print(f"Found {len(written_files)} tracked files, but none exist on disk.")
                if missing_files:
                    self.print(
                        f"Use 'roar clean --db-only' to clean up {len(missing_files)} stale database records."
                    )
                return self.success()

            # Show what will be deleted
            self.print(f"Files to delete ({len(existing_files)}):")
            total_size = 0
            for f in existing_files[:20]:
                path = f["path"]
                size = f.get("size", 0)
                total_size += size
                # Make path relative if possible
                try:
                    rel = os.path.relpath(path)
                    if not rel.startswith(".."):
                        path = rel
                except ValueError:
                    pass
                self.print(f"  {path}")

            if len(existing_files) > 20:
                remaining = len(existing_files) - 20
                for f in existing_files[20:]:
                    total_size += f.get("size", 0)
                self.print(f"  ... and {remaining} more")

            # Show total size
            if total_size > 1024 * 1024 * 1024:
                size_str = f"{total_size / 1024 / 1024 / 1024:.1f} GB"
            elif total_size > 1024 * 1024:
                size_str = f"{total_size / 1024 / 1024:.1f} MB"
            elif total_size > 1024:
                size_str = f"{total_size / 1024:.1f} KB"
            else:
                size_str = f"{total_size} bytes"
            self.print(f"\nTotal size: {size_str}")

            # Confirm
            if not skip_confirm and not self.confirm("\nDelete these files?", default=False):
                self.print("Aborted.")
                return self.success()

            # Delete files and collect artifact IDs of successfully deleted files
            deleted = 0
            errors = 0
            deleted_artifact_ids = []
            for f in existing_files:
                path = f["path"]
                try:
                    os.remove(path)
                    deleted += 1
                    deleted_artifact_ids.append(f["artifact_id"])
                except OSError as e:
                    self.print(f"Error deleting {path}: {e}")
                    errors += 1

            # Clean up database records for deleted files
            if deleted_artifact_ids:
                ctx_db.jobs.clear_output_records(deleted_artifact_ids, ctx_db.artifacts)

            self.print(f"\nDeleted {deleted} file(s).")
            if errors:
                self.print(f"Failed to delete {errors} file(s).")

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar clean [-y] [--db-only]

Delete all files that were written by tracked jobs.

Options:
  -y         Skip confirmation prompt
  --db-only  Only clean database records for missing files (no file deletion)
"""
