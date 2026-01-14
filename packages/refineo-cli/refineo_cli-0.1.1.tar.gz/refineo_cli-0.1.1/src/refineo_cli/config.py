"""Configuration and credentials management."""

import json
import os
import platform
from pathlib import Path
from typing import TypedDict, Optional


class UserInfo(TypedDict):
    email: str
    name: Optional[str]
    tier: str


class Credentials(TypedDict):
    accessToken: str
    refreshToken: str
    expiresAt: int
    user: UserInfo


CONFIG_DIR = Path.home() / ".refineo"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"

API_BASE_URL = os.environ.get("REFINEO_API_URL", "https://www.refineo.app")


def ensure_config_dir() -> None:
    """Ensure config directory exists with proper permissions."""
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)


def load_credentials() -> Optional[Credentials]:
    """Load credentials from disk."""
    try:
        if not CREDENTIALS_FILE.exists():
            return None
        data = json.loads(CREDENTIALS_FILE.read_text())
        return data
    except Exception:
        return None


def save_credentials(credentials: Credentials) -> None:
    """Save credentials to disk."""
    ensure_config_dir()
    CREDENTIALS_FILE.write_text(json.dumps(credentials, indent=2))
    CREDENTIALS_FILE.chmod(0o600)


def clear_credentials() -> None:
    """Clear credentials from disk."""
    try:
        if CREDENTIALS_FILE.exists():
            CREDENTIALS_FILE.unlink()
    except Exception:
        pass


def is_token_expired(credentials: Credentials) -> bool:
    """Check if credentials are expired (with 1 minute buffer)."""
    import time
    now = int(time.time())
    return credentials["expiresAt"] <= now + 60


def get_platform_info() -> str:
    """Get current platform info for User-Agent."""
    system = platform.system()
    arch = platform.machine()
    py_version = platform.python_version()

    os_name = {
        "Darwin": "macOS",
        "Windows": "Windows",
        "Linux": "Linux",
    }.get(system, "Unknown")

    return f"refineo-cli-python/0.0.6 ({os_name}; {arch}) Python/{py_version}"
