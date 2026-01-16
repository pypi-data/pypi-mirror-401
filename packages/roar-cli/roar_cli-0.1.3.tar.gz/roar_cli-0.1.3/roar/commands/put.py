"""
Put command - Upload and register artifacts.

Usage: roar put <src...> <url>
"""

import json
from pathlib import Path

from ..config import config_get
from ..core.container import get_container
from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from ..presenters.run_report import format_size
from .base import BaseCommand


class PutCommand(BaseCommand):
    """
    Upload local artifacts to cloud storage and register with LaaS.
    Ensures traceability by requiring LaaS registration and git access.

    Supported URLs:
      s3://bucket/key           AWS S3
      gs://bucket/key           Google Cloud Storage

    Examples:
      roar put ./model.pt s3://my-bucket/models/model.pt
      roar put ./model.pt ./tokenizer.json s3://my-bucket/models/
      roar put ./outputs/ s3://my-bucket/results/  # directory
    """

    @property
    def name(self) -> str:
        return "put"

    @property
    def help_text(self) -> str:
        return "Upload and register artifacts"

    @property
    def usage(self) -> str:
        return "roar put <src...> <url>"

    def requires_init(self) -> bool:
        """Put command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the put command."""
        from ..laas_client import LaasClient
        from ..utils.cloud import parse_cloud_url

        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        if len(args) < 2:
            self.print_error("Both <src> and <url> are required.")
            self.print("Usage: roar put <src...> <url>")
            return self.failure("Missing arguments")

        # Last argument is destination URL, rest are sources
        dest_url = args[-1]
        source_paths = args[:-1]

        # Verify all sources exist
        sources = []
        for source_path in source_paths:
            src = Path(source_path)
            if not src.exists():
                self.print_error(f"Source path does not exist: {source_path}")
                return self.failure(f"Source not found: {source_path}")
            sources.append(src)

        # Parse URL
        try:
            scheme, _bucket, _key = parse_cloud_url(dest_url)
        except ValueError as e:
            self.print_error(str(e))
            return self.failure(str(e))

        # Multiple sources require destination to be a directory (end with /)
        if len(sources) > 1 and not dest_url.endswith("/"):
            self.print_error("When uploading multiple files, destination must end with /")
            return self.failure("Destination must end with /")

        is_dir = len(sources) > 1 or sources[0].is_dir()
        roar_dir = ctx.cwd / ".roar"

        # -------------------------------------------------------------------------
        # Pre-flight checks: Ensure traceability before uploading anything
        # -------------------------------------------------------------------------

        self.print("Checking traceability requirements...")

        # 1. Check LaaS server connectivity
        laas = LaasClient()

        if not laas.is_configured():
            self.print_error("LaaS server not configured.")
            self.print("Configure with: roar config set laas.url <server-url>")
            self.print("")
            self.print("roar put requires LaaS registration to ensure artifact traceability.")
            return self.failure("LaaS not configured")

        ok, err = laas.health_check()
        if not ok:
            self.print_error(f"Cannot reach LaaS server: {err}")
            self.print("")
            self.print("roar put requires LaaS registration to ensure artifact traceability.")
            self.print("Check your network connection and server URL.")
            return self.failure(f"LaaS unreachable: {err}")

        # 2. Check git push access (for tagging)
        vcs = get_container().get_vcs_provider("git")
        repo_root = vcs.get_repo_root()
        if repo_root:
            vcs_info = vcs.get_info(repo_root)
            git_repo = vcs_info.remote_url

            if git_repo:
                has_access, access_error = self._check_git_push_access(git_repo, repo_root)
                if not has_access:
                    self.print_error(f"No git push access: {access_error}")
                    self.print("")
                    self.print("roar put requires git push access for reproducibility tagging.")
                    self.print("Ensure you have write access to the repository.")
                    return self.failure(f"No git push access: {access_error}")

        self.print("  LaaS server: OK")
        if repo_root:
            self.print("  Git push access: OK")

        # -------------------------------------------------------------------------
        # Hash files locally
        # -------------------------------------------------------------------------

        artifacts = []  # List of (hash, size, path, rel_path)

        self.print("Hashing files...")
        with create_database_context(roar_dir) as ctx_db:
            for src in sources:
                if src.is_dir():
                    for file_path in src.rglob("*"):
                        if file_path.is_file():
                            file_hash = ctx_db.hashing.compute_file_hash(str(file_path))
                            if file_hash:
                                size = file_path.stat().st_size
                                rel_path = str(file_path.relative_to(src))
                                artifacts.append((file_hash, size, str(file_path), rel_path))
                else:
                    file_hash = ctx_db.hashing.compute_file_hash(str(src))
                    if file_hash:
                        size = src.stat().st_size
                        artifacts.append((file_hash, size, str(src), src.name))

        if not artifacts:
            self.print_error("No files to upload")
            return self.failure("No files to upload")

        total_size = sum(a[1] for a in artifacts)

        # -------------------------------------------------------------------------
        # Upload to cloud storage
        # -------------------------------------------------------------------------

        self.print(f"Uploading {len(artifacts)} file(s), {format_size(total_size)}...")

        # Build list of (local_path, dest_url) for batch upload
        upload_files = []
        for _file_hash, _size, path, rel_path in artifacts:
            if is_dir:
                file_url = f"{dest_url.rstrip('/')}/{rel_path}"
            else:
                file_url = dest_url
            upload_files.append((path, file_url))

        cloud_provider = get_container().get_cloud_provider(scheme)
        success, error = cloud_provider.upload_batch(upload_files)
        if not success:
            self.print_error(f"Upload failed: {error}")
            return self.failure(f"Upload failed: {error}")

        # -------------------------------------------------------------------------
        # Register with LaaS
        # -------------------------------------------------------------------------

        dag_hash = None

        self.print("Registering with LaaS...")

        # Get all artifact hashes being uploaded
        artifact_hashes = [a[0] for a in artifacts]

        # Collect lineage DAG
        with create_database_context(roar_dir) as ctx_db:
            lineage_jobs = ctx_db.lineage.get_lineage_jobs(artifact_hashes)

            # Also include build jobs from the active pipeline
            pipeline = ctx_db.sessions.get_active()
            if pipeline:
                build_jobs = ctx_db.conn.execute(
                    """
                    SELECT j.* FROM jobs j
                    INNER JOIN (
                        SELECT step_number, MAX(id) as max_id
                        FROM jobs
                        WHERE session_id = ? AND job_type = 'build'
                        GROUP BY step_number
                    ) latest ON j.id = latest.max_id
                    ORDER BY j.step_number
                    """,
                    (pipeline["id"],),
                ).fetchall()

                # Prepend build jobs
                build_job_ids = set()
                build_job_list = []
                for bj in build_jobs:
                    job_dict = dict(bj)
                    build_job_ids.add(bj["id"])
                    inputs = ctx_db.jobs.get_inputs(bj["id"], ctx_db.artifacts)
                    outputs = ctx_db.jobs.get_outputs(bj["id"], ctx_db.artifacts)

                    def get_blake3(item):
                        for h in item.get("hashes", []):
                            if h.get("algorithm") == "blake3":
                                return h.get("digest")
                        return None

                    job_dict["_input_hashes"] = [
                        h for h in (get_blake3(inp) for inp in inputs) if h
                    ]
                    job_dict["_output_hashes"] = [
                        h for h in (get_blake3(out) for out in outputs) if h
                    ]
                    build_job_list.append(job_dict)

                lineage_jobs = build_job_list + [
                    j for j in lineage_jobs if j["id"] not in build_job_ids
                ]

            # Collect ALL artifact hashes referenced by jobs
            all_lineage_hashes = set()
            for job in lineage_jobs:
                for h in job.get("_input_hashes", []):
                    all_lineage_hashes.add(h)
                for h in job.get("_output_hashes", []):
                    all_lineage_hashes.add(h)

            # Get artifact info for all lineage hashes
            lineage_artifacts = []
            for h in all_lineage_hashes:
                artifact = ctx_db.artifacts.get(h)
                if artifact:
                    lineage_artifacts.append(artifact)

        self.print(f"  Lineage: {len(lineage_jobs)} job(s), {len(lineage_artifacts)} artifact(s)")

        # Register artifacts with LaaS
        for file_hash, size, _path, rel_path in artifacts:
            if is_dir:
                file_url = f"{dest_url.rstrip('/')}/{rel_path}"
            else:
                file_url = dest_url

            reg_success, reg_error = laas.register_artifact(
                hashes=[{"algorithm": "blake3", "digest": file_hash}],
                size=size,
                source_url=file_url,
            )
            if reg_error:
                self.print(f"  Warning: Failed to register {file_hash[:12]}: {reg_error}")
            elif reg_success:
                self.print(f"  Registered: {file_hash[:12]}...")

        # Register lineage artifacts
        for art in lineage_artifacts:
            if art["hash"] not in artifact_hashes:
                _success, _error = laas.register_artifact(
                    hashes=[{"algorithm": "blake3", "digest": art["hash"]}],
                    size=art.get("size", 0),
                    source_url=art.get("source_url"),
                )

        # Register jobs
        server_job_ids = {}
        for job in lineage_jobs:
            job_id, _job_error = laas.register_job(
                command=job.get("command") or "",
                timestamp=job.get("timestamp") or 0.0,
                job_uid=job.get("job_uid"),
                duration_seconds=job.get("duration_seconds"),
                exit_code=job.get("exit_code"),
                git_repo=job.get("git_repo"),
                git_commit=job.get("git_commit"),
                metadata=job.get("metadata"),
                input_hashes=job.get("_input_hashes", []),
                output_hashes=job.get("_output_hashes", []),
                job_type=job.get("job_type"),
            )
            if job_id:
                server_job_ids[job["id"]] = job_id

        # Create DAG if we have jobs
        if lineage_jobs:
            jobs_data_for_dag = []
            for job in lineage_jobs:
                jobs_data_for_dag.append(
                    {
                        "job_uid": job.get("job_uid"),
                        "command": job.get("command"),
                        "step_number": job.get("step_number"),
                        "job_type": job.get("job_type"),
                    }
                )

            vcs_info_data = vcs.get_info(repo_root) if repo_root else None
            dag_metadata = {
                "git_repo": vcs_info_data.remote_url if vcs_info_data else None,
                "git_commit": vcs_info_data.commit if vcs_info_data else None,
            }

            dag_hash, is_new, dag_err = laas.create_dag(
                jobs=jobs_data_for_dag,
                job_ids=list(server_job_ids.values()),
                metadata=json.dumps(dag_metadata),
            )
            if dag_err:
                self.print(f"  Warning: Failed to create DAG: {dag_err}")
            elif dag_hash and is_new:
                self.print(f"  Created DAG: {dag_hash[:12]}...")
            elif dag_hash:
                self.print(f"  DAG exists: {dag_hash[:12]}...")

        # Update local database
        with create_database_context(roar_dir) as ctx_db:
            if is_dir:
                collection_id = ctx_db.collections.create(
                    name=dest_url,
                    collection_type="upload",
                    source_type=scheme,
                    source_url=None,
                )
                ctx_db.collections.update_upload(collection_id, dest_url)

                for file_hash, size, path, rel_path in artifacts:
                    artifact_id, _ = ctx_db.artifacts.register(
                        hashes={"blake3": file_hash}, size=size, path=path
                    )
                    upload_url = f"{dest_url.rstrip('/')}/{rel_path}"
                    ctx_db.artifacts.update_upload(artifact_id, upload_url)
                    ctx_db.collections.add_artifact(
                        collection_id=collection_id,
                        artifact_id=artifact_id,
                        path_in_collection=rel_path,
                    )

                self.print(f"Uploaded to: {dest_url}")
                self.print(f"Collection ID: {collection_id}")
            else:
                file_hash, size, path, _ = artifacts[0]
                artifact_id, _ = ctx_db.artifacts.register(
                    hashes={"blake3": file_hash}, size=size, path=path
                )
                ctx_db.artifacts.update_upload(artifact_id, dest_url)
                self.print(f"Uploaded to: {dest_url}")
                self.print(f"Hash: {file_hash[:12]}...")

        # Tag commit for reproducibility
        self._maybe_tag_commit(laas, repo_root)

        # Show DAG hash if one was created (for reproduction)
        if dag_hash:
            self.print("")
            self.print(f"To reproduce: roar reproduce {dag_hash[:12]}")

        self.print("Done.")
        return self.success()

    def _check_git_push_access(self, git_url: str, repo_root=None) -> tuple:
        """Check if we have push access to the git remote."""
        import re
        import subprocess

        if not git_url:
            return False, "No git URL"

        if repo_root:
            try:
                result = subprocess.run(
                    ["git", "push", "--dry-run", "origin", "HEAD"],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    return True, None
                stderr = result.stderr.lower()
                if "permission denied" in stderr:
                    return False, "Permission denied (no push access to repository)"
                if "could not read from remote" in stderr:
                    return False, "Cannot access remote repository (check SSH key/permissions)"
                if "authentication failed" in stderr:
                    return False, "Authentication failed"
                return False, result.stderr.strip()
            except subprocess.TimeoutExpired:
                return False, "Git push check timed out"
            except Exception:
                pass

        # Fallback: Parse SSH URL and test basic SSH connectivity
        ssh_match = re.match(r"^(?:ssh://)?git@([^:/]+)[:/]", git_url)
        if ssh_match:
            host = ssh_match.group(1)
            try:
                result = subprocess.run(
                    ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", f"git@{host}"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 255:
                    return False, f"SSH access denied to {host}"
                if "Permission denied" in result.stderr:
                    return False, f"SSH access denied to {host}"
                return True, None
            except subprocess.TimeoutExpired:
                return False, f"SSH connection to {host} timed out"
            except Exception as e:
                return False, str(e)

        # HTTPS URL - can't easily test, assume it will work
        if git_url.startswith("https://"):
            return True, None

        return True, None

    def _maybe_tag_commit(self, laas, repo_root):
        """Tag the current commit for reproducibility if needed."""
        import subprocess

        tagging_enabled = config_get("tagging.enabled")
        if tagging_enabled is not None and tagging_enabled.lower() in ("false", "0", "no"):
            return

        if not repo_root:
            return

        vcs = get_container().get_vcs_provider("git")
        vcs_info = vcs.get_info(repo_root)
        git_repo = vcs_info.remote_url
        git_commit = vcs_info.commit

        if not git_repo or not git_commit:
            return

        has_access, _ = self._check_git_push_access(git_repo, repo_root)
        if not has_access:
            return

        # Check if branch is pushed
        try:
            result = subprocess.run(
                ["git", "branch", "-r", "--contains", "HEAD"],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 or not result.stdout.strip():
                self.print("")
                self.print("Warning: Current commit hasn't been pushed to remote.")
                self.print("Push your branch to enable reproducibility tagging.")
                return
        except Exception:
            return

        if not laas:
            return

        is_tagged, _existing_tag, error = laas.check_commit_tagged(git_repo, git_commit)
        if error or is_tagged:
            return

        tag_name = f"roar/{git_commit[:8]}"

        # Check if tag already exists locally
        try:
            result = subprocess.run(
                ["git", "rev-parse", f"refs/tags/{tag_name}"],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                laas.record_tagged_commit(git_repo, git_commit, tag_name)
                return
        except Exception:
            pass

        self.print(f"Tagging commit for reproducibility: {tag_name}")

        try:
            result = subprocess.run(
                ["git", "tag", tag_name],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 and "already exists" not in result.stderr:
                self.print(f"  Warning: Failed to create tag: {result.stderr.strip()}")
                return

            result = subprocess.run(
                ["git", "push", "origin", tag_name],
                cwd=repo_root,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 and "already exists" not in result.stderr:
                self.print(f"  Warning: Failed to push tag: {result.stderr.strip()}")
                return

            ok, _err = laas.record_tagged_commit(git_repo, git_commit, tag_name)
            if ok:
                self.print(f"  Tagged: {tag_name}")

        except Exception as e:
            self.print(f"  Warning: Tagging failed: {e}")

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar put <src...> <url>

Upload local artifacts to cloud storage and register with LaaS.
Ensures traceability by requiring LaaS registration and git access.

Supported URLs:
  s3://bucket/key           AWS S3
  gs://bucket/key           Google Cloud Storage

Examples:
  roar put ./model.pt s3://my-bucket/models/model.pt
  roar put ./model.pt ./tokenizer.json s3://my-bucket/models/
  roar put ./outputs/ s3://my-bucket/results/  # directory
"""
