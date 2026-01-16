"""
Auth command - Manage LaaS authentication.

Usage: roar auth <command>
"""

import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from ..config import config_get
from ..core.interfaces.command import CommandContext, CommandResult
from .base import BaseCommand


def find_ssh_pubkey():
    """Find an SSH public key. Returns (key_type, pubkey_content, path) or None.

    Priority: ROAR_SSH_KEY env > laas.key config > ~/.ssh/ default
    """
    from ..config import config_get

    # 1. Environment variable - derive pubkey from private key path
    env_key = os.environ.get("ROAR_SSH_KEY")
    if env_key:
        pubkey_path = Path(env_key + ".pub")
        if pubkey_path.exists():
            content = pubkey_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, str(pubkey_path))

    # 2. Config file - derive pubkey from private key path
    config_key = config_get("laas.key")
    if config_key:
        pubkey_path = Path(config_key + ".pub")
        if pubkey_path.exists():
            content = pubkey_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, str(pubkey_path))

    # 3. Default ~/.ssh/ search
    ssh_dir = Path.home() / ".ssh"
    if not ssh_dir.exists():
        return None

    # Prefer Ed25519, then RSA
    key_prefs = ["id_ed25519.pub", "id_rsa.pub", "id_ecdsa.pub"]

    for key_name in key_prefs:
        key_path = ssh_dir / key_name
        if key_path.exists():
            content = key_path.read_text().strip()
            parts = content.split()
            if len(parts) >= 2:
                return (parts[0], content, str(key_path))

    # Check for any .pub file
    for pub_file in ssh_dir.glob("*.pub"):
        content = pub_file.read_text().strip()
        parts = content.split()
        if len(parts) >= 2:
            return (parts[0], content, str(pub_file))

    return None


