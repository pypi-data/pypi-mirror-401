"""Valthos Python SDK."""

from .auth import login
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    InvalidTokenError,
    NetworkError,
    TokenExpiredError,
    ValthosError,
    WorkspaceNotFoundError,
)
from .session import Session
from .workspace import WorkspaceProxy

__version__ = "0.1.1"

__all__ = [
    "login",
    "Session",
    "WorkspaceProxy",
    "ValthosError",
    "AuthenticationError",
    "TokenExpiredError",
    "InvalidTokenError",
    "APIError",
    "NetworkError",
    "ConfigurationError",
    "WorkspaceNotFoundError",
]
