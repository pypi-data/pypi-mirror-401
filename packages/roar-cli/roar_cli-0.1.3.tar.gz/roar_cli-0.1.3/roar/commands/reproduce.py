"""
Reproduce command - Reproduce an artifact from a LaaS server.

Usage: roar reproduce <hash> [options]
"""

import json
import subprocess
from pathlib import Path

from ..core.container import get_container
from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from .base import BaseCommand


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


class ReproduceCommand(BaseCommand):
    """
    Reproduce an artifact from a LaaS server.
    Clones the repository, installs packages, and optionally runs the pipeline.

    Options:
      --server URL  LaaS server URL (required if not configured)
      --run         Also run the pipeline after setup
      -y            Auto-confirm (no prompts)

    Examples:
      roar reproduce abc123de --server https://laas.example.com
      roar reproduce abc123de --run    # Setup and run pipeline
    """

    @property
    def name(self) -> str:
        return "reproduce"

    @property
    def help_text(self) -> str:
        return "Reproduce an artifact"

    @property
    def usage(self) -> str:
        return "roar reproduce <hash> [options]"

    def requires_init(self) -> bool:
        """Reproduce command doesn't require roar to be initialized."""
        return False

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the reproduce command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        # Parse arguments
        hash_prefix = None
        run_pipeline = False
        auto_confirm = False
        server_url = None

        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--run":
                run_pipeline = True
            elif arg == "-y":
                auto_confirm = True
            elif arg == "--server":
                if i + 1 < len(args):
                    server_url = args[i + 1]
                    i += 1
                else:
                    self.print_error("--server requires a URL")
                    return self.failure("--server requires a URL")
            elif not arg.startswith("-") and hash_prefix is None:
                hash_prefix = arg
            i += 1

        if not hash_prefix:
            self.print_error("Hash prefix is required.")
            self.print("Usage: roar reproduce <hash> [--server URL] [--run] [-y]")
            return self.failure("Hash prefix required")

        if len(hash_prefix) < 8:
            self.print_error("Hash prefix must be at least 8 characters.")
            return self.failure("Hash prefix too short")

        # First try local database (if initialized)
        roar_dir = ctx.cwd / ".roar"
        if roar_dir.exists():
            with create_database_context(roar_dir) as ctx_db:
                artifact = ctx_db.artifacts.get_by_prefix(hash_prefix)
                if artifact:
                    return self._reproduce_local(ctx_db, artifact, run_pipeline, auto_confirm)

        # Not found locally - try LaaS server
        from ..laas_client import LaasClient

        if server_url:
            laas = LaasClient(base_url=server_url)
        else:
            laas = LaasClient()

        if not laas.is_configured():
            if roar_dir.exists():
                self.print(f"No artifact found matching '{hash_prefix}' locally.")
            self.print("")
            self.print("LaaS server not configured. Use --server to specify:")
            self.print(f"  roar reproduce {hash_prefix} --server https://laas.example.com")
            return self.failure("LaaS not configured")

        # Query server - try artifact first, then DAG
        artifact, error = laas.get_artifact(hash_prefix)
        if artifact:
            return self._reproduce_from_server(
                laas, artifact, run_pipeline, auto_confirm, server_url
            )

        # Not found as artifact - try as DAG hash
        dag_info, _dag_error = laas.get_dag(hash_prefix)
        if dag_info:
            return self._reproduce_dag_from_server(
                laas, dag_info, run_pipeline, auto_confirm, server_url
            )

        # Neither found
        if error:
            self.print_error(f"Error querying LaaS: {error}")
        else:
            self.print(f"No artifact or DAG found matching '{hash_prefix}' on server.")
        return self.failure("Not found")

    def _reproduce_local(
        self, ctx, artifact: dict, run_pipeline: bool, auto_confirm: bool
    ) -> CommandResult:
        """Reproduce an artifact from local database."""
        full_hash = artifact.get("hash") or artifact.get("id") or ""
        self.print(f"Artifact: {full_hash[:12]}... (local)")
        if artifact.get("first_seen_path"):
            self.print(f"Path: {artifact['first_seen_path']}")
        self.print("")

        # Trace lineage to build pipeline
        lineage = ctx.lineage.get_artifact_lineage(full_hash, depth=10)

        # Collect all jobs in the lineage (reverse order - oldest first)
        jobs_in_lineage = []
        seen = set()

        def collect_jobs(node):
            if node.get("truncated") or node.get("not_found"):
                return
            if "produced_by" in node:
                producer = node["produced_by"]
                job_id = producer["job_id"]
                if job_id not in seen:
                    seen.add(job_id)
                    # Recurse into inputs first (to get proper order)
                    for inp in producer.get("inputs", []):
                        collect_jobs(inp)
                    # Then add this job
                    job = ctx.jobs.get(job_id)
                    if job:
                        jobs_in_lineage.append(job)

        collect_jobs(lineage)

        if not jobs_in_lineage:
            self.print("No lineage found for this artifact.")
            self.print("The artifact may have been registered externally (via 'roar get').")
            self.print("")
            if artifact.get("source_url"):
                self.print(f"Source: {artifact['source_url']}")
                self.print("Use 'roar get' to re-download from source.")
            return self.success()

        # Display the pipeline
        self.print(f"Pipeline to reproduce {full_hash[:12]}...")
        self.print(f"Steps: {len(jobs_in_lineage)}")
        self.print("")

        self.print("Steps:")
        for i, job in enumerate(jobs_in_lineage, 1):
            command = job["command"]
            git_commit = job.get("git_commit", "")[:8] if job.get("git_commit") else ""

            max_cmd_len = 60
            if len(command) > max_cmd_len:
                display_cmd = command[: max_cmd_len - 3] + "..."
            else:
                display_cmd = command

            commit_str = f" [{git_commit}]" if git_commit else ""
            self.print(f"  @{i}: {display_cmd}{commit_str}")

        self.print("")

        if not run_pipeline and not auto_confirm:
            self.print("Run 'roar reproduce <hash> --run' to execute this pipeline.")
            self.print("Or 'roar dag' after creation to see steps.")
            return self.success()

        # Ask for confirmation unless -y
        if not auto_confirm and not self.confirm("Create pipeline and run?", default=False):
            self.print("Aborted.")
            return self.success()

        # Create a new pipeline
        session_id = ctx.sessions.create(
            source_artifact_hash=artifact["hash"],
            make_active=True,
        )

        self.print(f"\nCreated pipeline {session_id}")

        # Add jobs as steps
        vcs = get_container().get_vcs_provider("git")
        repo_root = vcs.get_repo_root()
        for i, job in enumerate(jobs_in_lineage, 1):
            inputs = ctx.jobs.get_inputs(job["id"], ctx.artifacts)
            outputs = ctx.jobs.get_outputs(job["id"], ctx.artifacts)
            input_paths = [inp["path"] for inp in inputs if inp.get("path")]
            output_paths = [out["path"] for out in outputs if out.get("path")]
            step_identity = ctx.session_service.compute_step_identity(
                input_paths, output_paths, repo_root, job["command"]
            )

            ctx.conn.execute(
                """
                UPDATE jobs SET session_id = ?, step_number = ?, step_identity = ?
                WHERE id = ?
                """,
                (session_id, i, step_identity, job["id"]),
            )

        ctx.conn.commit()
        ctx.sessions.update_hash(session_id, ctx.jobs)

        self.print(f"Pipeline ready with {len(jobs_in_lineage)} steps.")
        self.print("")

        if run_pipeline:
            self.print("Running pipeline...")
            self.print("")

            for i, job in enumerate(jobs_in_lineage, 1):
                ctx.sessions.update_current_step(session_id, i)
                command = job["command"]
                self.print(f"--- Step @{i}: {command} ---")

                result = subprocess.run(["roar", "run", *command.split()], cwd=Path.cwd())

                if result.returncode != 0:
                    self.print(f"\nStep @{i} failed with exit code {result.returncode}")
                    self.print(f"Resume with: roar run @{i}")
                    return self.failure(f"Step @{i} failed", exit_code=result.returncode)

                self.print(f"Step @{i} completed.")
                self.print("")

            self.print("Pipeline completed! Target artifact should be reproduced.")
        else:
            self.print("Run 'roar dag' to see the pipeline.")
            self.print("Run 'roar run @1' to execute step 1, etc.")

        return self.success()

    def _reproduce_from_server(
        self,
        laas,
        artifact: dict,
        run_pipeline: bool,
        auto_confirm: bool,
        server_url: str | None = None,
    ) -> CommandResult:
        """Reproduce an artifact from LaaS server using its DAG."""
        full_hash = artifact["hash"]

        # Check if we're in a git repo - must run from empty directory
        vcs = get_container().get_vcs_provider("git")
        repo_root = vcs.get_repo_root()
        if repo_root is not None:
            self.print_error("Cannot run 'roar reproduce' from inside a git repository.")
            self.print("")
            self.print(
                "Run from an empty directory to clone and set up the reproduction environment:"
            )
            self.print("  cd /path/to/empty/dir")
            self.print(f"  roar reproduce {full_hash[:12]} --server <url>")
            return self.failure("Inside git repository")

        self.print(f"Artifact: {full_hash[:12]}... (from server)")
        if artifact.get("source_url"):
            self.print(f"Source: {artifact['source_url']}")
        self.print("")

        # Get the DAG for this artifact from server
        dag_info, error = laas.get_artifact_dag(full_hash)
        if error:
            self.print_error(f"Error getting DAG: {error}")
            return self.failure(f"DAG error: {error}")

        # Check if artifact is external (no producing DAG)
        if dag_info.get("is_external"):
            self.print("This artifact is external (registered via 'roar get').")
            self.print("It was not produced by a tracked job.")
            self.print("")
            if artifact.get("source_url"):
                self.print("To download:")
                self.print(f"  roar get {artifact['source_url']} <dest>")
            return self.success()

        return self._reproduce_with_dag(
            laas, dag_info, full_hash, run_pipeline, auto_confirm, server_url
        )

    def _reproduce_dag_from_server(
        self,
        laas,
        dag_response: dict,
        run_pipeline: bool,
        auto_confirm: bool,
        server_url: str | None = None,
    ) -> CommandResult:
        """Reproduce a DAG directly from LaaS server."""
        dag = dag_response.get("dag", dag_response)
        jobs = dag_response.get("jobs", [])
        dag_hash = dag.get("hash", "?")

        # Check if we're in a git repo
        vcs = get_container().get_vcs_provider("git")
        repo_root = vcs.get_repo_root()
        if repo_root is not None:
            self.print_error("Cannot run 'roar reproduce' from inside a git repository.")
            self.print("")
            self.print(
                "Run from an empty directory to clone and set up the reproduction environment:"
            )
            self.print("  cd /path/to/empty/dir")
            self.print(f"  roar reproduce {dag_hash[:12]} --server <url>")
            return self.failure("Inside git repository")

        self.print(f"DAG: {dag_hash[:12]}...")
        self.print("")

        if not jobs:
            self.print("No jobs found in DAG.")
            return self.success()

        dag_info = {
            "dag": dag,
            "jobs": jobs,
            "external_deps": [],
            "is_external": False,
        }

        return self._reproduce_with_dag(
            laas, dag_info, dag_hash, run_pipeline, auto_confirm, server_url
        )

    def _reproduce_with_dag(
        self,
        laas,
        dag_info: dict,
        ref_hash: str,
        run_pipeline: bool,
        auto_confirm: bool,
        server_url: str | None = None,
    ) -> CommandResult:
        """Shared implementation for reproducing from a DAG."""
        dag = dag_info.get("dag")
        jobs = dag_info.get("jobs", [])
        external_deps = dag_info.get("external_deps", [])

        if not jobs:
            self.print("No jobs found in DAG.")
            self.print("The artifact may have been registered without job tracking.")
            return self.success()

        # Extract git and package info from jobs
        git_repo = None
        git_commit = None
        cwd = None
        _packages: dict[str, dict[str, str]] = {"pip": {}, "dpkg": {}}

        for job in jobs:
            if not git_repo and job.get("git_repo"):
                git_repo = job["git_repo"]
            if not git_commit and job.get("git_commit"):
                git_commit = job["git_commit"]
            if job.get("metadata"):
                try:
                    meta = (
                        json.loads(job["metadata"])
                        if isinstance(job["metadata"], str)
                        else job["metadata"]
                    )
                    if not cwd and meta.get("cwd"):
                        cwd = meta["cwd"]
                    job_packages = meta.get("packages", {})
                    for pkg_type in ("pip", "dpkg"):
                        job_pkgs = job_packages.get(pkg_type, {})
                        if isinstance(job_pkgs, dict):
                            for pkg, version in job_pkgs.items():
                                if pkg not in _packages[pkg_type]:
                                    _packages[pkg_type][pkg] = version
                except (json.JSONDecodeError, TypeError):
                    pass

        packages: dict[str, dict[str, str]] | None = (
            _packages if _packages["pip"] or _packages["dpkg"] else None
        )

        # Display info
        dag_hash_short = dag["hash"][:12] if dag else "?"
        self.print(f"DAG: {dag_hash_short}...")
        self.print(f"Steps: {len(jobs)}")
        self.print("")

        if git_repo:
            self.print(f"Repository: {git_repo}")
        if git_commit:
            self.print(f"Commit: {git_commit}")
        if packages:
            pip_pkgs = packages.get("pip", {})
            if pip_pkgs:
                self.print(f"Packages: {len(pip_pkgs)} pip packages")
        self.print("")

        if external_deps:
            self.print("External dependencies:")
            for dep in external_deps:
                source = dep.get("source_url", "")
                self.print(f"  {dep['hash'][:12]}...  {source or '(no source)'}")
            self.print("")

        self.print("Steps:")
        for job in jobs:
            step_num = job.get("step_number", "?")
            command = job.get("command", "(unknown)")
            commit = (job.get("git_commit") or "")[:8]
            job_type = job.get("job_type") or "run"

            max_cmd_len = 60
            if len(command) > max_cmd_len:
                display_cmd = command[: max_cmd_len - 3] + "..."
            else:
                display_cmd = command

            commit_str = f" [{commit}]" if commit else ""
            step_prefix = "@B" if job_type == "build" else "@"
            self.print(f"  {step_prefix}{step_num}: {display_cmd}{commit_str}")

        self.print("")

        if not git_repo:
            self.print_error("No git repository information in DAG.")
            self.print("Cannot set up reproduction environment.")
            return self.failure("No git repo info")

        # Clone the repository
        if not auto_confirm and not self.confirm(f"Clone {git_repo}?", default=True):
            self.print("Aborted.")
            self.print("")
            self.print("To set up manually:")
            self.print(f"  git clone {git_repo}")
            repo_name = git_repo.rstrip("/").split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
            self.print(f"  cd {repo_name}")
            if git_commit:
                self.print(f"  git checkout {git_commit}")
            self.print("  roar init")
            self.print(f"  roar reproduce {ref_hash[:12]} --run")
            return self.success()

        repo_name = git_repo.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        repo_dir = Path.cwd() / repo_name

        if repo_dir.exists():
            existing_remote = None
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    existing_remote = result.stdout.strip()
            except Exception:
                pass

            if existing_remote == git_repo:
                self.print(f"Using existing clone of {git_repo}")
            else:
                self.print(f"Directory '{repo_name}' already exists.")
                if existing_remote:
                    self.print(f"  (contains different repo: {existing_remote})")
                if not auto_confirm and not self.confirm(
                    "Use existing directory anyway?", default=False
                ):
                    self.print("Aborted.")
                    return self.success()
        else:
            self.print(f"Cloning {git_repo}...")
            result = subprocess.run(
                ["git", "clone", git_repo, str(repo_dir)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.print_error(f"Error cloning repository: {result.stderr}")
                return self.failure("Clone failed")
            self.print(f"  Cloned to {repo_dir}")

        # Checkout the specific commit
        if git_commit:
            self.print(f"Checking out {git_commit[:12]}...")
            result = subprocess.run(
                ["git", "checkout", git_commit],
                cwd=repo_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                self.print("  Commit not found locally, fetching from remote...")
                subprocess.run(
                    ["git", "fetch", "origin"],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                )
                result = subprocess.run(
                    ["git", "checkout", git_commit],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    self.print_error(f"Error checking out commit: {result.stderr}")
                    return self.failure("Checkout failed")

        # Initialize roar in the repo
        roar_dir = repo_dir / ".roar"
        if not roar_dir.exists():
            self.print("Initializing roar...")
            subprocess.run(
                ["roar", "init"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
            )

        # Configure LaaS server if provided
        if server_url:
            self.print(f"Configuring LaaS server: {server_url}")
            subprocess.run(
                ["roar", "config", "set", "laas.url", server_url],
                cwd=repo_dir,
                capture_output=True,
                text=True,
            )

        # Create venv and install packages
        venv_dir = repo_dir / ".venv"

        if packages:
            pip_pkgs = packages.get("pip", {})
            if pip_pkgs:
                requirements = []
                skipped = []
                for pkg, version in pip_pkgs.items():
                    pkg_lower = pkg.lower().replace("-", "_").replace(".", "_")
                    repo_lower = repo_name.lower().replace("-", "_").replace(".", "_")
                    if pkg_lower == repo_lower or repo_lower.startswith(pkg_lower + "_"):
                        skipped.append(pkg)
                        continue
                    if version:
                        requirements.append(f"{pkg}=={version}")
                    else:
                        requirements.append(pkg)

                if skipped:
                    self.print(f"Skipping local project package: {', '.join(skipped)}")

                if requirements:
                    if not venv_dir.exists():
                        self.print("Creating virtual environment...")
                        result = subprocess.run(
                            ["uv", "venv", str(venv_dir)],
                            cwd=repo_dir,
                            capture_output=True,
                            text=True,
                        )
                        if result.returncode != 0:
                            subprocess.run(
                                ["python", "-m", "venv", str(venv_dir)],
                                cwd=repo_dir,
                                capture_output=True,
                                text=True,
                            )

                    self.print(f"Installing {len(requirements)} pip packages...")

                    uv_available = (
                        subprocess.run(["which", "uv"], capture_output=True).returncode == 0
                    )

                    if uv_available and venv_dir.exists():
                        subprocess.run(
                            [
                                "uv",
                                "pip",
                                "install",
                                "--prefix",
                                str(venv_dir.resolve()),
                                *requirements,
                            ],
                            cwd=repo_dir,
                            capture_output=True,
                            text=True,
                        )
                    else:
                        venv_pip = venv_dir / "bin" / "pip"
                        if venv_pip.exists():
                            subprocess.run(
                                [str(venv_pip.resolve()), "install", *requirements],
                                cwd=repo_dir,
                                capture_output=True,
                                text=True,
                            )

        # Populate local DB with DAG jobs
        roar_dir = repo_dir / ".roar"
        if roar_dir.exists() and jobs:
            self.print("Populating local DAG...")
            with create_database_context(roar_dir) as local_ctx:
                local_ctx.sessions.populate_from_server(
                    source_artifact_hash=ref_hash,
                    jobs=jobs,
                    git_repo=git_repo,
                    git_commit=git_commit,
                )
            self.print(f"  {len(jobs)} steps ready (use 'roar dag' to view)")

        if venv_dir.exists():
            self.print("")
            self.print("Note: Activate the virtual environment before running:")
            self.print(f"  source {venv_dir}/bin/activate")

        if external_deps:
            self.print("")
            self.print("External dependencies needed:")
            for dep in external_deps:
                source = dep.get("source_url")
                self.print(f"  {dep['hash'][:12]}...  {source or '(no source)'}")
            self.print("")
            self.print("Download these with 'roar get <url> <dest>' before running.")

        self.print("")
        self.print(f"Repository ready at: {repo_dir}")
        self.print("")

        if not run_pipeline:
            self.print("To run the reproduction pipeline:")
            self.print(f"  cd {repo_dir}")
            self.print("  source .venv/bin/activate")
            self.print("  roar dag              # View steps")
            self.print("  roar run @1           # Run step 1")
            self.print("  roar dag script | bash  # Run all steps")
            return self.success()

        # --run specified: execute the pipeline
        self.print(f"Running pipeline in {repo_dir}...")
        self.print("")

        build_jobs = [j for j in jobs if j.get("job_type") == "build"]
        run_jobs = [j for j in jobs if j.get("job_type") != "build"]

        if build_jobs:
            self.print("=== Build Steps ===")
            self.print("")
            for job in build_jobs:
                step_num = job.get("step_number", "?")
                command = job.get("command", "")
                if not command:
                    self.print(f"Build @B{step_num}: No command found, skipping")
                    continue

                self.print(f"--- Build @B{step_num}: {command} ---")
                build_result = subprocess.run(["roar", "build", *command.split()], cwd=repo_dir)
                if build_result.returncode != 0:
                    self.print(
                        f"\nBuild @B{step_num} failed with exit code {build_result.returncode}"
                    )
                    return self.failure(
                        f"Build @B{step_num} failed", exit_code=build_result.returncode
                    )
                self.print(f"Build @B{step_num} completed.")
                self.print("")

        if run_jobs:
            if build_jobs:
                self.print("=== Run Steps ===")
                self.print("")
            for job in run_jobs:
                step_num = job.get("step_number", "?")
                command = job.get("command", "")
                if not command:
                    self.print(f"Step @{step_num}: No command found, skipping")
                    continue

                self.print(f"--- Step @{step_num}: {command} ---")
                run_result = subprocess.run(["roar", "run", *command.split()], cwd=repo_dir)
                if run_result.returncode != 0:
                    self.print(f"\nStep @{step_num} failed with exit code {run_result.returncode}")
                    return self.failure(f"Step @{step_num} failed", exit_code=run_result.returncode)
                self.print(f"Step @{step_num} completed.")
                self.print("")

        self.print("Pipeline completed! Target artifact should be reproduced.")
        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar reproduce <hash> [options]

Reproduce an artifact from a LaaS server.
Clones the repository, installs packages, and optionally runs the pipeline.

Options:
  --server URL  LaaS server URL (required if not configured)
  --run         Also run the pipeline after setup
  -y            Auto-confirm (no prompts)

Examples:
  roar reproduce abc123de --server https://laas.example.com
  roar reproduce abc123de --run    # Setup and run pipeline
"""
