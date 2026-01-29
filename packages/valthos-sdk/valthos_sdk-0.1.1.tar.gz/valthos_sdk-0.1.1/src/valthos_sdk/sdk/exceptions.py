"""Custom exceptions for Valthos SDK."""


class ValthosError(Exception):
    """Base exception for all Valthos SDK errors."""
    pass


class AuthenticationError(ValthosError):
    """Authentication related errors."""
    pass


class TokenExpiredError(AuthenticationError):
    """Token has expired and needs refresh."""
    pass


class InvalidTokenError(AuthenticationError):
    """Token is invalid or malformed."""
    pass


class APIError(ValthosError):
    """API request errors."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class NetworkError(ValthosError):
    """Network connectivity errors."""
    pass


class ConfigurationError(ValthosError):
    """Configuration or setup errors."""
    pass


class WorkspaceNotFoundError(ValthosError):
    """Workspace not found error."""
    pass


class FileError(ValthosError):
    """Base class for file operation errors."""
    pass


class FileNotFoundError(FileError):
    """File not found error."""
    pass


class FileUploadError(FileError):
    """File upload operation error."""
    pass


class FileOperationError(FileError):
    """General file operation error (rename, copy, delete)."""
    pass


class FolderNotFoundError(FileError):
    """Folder not found error."""
    pass