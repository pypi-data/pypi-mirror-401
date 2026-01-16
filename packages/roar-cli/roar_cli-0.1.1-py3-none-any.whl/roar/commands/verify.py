"""
Verify command - Verify artifact integrity.

Usage: roar verify [--fix] [-v]
"""

from pathlib import Path

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


class VerifyCommand(BaseCommand):
    """
    Re-compute hashes for tracked files and verify integrity.

    Options:
      --fix      Update cache for changed files
      -v         Show details for each file checked
    """

    @property
    def name(self) -> str:
        return "verify"

    @property
    def help_text(self) -> str:
        return "Verify artifact integrity"

    @property
    def usage(self) -> str:
        return "roar verify [--fix] [-v]"

    def requires_init(self) -> bool:
        """Verify command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the verify command."""
        args = ctx.args

        # Check for help first
        if "-h" in args or "--help" in args:
            self.print(self.get_help())
            return self.success()

        # Parse options
        fix_cache = "--fix" in args
        verbose = "-v" in args or "--verbose" in args

        roar_dir = ctx.cwd / ".roar"
        with create_database_context(roar_dir) as ctx_db:
            # Get all output artifacts with their paths
            artifacts = ctx_db.artifacts.get_all_outputs_with_paths()

            if not artifacts:
                self.print("No output artifacts to verify.")
                return self.success()

            self.print(f"Verifying {len(artifacts)} artifact(s)...")
            self.print("")

            ok_count = 0
            changed_count = 0
            missing_count = 0

            for art in artifacts:
                path = art["path"]
                expected_hash = art["hash"]
                hash_short = expected_hash[:12]

                try:
                    rel_path = str(Path(path).relative_to(ctx.cwd))
                    if not rel_path.startswith(".."):
                        display_path = rel_path
                    else:
                        display_path = path
                except ValueError:
                    display_path = path

                if not Path(path).exists():
                    missing_count += 1
                    if verbose:
                        self.print(f"  MISSING  {hash_short}  {display_path}")
                    continue

                # Compute current hash
                import blake3

                hasher = blake3.blake3()
                try:
                    with open(path, "rb") as f:
                        for chunk in iter(lambda: f.read(8192 * 1024), b""):
                            hasher.update(chunk)
                    current_hash = hasher.hexdigest()
                except OSError as e:
                    missing_count += 1
                    if verbose:
                        self.print(f"  ERROR    {hash_short}  {display_path}: {e}")
                    continue

                if current_hash == expected_hash:
                    ok_count += 1
                    if verbose:
                        self.print(f"  OK       {hash_short}  {display_path}")
                else:
                    changed_count += 1
                    new_short = current_hash[:12]
                    self.print(f"  CHANGED  {hash_short} → {new_short}  {display_path}")

                    if fix_cache:
                        # Update the hash cache
                        ctx_db.hashing.invalidate_cache(path)
                        ctx_db.hashing.compute_file_hash(path)

            self.print("")
            self.print(f"Results: {ok_count} OK, {changed_count} changed, {missing_count} missing")

            if changed_count > 0 and not fix_cache:
                self.print("")
                self.print("Run 'roar verify --fix' to update cache for changed files.")

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar verify [--fix] [-v]

Re-compute hashes for tracked files and verify integrity.

Options:
  --fix      Update cache for changed files
  -v         Show details for each file checked
"""
