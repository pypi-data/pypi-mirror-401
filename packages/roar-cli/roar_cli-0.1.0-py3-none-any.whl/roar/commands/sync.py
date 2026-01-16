"""
Sync command - Manage live sync to LaaS.

Usage: roar sync <command>
"""

import os

from ..config import config_get, config_set
from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


class SyncCommand(BaseCommand):
    """
    Manage live sync to LaaS server during roar run.

    Subcommands:
      on       Enable live sync
      off      Disable live sync
      status   Show current sync status
    """

    @property
    def name(self) -> str:
        return "sync"

    @property
    def help_text(self) -> str:
        return "Manage live sync to LaaS"

    @property
    def usage(self) -> str:
        return "roar sync <command>"

    def requires_init(self) -> bool:
        """Sync command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the sync command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        subcmd = args[0]

        if subcmd == "on":
            return self._cmd_on()
        elif subcmd == "off":
            return self._cmd_off()
        elif subcmd == "status":
            return self._cmd_status(ctx)
        else:
            self.print_error(f"Unknown sync command: {subcmd}")
            self.print("Use: on, off, status")
            return self.failure(f"Unknown subcommand: {subcmd}")

    def _cmd_on(self) -> CommandResult:
        """Enable live sync."""
        # Check LaaS URL is configured
        laas_url = config_get("laas.url")
        if not laas_url:
            laas_url = os.environ.get("LAAS_URL")

        if not laas_url:
            self.print_error("LaaS server URL not configured.")
            self.print("")
            self.print("Set it first with:")
            self.print("  roar config set laas.url https://laas.example.com")
            return self.failure("LaaS URL not configured")

        try:
            config_set("sync.enabled", "true")
            self.print("Live sync enabled.")
            self.print(f"Server: {laas_url}")
            self.print("")
            self.print("Jobs will be visible at LaaS during roar run.")
            return self.success()
        except ValueError as e:
            self.print_error(str(e))
            return self.failure(str(e))

    def _cmd_off(self) -> CommandResult:
        """Disable live sync."""
        try:
            config_set("sync.enabled", "false")
            self.print("Live sync disabled.")
            return self.success()
        except ValueError as e:
            self.print_error(str(e))
            return self.failure(str(e))

    def _cmd_status(self, ctx: CommandContext) -> CommandResult:
        """Show current sync status."""
        sync_enabled = config_get("sync.enabled")
        laas_url = config_get("laas.url")
        if not laas_url:
            laas_url = os.environ.get("LAAS_URL")

        if sync_enabled:
            self.print("Live sync: enabled")
        else:
            self.print("Live sync: disabled")

        if laas_url:
            self.print(f"LaaS server: {laas_url}")
        else:
            self.print("LaaS server: (not configured)")

        # Show current session info if we have one
        roar_dir = ctx.cwd / ".roar"
        with create_database_context(roar_dir) as ctx_db:
            pipeline = ctx_db.sessions.get_active()
            if pipeline:
                dag_hash = pipeline.get("hash", "")
                self.print(f"Current DAG: {dag_hash[:12]}...")
                if sync_enabled and laas_url:
                    self.print(f"Dashboard: {laas_url.rstrip('/')}/sessions/{dag_hash}")

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar sync <command>

Manage live sync to LaaS server during roar run.

Commands:
  on       Enable live sync
  off      Disable live sync
  status   Show current sync status

When enabled, roar run will push job status and I/O to LaaS
every 15 seconds, allowing live monitoring via web dashboard.
"""
