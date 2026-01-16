"""Tests for roar cloud module."""

import pytest

from roar.utils.cloud import is_directory_url, parse_cloud_url


class TestParseCloudUrl:
    """Tests for parse_cloud_url function."""

    def test_parse_s3_url(self):
        """Should parse S3 URLs correctly."""
        scheme, bucket, key = parse_cloud_url("s3://my-bucket/path/to/file.txt")
        assert scheme == "s3"
        assert bucket == "my-bucket"
        assert key == "path/to/file.txt"

    def test_parse_s3_url_no_key(self):
        """Should parse S3 URL with bucket only."""
        scheme, bucket, key = parse_cloud_url("s3://my-bucket/")
        assert scheme == "s3"
        assert bucket == "my-bucket"
        assert key == ""

    def test_parse_gs_url(self):
        """Should parse GCS URLs correctly."""
        scheme, bucket, key = parse_cloud_url("gs://my-bucket/data/file.parquet")
        assert scheme == "gs"
        assert bucket == "my-bucket"
        assert key == "data/file.parquet"

    def test_parse_unsupported_scheme(self):
        """Should raise for unsupported schemes."""
        with pytest.raises(ValueError, match="Unsupported cloud scheme"):
            parse_cloud_url("http://example.com/file.txt")

    def test_parse_unsupported_scheme_ftp(self):
        """Should raise for FTP scheme."""
        with pytest.raises(ValueError, match="Unsupported cloud scheme"):
            parse_cloud_url("ftp://server/file.txt")


class TestIsDirectoryUrl:
    """Tests for is_directory_url function."""

    def test_directory_with_trailing_slash(self):
        """URLs ending with / are directories."""
        assert is_directory_url("s3://bucket/prefix/") is True

    def test_file_url(self):
        """URLs pointing to files are not directories."""
        assert is_directory_url("s3://bucket/path/file.txt") is False

    def test_bucket_only(self):
        """Bucket-only URLs are directories."""
        # s3://bucket has no path component with file
        assert is_directory_url("s3://bucket") is True
