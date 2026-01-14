"""API client for Refineo."""

import json
import time
import urllib.request
import urllib.error
from typing import Optional, Callable, TypedDict, Any

from .config import (
    API_BASE_URL,
    Credentials,
    load_credentials,
    save_credentials,
    is_token_expired,
    get_platform_info,
)


class DeviceCodeResponse(TypedDict):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class HumanizeResult(TypedDict):
    humanizedText: str
    wordCount: int
    model: str


class UsageStats(TypedDict):
    tier: str
    used: int
    limit: int
    remaining: int
    resetDate: Optional[str]
    wordLimit: int
    rateLimit: Optional[int]


USER_AGENT = get_platform_info()


def _make_request(
    path: str,
    method: str = "GET",
    data: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
) -> Any:
    """Make an HTTP request."""
    url = f"{API_BASE_URL}{path}"

    req_headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }
    if headers:
        req_headers.update(headers)

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            msg = (
                error_data.get("message")
                or error_data.get("error_description")
                or error_data.get("error")
                or f"HTTP {e.code}"
            )
            raise Exception(msg) from e
        except json.JSONDecodeError:
            raise Exception(f"HTTP {e.code}: {error_body}") from e


def _api_request(
    path: str,
    method: str = "GET",
    data: Optional[dict[str, Any]] = None,
) -> Any:
    """Make an authenticated API request."""
    credentials = load_credentials()

    if not credentials:
        raise Exception("Not logged in. Run: refineo login")

    # Refresh token if expired
    token = credentials["accessToken"]
    if is_token_expired(credentials):
        refreshed = _refresh_token(credentials["refreshToken"])
        if refreshed:
            token = refreshed["accessToken"]
        else:
            raise Exception("Session expired. Run: refineo login")

    return _make_request(
        path,
        method=method,
        data=data,
        headers={"Authorization": f"Bearer {token}"},
    )


def _refresh_token(refresh_token: str) -> Optional[Credentials]:
    """Refresh access token."""
    try:
        data = _make_request(
            "/api/auth/device/refresh",
            method="POST",
            data={
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )

        old_credentials = load_credentials()

        credentials: Credentials = {
            "accessToken": data["access_token"],
            "refreshToken": data["refresh_token"],
            "expiresAt": data["expires_at"],
            "user": old_credentials["user"] if old_credentials else {"email": "", "tier": "", "name": None},
        }

        save_credentials(credentials)
        return credentials
    except Exception:
        return None


def start_device_code_flow() -> DeviceCodeResponse:
    """Start device code flow."""
    return _make_request("/api/auth/device/code", method="POST")


def poll_for_token(
    device_code: str,
    interval: int,
    expires_in: int,
    on_poll: Optional[Callable[[], None]] = None,
) -> Credentials:
    """Poll for device code authorization."""
    start_time = time.time()
    timeout = expires_in

    while time.time() - start_time < timeout:
        if on_poll:
            on_poll()

        try:
            data = _make_request(
                "/api/auth/device/token",
                method="POST",
                data={
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
            )

            # Success!
            credentials: Credentials = {
                "accessToken": data["access_token"],
                "refreshToken": data["refresh_token"],
                "expiresAt": data["expires_at"],
                "user": data.get("user", {"email": "", "tier": "", "name": None}),
            }
            save_credentials(credentials)
            return credentials

        except Exception as e:
            error_msg = str(e)

            if "authorization_pending" in error_msg:
                time.sleep(interval)
                continue

            if "slow_down" in error_msg:
                time.sleep(interval + 5)
                continue

            if "access_denied" in error_msg:
                raise Exception(
                    "Access denied. CLI requires Pro or Ultra subscription."
                ) from e

            if "expired_token" in error_msg:
                raise Exception("Login timed out. Please try again.") from e

            raise

    raise Exception("Login timed out. Please try again.")


def humanize(
    text: str,
    model: str = "enhanced",
) -> HumanizeResult:
    """Humanize text."""
    api_model = "BALANCE" if model == "standard" else "ENHANCED"

    result = _api_request(
        "/api/humanize",
        method="POST",
        data={"text": text, "model": api_model},
    )

    return {
        "humanizedText": result["data"]["humanizedText"],
        "wordCount": result["data"]["wordCount"],
        "model": result["data"]["model"],
    }


def get_usage() -> UsageStats:
    """Get usage stats."""
    result = _api_request("/api/usage")

    return {
        "tier": result["tier"],
        "used": result["used"],
        "limit": result["limit"],
        "remaining": result["remaining"],
        "resetDate": result.get("resetDate"),
        "wordLimit": result["wordLimit"],
        "rateLimit": result.get("rateLimit"),
    }
