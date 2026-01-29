"""Valthos Python SDK - Main package."""

from . import tools
from .sdk import Session, WorkspaceProxy, login
from .sdk.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    InvalidTokenError,
    NetworkError,
    TokenExpiredError,
    ValthosError,
    WorkspaceNotFoundError,
)

__version__ = "0.1.1"

__all__ = [
    "login",
    "Session",
    "WorkspaceProxy",
    "tools",
    "ValthosError",
    "AuthenticationError",
    "TokenExpiredError",
    "InvalidTokenError",
    "APIError",
    "NetworkError",
    "ConfigurationError",
    "WorkspaceNotFoundError",
]
