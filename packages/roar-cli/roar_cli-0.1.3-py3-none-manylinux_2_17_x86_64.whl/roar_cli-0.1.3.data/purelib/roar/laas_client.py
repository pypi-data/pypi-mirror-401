"""LaaS client for communicating with the Lineage-as-a-Service server."""

import base64
import contextlib
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def get_laas_url() -> str | None:
    """Get LaaS server URL from config or environment."""
    from .config import config_get

    url = config_get("laas.url")
    if not url:
        url = os.environ.get("LAAS_URL")
    return url


def _detect_key_type(key_path: Path) -> str:
    """Detect SSH key type from filename or content."""
    name = key_path.name
    if "ed25519" in name:
        return "ed25519"
    elif "ecdsa" in name:
        return "ecdsa"
    elif "rsa" in name:
        return "rsa"
    # Fallback: check content
    content = key_path.read_text()
    if "ed25519" in content.lower():
        return "ed25519"
    elif "ecdsa" in content.lower():
        return "ecdsa"
    return "rsa"  # default


def find_ssh_private_key() -> tuple[str, Path] | None:
    """Find SSH private key for signing. Returns (key_type, path) or None.

    Priority: ROAR_SSH_KEY env > laas.key config > ~/.ssh/ default
    """
    from .config import config_get

    # 1. Environment variable
    env_key = os.environ.get("ROAR_SSH_KEY")
    if env_key:
        path = Path(env_key)
        if path.exists():
            key_type = _detect_key_type(path)
            return (key_type, path)

    # 2. Config file
    config_key = config_get("laas.key")
    if config_key:
        path = Path(config_key)
        if path.exists():
            key_type = _detect_key_type(path)
            return (key_type, path)

    # 3. Default ~/.ssh/ search
    ssh_dir = Path.home() / ".ssh"
    if not ssh_dir.exists():
        return None

    # Prefer Ed25519, then RSA
    key_prefs = [
        ("ed25519", "id_ed25519"),
        ("rsa", "id_rsa"),
        ("ecdsa", "id_ecdsa"),
    ]

    for key_type, key_name in key_prefs:
        key_path = ssh_dir / key_name
        if key_path.exists():
            return (key_type, key_path)

    return None


def find_ssh_pubkey() -> tuple[str, str, Path] | None:
    """Find SSH public key. Returns (key_type, content, path) or None.

    Priority: ROAR_SSH_KEY env > laas.key config > ~/.ssh/ default
    Derives pubkey path from private key path by adding .pub extension.
    """
    from .config import config_get

    # 1. Environment variable - derive pubkey from private key path
    env_key = os.environ.get("ROAR_SSH_KEY")
    if env_key:
        pubkey_path = Path(env_key + ".pub")
        if pubkey_path.exists():
            content = pubkey_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, pubkey_path)

    # 2. Config file - derive pubkey from private key path
    config_key = config_get("laas.key")
    if config_key:
        pubkey_path = Path(config_key + ".pub")
        if pubkey_path.exists():
            content = pubkey_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, pubkey_path)

    # 3. Default ~/.ssh/ search
    ssh_dir = Path.home() / ".ssh"
    if not ssh_dir.exists():
        return None

    key_prefs = ["id_ed25519.pub", "id_rsa.pub", "id_ecdsa.pub"]

    for key_name in key_prefs:
        key_path = ssh_dir / key_name
        if key_path.exists():
            content = key_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, key_path)

    return None


def compute_pubkey_fingerprint(pubkey: str) -> str:
    """Compute SHA256 fingerprint of an SSH public key."""
    parts = pubkey.strip().split()
    if len(parts) < 2:
        raise ValueError("Invalid public key format")

    key_data = base64.b64decode(parts[1])
    digest = hashlib.sha256(key_data).digest()
    fingerprint = base64.b64encode(digest).decode().rstrip("=")
    return f"SHA256:{fingerprint}"


