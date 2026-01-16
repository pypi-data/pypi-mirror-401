"""
Init command - Initialize roar in current directory.

Usage: roar init
"""

from ..core.interfaces.command import CommandContext, CommandResult
from .base import BaseCommand


class InitCommand(BaseCommand):
    """
    Initialize roar in the current directory.

    Creates .roar directory and optionally adds it to .gitignore.
    """

    @property
    def name(self) -> str:
        return "init"

    @property
    def help_text(self) -> str:
        return "Initialize roar in current directory"

    @property
    def usage(self) -> str:
        return "roar init"

    def requires_init(self) -> bool:
        """Init command doesn't require roar to be initialized."""
        return False

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the init command."""
        # Check for help flag
        if self.has_flag(ctx, "-h", "--help"):
            self.print(self.get_help())
            return self.success()

        cwd = ctx.cwd

        # Check if .roar already exists
        roar_dir = cwd / ".roar"
        if roar_dir.exists():
            self.print(f".roar directory already exists at {roar_dir}")
            return self.success()

        # Create .roar directory
        roar_dir.mkdir()
        self.print(f"Created {roar_dir}")

        # Check if we're in a git repo
        if ctx.repo_root is None:
            self.print("Not in a git repository. Done.")
            return self.success()

        # Check if .gitignore exists
        gitignore_path = ctx.repo_root / ".gitignore"
        if not gitignore_path.exists():
            self.print("No .gitignore found. Done.")
            return self.success()

        # Check if .roar is already in .gitignore
        gitignore_content = gitignore_path.read_text()
        if ".roar" in gitignore_content or ".roar/" in gitignore_content:
            self.print(".roar is already in .gitignore. Done.")
            return self.success()

        # Ask user if they want to add .roar to .gitignore
        self.print("")
        add_to_gitignore = self.confirm("Add .roar/ to .gitignore?", default=True)

        if add_to_gitignore:
            # Append to .gitignore
            with open(gitignore_path, "a") as f:
                if not gitignore_content.endswith("\n"):
                    f.write("\n")
                f.write(".roar/\n")
            self.print("Added .roar/ to .gitignore")
        else:
            self.print("Skipped .gitignore update.")

        self.print("Done.")
        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar init

Initialize roar in the current directory.

This command:
  1. Creates a .roar directory for storing tracking data
  2. Optionally adds .roar/ to .gitignore if in a git repo

Options:
  -h, --help    Show this help message
"""
