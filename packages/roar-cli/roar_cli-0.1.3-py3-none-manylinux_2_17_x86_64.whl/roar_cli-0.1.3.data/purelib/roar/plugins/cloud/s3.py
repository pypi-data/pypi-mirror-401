"""
S3 cloud storage provider.

Implements cloud storage operations for Amazon S3 using boto3.
"""

import os
import subprocess

from .base import BaseCloudProvider, UploadProgress


class S3CloudProvider(BaseCloudProvider):
    """
    Amazon S3 cloud storage provider.

    Uses boto3 for batch uploads with progress tracking,
    falls back to AWS CLI for basic operations.
    """

    @property
    def scheme(self) -> str:
        return "s3"

    @property
    def cli_tool(self) -> str:
        return "aws"

    @property
    def install_hint(self) -> str:
        return "pip install awscli"

    def _cli_version_command(self) -> list[str]:
        return ["aws", "--version"]

    def download(
        self,
        source_url: str,
        dest_path: str,
        recursive: bool = False,
    ) -> tuple[bool, str]:
        """Download from S3 using AWS CLI."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, f"AWS CLI not found. Install with: {self.install_hint}"

        cmd = ["aws", "s3", "cp", source_url, dest_path]
        if recursive:
            cmd.append("--recursive")

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
        """Upload to S3 using AWS CLI."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, f"AWS CLI not found. Install with: {self.install_hint}"

        cmd = ["aws", "s3", "cp", source_path, dest_url]
        if recursive:
            cmd.append("--recursive")
        if not show_progress:
            cmd.append("--no-progress")

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
        """List objects at an S3 URL prefix."""
        available, _tool = self.check_cli_available()
        if not available:
            return False, [], f"AWS CLI not found. Install with: {self.install_hint}"

        _bucket, key = self.parse_url(url)
        cmd = ["aws", "s3", "ls", url, "--recursive"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, [], result.stderr.strip() or result.stdout.strip()

            files = []
            prefix = key.rstrip("/")

            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 4:
                    full_key = parts[-1]
                    if prefix and full_key.startswith(prefix):
                        rel_path = full_key[len(prefix) :].lstrip("/")
                    else:
                        rel_path = full_key
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
        Upload multiple files to S3 using boto3 with progress bar.

        Uses multipart uploads with parallel threads for speed.
        """
        if not files:
            return True, ""

        try:
            import boto3
            from boto3.s3.transfer import TransferConfig
        except ImportError:
            return False, "boto3 not installed. Install with: pip install roar[s3]"

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

        # Configure for parallel multipart uploads
        config = TransferConfig(
            multipart_threshold=8 * 1024 * 1024,  # 8MB
            max_concurrency=10,
            multipart_chunksize=8 * 1024 * 1024,  # 8MB chunks
            use_threads=True,
        )

        s3 = boto3.client("s3")

        if show_progress:
            progress = UploadProgress(total_bytes, len(files))
            progress.start()
        else:
            progress = None

        try:
            for bucket, bucket_file_list in bucket_files.items():
                for local_path, s3_key in bucket_file_list:
                    if progress:
                        filename = os.path.basename(local_path)
                        progress.set_current_file(filename)

                    # Create callback that adds bytes
                    callback = None
                    if progress:

                        def make_callback(prog):
                            def cb(bytes_amount):
                                prog.add_bytes(bytes_amount)

                            return cb

                        callback = make_callback(progress)

                    s3.upload_file(
                        local_path,
                        bucket,
                        s3_key,
                        Config=config,
                        Callback=callback,
                    )

                    if progress:
                        progress.file_completed()

            if progress:
                progress.finish()

            return True, ""

        except Exception as e:
            if progress:
                print()  # Newline after progress bar
            return False, str(e)
