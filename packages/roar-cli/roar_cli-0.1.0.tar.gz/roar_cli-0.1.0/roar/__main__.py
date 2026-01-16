"""
Entry point for the `roar` command-line interface.

roar (Run Observation & Artifact Registration) is a local front-end to
TReqs' Lineage-as-a-Service (LaaS). It registers data artifacts and
execution steps (jobs) in ML pipelines.

Commands:
    roar init              Initialize roar in current directory
    roar auth              Manage LaaS authentication
    roar run <command>     Run a command with provenance tracking
    roar step              Navigate and execute pipeline steps
    roar reproduce <hash>  Create pipeline to reproduce an artifact
    roar get <url> <dest>  Download and register external data
    roar put <src> <url>   Upload and register artifacts
    roar log               Show recent jobs
    roar history <script>  Show job history for a script
    roar show <hash>       Show artifact details
    roar status            Show tracked artifacts
    roar verify            Verify artifact integrity
    roar config            View or set configuration
"""

import sys


def _print_help():
    """Print main help message."""
    print("roar - Run Observation & Artifact Registration")
    print("")
    print("A local front-end to TReqs' Lineage-as-a-Service (LaaS).")
    print("Tracks data artifacts and execution steps in ML pipelines.")
    print("")
    print("Usage: roar <command> [args...]")
    print("")
    print("Commands:")
    print("  init               Initialize roar in current directory")
    print("  run <command>      Run a command with provenance tracking")
    print("  run @N             Re-run DAG node N")
    print("  build <command>    Run a build step (e.g., maturin, make)")
    print("  dag                View and manage execution DAG")
    print("  show <id>          Show artifact, job, or DAG node details")
    print("  reproduce <hash>   Reproduce an artifact")
    print("  log                Show recent jobs")
    print("  history <script>   Show job history for a script")
    print("  status             Show tracked artifacts")
    print("  get <url> <dest>   Download and register external data")
    print("  put <src> <url>    Upload and register artifacts")
    print("  clean              Delete all written files")
    print("  rm <file>          Remove specific file(s)")
    print("  verify             Verify artifact integrity")
    print("  auth               Manage LaaS authentication")
    print("  sync               Manage live sync to LaaS")
    print("  config             View or set configuration")


def main():
    # Bootstrap the application (registers plugins and commands)
    from .commands.dispatcher import dispatch_command
    from .core.bootstrap import bootstrap

    bootstrap()

    if len(sys.argv) < 2:
        _print_help()
        sys.exit(1)

    sub = sys.argv[1]
    args = sys.argv[2:]

    # Handle help flag
    if sub in ("-h", "--help"):
        _print_help()
        sys.exit(0)

    # Dispatch through the command system
    exit_code = dispatch_command(sub, args)
    if exit_code is not None:
        sys.exit(exit_code)

    # Unknown command
    print(f"Unknown subcommand: {sub}")
    print("Run 'roar --help' for available commands.")
    sys.exit(1)


if __name__ == "__main__":
    main()
