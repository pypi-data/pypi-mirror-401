"""
Command dispatcher for roar CLI.

Routes command names to command implementations and handles execution.
"""

import sys
from pathlib import Path

from ..core.container import get_container
from ..core.interfaces.command import CommandContext, ICommand


def create_context(args: list) -> CommandContext:
    """
    Create a command context from command-line arguments.

    Args:
        args: Command arguments (excluding the command name)

    Returns:
        CommandContext for the command
    """
    cwd = Path.cwd()
    roar_dir = cwd / ".roar"
    vcs = get_container().get_vcs_provider("git")
    repo_root = vcs.get_repo_root()

    return CommandContext(
        roar_dir=roar_dir,
        repo_root=Path(repo_root) if repo_root else None,
        cwd=cwd,
        args=args,
        is_interactive=sys.stdin.isatty(),
    )


def get_registered_commands() -> dict[str, type[ICommand]]:
    """
    Get all registered command classes from the container.

    Returns:
        Dict mapping command names to command classes
    """
    container = get_container()
    return container.list_commands()


def dispatch_command(name: str, args: list) -> int:
    """
    Dispatch a command by name.

    Args:
        name: Command name
        args: Command arguments

    Returns:
        Exit code from command execution
    """
    container = get_container()

    # Try to get command from registry
    command_class = container.get_command(name)
    if command_class is None:
        return 127  # Command not found (standard shell exit code)

    # Create context
    ctx = create_context(args)

    # Instantiate command
    command = command_class()

    # Check requirements
    if command.requires_init() and not ctx.roar_dir.exists():
        print("Error: roar is not initialized in this directory.")
        print("")
        print("Run 'roar init' first to set up roar.")
        return 1

    if command.requires_git() and ctx.repo_root is None:
        print("Error: Not in a git repository.")
        return 1

    # Validate arguments
    error = command.validate_args(ctx)
    if error:
        print(f"Error: {error}")
        return 1

    # Execute command
    try:
        result = command.execute(ctx)
        return result.exit_code
    except KeyboardInterrupt:
        print("\nAborted.")
        return 130
    except Exception as e:
        print(f"Error: {e}")
        return 1


def register_builtin_commands() -> None:
    """
    Register built-in commands with the container.

    This should be called during application startup.
    """
    from . import ConfigCommand, InitCommand, LogCommand, StatusCommand

    container = get_container()

    # Register commands
    container.register_command(InitCommand)
    container.register_command(StatusCommand)
    container.register_command(ConfigCommand)
    container.register_command(LogCommand)
