"""
Run command - Run a command with provenance tracking.

Usage: roar run <command>
       roar run @N  (re-run DAG node N)

Refactored to use SOLID services for better maintainability.
"""

import shlex

from ..core.container import get_container
from ..core.interfaces.command import CommandContext, CommandResult
from ..core.interfaces.run import IRunArgumentParser, IRunCoordinator, RunContext
from ..presenters.run_report import RunReportPresenter
from ..services.execution import DAGReferenceResolver, RunArgumentParser, RunCoordinator
from .base import BaseCommand


class RunCommand(BaseCommand):
    """
    Run a command with provenance tracking.

    Automatically tracks:
    - Input files (files read by the command)
    - Output files (files written by the command)
    - Command exit code and duration
    - Git commit (if in a git repo)
    - Runtime environment (packages, GPU, etc.)

    Refactored to follow SOLID principles:
    - SRP: Delegates to specialized services
    - OCP: Extensible via service composition
    - DIP: Depends on abstractions via container

    Examples:
      roar run python train.py
      roar run ./scripts/train.sh
      roar run @2   # Re-run DAG node 2
    """

    def __init__(
        self,
        arg_parser: IRunArgumentParser | None = None,
        coordinator: IRunCoordinator | None = None,
    ) -> None:
        """
        Initialize run command with optional service overrides.

        Args:
            arg_parser: Argument parser service
            coordinator: Run coordinator service
        """
        super().__init__()
        self._arg_parser = arg_parser or RunArgumentParser()
        self._coordinator = coordinator

    @property
    def name(self) -> str:
        return "run"

    @property
    def help_text(self) -> str:
        return "Run a command with provenance tracking"

    @property
    def usage(self) -> str:
        return "roar run <command>"

    def requires_init(self) -> bool:
        """Run command requires roar to be initialized."""
        return True

    def requires_git(self) -> bool:
        """Run command requires a git repository."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the run command."""
        # Parse arguments
        args = self._arg_parser.parse(ctx.args, job_type=None)

        if args.show_help:
            self.print(self._arg_parser.get_help_text(is_build=False))
            return self.success()

        if not args.command and not args.dag_reference:
            self.print(self._arg_parser.get_help_text(is_build=False))
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

        # Resolve DAG reference if present
        command = args.command
        is_build = False

        if args.dag_reference:
            resolved, error = self._resolve_dag_reference(
                ctx, args.dag_reference, args.param_overrides
            )
            if error:
                return self.failure(error)

            # Check for stale upstream and confirm
            if resolved.stale_upstream:
                report = RunReportPresenter(self.presenter)
                if not report.show_upstream_stale_warning(
                    resolved.step_number, resolved.stale_upstream
                ):
                    self.print("Aborted.")
                    return self.success()
                self.print("")

            command = shlex.split(resolved.command)
            is_build = resolved.is_build

            self.print(f"Re-running @{resolved.step_number}: {resolved.command}")
            self.print("")

        # Get quiet setting from args or config
        quiet = args.quiet
        if not quiet:
            from ..config import load_config

            config = load_config(start_dir=repo_root)
            quiet = config.get("output", {}).get("quiet", False)

        # Execute run
        coordinator = self._get_coordinator()
        run_ctx = RunContext(
            roar_dir=ctx.roar_dir,
            repo_root=repo_root,
            command=command,
            job_type="build" if is_build else None,
            quiet=quiet,
            hash_algorithms=args.hash_algorithms,
            git_commit=git_commit,
            git_branch=git_branch,
            git_repo=git_repo,
        )

        result = coordinator.execute(run_ctx)

        # Present report
        report = RunReportPresenter(self.presenter)
        report.show_report(result, command, quiet)

        # Show stale warnings
        if result.stale_upstream or result.stale_downstream:
            report.show_stale_warnings(
                result.stale_upstream,
                result.stale_downstream,
                is_build=result.is_build,
            )

        return CommandResult(
            success=(result.exit_code == 0),
            exit_code=result.exit_code,
            data={"job_uid": result.job_uid},
        )

    def _resolve_dag_reference(
        self,
        ctx: CommandContext,
        reference: str,
        param_overrides: dict,
    ) -> tuple:
        """
        Resolve a DAG reference to a command.

        Returns (ResolvedStep, None) on success or (None, error_message) on failure.
        """
        from ..db.context import create_database_context

        with create_database_context(ctx.roar_dir) as db_ctx:
            resolver = DAGReferenceResolver(
                db_ctx.sessions,
                db_ctx.jobs,
                db_ctx.artifacts,
                db_ctx.lineage,
                db_ctx.session_service,
            )
            return resolver.resolve(reference, param_overrides)

    def _get_coordinator(self) -> IRunCoordinator:
        """Get run coordinator, creating default if needed."""
        if self._coordinator:
            return self._coordinator
        return RunCoordinator(presenter=self.presenter)

    def get_help(self) -> str:
        """Return detailed help text."""
        return self._arg_parser.get_help_text(is_build=False)
