"""OAuth authentication for Gmail API."""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Read-only scope for searching and reading emails
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Default credential paths
DEFAULT_CREDS_DIR = Path.home() / ".gmail-mcp"
DEFAULT_CREDS_PATH = DEFAULT_CREDS_DIR / "gcp-oauth.keys.json"
DEFAULT_TOKEN_PATH = DEFAULT_CREDS_DIR / "token.json"


def get_credentials(
    creds_path: Path | str | None = None,
    token_path: Path | str | None = None,
) -> Credentials:
    """
    Get valid Gmail API credentials.

    Loads existing token if valid, refreshes if expired, or runs OAuth flow
    if no token exists (opens browser for user authorization).

    Args:
        creds_path: Path to OAuth client secrets JSON (from Google Cloud Console)
        token_path: Path to store/load user's access token

    Returns:
        Valid Credentials object for Gmail API

    Raises:
        FileNotFoundError: If credentials file doesn't exist
        ValueError: If OAuth flow fails
    """
    # Use environment variable or defaults
    if creds_path is None:
        creds_path = Path(os.environ.get("GMAIL_CREDENTIALS_PATH", DEFAULT_CREDS_PATH))
    else:
        creds_path = Path(creds_path)

    if token_path is None:
        token_path = Path(os.environ.get("GMAIL_TOKEN_PATH", DEFAULT_TOKEN_PATH))
    else:
        token_path = Path(token_path)

    creds = None

    # Load existing token if available
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # Refresh or get new credentials
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Need to run OAuth flow
            if not creds_path.exists():
                raise FileNotFoundError(
                    f"OAuth credentials not found at {creds_path}. "
                    f"Download from Google Cloud Console and save to {creds_path}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds
