"""Data models for Valthos SDK."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TokenExchangeRequest(BaseModel):
    """Request model for token exchange."""
    token: str


class TokenExchangeResponse(BaseModel):
    """Response model for token exchange."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    scope: Optional[str] = None


class Credentials(BaseModel):
    """User credentials stored locally."""
    root_domain: str  # e.g., "dev-valthos.com" 
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    @property
    def admin_url(self) -> str:
        """Get the admin API URL."""
        return f"https://admin.{self.root_domain}"
    
    @property
    def library_url(self) -> str:
        """Get the library API URL."""
        return f"https://library.{self.root_domain}"


class WorkspaceData(BaseModel):
    """Workspace data from API."""
    rid: str
    name: str
    description: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorkspaceListResponse(BaseModel):
    """Response model for workspace listing."""
    workspaces: List[WorkspaceData]
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class WorkspaceCreateRequest(BaseModel):
    """Request model for workspace creation."""
    name: str
    description: Optional[str] = None


class FileItem(BaseModel):
    """File or folder item in workspace listing."""
    path: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    is_folder: bool = False


class FileProxy(BaseModel):
    """Proxy object for uploaded files."""
    file_key: str
    workspace_rid: str
    path: str
    filename: str