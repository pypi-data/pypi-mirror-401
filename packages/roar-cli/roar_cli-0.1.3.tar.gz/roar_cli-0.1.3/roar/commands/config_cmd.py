"""
Config command - View or set configuration.

Usage: roar config [list|get|set] [key] [value]
"""

from ..config import config_get, config_list, config_set
from ..core.interfaces.command import CommandContext, CommandResult
from .base import BaseCommand


class ConfigCommand(BaseCommand):
    """
    View or set roar configuration.

    Subcommands:
      list              List all config options
      get <key>         Get a config value
      set <key> <value> Set a config value
    """

    @property
    def name(self) -> str:
        return "config"

    @property
    def help_text(self) -> str:
        return "View or set configuration"

    @property
    def usage(self) -> str:
        return "roar config [list|get|set] [key] [value]"

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the config command."""
        args = ctx.args

        # Check for help or no args
        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        subcmd = args[0]

        if subcmd == "list":
            return self._cmd_list()
        elif subcmd == "get":
            if len(args) < 2:
                self.print_error("Usage: roar config get <key>")
                return self.failure("Missing key argument")
            return self._cmd_get(args[1])
        elif subcmd == "set":
            if len(args) < 3:
                self.print_error("Usage: roar config set <key> <value>")
                return self.failure("Missing key or value argument")
            return self._cmd_set(args[1], args[2])
        else:
            self.print_error(f"Unknown config subcommand: {subcmd}")
            self.print("Use: list, get, set")
            return self.failure(f"Unknown subcommand: {subcmd}")

    def _cmd_list(self) -> CommandResult:
        """List all config options."""
        keys = config_list()
        self.print("Available config options:")
        self.print("")

        for key, info in keys.items():
            default = info["default"]
            desc = info["description"]
            self.print(f"  {key}")
            self.print(f"    {desc}")
            self.print(f"    Default: {default}")
            self.print("")

        return self.success()

    def _cmd_get(self, key: str) -> CommandResult:
        """Get a config value."""
        value = config_get(key)
        if value is None:
            self.print(f"{key}: (not set)")
        else:
            self.print(f"{key}: {value}")
        return self.success()

    def _cmd_set(self, key: str, value: str) -> CommandResult:
        """Set a config value."""
        try:
            config_path, typed_value = config_set(key, value)
            self.print(f"Set {key} = {typed_value}")
            self.print(f"Saved to {config_path}")
            return self.success()
        except ValueError as e:
            self.print_error(str(e))
            return self.failure(str(e))

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage:
  roar config list              List all config options
  roar config get <key>         Get a config value
  roar config set <key> <value> Set a config value

Config is stored in .roar/config.toml

Options:
  -h, --help    Show this help message
"""