def create_signature_payload(
    method: str,
    path: str,
    timestamp: int,
    body_hash: str | None = None,
) -> bytes:
    """Create the payload that gets signed."""
    payload = f"{timestamp}\n{method}\n{path}"
    if body_hash:
        payload += f"\n{body_hash}"
    return payload.encode()


def sign_payload(payload: bytes, key_path: Path, key_type: str) -> bytes | None:
    """
    Sign payload with SSH private key.

    Uses ssh-keygen for signing (available on most systems).
    Returns base64-encoded signature or None on failure.
    """
    import subprocess
    import tempfile

    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".data") as f:
        f.write(payload)
        payload_path = f.name

    sig_path = payload_path + ".sig"

    try:
        # Use ssh-keygen to sign
        # -Y sign: create signature
        # -f: identity file
        # -n: namespace (we use "laas")
        result = subprocess.run(
            [
                "ssh-keygen",
                "-Y",
                "sign",
                "-f",
                str(key_path),
                "-n",
                "laas",
                payload_path,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return None

        # Read signature file
        if not Path(sig_path).exists():
            return None

        sig_content = Path(sig_path).read_text()

        # Parse SSH signature format
        # Format: -----BEGIN SSH SIGNATURE-----\n<base64>\n-----END SSH SIGNATURE-----
        lines = sig_content.strip().split("\n")
        sig_lines = []
        in_sig = False
        for line in lines:
            if line.startswith("-----BEGIN"):
                in_sig = True
                continue
            if line.startswith("-----END"):
                break
            if in_sig:
                sig_lines.append(line)

        if not sig_lines:
            return None

        # Return the base64 signature data
        sig_b64 = "".join(sig_lines)
        return base64.b64decode(sig_b64)

    except Exception:
        return None
    finally:
        # Cleanup temp files
        with contextlib.suppress(Exception):
            Path(payload_path).unlink()
        with contextlib.suppress(Exception):
            Path(sig_path).unlink()


def make_auth_header(
    method: str,
    path: str,
    body: bytes | None = None,
) -> str | None:
    """Create Authorization header with SSH signature."""
    # Find keys
    pubkey_info = find_ssh_pubkey()
    privkey_info = find_ssh_private_key()

    if not pubkey_info or not privkey_info:
        return None

    _, pubkey_content, _ = pubkey_info
    key_type, privkey_path = privkey_info

    # Compute fingerprint
    fingerprint = compute_pubkey_fingerprint(pubkey_content)

    # Create timestamp
    timestamp = int(time.time())

    # Compute body hash if body present
    body_hash = None
    if body:
        body_hash = hashlib.sha256(body).hexdigest()

    # Create payload
    payload = create_signature_payload(method, path, timestamp, body_hash)

    # Sign
    signature = sign_payload(payload, privkey_path, key_type)
    if not signature:
        return None

    # Encode signature
    sig_b64 = base64.b64encode(signature).decode()

    # Build header
    header = f'Signature keyid="{fingerprint}" ts="{timestamp}" sig="{sig_b64}"'
    return header


class LaasClient:
    """Client for interacting with LaaS server."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or get_laas_url()
        if self.base_url:
            self.base_url = self.base_url.rstrip("/")

    def is_configured(self) -> bool:
        """Check if LaaS is configured."""
        return self.base_url is not None

    def health_check(self) -> tuple[bool, str | None]:
        """Check server health. Returns (ok, error_message)."""
        if not self.base_url:
            return False, "LaaS URL not configured"

        try:
            url = f"{self.base_url}/api/v1/health"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return True, None
                return False, f"Server returned status {resp.status}"
        except urllib.error.URLError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    def _request(
        self,
        method: str,
        path: str,
        body: dict | None = None,
    ) -> tuple[dict | None, str | None]:
        """Make authenticated request. Returns (response_dict, error_message)."""
        if not self.base_url:
            return None, "LaaS URL not configured"

        url = f"{self.base_url}{path}"
        body_bytes = json.dumps(body).encode() if body else None

        # Create auth header
        auth_header = make_auth_header(method, path, body_bytes)
        if not auth_header:
            return None, "Failed to create authentication signature"

        # Build request
        req = urllib.request.Request(
            url,
            data=body_bytes,
            method=method,
        )
        req.add_header("Authorization", auth_header)
        if body_bytes:
            req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                response_body = resp.read().decode()
                if response_body:
                    result = json.loads(response_body)
                    # Unwrap ApiResponse format: {"success": true, "data": {...}}
                    if isinstance(result, dict) and result.get("success") and "data" in result:
                        return result["data"], None
                    return result, None
                return {}, None
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                error_data = json.loads(error_body)
                detail = error_data.get("detail", str(e))
            except Exception:
                detail = error_body or str(e)
            return None, f"HTTP {e.code}: {detail}"
        except urllib.error.URLError as e:
            return None, f"Connection error: {e}"
        except Exception as e:
            return None, str(e)

    def register_artifact(
        self,
        hashes: list,
        size: int,
        source_type: str | None = None,
        source_url: str | None = None,
        metadata: str | None = None,
    ) -> tuple[bool, str | None]:
        """
        Register an artifact with LaaS.

        Args:
            hashes: List of dicts with 'algorithm' and 'digest' keys
                    e.g., [{"algorithm": "blake3", "digest": "abc123..."}]
            size: File size in bytes
            source_type: Optional source type (e.g., 's3', 'gs', 'https')
            source_url: Optional source URL
            metadata: Optional JSON metadata

        Returns (success, error_message).
        """
        body = {
            "hashes": hashes,
            "size": size,
        }
        if source_type:
            body["source_type"] = source_type
        if source_url:
            body["source_url"] = source_url
        if metadata:
            body["metadata"] = metadata

        _result, error = self._request("POST", "/api/v1/artifacts", body)
        if error:
            return False, error
        return True, None

    def register_artifacts_batch(
        self,
        artifacts: list,
    ) -> tuple[int, int, str | None]:
        """
        Register multiple artifacts with LaaS in a single request.

        Args:
            artifacts: List of dicts with keys:
                - hashes: List of {algorithm, digest} dicts (required)
                - size: File size in bytes (required)
                - source_type: Optional source type
                - source_url: Optional source URL
                - metadata: Optional JSON metadata

        Returns (success_count, error_count, error_message).
        """
        if not artifacts:
            return 0, 0, None

        body = {"artifacts": artifacts}
        result, error = self._request("POST", "/api/v1/artifacts/batch", body)
        if error:
            return 0, len(artifacts), error
        if result is None:
            return 0, 0, None
        return result.get("created", 0) + result.get("existing", 0), 0, None

    def get_artifact(self, hash_prefix: str) -> tuple[dict | None, str | None]:
        """
        Look up artifact by hash prefix.

        Returns (artifact_dict, error_message).
        """
        result, error = self._request("GET", f"/api/v1/artifacts/{hash_prefix}")
        return result, error

    def get_artifact_lineage(
        self, hash_prefix: str, depth: int = 1
    ) -> tuple[dict | None, str | None]:
        """
        Get lineage for an artifact.

        Args:
            hash_prefix: Hash or hash prefix (min 8 chars)
            depth: How many levels to recurse into inputs (default 1, max 10)

        Returns (lineage_dict, error_message).
        """
        path = f"/api/v1/artifacts/{hash_prefix}/lineage"
        if depth > 1:
            path += f"?depth={depth}"
        result, error = self._request("GET", path)
        return result, error

    def register_job(
        self,
        command: str,
        timestamp: float,
        job_uid: str | None = None,
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
        duration_seconds: float | None = None,
        exit_code: int | None = None,
        input_hashes: list | None = None,
        output_hashes: list | None = None,
        metadata: str | None = None,
        job_type: str | None = None,
    ) -> tuple[int | None, str | None]:
        """
        Register a job with LaaS.

        Returns (job_id, error_message).
        """
        body = {
            "command": command,
            "timestamp": timestamp,
        }
        if job_uid:
            body["job_uid"] = job_uid
        if git_repo:
            body["git_repo"] = git_repo
        if git_commit:
            body["git_commit"] = git_commit
        if git_branch:
            body["git_branch"] = git_branch
        if duration_seconds is not None:
            body["duration_seconds"] = duration_seconds
        if exit_code is not None:
            body["exit_code"] = exit_code
        if input_hashes:
            body["input_hashes"] = input_hashes
        if output_hashes:
            body["output_hashes"] = output_hashes
        if metadata:
            body["metadata"] = metadata
        if job_type:
            body["job_type"] = job_type

        result, error = self._request("POST", "/api/v1/jobs", body)
        if error:
            return None, error
        if result is None:
            return None, None
        return result.get("id"), None

    def register_jobs_batch(
        self,
        jobs: list,
    ) -> tuple[list, list, str | None]:
        """
        Register multiple jobs with LaaS in a single request.

        Args:
            jobs: List of dicts with keys matching register_job parameters:
                  command, timestamp, job_uid, git_repo, git_commit, git_branch,
                  duration_seconds, exit_code, input_hashes, output_hashes,
                  metadata, job_type

        Returns (job_ids, errors, error_message).
            job_ids: List of server job IDs for successful registrations
            errors: List of error messages for failed registrations
            error_message: Overall error if the request failed entirely
        """
        if not jobs:
            return [], [], None

        body = {"jobs": jobs}
        result, error = self._request("POST", "/api/v1/jobs/batch", body)
        if error:
            return [], [error] * len(jobs), error
        if result is None:
            return [], [], None
        return result.get("job_ids", []), result.get("errors", []), None

    def check_commit_tagged(
        self,
        git_repo: str,
        git_commit: str,
    ) -> tuple[bool, str | None, str | None]:
        """
        Check if a commit has already been tagged on the server.

        Returns (is_tagged, tag_name, error_message).
        """
        body = {
            "git_repo": git_repo,
            "git_commit": git_commit,
        }
        result, error = self._request("POST", "/api/v1/tags/check", body)
        if error:
            return False, None, error
        if result is None:
            return False, None, None
        return result.get("tagged", False), result.get("tag_name"), None

    def record_tagged_commit(
        self,
        git_repo: str,
        git_commit: str,
        tag_name: str,
    ) -> tuple[bool, str | None]:
        """
        Record that a commit has been tagged.

        Returns (success, error_message).
        """
        body = {
            "git_repo": git_repo,
            "git_commit": git_commit,
            "tag_name": tag_name,
        }
        _result, error = self._request("POST", "/api/v1/tags/record", body)
        if error:
            return False, error
        return True, None

    def create_dag(
        self,
        jobs: list,
        job_ids: list,
        metadata: str | None = None,
    ) -> tuple[str | None, bool, str | None]:
        """
        Create a DAG on the server.

        Args:
            jobs: List of dicts with command, input_hashes, output_hashes
            job_ids: Server-side job IDs corresponding to each job
            metadata: Optional JSON metadata

        Returns (dag_hash, is_new, error_message).
        """
        body: dict[str, Any] = {
            "jobs": jobs,
            "job_ids": job_ids,
        }
        if metadata:
            body["metadata"] = metadata

        result, error = self._request("POST", "/api/v1/dags", body)
        if error:
            return None, False, error
        if result is None:
            return None, False, None
        return result.get("hash"), result.get("created", False), None

    def get_dag(self, dag_hash: str) -> tuple[dict | None, str | None]:
        """
        Get DAG by hash or hash prefix.

        Returns (dag_info, error_message).
        """
        result, error = self._request("GET", f"/api/v1/dags/{dag_hash}")
        return result, error

    def get_artifact_dag(self, hash_prefix: str) -> tuple[dict | None, str | None]:
        """
        Get the DAG needed to reproduce an artifact.

        Returns dict with:
            - artifact: the artifact info
            - dag: the DAG info (or None if external)
            - jobs: ordered list of jobs in the DAG
            - external_deps: list of external dependency artifacts
            - is_external: True if artifact has no producing DAG

        Returns (result, error_message).
        """
        result, error = self._request("GET", f"/api/v1/artifacts/{hash_prefix}/dag")
        return result, error

    # -------------------------------------------------------------------------
    # Live Sync Methods
    # -------------------------------------------------------------------------

    def register_session(
        self,
        session_hash: str,
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
    ) -> tuple[dict | None, str | None]:
        """
        Register or update a sync session.

        Returns (session_info, error_message).
        session_info contains: hash, url, created (bool)
        """
        body = {"hash": session_hash}
        if git_repo:
            body["git_repo"] = git_repo
        if git_commit:
            body["git_commit"] = git_commit
        if git_branch:
            body["git_branch"] = git_branch

        result, error = self._request("POST", "/api/v1/sessions", body)
        return result, error

    def create_live_job(
        self,
        job_uid: str,
        session_hash: str,
        command: str,
        step_number: int | None = None,
        job_type: str = "run",
        git_repo: str | None = None,
        git_commit: str | None = None,
        git_branch: str | None = None,
        started_at: float | None = None,
    ) -> tuple[dict | None, str | None]:
        """
        Create a live (running) job.

        Returns (job_info, error_message).
        job_info contains: job_uid, status
        """
        body: dict[str, Any] = {
            "job_uid": job_uid,
            "session_hash": session_hash,
            "command": command,
            "job_type": job_type,
        }
        if step_number is not None:
            body["step_number"] = step_number
        if git_repo:
            body["git_repo"] = git_repo
        if git_commit:
            body["git_commit"] = git_commit
        if git_branch:
            body["git_branch"] = git_branch
        if started_at is not None:
            body["started_at"] = started_at

        result, error = self._request("POST", "/api/v1/jobs/live", body)
        return result, error

    def update_live_job(
        self,
        job_uid: str,
        inputs: list | None = None,
        outputs: list | None = None,
        elapsed_seconds: float | None = None,
        telemetry: str | None = None,
    ) -> tuple[dict | None, str | None]:
        """
        Update a running job with current I/O state.

        Args:
            job_uid: The job's unique identifier
            inputs: List of {path, hash (optional), size (optional)}
            outputs: List of {path, hash (optional), size (optional)}
            elapsed_seconds: Seconds since job started
            telemetry: JSON string with external service links (wandb, etc.)

        Returns (job_info, error_message).
        """
        body: dict[str, Any] = {}
        if inputs is not None:
            body["inputs"] = inputs
        if outputs is not None:
            body["outputs"] = outputs
        if elapsed_seconds is not None:
            body["elapsed_seconds"] = elapsed_seconds
        if telemetry is not None:
            body["telemetry"] = telemetry

        result, error = self._request("PATCH", f"/api/v1/jobs/{job_uid}", body)
        return result, error

    def complete_live_job(
        self,
        job_uid: str,
        exit_code: int,
        duration_seconds: float | None = None,
        inputs: list | None = None,
        outputs: list | None = None,
        metadata: str | None = None,
        telemetry: str | None = None,
    ) -> tuple[dict | None, str | None]:
        """
        Mark a live job as completed.

        Returns (job_info, error_message).
        """
        body: dict[str, Any] = {"exit_code": exit_code}
        if duration_seconds is not None:
            body["duration_seconds"] = duration_seconds
        if inputs is not None:
            body["inputs"] = inputs
        if outputs is not None:
            body["outputs"] = outputs
        if metadata is not None:
            body["metadata"] = metadata
        if telemetry is not None:
            body["telemetry"] = telemetry

        result, error = self._request("POST", f"/api/v1/jobs/{job_uid}/complete", body)
        return result, error

    def heartbeat_job(self, job_uid: str) -> tuple[dict | None, str | None]:
        """
        Send heartbeat for a running job.

        Returns (job_info, error_message).
        """
        result, error = self._request("POST", f"/api/v1/jobs/{job_uid}/heartbeat", {})
        return result, error

    def get_session(self, session_hash: str) -> tuple[dict | None, str | None]:
        """
        Get session details including jobs.

        Returns (session_info, error_message).
        """
        result, error = self._request("GET", f"/api/v1/sessions/{session_hash}")
        return result, error
