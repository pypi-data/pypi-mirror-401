"""
Dag command - View and manage the execution DAG.

Usage: roar dag [command] [options]
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


def format_timestamp(ts: float) -> str:
    """Format a timestamp for display."""
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds is None:
        return "?"
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


class DagCommand(BaseCommand):
    """
    View and manage the execution DAG.

    Commands:
      (none)            Show DAG nodes (list view)
      -i                Interactive mode (cursor nav, q to quit)
      clear             Clear the active DAG
      script            Output all steps as a shell script
      rename @N <name>  Rename a node (e.g., rename @2 train)

    Examples:
      roar dag                  # Show DAG
      roar dag -i               # Interactive browser
      roar dag clear            # Clear DAG
      roar dag script > run.sh  # Export as script
      roar dag rename @2 train  # Name step 2 'train'
    """

    @property
    def name(self) -> str:
        return "dag"

    @property
    def help_text(self) -> str:
        return "View and manage execution DAG"

    @property
    def usage(self) -> str:
        return "roar dag [command] [options]"

    def requires_init(self) -> bool:
        """Dag command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the dag command."""
        args = ctx.args

        # Check for help
        if args and args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        roar_dir = ctx.cwd / ".roar"

        # Parse subcommand
        subcmd = None
        interactive = False
        position = None
        rename_to = None

        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "-i":
                interactive = True
                i += 1
            elif arg == "clear":
                subcmd = "clear"
                i += 1
            elif arg == "script":
                subcmd = "script"
                i += 1
            elif arg == "rename":
                subcmd = "rename"
                # Expect @N and name
                if i + 2 < len(args):
                    pos_arg = args[i + 1]
                    if pos_arg.startswith("@"):
                        position = pos_arg[1:]
                    else:
                        position = pos_arg
                    rename_to = args[i + 2]
                    i += 3
                else:
                    self.print_error("rename requires @N and name (e.g., rename @2 train)")
                    return self.failure("Invalid rename arguments")
            elif arg.startswith("@"):
                position = arg[1:]
                i += 1
            else:
                i += 1

        with create_database_context(roar_dir) as ctx_db:
            pipeline = ctx_db.sessions.get_active()

            if not pipeline:
                self.print("No active DAG.")
                self.print("")
                self.print("Run 'roar run <command>' to start recording,")
                self.print("or 'roar reproduce <hash>' to reproduce an artifact.")
                return self.success()

            # Handle clear
            if subcmd == "clear":
                return self._cmd_clear(ctx_db, pipeline, args)

            # Handle script
            if subcmd == "script":
                return self._cmd_script(ctx_db, pipeline)

            # Handle rename
            if subcmd == "rename":
                if not position or not rename_to:
                    self.print_error("rename requires: roar dag rename @N <new_name>")
                    return self.failure("Invalid rename arguments")
                return self._cmd_rename(ctx_db, pipeline, position, rename_to)

            # Default: show DAG list
            summary = ctx_db.sessions.get_summary(pipeline["id"], ctx_db.jobs)
            if not summary:
                self.print("No DAG found.")
                return self.success()

            # Get stale steps for display
            stale_steps = set(ctx_db.session_service.get_stale_steps(pipeline["id"]))

            if interactive:
                # Interactive mode
                self._dag_interactive(ctx_db, pipeline, summary)
            else:
                # List view
                self._dag_list(summary, stale_steps)

        return self.success()

    def _cmd_clear(self, ctx_db, pipeline: dict, args: list) -> CommandResult:
        """Clear the active DAG."""
        summary = ctx_db.sessions.get_summary(pipeline["id"], ctx_db.jobs)
        step_count = summary.get("total_steps", 0) if summary else 0

        if step_count == 0:
            self.print("DAG is already empty.")
            return self.success()

        # Check for --force flag
        if "--force" not in args and "-f" not in args:
            self.print(f"This will clear {step_count} node(s) from the DAG.")
            self.print("")
            if not self.confirm("Continue?", default=False):
                self.print("Cancelled.")
                return self.success()

        self.print(f"Clearing DAG ({step_count} nodes)...")
        ctx_db.sessions.clear(pipeline["id"])
        self.print("DAG cleared.")
        return self.success()

    def _cmd_script(self, ctx_db, pipeline: dict) -> CommandResult:
        """Output all steps as a shell script."""
        summary = ctx_db.sessions.get_summary(pipeline["id"], ctx_db.jobs)
        if not summary or not summary.get("steps"):
            print("# No steps in DAG", file=sys.stderr)
            return self.success()

        # Separate build and run steps
        build_steps = [s for s in summary["steps"] if s.get("job_type") == "build"]
        run_steps = [s for s in summary["steps"] if s.get("job_type") != "build"]

        print("#!/bin/bash")
        print("# DAG script generated by roar")
        print(f"# Build steps: {len(build_steps)}")
        print(f"# Run steps: {len(run_steps)}")
        print("")
        print("set -e  # Exit immediately if any command fails")
        print("")

        # Output build steps first
        if build_steps:
            print("# === Build Steps ===")
            print("")
            for step in build_steps:
                step_num = step["step_number"]
                command = step["command"]
                step_name = step.get("step_name", "")

                if step_name:
                    print(f"# @B{step_num} ({step_name})")
                else:
                    print(f"# @B{step_num}")

                print(f"roar build {command}")
                print("")

        # Output run steps
        if run_steps:
            if build_steps:
                print("# === Run Steps ===")
                print("")
            for step in run_steps:
                step_num = step["step_number"]
                command = step["command"]
                step_name = step.get("step_name", "")

                if step_name:
                    print(f"# @{step_num} ({step_name})")
                else:
                    print(f"# @{step_num}")

                print(f"roar run {command}")
                print("")

        return self.success()

    def _cmd_rename(self, ctx_db, pipeline: dict, position: str, rename_to: str) -> CommandResult:
        """Rename a step."""
        if not position:
            self.print_error(
                "rename requires a step number (e.g., rename @2 train or rename @B1 build)"
            )
            return self.failure("Invalid rename arguments")

        # Check for @BN (build step) vs @N (run step)
        is_build = False
        step_ref = position
        if step_ref.upper().startswith("B"):
            is_build = True
            step_ref = step_ref[1:]

        if not step_ref.isdigit():
            self.print_error(
                "rename requires a step number (e.g., rename @2 train or rename @B1 build)"
            )
            return self.failure("Invalid step number")

        step_num = int(step_ref)
        step = ctx_db.sessions.get_step_by_number(
            pipeline["id"], step_num, job_type="build" if is_build else None
        )
        if not step:
            prefix = "@B" if is_build else "@"
            self.print(f"No step {prefix}{step_num} in DAG.")
            return self.failure("Step not found")

        ctx_db.sessions.rename_step(
            pipeline["id"], step_num, rename_to, job_type="build" if is_build else None
        )
        prefix = "@B" if is_build else "@"
        self.print(f"Renamed {prefix}{step_num} to '{rename_to}'")
        self.print(f"Command: {step['command']}")
        return self.success()

    def _dag_list(self, summary: dict, stale_steps: set | None = None):
        """Display DAG as a simple list."""
        if stale_steps is None:
            stale_steps = set()

        # Separate build steps from run steps
        build_steps = [s for s in summary["steps"] if s.get("job_type") == "build"]
        run_steps = [s for s in summary["steps"] if s.get("job_type") != "build"]

        total = len(build_steps) + len(run_steps)
        self.print(f"DAG ({total} nodes)")
        if summary.get("hash"):
            self.print(f"Hash: {summary['hash'][:12]}...")
        self.print(f"Created: {format_timestamp(summary['created_at'])}")
        self.print("")

        if summary.get("git_warning"):
            self.print(f"Warning: {summary['git_warning']}")
            self.print("")

        # Calculate widths for column alignment
        all_steps = build_steps + run_steps
        max_step_num = max((s["step_number"] for s in all_steps), default=1)
        step_num_width = len(str(max_step_num))

        # Get terminal width for layout calculations
        term_width = shutil.get_terminal_size((80, 24)).columns

        # Fixed widths for suffix columns: " [12345678]" (12) + " [stale]" (8)
        suffix_width = 22  # hash bracket + stale label
        # Prefix: "  ✓ @NN: "
        prefix_width = 5 + step_num_width + 2  # "  ✓ @" + digits + ": "

        # Command gets remaining space
        cmd_col_width = max(30, term_width - prefix_width - suffix_width)

        def print_step(step, prefix="@"):
            step_num = step["step_number"]
            command = step["command"]
            step_name = step.get("step_name", "")
            job_uid = step.get("job_uid", "")
            exit_code = step.get("exit_code")
            is_stale = step_num in stale_steps

            # Truncate command if needed
            if len(command) > cmd_col_width:
                command = command[: cmd_col_width - 3] + "..."

            # Status indicator
            job_status = step.get("status")
            if job_status == "pending":
                status = "○"  # Not yet run
            elif is_stale:
                status = "⚠"  # Stale - needs re-run
            elif exit_code == 0:
                status = "✓"
            elif exit_code is None:
                status = "◐"  # Running or incomplete
            else:
                status = "✗"

            name_str = f" ({step_name})" if step_name else ""
            uid_str = f"[{job_uid}]" if job_uid else ""
            stale_str = "[stale]" if is_stale else ""

            # Build the suffix (hash + stale), right-justified
            suffix_parts = []
            if uid_str:
                suffix_parts.append(uid_str)
            if stale_str:
                suffix_parts.append(stale_str)
            suffix = " ".join(suffix_parts)

            # Right-justify step number (no space after @)
            step_num_str = str(step_num).rjust(step_num_width)

            # Pad command to fixed width for column alignment
            cmd_with_name = f"{command}{name_str}"
            cmd_padded = cmd_with_name.ljust(cmd_col_width)

            self.print(f"  {status} {prefix}{step_num_str}: {cmd_padded} {suffix}")

        # Print build steps first
        if build_steps:
            self.print("Build steps:")
            for step in build_steps:
                print_step(step, prefix="@B")
            self.print("")

        # Print run steps
        if run_steps:
            if build_steps:
                self.print("Run steps:")
            for step in run_steps:
                print_step(step, prefix="@")
            self.print("")

        self.print("Use 'roar show @N' for details, 'roar run @N' to re-run (use @BN for builds)")

    def _dag_interactive(self, ctx_db, pipeline: dict, summary: dict):
        """Interactive DAG browser with cursor navigation."""
        import termios
        import tty

        steps = summary.get("steps", [])
        if not steps:
            self.print("No steps in DAG.")
            return

        selected = 0
        detail_view = False

        def get_key():
            """Read a single keypress."""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == "\x1b":  # Escape sequence
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        ch3 = sys.stdin.read(1)
                        if ch3 == "A":
                            return "up"
                        elif ch3 == "B":
                            return "down"
                    return "esc"
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        def clear_screen():
            print("\033[2J\033[H", end="")

        def render_list():
            clear_screen()
            print(f"DAG ({len(steps)} nodes) - ↑/↓ navigate, Enter for details, q to quit")
            print("")

            for i, step in enumerate(steps):
                step_num = step["step_number"]
                command = step["command"]
                step_name = step.get("step_name", "")
                exit_code = step.get("exit_code")

                # Truncate command
                max_cmd_len = 60
                if len(command) > max_cmd_len:
                    command = command[: max_cmd_len - 3] + "..."

                # Status indicator
                if exit_code == 0:
                    status = "✓"
                elif exit_code is None:
                    status = " "
                else:
                    status = "✗"

                name_str = f" ({step_name})" if step_name else ""

                if i == selected:
                    print(f"  > {status} @{step_num}: {command}{name_str}")
                else:
                    print(f"    {status} @{step_num}: {command}{name_str}")

        def render_detail():
            clear_screen()
            step = steps[selected]
            step_num = step["step_number"]

            print(f"@{step_num} Details - Backspace/Esc to go back, q to quit")
            print("")
            print(f"Command: {step['command']}")
            if step.get("step_name"):
                print(f"Name: {step['step_name']}")
            if step.get("job_uid"):
                print(f"Job UID: {step['job_uid']}")
            if step.get("git_commit"):
                print(f"Git: {step['git_commit'][:8]}")
            print(f"Timestamp: {format_timestamp(step['timestamp'])}")
            if step.get("duration_seconds"):
                print(f"Duration: {format_duration(step['duration_seconds'])}")
            if step.get("exit_code") is not None:
                print(f"Exit code: {step['exit_code']}")

            # Get inputs/outputs
            inputs = ctx_db.jobs.get_inputs(step["id"], ctx_db.artifacts)
            outputs = ctx_db.jobs.get_outputs(step["id"], ctx_db.artifacts)

            if inputs:
                print(f"\nInputs ({len(inputs)}):")
                for inp in inputs[:5]:
                    path = inp["path"]
                    try:
                        rel = str(Path(path).relative_to(Path.cwd()))
                        if not rel.startswith(".."):
                            path = rel
                    except ValueError:
                        pass
                    print(f"  {inp['artifact_hash'][:12]}  {path}")
                if len(inputs) > 5:
                    print(f"  ... and {len(inputs) - 5} more")

            if outputs:
                print(f"\nOutputs ({len(outputs)}):")
                for out in outputs[:5]:
                    path = out["path"]
                    try:
                        rel = str(Path(path).relative_to(Path.cwd()))
                        if not rel.startswith(".."):
                            path = rel
                    except ValueError:
                        pass
                    print(f"  {out['artifact_hash'][:12]}  {path}")
                if len(outputs) > 5:
                    print(f"  ... and {len(outputs) - 5} more")

            print("")
            print(f"To re-run: roar run @{step_num}")

        try:
            while True:
                if detail_view:
                    render_detail()
                else:
                    render_list()

                key = get_key()

                if key == "q":
                    clear_screen()
                    break
                elif key == "up" and not detail_view:
                    selected = max(0, selected - 1)
                elif key == "down" and not detail_view:
                    selected = min(len(steps) - 1, selected + 1)
                elif key == "\r" and not detail_view:  # Enter
                    detail_view = True
                elif key in ("\x7f", "esc") and detail_view:  # Backspace or Esc
                    detail_view = False
                elif key == "esc":
                    clear_screen()
                    break

        except Exception:
            # Restore terminal on error
            clear_screen()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar dag [command] [options]

View and manage the execution DAG.

Commands:
  (none)            Show DAG nodes (list view)
  -i                Interactive mode (cursor nav, q to quit)
  clear             Clear the active DAG
  script            Output all steps as a shell script
  rename @N <name>  Rename a node (e.g., rename @2 train)

Examples:
  roar dag                  # Show DAG
  roar dag -i               # Interactive browser
  roar dag clear            # Clear DAG
  roar dag script > run.sh  # Export as script
  roar dag rename @2 train  # Name step 2 'train'

To re-run a step: roar run @2
To view step details: roar show @2
"""
