"""Authentication functionality for Valthos SDK."""

import json
import os
import stat
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .client import HTTPClient
from .exceptions import AuthenticationError, ConfigurationError
from .models import Credentials, TokenExchangeRequest, TokenExchangeResponse


def get_credentials_path() -> Path:
    """Get the path to the credentials file."""
    return Path.home() / ".valthos" / "credentials"


def save_credentials(credentials: Credentials) -> None:
    """Save credentials to local file with secure permissions."""
    credentials_path = get_credentials_path()
    credentials_path.parent.mkdir(exist_ok=True)
    
    # Write credentials to file
    with open(credentials_path, 'w') as f:
        json.dump(credentials.dict(), f, indent=2, default=str)
    
    # Set secure permissions (user read/write only)
    os.chmod(credentials_path, stat.S_IRUSR | stat.S_IWUSR)


def load_credentials() -> Optional[Credentials]:
    """Load credentials from local file."""
    credentials_path = get_credentials_path()
    
    if not credentials_path.exists():
        return None
    
    try:
        with open(credentials_path, 'r') as f:
            data = json.load(f)
        
        # Convert expires_at string back to datetime if present
        if data.get('expires_at'):
            data['expires_at'] = datetime.fromisoformat(data['expires_at'].replace('Z', '+00:00'))
        
        return Credentials(**data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        raise ConfigurationError(f"Invalid credentials file: {e}")


def exchange_token(admin_url: str, pat_token: str) -> TokenExchangeResponse:
    """Exchange PAT for bearer token using admin API."""
    client = HTTPClient(admin_url)
    
    request_data = TokenExchangeRequest(token=pat_token)
    
    try:
        response_data = client.post("/api/v1/exchange", request_data.dict())
        return TokenExchangeResponse(**response_data)
    except Exception as e:
        raise AuthenticationError(f"Token exchange failed: {str(e)}")


def login(root_domain: Optional[str] = None, token: Optional[str] = None):
    """Interactive login flow that prompts for credentials and saves them."""
    from .session import Session  # Import here to avoid circular import
    
    # Get root domain
    if not root_domain:
        root_domain = input("Root domain [valthos.com]: ").strip()
        if not root_domain:
            root_domain = "valthos.com"
    
    # Remove any protocol prefix if provided
    root_domain = root_domain.replace('https://', '').replace('http://', '')
    # Remove any subdomain prefixes if accidentally included
    if root_domain.startswith('admin.') or root_domain.startswith('library.'):
        root_domain = root_domain.split('.', 1)[1]
    
    # Get PAT token
    if not token:
        token = input("Personal Access Token: ").strip()
        if not token:
            raise ConfigurationError("Personal Access Token is required")
    
    # Construct admin URL for token exchange
    admin_url = f"https://admin.{root_domain}"
    
    # Exchange PAT for bearer token
    try:
        token_response = exchange_token(admin_url, token)
    except Exception as e:
        raise AuthenticationError(f"Authentication failed: {str(e)}")
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + timedelta(seconds=token_response.expires_in)
    
    # Create and save credentials
    credentials = Credentials(
        root_domain=root_domain,
        access_token=token_response.access_token,
        refresh_token=token,  # Store PAT as refresh token for future exchanges
        expires_at=expires_at
    )
    
    save_credentials(credentials)
    
    # Return authenticated session
    return Session(credentials=credentials)


def refresh_token(credentials: Credentials) -> Credentials:
    """Refresh an expired token using the stored PAT."""
    if not credentials.refresh_token:
        raise AuthenticationError("No refresh token available")
    
    try:
        token_response = exchange_token(credentials.admin_url, credentials.refresh_token)
    except Exception as e:
        raise AuthenticationError(f"Token refresh failed: {str(e)}")
    
    # Update credentials with new token
    expires_at = datetime.utcnow() + timedelta(seconds=token_response.expires_in)
    updated_credentials = credentials.copy(update={
        'access_token': token_response.access_token,
        'expires_at': expires_at
    })
    
    # Save updated credentials
    save_credentials(updated_credentials)
    
    return updated_credentials