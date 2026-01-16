"""
Base command class for all CLI commands.

Provides common functionality and implements the ICommand interface.
"""

from abc import abstractmethod

from ..core.interfaces.command import CommandContext, CommandResult, ICommand
from ..core.interfaces.logger import ILogger
from ..core.interfaces.presenter import IPresenter


class BaseCommand(ICommand):
    """
    Abstract base class for all commands.

    Provides:
    - Common argument parsing utilities
    - Help text generation
    - Error handling patterns
    - Presenter integration for output
    """

    def __init__(
        self,
        presenter: IPresenter | None = None,
        logger: ILogger | None = None,
    ) -> None:
        """
        Initialize command with optional presenter and logger.

        Args:
            presenter: Output presenter (defaults to ConsolePresenter)
            logger: Internal logger (defaults to container-resolved or NullLogger)
        """
        self._presenter = presenter
        self._logger = logger

    @property
    def presenter(self) -> IPresenter:
        """Get the presenter, creating a default if needed."""
        if self._presenter is None:
            from ..presenters.console import ConsolePresenter

            self._presenter = ConsolePresenter()
        return self._presenter

    @property
    def logger(self) -> ILogger:
        """Get the logger, resolving from container or creating NullLogger."""
        if self._logger is None:
            from ..core.container import get_container
            from ..services.logging import NullLogger

            container = get_container()
            self._logger = container.try_resolve(ILogger)  # type: ignore[type-abstract]
            if self._logger is None:
                self._logger = NullLogger()
        return self._logger

    @property
    @abstractmethod
    def name(self) -> str:
        """Command name (e.g., 'status', 'run')."""
        pass

    @property
    def aliases(self) -> list[str]:
        """Command aliases."""
        return []

    @property
    def help_text(self) -> str:
        """Short description for help listing."""
        return ""

    @property
    def usage(self) -> str:
        """Usage string for detailed help."""
        return f"roar {self.name}"

    @abstractmethod
    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the command."""
        pass

    def requires_init(self) -> bool:
        """Whether this command requires roar to be initialized."""
        return True

    def requires_git(self) -> bool:
        """Whether this command requires a git repository."""
        return False

    def get_help(self) -> str:
        """Return detailed help text."""
        lines = [
            f"Usage: {self.usage}",
            "",
            self.help_text,
        ]
        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Argument parsing utilities
    # -------------------------------------------------------------------------

    def has_flag(self, ctx: CommandContext, *flags: str) -> bool:
        """Check if any of the given flags are present in args."""
        return any(flag in ctx.args for flag in flags)

    def get_flag_value(
        self,
        ctx: CommandContext,
        *flags: str,
        default: str | None = None,
    ) -> str | None:
        """
        Get the value following a flag.

        Args:
            ctx: Command context
            flags: Flag names to look for (e.g., '-o', '--output')
            default: Default value if flag not found

        Returns:
            Value following the flag, or default
        """
        for i, arg in enumerate(ctx.args):
            if arg in flags and i + 1 < len(ctx.args):
                return ctx.args[i + 1]
        return default

    def get_positional_args(
        self,
        ctx: CommandContext,
        skip_flags: bool = True,
    ) -> list[str]:
        """
        Get positional arguments (non-flag arguments).

        Args:
            ctx: Command context
            skip_flags: If True, skip arguments that look like flags

        Returns:
            List of positional arguments
        """
        result = []
        skip_next = False

        for i, arg in enumerate(ctx.args):
            if skip_next:
                skip_next = False
                continue

            if skip_flags and arg.startswith("-"):
                # Check if this flag has a value
                if "=" not in arg and i + 1 < len(ctx.args):
                    next_arg = ctx.args[i + 1]
                    if not next_arg.startswith("-"):
                        skip_next = True
                continue

            result.append(arg)

        return result

    # -------------------------------------------------------------------------
    # Result helpers
    # -------------------------------------------------------------------------

    def success(self, message: str | None = None, data: dict | None = None) -> CommandResult:
        """Create a successful result."""
        return CommandResult(success=True, exit_code=0, message=message, data=data)

    def failure(
        self,
        message: str,
        exit_code: int = 1,
        data: dict | None = None,
    ) -> CommandResult:
        """Create a failure result."""
        return CommandResult(
            success=False,
            exit_code=exit_code,
            message=message,
            data=data,
        )

    # -------------------------------------------------------------------------
    # Output helpers (delegate to presenter)
    # -------------------------------------------------------------------------

    def print(self, message: str) -> None:
        """Print a message."""
        self.presenter.print(message)

    def print_error(self, message: str) -> None:
        """Print an error message."""
        self.presenter.print_error(message)

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for user confirmation."""
        return self.presenter.confirm(message, default)
