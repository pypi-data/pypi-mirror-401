"""
Get command - Download and register external data.

Usage: roar get <url> <dest>
"""

from pathlib import Path

from ..core.container import get_container
from ..core.interfaces.command import CommandContext, CommandResult
from ..db.context import create_database_context
from ..presenters.run_report import format_size
from ..utils.cloud import is_directory_url, parse_cloud_url
from .base import BaseCommand


class GetCommand(BaseCommand):
    """
    Download data from cloud storage and register as external artifact.

    Supported URLs:
      s3://bucket/key           AWS S3
      gs://bucket/key           Google Cloud Storage

    Examples:
      roar get s3://my-bucket/data.parquet ./data/
      roar get s3://my-bucket/dataset/ ./data/  # directory
      roar get gs://my-bucket/model.pt ./models/
    """

    @property
    def name(self) -> str:
        return "get"

    @property
    def help_text(self) -> str:
        return "Download and register external data"

    @property
    def usage(self) -> str:
        return "roar get <url> <dest>"

    def requires_init(self) -> bool:
        """Get command requires roar to be initialized."""
        return True

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the get command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        if len(args) < 2:
            self.print_error("Both <url> and <dest> are required.")
            self.print("Usage: roar get <url> <dest>")
            return self.failure("Missing arguments")

        source_url = args[0]
        dest_path = args[1]

        # Parse URL
        try:
            scheme, _bucket, key = parse_cloud_url(source_url)
        except ValueError as e:
            self.print_error(str(e))
            return self.failure(str(e))

        # Determine if this is a directory download
        is_dir = is_directory_url(source_url) or source_url.endswith("/")

        # Create destination directory if needed
        dest = Path(dest_path)
        if is_dir:
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)

        self.print(f"Downloading from {source_url}...")

        # Get cloud provider and download
        cloud_provider = get_container().get_cloud_provider(scheme)
        if cloud_provider is None:
            error = f"No cloud provider available for scheme: {scheme}"
            self.print_error(error)
            return self.failure(error)

        success, error = cloud_provider.download(source_url, str(dest), recursive=is_dir)
        if not success:
            self.print_error(error)
            return self.failure(error)

        # Hash and register downloaded files
        roar_dir = ctx.cwd / ".roar"
        with create_database_context(roar_dir) as ctx_db:
            if is_dir:
                # Directory download - create a collection
                collection_id = ctx_db.collections.create(
                    name=source_url,
                    collection_type="download",
                    source_type=scheme,
                    source_url=source_url,
                )

                # Find all downloaded files
                file_count = 0
                total_size = 0
                for file_path in dest.rglob("*"):
                    if file_path.is_file():
                        file_hash = ctx_db.hashing.compute_file_hash(str(file_path))
                        if file_hash:
                            size = file_path.stat().st_size
                            total_size += size
                            rel_path = str(file_path.relative_to(dest))

                            # Register artifact
                            artifact_id, _created = ctx_db.artifacts.register(
                                hashes={"blake3": file_hash},
                                size=size,
                                path=str(file_path),
                                source_type=scheme,
                                source_url=f"{source_url.rstrip('/')}/{rel_path}",
                            )

                            # Add to collection
                            ctx_db.collections.add_artifact(
                                collection_id=collection_id,
                                artifact_id=artifact_id,
                                path_in_collection=rel_path,
                            )
                            file_count += 1

                self.print(f"Downloaded {file_count} file(s), {format_size(total_size)}")
                self.print(f"Collection ID: {collection_id}")

            else:
                # Single file download
                if dest.is_dir():
                    # Dest is directory, file name from URL
                    file_name = key.split("/")[-1] if "/" in key else key
                    file_path = dest / file_name
                else:
                    file_path = dest

                file_hash = ctx_db.hashing.compute_file_hash(str(file_path))
                if file_hash:
                    size = file_path.stat().st_size
                    ctx_db.artifacts.register(
                        hashes={"blake3": file_hash},
                        size=size,
                        path=str(file_path),
                        source_type=scheme,
                        source_url=source_url,
                    )
                    self.print(f"Downloaded {format_size(size)}")
                    self.print(f"Hash: {file_hash[:12]}...")
                else:
                    self.print("Warning: Could not hash downloaded file")

        self.print("Done.")
        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar get <url> <dest>

Download data from cloud storage and register as external artifact.

Supported URLs:
  s3://bucket/key           AWS S3
  gs://bucket/key           Google Cloud Storage

Examples:
  roar get s3://my-bucket/data.parquet ./data/
  roar get s3://my-bucket/dataset/ ./data/  # directory
  roar get gs://my-bucket/model.pt ./models/
"""
