"""
Rm command - Remove specific files from disk and database.

Usage: roar rm <file> [file2 ...] [options]
"""

import os

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from ..presenters.run_report import format_size
from .base import BaseCommand


class RmCommand(BaseCommand):
    """
    Remove files from disk and their records from the database.

    Arguments:
      <file>      File path or artifact hash prefix

    Options:
      --db-only   Only remove from database, don't delete file
      -y          Skip confirmation prompt
    """

    @property
    def name(self) -> str:
        return "rm"

    @property
    def help_text(self) -> str:
        return "Remove specific file(s)"

    @property
    def usage(self) -> str:
        return "roar rm <file> [file2 ...] [options]"

    def requires_init(self) -> bool:
        """Rm command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the rm command."""
        args = ctx.args

        # Check for help
        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        db_only = "--db-only" in args
        skip_confirm = "-y" in args

        # Filter out options from file list
        targets = [a for a in args if not a.startswith("-")]

        if not targets:
            self.print_error("No files specified.")
            return self.failure("No files specified")

        roar_dir = ctx.cwd / ".roar"

        with create_database_context(roar_dir) as ctx_db:
            # Resolve targets to artifacts
            to_remove = []  # List of (path, artifact_id, hash, size, exists_on_disk)
            not_found = []  # Track targets that were not found

            for target in targets:
                # Check if it's a hash prefix
                if len(target) >= 8 and all(c in "0123456789abcdef" for c in target.lower()):
                    artifact = ctx_db.artifacts.get_by_hash(target)
                    if artifact:
                        path = artifact.get("first_seen_path", "")
                        exists = os.path.exists(path) if path else False
                        to_remove.append(
                            (path, artifact["id"], artifact["hash"], artifact["size"], exists)
                        )
                        continue

                # Check if it's a file path
                abs_path = os.path.abspath(target)
                if os.path.exists(abs_path):
                    # Find artifact by path in job_outputs
                    cursor = ctx_db.conn.execute(
                        """
                        SELECT jo.artifact_id, a.size, ah.digest as hash
                        FROM job_outputs jo
                        JOIN artifacts a ON jo.artifact_id = a.id
                        JOIN artifact_hashes ah ON a.id = ah.artifact_id
                        WHERE jo.path = ?
                        LIMIT 1
                        """,
                        (abs_path,),
                    )
                    row = cursor.fetchone()
                    if row:
                        to_remove.append(
                            (abs_path, row["artifact_id"], row["hash"], row["size"], True)
                        )
                    else:
                        self.print(f"Warning: {target} exists but is not tracked in database")
                        to_remove.append((abs_path, None, None, None, True))
                else:
                    # Try to find in database by path
                    cursor = ctx_db.conn.execute(
                        """
                        SELECT jo.path, jo.artifact_id, a.size, ah.digest as hash
                        FROM job_outputs jo
                        JOIN artifacts a ON jo.artifact_id = a.id
                        JOIN artifact_hashes ah ON a.id = ah.artifact_id
                        WHERE jo.path = ? OR jo.path LIKE ?
                        LIMIT 1
                        """,
                        (abs_path, f"%{target}"),
                    )
                    row = cursor.fetchone()
                    if row:
                        to_remove.append(
                            (row["path"], row["artifact_id"], row["hash"], row["size"], False)
                        )
                    else:
                        self.print_error(f"{target} not found")
                        not_found.append(target)

            if not to_remove:
                if not_found:
                    return self.failure(f"File(s) not found: {', '.join(not_found)}")
                self.print("No files to remove.")
                return self.success()

            # Show what will be removed
            self.print(f"Files to remove ({len(to_remove)}):")
            for path, _artifact_id, hash, size, exists in to_remove:
                size_val = size or 0
                size_str = format_size(size_val) if size else "?"
                hash_str = hash[:12] + "..." if hash else "(untracked)"
                exists_str = "" if exists else " (missing)"
                display_path = path
                try:
                    rel = os.path.relpath(path)
                    if not rel.startswith(".."):
                        display_path = rel
                except (ValueError, TypeError):
                    pass
                self.print(f"  {display_path}{exists_str}")
                self.print(f"    {hash_str}  {size_str}")

            action = "Remove from database" if db_only else "Delete from disk and database"
            self.print(f"\n{action}")

            # Confirm
            if not skip_confirm and not self.confirm("\nProceed?", default=False):
                self.print("Aborted.")
                return self.success()

            # Remove files
            deleted_files = 0
            deleted_records = 0
            errors = 0

            for path, artifact_id, _hash, _size, exists in to_remove:
                # Delete from disk if not db_only
                if not db_only and exists and path:
                    try:
                        os.remove(path)
                        deleted_files += 1
                    except OSError as e:
                        self.print(f"Error deleting {path}: {e}")
                        errors += 1

                # Remove from database
                if artifact_id:
                    ctx_db.jobs.clear_output_records([artifact_id], ctx_db.artifacts)
                    deleted_records += 1

            self.print("")
            if not db_only:
                self.print(f"Deleted {deleted_files} file(s) from disk.")
            self.print(f"Removed {deleted_records} record(s) from database.")
            if errors:
                self.print(f"Failed to delete {errors} file(s).")

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar rm <file> [file2 ...] [options]

Remove files from disk and their records from the database.

Arguments:
  <file>      File path or artifact hash prefix

Options:
  --db-only   Only remove from database, don't delete file
  -y          Skip confirmation prompt
"""
