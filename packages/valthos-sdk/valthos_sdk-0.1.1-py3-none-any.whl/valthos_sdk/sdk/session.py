"""Session management for Valthos SDK.

This module provides the main Session class for interacting with the Valthos API.
The Session class handles authentication, token management, and workspace operations,
serving as the primary entry point for SDK users.

The Session class automatically manages authentication tokens, handles token refresh,
and provides methods for workspace discovery, creation, and management. It maintains
a persistent HTTP client with proper retry logic and error handling.

Key Classes:
    Session: Main API client for workspace operations with automatic authentication.

Main Features:
    - Automatic token management and refresh
    - Workspace listing with filtering and pagination
    - Workspace creation and archiving
    - Integration with WorkspaceProxy for file operations
    - Comprehensive error handling and logging

Example Usage:
    Basic session setup:
        >>> import valthos_sdk
        >>> session = valthos_sdk.Session()  # Uses stored credentials
        
    Workspace operations:
        >>> workspaces = session.list_workspaces()
        >>> workspace = session.create_workspace("My Project")
        >>> files = workspace.list()

Authentication:
    The Session expects credentials to be stored locally (typically in ~/.valthos/credentials)
    or provided during initialization. Use valthos_sdk.login() to set up credentials initially.
"""

from datetime import datetime
from typing import Optional, List

from .auth import load_credentials, refresh_token
from .client import HTTPClient
from .exceptions import AuthenticationError, WorkspaceNotFoundError
from .models import Credentials, WorkspaceData, WorkspaceListResponse, WorkspaceCreateRequest
from .workspace import WorkspaceProxy


class ToolsNamespace:
    """Namespace for creating analysis tools through the session."""

    def __init__(self, session):
        self.session = session

    def ProteinProfiling(self, **kwargs):
        """Create a Protein Profiling analysis tool."""
        from ..tools import ProteinProfiling
        return ProteinProfiling(session=self.session, **kwargs)

    def GenomeProfiling(self, **kwargs):
        """Create a Genome Profiling analysis tool."""
        from ..tools import GenomeProfiling
        return GenomeProfiling(session=self.session, **kwargs)


