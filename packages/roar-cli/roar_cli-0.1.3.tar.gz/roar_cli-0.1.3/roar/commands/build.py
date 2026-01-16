"""
Build command - Run a build step with provenance tracking.

Usage: roar build <command>

Refactored to use SOLID services for better maintainability.
"""

from ..core.container import get_container
from ..core.interfaces.command import CommandContext, CommandResult
from ..core.interfaces.run import IRunArgumentParser, IRunCoordinator, RunContext
from ..presenters.run_report import RunReportPresenter
from ..services.execution import RunArgumentParser, RunCoordinator
from .base import BaseCommand


class BuildCommand(BaseCommand):
    """
    Run a build step with provenance tracking.

    Build steps are tracked separately from run steps and are used for
    environment setup tasks like compiling native extensions, installing
    dependencies, etc.

    Build steps run before DAG steps during reproduction.

    Examples:
      roar build maturin develop --release
      roar build make
      roar build pip install -e .
    """

    def __init__(
        self,
        arg_parser: IRunArgumentParser | None = None,
        coordinator: IRunCoordinator | None = None,
    ) -> None:
        """
        Initialize build command with optional service overrides.

        Args:
            arg_parser: Argument parser service
            coordinator: Run coordinator service
        """
        super().__init__()
        self._arg_parser = arg_parser or RunArgumentParser()
        self._coordinator = coordinator

    @property
    def name(self) -> str:
        return "build"

    @property
    def help_text(self) -> str:
        return "Run a build step with provenance tracking"

    @property
    def usage(self) -> str:
        return "roar build <command>"

    def requires_init(self) -> bool:
        """Build command requires roar to be initialized."""
        return True

    def requires_git(self) -> bool:
        """Build command requires a git repository."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the build command."""
        # Parse arguments
        args = self._arg_parser.parse(ctx.args, job_type="build")

        if args.show_help:
            self.print(self._arg_parser.get_help_text(is_build=True))
            return self.success()

        if not args.command:
            self.print(self._arg_parser.get_help_text(is_build=True))
            return self.failure("No command specified")

        # Validate git repo (clean working tree)
        vcs = get_container().get_vcs_provider("git")
        repo_root = vcs.get_repo_root()
        if not repo_root:
            self.print_error("roar requires the working directory to be inside a git repository.")
            return self.failure("Not in a git repository")

        clean, changes = vcs.get_status(repo_root)
        if not clean:
            self.print_error("Git repo has uncommitted changes:")
            for c in changes:
                self.print(f"   {c}")
            return self.failure("Uncommitted changes")

        # Get git info
        vcs_info = vcs.get_info(repo_root)
        git_commit = vcs_info.commit if vcs_info else None
        git_branch = vcs_info.branch if vcs_info else None
        git_repo = vcs_info.remote_url if vcs_info else None

        # Get quiet setting from args or config
        quiet = args.quiet
        if not quiet:
            from ..config import load_config

            config = load_config(start_dir=repo_root)
            quiet = config.get("output", {}).get("quiet", False)

        # Execute build
        coordinator = self._get_coordinator()
        run_ctx = RunContext(
            roar_dir=ctx.roar_dir,
            repo_root=repo_root,
            command=args.command,
            job_type="build",
            quiet=quiet,
            hash_algorithms=args.hash_algorithms,
            git_commit=git_commit,
            git_branch=git_branch,
            git_repo=git_repo,
        )

        result = coordinator.execute(run_ctx)

        # Present report
        report = RunReportPresenter(self.presenter)
        report.show_report(result, args.command, quiet)

        # Show stale warnings
        if result.stale_upstream or result.stale_downstream:
            report.show_stale_warnings(
                result.stale_upstream,
                result.stale_downstream,
                is_build=True,
            )

        return CommandResult(
            success=(result.exit_code == 0),
            exit_code=result.exit_code,
            data={"job_uid": result.job_uid},
        )

    def _get_coordinator(self) -> IRunCoordinator:
        """Get run coordinator, creating default if needed."""
        if self._coordinator:
            return self._coordinator
        return RunCoordinator(presenter=self.presenter)

    def get_help(self) -> str:
        """Return detailed help text."""
        return self._arg_parser.get_help_text(is_build=True)