class AuthCommand(BaseCommand):
    """
    Manage LaaS authentication.

    Subcommands:
      register    Show your SSH public key for registration
      test        Test connection to LaaS server
      status      Show current auth status
    """

    @property
    def name(self) -> str:
        return "auth"

    @property
    def help_text(self) -> str:
        return "Manage LaaS authentication"

    @property
    def usage(self) -> str:
        return "roar auth <command>"

    def requires_init(self) -> bool:
        """Auth command doesn't require roar to be initialized."""
        return False

    def execute(self, ctx: CommandContext) -> CommandResult:
        """Execute the auth command."""
        args = ctx.args

        if not args or args[0] in ("-h", "--help"):
            self.print(self.get_help())
            return self.success()

        subcmd = args[0]

        if subcmd == "register":
            return self._cmd_register()
        elif subcmd == "test":
            return self._cmd_test()
        elif subcmd == "status":
            return self._cmd_status()
        else:
            self.print_error(f"Unknown auth command: {subcmd}")
            self.print("Use: register, test, status")
            return self.failure(f"Unknown subcommand: {subcmd}")

    def _cmd_register(self) -> CommandResult:
        """Show SSH public key for registration."""
        key_info = find_ssh_pubkey()

        if not key_info:
            self.print("No SSH public key found.")
            self.print("")
            self.print("Generate one with:")
            self.print("  ssh-keygen -t ed25519")
            self.print("")
            self.print("Then run 'roar auth register' again.")
            return self.failure("No SSH key found")

        key_type, pubkey, path = key_info
        self.print("Your SSH public key:")
        self.print("")
        self.print(f"  {pubkey}")
        self.print("")
        self.print(f"Key type: {key_type}")
        self.print(f"Path: {path}")
        self.print("")
        self.print("Send this key to your LaaS administrator to complete registration.")
        return self.success()

    def _cmd_test(self) -> CommandResult:
        """Test connection to LaaS server."""
        # Get LaaS server URL from config
        laas_url = config_get("laas.url")
        if not laas_url:
            laas_url = os.environ.get("LAAS_URL")

        if not laas_url:
            self.print("LaaS server URL not configured.")
            self.print("")
            self.print("Set it with:")
            self.print("  roar config set laas.url https://laas.example.com")
            self.print("")
            self.print("Or set LAAS_URL environment variable.")
            return self.failure("LaaS URL not configured")

        self.print(f"Testing connection to {laas_url}...")

        # Try health endpoint (no auth required)
        try:
            health_url = f"{laas_url.rstrip('/')}/api/v1/health"
            req = urllib.request.Request(health_url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    self.print("Server is reachable.")
                else:
                    self.print(f"Server returned status {resp.status}")
                    return self.failure(f"Server returned status {resp.status}")
        except urllib.error.URLError as e:
            self.print(f"Failed to connect: {e}")
            return self.failure(str(e))

        # Test authenticated endpoint
        self.print("Testing authentication...")

        from ..laas_client import compute_pubkey_fingerprint, make_auth_header
        from ..laas_client import find_ssh_pubkey as laas_find_ssh_pubkey

        key_info = laas_find_ssh_pubkey()
        if not key_info:
            self.print("No SSH key found. Run 'roar auth register' first.")
            return self.failure("No SSH key found")

        _, pubkey, key_path = key_info
        fingerprint = compute_pubkey_fingerprint(pubkey)
        self.print(f"Using key: {key_path}")
        self.print(f"Fingerprint: {fingerprint}")

        # Try to get a non-existent artifact (will fail with 404 if auth works, 401 if not)
        test_path = "/api/v1/artifacts/00000000"
        auth_header = make_auth_header("GET", test_path, None)

        if not auth_header:
            self.print("Failed to create signature. Check your SSH key.")
            return self.failure("Failed to create signature")

        try:
            test_url = f"{laas_url.rstrip('/')}{test_path}"
            req = urllib.request.Request(test_url)
            req.add_header("Authorization", auth_header)

            with urllib.request.urlopen(req, timeout=10) as resp:
                # 200 means it found something (unlikely with our dummy hash)
                self.print("Authentication successful!")
                return self.success()

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 404 = auth worked, artifact just doesn't exist
                self.print("Authentication successful!")
                return self.success()
            elif e.code == 401:
                # Try to get error detail
                try:
                    error_body = e.read().decode()
                    error_data = json.loads(error_body)
                    detail = error_data.get("detail", "Unknown error")
                except Exception:
                    detail = str(e)
                self.print(f"Authentication failed: {detail}")
                self.print("")
                self.print("Your key may not be registered with the server.")
                self.print("Contact your LaaS administrator.")
                return self.failure("Authentication failed")
            else:
                self.print(f"Server error: {e.code}")
                return self.failure(f"Server error: {e.code}")

        except urllib.error.URLError as e:
            self.print(f"Connection failed: {e}")
            return self.failure(str(e))

    def _cmd_status(self) -> CommandResult:
        """Show current auth status."""
        laas_url = config_get("laas.url") or os.environ.get("LAAS_URL")
        key_info = find_ssh_pubkey()

        self.print("LaaS Auth Status")
        self.print("=" * 40)
        self.print(f"Server URL: {laas_url or '(not configured)'}")
        self.print(f"SSH key: {key_info[2] if key_info else '(not found)'}")

        if key_info:
            # Compute fingerprint
            parts = key_info[1].split()
            if len(parts) >= 2:
                try:
                    key_data = base64.b64decode(parts[1])
                    digest = hashlib.sha256(key_data).digest()
                    fp = base64.b64encode(digest).decode().rstrip("=")
                    self.print(f"Fingerprint: SHA256:{fp}")
                except Exception:
                    pass

        return self.success()

    def get_help(self) -> str:
        """Return detailed help text."""
        return """Usage: roar auth <command>

Manage LaaS authentication.

Commands:
  register    Show your SSH public key for registration
  test        Test connection to LaaS server
  status      Show current auth status

To register with LaaS:
  1. Run 'roar auth register' to display your public key
  2. Send the key to your LaaS administrator
  3. Once added, run 'roar auth test' to verify
"""
