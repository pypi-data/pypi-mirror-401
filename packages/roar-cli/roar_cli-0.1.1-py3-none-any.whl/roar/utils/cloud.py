"""
Cloud storage utilities.

Pure utility functions for cloud URL parsing and CLI availability checking.
These functions have no provider dependencies and can be used independently.
"""

import subprocess
from urllib.parse import urlparse


def parse_cloud_url(url: str) -> tuple[str, str, str]:
    """
    Parse a cloud URL into (scheme, bucket, key).

    Supports:
      s3://bucket/key/path
      gs://bucket/key/path

    Args:
        url: Cloud storage URL

    Returns:
        Tuple of (scheme, bucket, key) where key may be empty or end with /

    Raises:
        ValueError: If scheme is not s3 or gs
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    if scheme not in ("s3", "gs"):
        raise ValueError(f"Unsupported cloud scheme: {scheme}. Use s3:// or gs://")

    bucket = parsed.netloc
    key = parsed.path.lstrip("/")

    return scheme, bucket, key


def is_directory_url(url: str) -> bool:
    """
    Check if a URL represents a directory (ends with /).

    Args:
        url: Cloud storage URL

    Returns:
        True if URL represents a directory
    """
    return url.rstrip("/") != url or not urlparse(url).path.split("/")[-1]


def check_cli_available(scheme: str) -> tuple[bool, str]:
    """
    Check if the required CLI tool is available for a cloud scheme.

    Args:
        scheme: Cloud scheme ('s3' or 'gs')

    Returns:
        Tuple of (available, tool_name)
    """
    if scheme == "s3":
        tool = "aws"
        check_cmd = ["aws", "--version"]
    elif scheme == "gs":
        tool = "gsutil"
        check_cmd = ["gsutil", "--version"]
    else:
        return False, f"unknown-{scheme}"

    try:
        subprocess.run(check_cmd, capture_output=True, check=True)
        return True, tool
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, tool


def get_cli_install_hint(scheme: str) -> str:
    """
    Get installation hint for a cloud CLI tool.

    Args:
        scheme: Cloud scheme ('s3' or 'gs')

    Returns:
        Installation hint string
    """
    if scheme == "s3":
        return "AWS CLI not found. Install with: pip install awscli"
    elif scheme == "gs":
        return "gsutil not found. Install with: pip install gsutil"
    else:
        return f"Unknown cloud scheme: {scheme}"
