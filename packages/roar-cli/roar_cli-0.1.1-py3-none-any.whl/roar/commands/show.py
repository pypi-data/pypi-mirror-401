"""
Show command - Show artifact, job, or DAG node details.

Usage: roar show <id>
"""

import json
from datetime import datetime
from pathlib import Path

from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from ..presenters.run_report import format_size
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


class ShowCommand(BaseCommand):
    """
    Show details for an artifact, job, DAG, or DAG node.

    Arguments:
      <id>    Artifact hash, job UID, DAG hash, or DAG node (@N or @BN)

    Examples:
      roar show abc123de          # artifact hash prefix
      roar show a1b2c3d4          # job UID
      roar show b4a0c4dd5c5f      # DAG hash (from LaaS)
      roar show @2                # DAG node 2
      roar show @B1               # build node 1
    """

    @property
    def name(self) -> str:
        return "show"

    @property
    def help_text(self) -> str:
        return "Show artifact, job, or DAG node details"

    @property
    def usage(self) -> str:
        return "roar show <id>"

    def requires_init(self) -> bool:
        """Show command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the show command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        lookup_id = args[0]
        roar_dir = ctx.cwd / ".roar"

        with create_database_context(roar_dir) as ctx_db:
            # Check for @N or @BN DAG node reference
            if lookup_id.startswith("@"):
                return self._show_dag_node(ctx_db, lookup_id)

            if len(lookup_id) < 4:
                self.print_error("ID must be at least 4 characters.")
                return self.failure("ID too short")

            # Try job UID first (shorter IDs, 8 hex chars)
            job = ctx_db.jobs.get_by_uid(lookup_id)
            if job:
                self._show_job(ctx_db, job, ctx.cwd)
                return self.success()

            # Try artifact hash (longer, 64 hex chars)
            artifact = None
            from_laas = False

            if len(lookup_id) >= 8:
                artifact = ctx_db.artifacts.get_by_prefix(lookup_id)

                if not artifact:
                    # Try LaaS if configured
                    from ..laas_client import LaasClient

                    laas = LaasClient()

                    if laas.is_configured():
                        laas_artifact, _laas_error = laas.get_artifact(lookup_id)
                        if laas_artifact:
                            artifact = laas_artifact
                            from_laas = True

            if not artifact:
                # Try local DAG/pipeline hash first
                pipeline = ctx_db.sessions.get_by_hash(lookup_id)
                if not pipeline:
                    # Try prefix match
                    cursor = ctx_db.conn.execute(
                        "SELECT * FROM sessions WHERE hash LIKE ? LIMIT 1", (f"{lookup_id}%",)
                    )
                    row = cursor.fetchone()
                    if row:
                        pipeline = dict(row)

                if pipeline:
                    self._show_local_dag(ctx_db, pipeline, ctx.cwd)
                    return self.success()

                # Try DAG hash from LaaS
                from ..laas_client import LaasClient

                laas = LaasClient()

                if laas.is_configured():
                    dag_info, _dag_error = laas.get_dag(lookup_id)
                    if dag_info:
                        self._show_dag_from_laas(dag_info)
                        return self.success()

                self.print(f"No job, artifact, or DAG found matching '{lookup_id}'.")
                return self.failure(f"Not found: {lookup_id}")

            # Display artifact details
            self._show_artifact(ctx_db, artifact, from_laas, ctx.cwd)
            return self.success()

    def _show_dag_node(self, ctx_db, lookup_id: str) -> CommandResult:
        """Show DAG node details."""
        step_ref = lookup_id[1:]

        # Check for @BN (build step) vs @N (run step)
        is_build = False
        if step_ref.upper().startswith("B"):
            is_build = True
            step_ref = step_ref[1:]

        if not step_ref.isdigit():
            self.print_error(
                f"Invalid DAG reference '{lookup_id}'. Use @N or @BN where N is a number."
            )
            return self.failure("Invalid DAG reference")

        step_num = int(step_ref)
        pipeline = ctx_db.sessions.get_active()
        if not pipeline:
            self.print("No active DAG.")
            return self.failure("No active DAG")

        step = ctx_db.sessions.get_step_by_number(
            pipeline["id"], step_num, job_type="build" if is_build else None
        )
        if not step:
            prefix = "@B" if is_build else "@"
            self.print(f"No node {prefix}{step_num} in DAG.")
            return self.failure("Node not found")

        self._show_job(ctx_db, step, Path.cwd())
        return self.success()

    def _show_job(self, ctx_db, job: dict, cwd: Path):
        """Display job details."""
        self.print("Job")
        self.print("=" * 60)
        self.print(f"UID:        {job.get('job_uid', '(none)')}")
        self.print(f"Command:    {job['command']}")
        self.print(f"Timestamp:  {format_timestamp(job['timestamp'])}")
        if job.get("duration_seconds"):
            self.print(f"Duration:   {format_duration(job['duration_seconds'])}")
        if job.get("exit_code") is not None:
            self.print(f"Exit code:  {job['exit_code']}")
        if job.get("git_commit"):
            self.print(f"Git commit: {job['git_commit']}")
        if job.get("session_id"):
            self.print(f"Session:   {job['session_id']} (step @{job.get('step_number', '?')})")
        if job.get("step_name"):
            self.print(f"Step name:  {job['step_name']}")
        self.print("")

        # Show inputs
        inputs = ctx_db.jobs.get_inputs(job["id"], ctx_db.artifacts)
        if inputs:
            self.print(f"Inputs ({len(inputs)}):")
            for inp in inputs[:10]:
                path = inp["path"]
                try:
                    rel = str(Path(path).relative_to(cwd))
                    if not rel.startswith(".."):
                        path = rel
                except ValueError:
                    pass
                # Get blake3 hash from hashes list
                blake3_hash = None
                for h in inp.get("hashes", []):
                    if h.get("algorithm") == "blake3":
                        blake3_hash = h.get("digest")
                        break
                hash_display = (
                    blake3_hash[:12] + "..."
                    if blake3_hash
                    else inp.get("artifact_id", "???")[:12] + "..."
                )
                self.print(f"  {hash_display}  {path}")
            if len(inputs) > 10:
                self.print(f"  ... and {len(inputs) - 10} more")
            self.print("")

        # Show outputs
        outputs = ctx_db.jobs.get_outputs(job["id"], ctx_db.artifacts)
        if outputs:
            self.print(f"Outputs ({len(outputs)}):")
            for out in outputs[:10]:
                path = out["path"]
                try:
                    rel = str(Path(path).relative_to(cwd))
                    if not rel.startswith(".."):
                        path = rel
                except ValueError:
                    pass
                # Get blake3 hash from hashes list
                blake3_hash = None
                for h in out.get("hashes", []):
                    if h.get("algorithm") == "blake3":
                        blake3_hash = h.get("digest")
                        break
                hash_display = (
                    blake3_hash[:12] + "..."
                    if blake3_hash
                    else out.get("artifact_id", "???")[:12] + "..."
                )
                self.print(f"  {hash_display}  {path}")
            if len(outputs) > 10:
                self.print(f"  ... and {len(outputs) - 10} more")
            self.print("")

        # Show metadata (runtime, packages, GPU, etc.)
        if job.get("metadata"):
            try:
                meta = json.loads(job["metadata"])
                self._show_job_metadata(meta)
            except json.JSONDecodeError:
                pass

        # Show telemetry (wandb, etc.)
        if job.get("telemetry"):
            try:
                telemetry = json.loads(job["telemetry"])
                if telemetry:
                    self.print("\nTelemetry:")
                    if "wandb" in telemetry:
                        wandb_url = telemetry["wandb"]
                        if isinstance(wandb_url, list):
                            for url in wandb_url:
                                self.print(f"  wandb: {url}")
                        else:
                            self.print(f"  wandb: {wandb_url}")
            except json.JSONDecodeError:
                pass

    def _show_job_metadata(self, meta: dict):
        """Display job metadata."""
        # Runtime info (GPU, CUDA, CPU)
        runtime = meta.get("runtime", {})
        if runtime.get("gpu"):
            self.print("GPU:")
            for gpu in runtime["gpu"]:
                mem = gpu.get("memory_mb", "?")
                self.print(f"  {gpu.get('name', '?')} ({mem} MB)")

        if runtime.get("cuda"):
            cuda = runtime["cuda"]
            cuda_str = cuda.get("version", "?")
            if cuda.get("cudnn_version"):
                cuda_str += f", cuDNN {cuda['cudnn_version']}"
            self.print(f"CUDA: {cuda_str}")

        if runtime.get("cpu"):
            cpu = runtime["cpu"]
            model = cpu.get("model", "?")
            count = cpu.get("count", "?")
            self.print(f"CPU: {model} ({count} cores)")

        # Packages (pip)
        packages = meta.get("packages", {})
        pip_pkgs = packages.get("pip", {})
        if pip_pkgs:
            self.print(f"\nPackages ({len(pip_pkgs)} pip):")
            # Show key packages first, then the rest alphabetically
            key_pkgs = [
                "torch",
                "tensorflow",
                "jax",
                "numpy",
                "pandas",
                "transformers",
                "scikit-learn",
            ]
            shown_keys = set()
            for pkg in key_pkgs:
                if pkg in pip_pkgs:
                    self.print(f"  {pkg}=={pip_pkgs[pkg]}")
                    shown_keys.add(pkg)
            # Show remaining packages alphabetically
            remaining = sorted([(k, v) for k, v in pip_pkgs.items() if k not in shown_keys])
            for pkg, version in remaining:
                self.print(f"  {pkg}=={version}")

        # Environment variables
        env_vars = runtime.get("env_vars", {})
        if env_vars:
            self.print(f"\nEnvironment ({len(env_vars)} vars):")
            for name, value in sorted(env_vars.items()):
                # Truncate long values
                if len(value) > 60:
                    value = value[:57] + "..."
                self.print(f"  {name}={value}")

    def _show_artifact(self, ctx_db, artifact: dict, from_laas: bool, cwd: Path):
        """Display artifact details."""
        self.print("Artifact")
        self.print("=" * 60)
        self.print(f"Hash:       {artifact['hash']}")
        self.print(f"Size:       {format_size(artifact['size'])}")

        if from_laas:
            self.print("Source:     LaaS")
            if artifact.get("registered_at"):
                self.print(f"Registered: {format_timestamp(artifact['registered_at'])}")
            if artifact.get("registered_by_email"):
                self.print(f"By:         {artifact['registered_by_email']}")
            if artifact.get("source_url"):
                self.print(f"Location:   {artifact['source_url']}")
            self.print("")

            # Get lineage from LaaS
            from ..laas_client import LaasClient

            laas = LaasClient()
            lineage, _ = laas.get_artifact_lineage(artifact["hash"][:12])
            if lineage and lineage.get("produced_by"):
                job = lineage["produced_by"]
                self.print("Produced by:")
                ts = format_timestamp(job["timestamp"]) if job.get("timestamp") else "?"
                cmd = job.get("command", "?")
                if len(cmd) > 50:
                    cmd = cmd[:47] + "..."
                self.print(f"  {ts}  {cmd}")
                if job.get("git_commit"):
                    self.print(f"  commit: {job['git_commit'][:8]}")
                if job.get("user_email"):
                    self.print(f"  user: {job['user_email']}")
                self.print("")

                if lineage.get("inputs"):
                    self.print("Inputs:")
                    for inp in lineage["inputs"][:5]:
                        self.print(f"  {inp['hash'][:12]}...")
                    if len(lineage["inputs"]) > 5:
                        self.print(f"  ... and {len(lineage['inputs']) - 5} more")
        else:
            self.print(f"First seen: {format_timestamp(artifact['first_seen_at'])}")
            if artifact.get("first_seen_path"):
                path = artifact["first_seen_path"]
                try:
                    rel_path = str(Path(path).relative_to(cwd))
                    if not rel_path.startswith(".."):
                        path = rel_path
                except ValueError:
                    pass
                self.print(f"Path:       {path}")
            if artifact.get("synced_at"):
                self.print(f"Synced:     {format_timestamp(artifact['synced_at'])}")
            self.print("")

            # Show lineage from local DB
            jobs = ctx_db.lineage.get_artifact_jobs(artifact["hash"])

            if jobs["produced_by"]:
                self.print("Produced by:")
                for job in jobs["produced_by"][:5]:
                    ts = format_timestamp(job["timestamp"])
                    cmd = job["command"]
                    job_uid = job.get("job_uid", "")
                    if len(cmd) > 50:
                        cmd = cmd[:47] + "..."
                    uid_str = f"[{job_uid}]" if job_uid else f"[job {job['id']}]"
                    self.print(f"  {uid_str} {ts}  {cmd}")
                if len(jobs["produced_by"]) > 5:
                    self.print(f"  ... and {len(jobs['produced_by']) - 5} more")
                self.print("")

            if jobs["consumed_by"]:
                self.print("Consumed by:")
                for job in jobs["consumed_by"][:5]:
                    ts = format_timestamp(job["timestamp"])
                    cmd = job["command"]
                    job_uid = job.get("job_uid", "")
                    if len(cmd) > 50:
                        cmd = cmd[:47] + "..."
                    uid_str = f"[{job_uid}]" if job_uid else f"[job {job['id']}]"
                    self.print(f"  {uid_str} {ts}  {cmd}")
                if len(jobs["consumed_by"]) > 5:
                    self.print(f"  ... and {len(jobs['consumed_by']) - 5} more")
                self.print("")

            # Show current locations of this artifact
            locations = ctx_db.artifacts.get_locations(artifact["hash"])
            if locations:
                self.print("Known locations:")
                for loc in locations[:10]:
                    path = loc["path"]
                    try:
                        rel_path = str(Path(path).relative_to(cwd))
                        if not rel_path.startswith(".."):
                            path = rel_path
                    except ValueError:
                        pass
                    self.print(f"  {path}")
                if len(locations) > 10:
                    self.print(f"  ... and {len(locations) - 10} more")

    def _show_local_dag(self, ctx_db, pipeline: dict, cwd: Path):
        """Display local DAG/pipeline details."""
        self.print("DAG (local)")
        self.print("=" * 60)
        self.print(f"Hash:       {pipeline.get('hash', '?')}")
        if pipeline.get("created_at"):
            self.print(f"Created:    {format_timestamp(pipeline['created_at'])}")
        if pipeline.get("git_repo"):
            self.print(f"Git repo:   {pipeline['git_repo']}")
        if pipeline.get("git_commit_start"):
            self.print(f"Git commit: {pipeline['git_commit_start']}")
        if pipeline.get("is_active"):
            self.print("Status:     active")
        self.print("")

        # Get steps
        steps = ctx_db.sessions.get_steps(pipeline["id"])

        if steps:
            # Separate build and run steps
            build_steps = [s for s in steps if s.get("job_type") == "build"]
            run_steps = [s for s in steps if s.get("job_type") != "build"]

            if build_steps:
                self.print(f"Build steps ({len(build_steps)}):")
                for step in build_steps:
                    step_num = step.get("step_number", "?")
                    cmd = step.get("command", "?")
                    uid = step.get("uid", "")[:8] if step.get("uid") else ""
                    exit_code = step.get("exit_code")
                    status = "✓" if exit_code == 0 else "✗" if exit_code else "?"
                    if len(cmd) > 55:
                        cmd = cmd[:52] + "..."
                    uid_str = f" [{uid}]" if uid else ""
                    self.print(f"  {status} @B{step_num}: {cmd}{uid_str}")
                self.print("")

            if run_steps:
                self.print(f"Run steps ({len(run_steps)}):")
                for step in run_steps:
                    step_num = step.get("step_number", "?")
                    cmd = step.get("command", "?")
                    uid = step.get("uid", "")[:8] if step.get("uid") else ""
                    exit_code = step.get("exit_code")
                    status = "✓" if exit_code == 0 else "✗" if exit_code else "?"
                    if len(cmd) > 55:
                        cmd = cmd[:52] + "..."
                    uid_str = f" [{uid}]" if uid else ""
                    self.print(f"  {status} @{step_num}: {cmd}{uid_str}")
                self.print("")

        # Show outputs from this pipeline's jobs
        cursor = ctx_db.conn.execute(
            """
            SELECT DISTINCT da.hash, da.size, jo.path
            FROM job_outputs jo
            JOIN data_artifacts da ON jo.artifact_hash = da.hash
            JOIN jobs j ON jo.job_id = j.id
            WHERE j.session_id = ?
            ORDER BY j.timestamp DESC
            LIMIT 10
            """,
            (pipeline["id"],),
        )
        outputs = [dict(row) for row in cursor.fetchall()]

        if outputs:
            self.print(f"Outputs ({len(outputs)} shown):")
            for out in outputs:
                hash_short = out["hash"][:12]
                size = format_size(out.get("size"))
                path = out.get("path", "")
                if path:
                    try:
                        rel_path = str(Path(path).relative_to(cwd))
                        if not rel_path.startswith(".."):
                            path = rel_path
                    except ValueError:
                        pass
                    if len(path) > 40:
                        path = "..." + path[-37:]
                self.print(f"  {hash_short}...  {size:>8}  {path}")
            self.print("")

        pipeline.get("hash", "")[:12]
        self.print(
            "Use 'roar show @N' for step details, 'roar run @N' to re-run (use @BN for builds)"
        )

    def _show_dag_from_laas(self, dag_response: dict):
        """Display DAG details from LaaS."""
        # Handle the nested structure from API
        dag_info = dag_response.get("dag", dag_response)
        jobs = dag_response.get("jobs", [])

        self.print("DAG")
        self.print("=" * 60)
        self.print(f"Hash:       {dag_info.get('hash', '?')}")
        if dag_info.get("created_at"):
            self.print(f"Created:    {format_timestamp(dag_info['created_at'])}")
        if dag_info.get("created_by_email"):
            self.print(f"By:         {dag_info['created_by_email']}")
        if dag_info.get("git_repo"):
            self.print(f"Git repo:   {dag_info['git_repo']}")
        if dag_info.get("git_commit"):
            self.print(f"Git commit: {dag_info['git_commit']}")
        self.print("")

        dag_hash = dag_info.get("hash", "")[:12]

        if jobs:
            # Separate build and run steps
            build_steps = [j for j in jobs if j.get("job_type") == "build"]
            run_steps = [j for j in jobs if j.get("job_type") != "build"]

            if build_steps:
                self.print(f"Build steps ({len(build_steps)}):")
                for job in build_steps:
                    step = job.get("step_number", "?")
                    cmd = job.get("command", "?")
                    if len(cmd) > 60:
                        cmd = cmd[:57] + "..."
                    self.print(f"  @B{step}  {cmd}")
                self.print("")

            if run_steps:
                self.print(f"DAG steps ({len(run_steps)}):")
                for job in run_steps:
                    step = job.get("step_number", "?")
                    cmd = job.get("command", "?")
                    if len(cmd) > 60:
                        cmd = cmd[:57] + "..."
                    self.print(f"  @{step}  {cmd}")
                self.print("")

        # Show produced artifacts
        artifacts = dag_info.get("artifacts", [])
        if artifacts:
            self.print(f"Produced artifacts ({len(artifacts)}):")
            for art in artifacts[:10]:
                hash_short = art.get("hash", "?")[:12]
                size = format_size(art.get("size"))
                url = art.get("source_url", "")
                if url:
                    # Extract filename from URL
                    name = url.split("/")[-1] if "/" in url else url
                    if len(name) > 40:
                        name = name[:37] + "..."
                    self.print(f"  {hash_short}...  {size:>8}  {name}")
                else:
                    self.print(f"  {hash_short}...  {size:>8}")
            if len(artifacts) > 10:
                self.print(f"  ... and {len(artifacts) - 10} more")
            self.print("")

        self.print(f"To reproduce: roar reproduce {dag_hash}")

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar show <id>

Show details for an artifact, job, DAG, or DAG node.

Arguments:
  <id>    Artifact hash, job UID, DAG hash, or DAG node (@N or @BN)

Examples:
  roar show abc123de          # artifact hash prefix
  roar show a1b2c3d4          # job UID
  roar show b4a0c4dd5c5f      # DAG hash (from LaaS)
  roar show @2                # DAG node 2
  roar show @B1               # build node 1
"""