class Session:
    """Valthos API session with automatic token management.
    
    The Session class provides the main interface for interacting with
    Valthos workspaces. It handles authentication, token refresh, and
    workspace management operations automatically.
    
    The session maintains your authentication credentials and provides
    methods to list, create, and manage workspaces. All API calls are
    automatically authenticated and tokens are refreshed as needed.
    
    Examples:
        Basic usage with stored credentials:
            >>> import valthos_sdk
            >>> session = valthos_sdk.Session()
            >>> workspaces = session.list_workspaces()
            
        Create a new workspace:
            >>> workspace = session.create_workspace(name="My Project")
            >>> print(f"Created workspace: {workspace.name}")
            
        Get an existing workspace:
            >>> workspace = session.workspace(name="Data Analysis")
            >>> files = workspace.list()
    
    Attributes:
        credentials (Credentials): User authentication credentials loaded
            from storage or provided during initialization.
        client (HTTPClient): HTTP client configured for API requests
            with automatic retry and error handling.
    """
    
    def __init__(self, root_domain: Optional[str] = None, token: Optional[str] = None, 
                 credentials: Optional[Credentials] = None):
        """Initialize session with credentials or load from storage."""
        
        if credentials:
            # Use provided credentials
            self.credentials = credentials
        elif root_domain and token:
            # Create temporary credentials
            self.credentials = Credentials(
                root_domain=root_domain,
                access_token=token
            )
        else:
            # Load from stored credentials
            self.credentials = load_credentials()
            if not self.credentials:
                raise AuthenticationError(
                    "No credentials found. Please run valthos_sdk.login() first."
                )
        
        # Use library URL for workspace operations
        self.client = HTTPClient(
            base_url=self.credentials.library_url,
            access_token=self.credentials.access_token
        )
        
        # Initialize tools namespace
        self._tools = None
    
    @property
    def tools(self) -> ToolsNamespace:
        """Get tools namespace for creating analysis tools.
        
        Returns:
            ToolsNamespace object for creating tools
            
        Examples:
            >>> fitness = session.tools.Fitness(
            ...     input_path='s3://bucket/proteins.parquet',
            ...     output_path='s3://bucket/results/fitness.parquet',
            ...     log_file='s3://bucket/logs/fitness.log'
            ... )
            >>> embeddings = session.tools.Embeddings(
            ...     input_path='s3://bucket/sequences.parquet',
            ...     output_path='s3://bucket/embeddings.parquet',
            ...     log_file='s3://bucket/logs/embeddings.log'
            ... )
        """
        if self._tools is None:
            self._tools = ToolsNamespace(self)
        return self._tools
    
    def _ensure_valid_token(self):
        """Ensure we have a valid, non-expired token."""
        if not self.credentials.expires_at:
            # No expiration info, assume token is valid
            return
        
        # Check if token is expired (with 5 minute buffer)
        if datetime.utcnow() >= self.credentials.expires_at:
            if not self.credentials.refresh_token:
                raise AuthenticationError(
                    "Token has expired and no refresh token available. Please login again."
                )
            
            # Refresh the token
            self.credentials = refresh_token(self.credentials)
            self.client.set_access_token(self.credentials.access_token)
    
    def list_workspaces(self, status: Optional[str] = None, 
                       limit: Optional[int] = None, 
                       offset: Optional[int] = None) -> List[WorkspaceProxy]:
        """List user's workspaces with optional filtering.
        
        Retrieves all workspaces owned by the current user. Results can be
        filtered by status and paginated using limit and offset parameters.
        
        Args:
            status (str, optional): Filter by workspace status. Common values
                are "active" and "archived". Defaults to None (all statuses).
            limit (int, optional): Maximum number of workspaces to return.
                Useful for pagination. Defaults to None (no limit).
            offset (int, optional): Number of workspaces to skip. Used with
                limit for pagination. Defaults to None (start from beginning).
        
        Returns:
            List[WorkspaceProxy]: List of WorkspaceProxy objects representing
                the user's workspaces. Each proxy provides access to workspace
                metadata and file operations.
        
        Raises:
            AuthenticationError: If user is not properly authenticated.
            APIError: If the API request fails.
        
        Examples:
            List all workspaces:
                >>> workspaces = session.list_workspaces()
                >>> for ws in workspaces:
                ...     print(f"{ws.name}: {ws.status}")
                
            List only active workspaces:
                >>> active_workspaces = session.list_workspaces(status="active")
                
            Paginated listing:
                >>> first_10 = session.list_workspaces(limit=10, offset=0)
                >>> next_10 = session.list_workspaces(limit=10, offset=10)
        """
        self._ensure_valid_token()
        
        params = {}
        if status:
            params['status'] = status
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        
        response_data = self.client.get("/api/v1/workspaces", params=params)
        
        # Handle both list and object response formats
        if isinstance(response_data, list):
            # API returns list directly
            workspaces_data = [WorkspaceData(**workspace) for workspace in response_data]
        else:
            # API returns object with workspaces field
            workspace_list = WorkspaceListResponse(**response_data)
            workspaces_data = workspace_list.workspaces
        
        return [WorkspaceProxy(workspace, self.client, self) for workspace in workspaces_data]
    
    def workspace(self, name: Optional[str] = None, 
                  rid: Optional[str] = None) -> WorkspaceProxy:
        """Get workspace by name or RID.
        
        Retrieves a specific workspace that the user owns. The workspace
        can be identified by either its display name or its unique resource
        identifier (RID).
        
        Args:
            name (str, optional): Display name of the workspace. Either name
                or rid must be provided, but not both.
            rid (str, optional): Resource identifier of the workspace. Either
                name or rid must be provided, but not both.
        
        Returns:
            WorkspaceProxy: Proxy object for the specified workspace, providing
                access to workspace metadata and file operations.
        
        Raises:
            ValueError: If neither name nor rid is provided.
            WorkspaceNotFoundError: If no workspace with the specified name
                or RID exists or the user doesn't have access to it.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Get workspace by name:
                >>> workspace = session.workspace(name="Data Analysis")
                >>> print(f"Workspace RID: {workspace.rid}")
                
            Get workspace by RID:
                >>> workspace = session.workspace(rid="ws_123456789")
                >>> print(f"Workspace name: {workspace.name}")
                
            Use the workspace for file operations:
                >>> workspace = session.workspace(name="My Project")
                >>> files = workspace.list()
                >>> workspace.add('/local/data.csv', 'data/raw.csv')
        """
        if not name and not rid:
            raise ValueError("Either name or rid must be provided")
        
        self._ensure_valid_token()
        
        if rid:
            # Get workspace by RID directly
            response_data = self.client.get(f"/api/v1/workspaces/{rid}")
            workspace_data = WorkspaceData(**response_data)
            return WorkspaceProxy(workspace_data, self.client, self)
        else:
            # Search for workspace by name
            workspaces = self.list_workspaces()
            for workspace in workspaces:
                if workspace.name == name:
                    return workspace
            
            raise WorkspaceNotFoundError(f"Workspace with name '{name}' not found")
    
    def create_workspace(self, name: str, description: Optional[str] = None) -> WorkspaceProxy:
        """Create a new workspace.
        
        Creates a new workspace owned by the current user. Workspace names
        must be unique within the user's account. The new workspace starts
        in "active" status and is immediately available for file operations.
        
        Args:
            name (str): Name for the new workspace. Must be unique within
                the user's account and cannot be empty.
            description (str, optional): Optional description for the workspace.
                Helpful for documenting the workspace purpose. Defaults to None.
        
        Returns:
            WorkspaceProxy: Proxy object for the newly created workspace,
                ready for file operations and management.
        
        Raises:
            APIError: If workspace name already exists, name is invalid,
                or creation fails for any other reason.
            AuthenticationError: If user is not properly authenticated.
            ValueError: If name is empty or invalid.
        
        Examples:
            Create a simple workspace:
                >>> workspace = session.create_workspace(name="Data Analysis")
                >>> print(f"Created: {workspace.name} ({workspace.rid})")
                
            Create workspace with description:
                >>> workspace = session.create_workspace(
                ...     name="ML Experiments",
                ...     description="Machine learning model training workspace"
                ... )
                
            Immediately use the new workspace:
                >>> workspace = session.create_workspace(name="Quick Analysis")
                >>> workspace.create_folder("raw_data")
                >>> workspace.create_folder("processed")
        """
        self._ensure_valid_token()
        
        workspace_data = WorkspaceCreateRequest(name=name, description=description)
        response_data = self.client.post("/api/v1/workspaces/", data=workspace_data.model_dump())
        
        workspace_data = WorkspaceData(**response_data)
        return WorkspaceProxy(workspace_data, self.client, self)
    
    def archive_workspace(self, name: Optional[str] = None, rid: Optional[str] = None) -> dict:
        """Archive a workspace by name or RID.
        
        Archives the specified workspace, changing its status to "archived".
        Archived workspaces are read-only and hidden from default workspace
        listings, but their files remain accessible. Archived workspaces can
        be unarchived later if needed.
        
        Args:
            name (str, optional): Name of workspace to archive. Either name
                or rid must be provided, but not both.
            rid (str, optional): Resource ID of workspace to archive. Either
                name or rid must be provided, but not both.
        
        Returns:
            dict: API response containing success message and workspace RID.
                Typically includes 'message' and 'workspace_rid' keys.
        
        Raises:
            ValueError: If neither name nor rid is provided.
            WorkspaceNotFoundError: If specified workspace doesn't exist
                or user doesn't have access to it.
            APIError: If archiving operation fails.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Archive by name:
                >>> result = session.archive_workspace(name="Old Project")
                >>> print(result['message'])  # "Workspace archived successfully"
                
            Archive by RID:
                >>> result = session.archive_workspace(rid="ws_123456")
                >>> archived_rid = result['workspace_rid']
                
            Archive and verify:
                >>> session.archive_workspace(name="Temporary Analysis")
                >>> workspaces = session.list_workspaces(status="active")
                >>> # "Temporary Analysis" no longer appears in active list
        """
        if not name and not rid:
            raise ValueError("Either name or rid must be provided")
        
        self._ensure_valid_token()
        
        # If name provided, get the workspace first to get the RID
        if name:
            workspace = self.workspace(name=name)
            rid = workspace.rid
        
        response_data = self.client.put(f"/api/v1/workspaces/{rid}/archive")
        return response_data
    
    def __repr__(self) -> str:
        return f"Session(root_domain='{self.credentials.root_domain}')"