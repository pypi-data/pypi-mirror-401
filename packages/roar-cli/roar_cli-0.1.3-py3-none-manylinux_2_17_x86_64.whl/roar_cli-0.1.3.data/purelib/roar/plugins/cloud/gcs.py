"""
GCS cloud storage provider.

Implements cloud storage operations for Google Cloud Storage.
"""

import os
import subprocess
from urllib.parse import urlparse

from .base import BaseCloudProvider, UploadProgress


class GCSCloudProvider(BaseCloudProvider):
    """
    Google Cloud Storage provider.

    Uses google-cloud-storage for batch uploads with progress tracking,
    falls back to gsutil for basic operations.
    """

    @property
    def scheme(self) -> str:
        return "gs"

    @property
    def cli_tool(self) -> str:
        return "gsutil"

    @property
    def install_hint(self) -> str:
        return "pip install gsutil"

    def _cli_version_command(self) -> list[str]:
        return ["gsutil", "--version"]

    def download(
        self,
        source_url: str,
        dest_path: str,
        recursive: bool = False,
    ) -> tuple[bool, str]:
        """Download from GCS using gsutil."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, f"gsutil not found. Install with: {self.install_hint}"

        cmd = ["gsutil"]
        if recursive:
            cmd.append("-r")
        cmd.extend(["cp", source_url, dest_path])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, result.stderr.strip() or result.stdout.strip()
            return True, ""
        except Exception as e:
            return False, str(e)

    def upload(
        self,
        source_path: str,
        dest_url: str,
        recursive: bool = False,
        show_progress: bool = True,
    ) -> tuple[bool, str]:
        """Upload to GCS using gsutil."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, f"gsutil not found. Install with: {self.install_hint}"

        cmd = ["gsutil"]
        if recursive:
            cmd.append("-r")
        cmd.extend(["cp", source_path, dest_url])

        try:
            if show_progress:
                proc = subprocess.run(cmd)
                if proc.returncode != 0:
                    return False, "Upload failed (see output above)"
                return True, ""
            else:
                proc_text = subprocess.run(cmd, capture_output=True, text=True)
                if proc_text.returncode != 0:
                    stderr = proc_text.stderr or ""
                    stdout = proc_text.stdout or ""
                    return False, stderr.strip() or stdout.strip()
                return True, ""
        except Exception as e:
            return False, str(e)

    def list_objects(self, url: str) -> tuple[bool, list[str], str]:
        """List objects at a GCS URL prefix."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, [], f"gsutil not found. Install with: {self.install_hint}"

        _bucket, key = self.parse_url(url)
        cmd = ["gsutil", "ls", "-r", url]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, [], result.stderr.strip() or result.stdout.strip()

            files = []
            prefix = key.rstrip("/")

            for line in result.stdout.strip().split("\n"):
                if not line.strip() or line.endswith("/"):
                    continue
                # Extract path from full URL
                parsed = urlparse(line.strip())
                file_key = parsed.path.lstrip("/")
                if prefix and file_key.startswith(prefix):
                    rel_path = file_key[len(prefix) :].lstrip("/")
                else:
                    rel_path = file_key
                if rel_path:
                    files.append(rel_path)

            return True, files, ""
        except Exception as e:
            return False, [], str(e)

    def upload_batch(
        self,
        files: list[tuple[str, str]],
        show_progress: bool = True,
    ) -> tuple[bool, str]:
        """
        Upload multiple files to GCS using google-cloud-storage.
        """
        if not files:
            return True, ""

        try:
            from google.cloud import storage
        except ImportError:
            return False, "google-cloud-storage not installed. Install with: pip install roar[gcs]"

        # Group files by bucket
        bucket_files: dict[str, list[tuple[str, str]]] = {}
        for local_path, dest_url in files:
            bucket, key = self.parse_url(dest_url)
            if bucket not in bucket_files:
                bucket_files[bucket] = []
            bucket_files[bucket].append((local_path, key))

        # Calculate total size
        total_bytes = 0
        for local_path, _ in files:
            try:
                total_bytes += os.path.getsize(local_path)
            except OSError as e:
                return False, f"Cannot read {local_path}: {e}"

        client = storage.Client()

        if show_progress:
            progress = UploadProgress(total_bytes, len(files))
            progress.start()
            cumulative_bytes = 0
        else:
            progress = None
            cumulative_bytes = 0

        try:
            for bucket_name, bucket_file_list in bucket_files.items():
                bucket = client.bucket(bucket_name)

                for local_path, gcs_object_name in bucket_file_list:
                    if progress:
                        filename = os.path.basename(local_path)
                        progress.set_current_file(filename)

                    blob = bucket.blob(gcs_object_name)
                    file_size = os.path.getsize(local_path)

                    blob.upload_from_filename(local_path, timeout=300)

                    cumulative_bytes += file_size
                    if progress:
                        progress.set_bytes(cumulative_bytes)
                        progress.file_completed()

            if progress:
                progress.finish()

            return True, ""

        except Exception as e:
            if progress:
                print()  # Newline after progress bar
            return False, str(e)
