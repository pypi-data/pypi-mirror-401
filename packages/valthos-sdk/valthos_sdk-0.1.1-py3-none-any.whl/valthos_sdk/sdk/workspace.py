"""Workspace file and folder operations for Valthos SDK.

This module provides the WorkspaceProxy class for managing files and folders within
Valthos workspaces. WorkspaceProxy objects are typically obtained through Session
methods and provide intuitive methods for file upload, download, organization, and
management.

The WorkspaceProxy class abstracts the complexity of API calls into simple, 
Pythonic methods for common file operations. It handles path normalization,
error handling, and provides comprehensive feedback on operation results.

Key Classes:
    WorkspaceProxy: Proxy object for workspace file and folder operations.

Main Features:
    - File upload from local filesystem
    - Folder creation and organization
    - File and folder renaming/moving
    - File copying and deletion
    - Directory listing with filtering
    - Comprehensive error handling

File Operations Supported:
    - add() / put(): Upload files from local filesystem
    - list() / dir(): List workspace contents with optional filtering
    - create_folder(): Create directory structures
    - rename(): Rename or move files and folders
    - copy(): Duplicate files within workspace
    - delete(): Remove files and folders

Example Usage:
    Basic file operations (multiple naming styles supported):
        >>> workspace = session.workspace("My Project")
        >>> workspace.add('/local/data.csv', 'data/input.csv')  # or workspace.put(...)
        >>> workspace.create_folder('processed')
        >>> files = workspace.list()  # or workspace.dir()
        
    File organization:
        >>> workspace.rename('input.csv', 'raw_data.csv')
        >>> workspace.copy('raw_data.csv', 'backup/raw_data.csv')
        >>> workspace.delete('temporary_files/')
        
    Familiar naming conventions:
        >>> workspace.put('/reports/analysis.pdf', 'docs/analysis.pdf')  # Cloud storage style
        >>> contents = workspace.dir('docs')  # Filesystem style

Error Handling:
    All methods raise appropriate exceptions from the valthos.sdk.exceptions module,
    including FileUploadError, FileOperationError, and FileNotFoundError for
    comprehensive error handling and debugging.
"""

import os
from typing import Optional, List
from .models import WorkspaceData, FileItem, FileProxy
from .exceptions import WorkspaceNotFoundError, FileUploadError, FileOperationError, FileNotFoundError
from .client import HTTPClient


class WorkspaceProxy:
    """Workspace for file management and bioinformatics analysis.
    
    WorkspaceProxy provides a unified interface for managing files and running
    bioinformatics analyses within a Valthos workspace. It supports file operations
    (upload, download, organize) and workspace-scoped analysis tools that automatically
    handle path resolution and data organization.
    
    WorkspaceProxy objects are typically obtained through Session methods
    like workspace(), create_workspace(), or list_workspaces(). They maintain
    a connection to the workspace and provide intuitive methods for both file
    management and analysis workflows.
    
    Key Features:
        - File Management: Upload, download, organize files and folders
        - Analysis Tools: Access to bioinformatics tools via workspace.tools
        - Path Abstraction: Work with simple relative paths instead of S3 URLs
        - Workspace Isolation: All operations are scoped to your workspace
    
    Examples:
        File management:
            >>> workspace = session.workspace("My Project")
            >>> file_proxy = workspace.add('/local/data.csv', 'raw/data.csv')
            >>> files = workspace.list()
            >>> workspace.create_folder('results')
            
        Bioinformatics analysis:
            >>> profiler = workspace.tools.ProteinProfiling(
            ...     input='raw/proteins.fasta',
            ...     output='results/profiling.json'
            ... )
            >>> validation = profiler.validate()
            >>> if validation['status'] == 'valid':
            ...     result = profiler.run()
            
        File organization:
            >>> workspace.copy('raw/data.csv', 'backup/data_backup.csv')
            >>> workspace.rename('temp.txt', 'results/final.txt')
            >>> workspace.delete('backup/old_file.txt')
    
    Analysis Tools:
        Access bioinformatics tools through the .tools namespace:
            >>> help(workspace.tools)          # See available analysis tools
            >>> help(workspace.tools.Fitness)  # Get help on specific tools
    
    Attributes:
        rid (str): Workspace resource identifier.
        name (str): Display name of the workspace.
        description (str): Optional workspace description.
        status (str): Current workspace status (e.g., "active", "archived").
        created_at (datetime): When the workspace was created.
        updated_at (datetime): When the workspace was last modified.
        tools: Namespace for accessing workspace-scoped analysis tools.
        
    See Also:
        help(workspace.tools): Available bioinformatics analysis tools
        session.create_workspace(): Create new workspaces
        session.list_workspaces(): List existing workspaces
    """
    
    def __init__(self, workspace_data: WorkspaceData, client: HTTPClient, session=None):
        self._data = workspace_data
        self._client = client
        self._session = session  # Reference to parent session for token refresh
    
    def _ensure_valid_token(self):
        """Ensure we have a valid, non-expired token using the parent session."""
        if self._session:
            self._session._ensure_valid_token()
    
    @property
    def rid(self) -> str:
        """Get workspace RID."""
        return self._data.rid
    
    @property
    def name(self) -> str:
        """Get workspace name."""
        return self._data.name
    
    @property
    def description(self) -> Optional[str]:
        """Get workspace description."""
        return self._data.description
    
    @property
    def status(self) -> str:
        """Get workspace status."""
        return self._data.status
    
    @property
    def created_at(self):
        """Get workspace creation timestamp."""
        return self._data.created_at
    
    @property
    def updated_at(self):
        """Get workspace last update timestamp."""
        return self._data.updated_at
    
    def add(self, local_path: str, workspace_path: Optional[str] = None) -> FileProxy:
        """Upload a file to the workspace.
        
        Uploads a local file to the specified path in the workspace. If no
        workspace path is provided, the file is uploaded to the workspace root
        using its original filename. The file is uploaded via multipart form
        data and a FileProxy object is returned for tracking.
        
        Args:
            local_path (str): Path to the local file to upload. Must be a valid
                file path that exists on the local filesystem.
            workspace_path (str, optional): Destination path in workspace
                relative to workspace root. If None, uses the original filename
                in the workspace root. Can include folder paths like 'data/input.csv'.
        
        Returns:
            FileProxy: Proxy object representing the uploaded file, containing
                metadata like file_key, workspace_rid, path, and filename.
        
        Raises:
            FileUploadError: If local file doesn't exist, upload fails due to
                network issues, or server-side processing fails.
            FileNotFoundError: If the specified local_path doesn't exist.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Upload file to workspace root:
                >>> file_proxy = workspace.add('/home/user/data.csv')
                >>> print(f"Uploaded: {file_proxy.filename}")
                
            Upload with custom workspace path:
                >>> file_proxy = workspace.add('/home/user/data.csv', 'raw/data.csv')
                >>> print(f"Uploaded to: {file_proxy.path}")
                
            Upload multiple files:
                >>> files = ['/home/report.pdf', '/home/analysis.py']
                >>> for local_file in files:
                ...     try:
                ...         proxy = workspace.add(local_file, f'uploads/{os.path.basename(local_file)}')
                ...         print(f"Successfully uploaded: {proxy.filename}")
                ...     except FileUploadError as e:
                ...         print(f"Failed to upload {local_file}: {e}")
        """
        self._ensure_valid_token()
        
        if not os.path.exists(local_path):
            raise FileUploadError(f"Local file not found: {local_path}")
        
        if workspace_path is None:
            workspace_path = os.path.basename(local_path)
        
        # Remove leading slash if present to match API expectations
        workspace_path = workspace_path.lstrip('/')
        
        try:
            response_data = self._client.upload_file(
                f"/api/v1/workspaces/{self.rid}/files",
                local_path,
                workspace_path
            )
            
            return FileProxy(
                file_key=response_data["file_key"],
                workspace_rid=self.rid,
                path=response_data["path"],
                filename=response_data["filename"]
            )
        except Exception as e:
            raise FileUploadError(f"Failed to upload file {local_path}: {str(e)}")
    
    def create_folder(self, path: str) -> dict:
        """Create a folder in the workspace.
        
        Creates a new folder at the specified path within the workspace.
        Parent directories will be created automatically if they don't exist.
        If the folder already exists, this operation will succeed silently.
        
        Args:
            path (str): Path for the new folder relative to workspace root.
                Can include nested paths like 'data/raw' to create nested
                folder structures.
        
        Returns:
            dict: API response containing success message and folder details.
                Typically includes 'message', 'path', and workspace RID.
        
        Raises:
            FileOperationError: If folder creation fails due to invalid
                path, permissions, or other API errors.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Create a simple folder:
                >>> result = workspace.create_folder('data')
                >>> print(result['message'])  # "Folder created successfully"
                
            Create nested folders:
                >>> workspace.create_folder('data/raw')
                >>> workspace.create_folder('data/processed')
                >>> workspace.create_folder('reports/2024/january')
                
            Organize a new workspace:
                >>> folders = ['input', 'output', 'scripts', 'docs']
                >>> for folder in folders:
                ...     workspace.create_folder(folder)
        """
        self._ensure_valid_token()
        
        path = path.strip('/')
        try:
            return self._client.post(
                f"/api/v1/workspaces/{self.rid}/folders?path={path}"
            )
        except Exception as e:
            raise FileOperationError(f"Failed to create folder {path}: {str(e)}")
    
    def rename(self, old_path: str, new_path: str) -> dict:
        """Rename/move a file or folder within the workspace.
        
        Renames or moves a file or folder from one path to another within
        the same workspace. This operation can be used for simple renaming
        or for moving files between folders. The destination folder must
        exist before moving files into it.
        
        Args:
            old_path (str): Current path of the file or folder relative to
                workspace root. Must exist in the workspace.
            new_path (str): New path for the file or folder relative to
                workspace root. Parent directory must exist.
        
        Returns:
            dict: API response containing success message and path details.
                Includes 'message', 'old_path', 'new_path', and workspace RID.
        
        Raises:
            FileOperationError: If source doesn't exist, destination already
                exists, parent directory doesn't exist, or operation fails.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Simple rename:
                >>> workspace.rename('data.csv', 'cleaned_data.csv')
                
            Move file to different folder:
                >>> workspace.rename('temp.txt', 'archive/temp.txt')
                
            Rename a folder:
                >>> workspace.rename('old_folder', 'new_folder')
                
            Reorganize files:
                >>> workspace.rename('raw_data.csv', 'input/raw_data.csv')
                >>> workspace.rename('results.txt', 'output/final_results.txt')
        """
        self._ensure_valid_token()
        
        old_path = old_path.strip('/')
        new_path = new_path.strip('/')
        
        try:
            return self._client.put(
                f"/api/v1/workspaces/{self.rid}/files/rename?old_path={old_path}&new_path={new_path}"
            )
        except Exception as e:
            raise FileOperationError(f"Failed to rename {old_path} to {new_path}: {str(e)}")
    
    def delete(self, path: str) -> dict:
        """Delete a file or folder from the workspace.
        
        Permanently deletes the specified file or folder from the workspace.
        The method automatically detects whether the path refers to a file or
        folder and handles the deletion appropriately. For folders, all contents
        are recursively deleted. This operation cannot be undone, so use with caution.
        
        Args:
            path (str): Path of the file or folder to delete, relative to
                workspace root. The method automatically detects whether it's
                a file or folder.
        
        Returns:
            dict: API response containing success message and deletion details.
                Response format varies based on whether a file or folder was deleted.
        
        Raises:
            FileOperationError: If the file/folder doesn't exist or deletion
                fails due to permissions or other errors.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Delete a file:
                >>> result = workspace.delete('old_data.csv')
                >>> print(result['message'])  # "File deleted successfully"
                
            Delete a folder and its contents:
                >>> result = workspace.delete('temporary_analysis')
                >>> print(result['message'])  # "Folder and all contents deleted successfully"
                
            Delete works for any path (auto-detection):
                >>> workspace.delete('data.txt')         # File
                >>> workspace.delete('reports/')         # Folder  
                >>> workspace.delete('cache')            # Folder (auto-detected)
                
            Clean up multiple items:
                >>> items_to_delete = ['temp1.txt', 'old_folder', 'cache/']
                >>> for item_path in items_to_delete:
                ...     try:
                ...         workspace.delete(item_path)
                ...         print(f"Deleted: {item_path}")
                ...     except FileOperationError as e:
                ...         print(f"Could not delete {item_path}: {e}")
        """
        self._ensure_valid_token()
        
        path = path.strip('/')
        
        try:
            return self._client.delete(f"/api/v1/workspaces/{self.rid}/items/{path}")
        except Exception as e:
            raise FileOperationError(f"Failed to delete {path}: {str(e)}")
    
    def copy(self, source_path: str, dest_path: str) -> dict:
        """Copy a file to a new location within the workspace.
        
        Creates a copy of an existing file at a new location within the same
        workspace. The original file remains unchanged. The destination folder
        must exist before copying files into it.
        
        Args:
            source_path (str): Path of the source file to copy, relative to
                workspace root. File must exist in the workspace.
            dest_path (str): Destination path for the copied file, relative
                to workspace root. Parent directory must exist.
        
        Returns:
            dict: API response containing success message and copy details.
                Includes 'message', 'source_path', 'destination_path', and 
                workspace RID.
        
        Raises:
            FileOperationError: If source file doesn't exist, destination
                already exists, parent directory doesn't exist, or copy fails.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            Simple file copy:
                >>> workspace.copy('data.csv', 'data_backup.csv')
                
            Copy to different folder:
                >>> workspace.copy('analysis.py', 'backup/analysis_v1.py')
                
            Create multiple backups:
                >>> workspace.copy('important.txt', 'backup/important.txt')
                >>> workspace.copy('important.txt', 'archive/important_2024.txt')
                
            Copy for processing:
                >>> workspace.copy('raw/dataset.csv', 'processing/dataset.csv')
                >>> # Process the file in processing folder
                >>> workspace.copy('processing/cleaned_dataset.csv', 'output/final.csv')
        """
        self._ensure_valid_token()
        
        source_path = source_path.strip('/')
        dest_path = dest_path.strip('/')
        
        try:
            return self._client.put(
                f"/api/v1/workspaces/{self.rid}/files/copy?source_path={source_path}&destination_path={dest_path}"
            )
        except Exception as e:
            raise FileOperationError(f"Failed to copy {source_path} to {dest_path}: {str(e)}")
    
    def list(self, path: Optional[str] = None, offset: Optional[int] = None, 
             limit: Optional[int] = None) -> List[FileItem]:
        """List files and folders in the workspace.
        
        Returns a list of all files and folders in the specified path within
        the workspace. If no path is specified, lists all contents in the
        workspace root. Results can be paginated using offset and limit.
        
        Args:
            path (str, optional): Path to list contents from, relative to
                workspace root. If None, lists workspace root contents.
                Use empty string '' for root, or folder paths like 'data/'.
            offset (int, optional): Number of items to skip for pagination.
                Useful when combined with limit. Defaults to None (no skip).
            limit (int, optional): Maximum number of items to return.
                Useful for pagination or limiting large listings. Defaults 
                to None (no limit).
        
        Returns:
            List[FileItem]: List of FileItem objects representing files and
                folders. Each item includes path, size, modification time,
                and folder status information.
        
        Raises:
            FileOperationError: If the specified path doesn't exist or
                listing fails due to permissions or other errors.
            AuthenticationError: If user is not properly authenticated.
        
        Examples:
            List all workspace contents:
                >>> files = workspace.list()
                >>> for item in files:
                ...     type_str = "folder" if item.is_folder else "file"
                ...     print(f"{item.path} ({type_str}) - {item.size or 0} bytes")
                
            List contents of a specific folder:
                >>> data_files = workspace.list('data')
                >>> csv_files = [f for f in data_files if f.path.endswith('.csv')]
                
            Paginated listing:
                >>> first_page = workspace.list(limit=10, offset=0)
                >>> second_page = workspace.list(limit=10, offset=10)
                
            Check if folder exists and list contents:
                >>> try:
                ...     contents = workspace.list('reports')
                ...     print(f"Found {len(contents)} items in reports folder")
                ... except FileOperationError:
                ...     print("Reports folder doesn't exist")
        """
        self._ensure_valid_token()
        
        params = {}
        if path:
            params["path"] = path.strip('/')
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        
        try:
            response_data = self._client.get(
                f"/api/v1/workspaces/{self.rid}/files",
                params=params
            )
            
            # response_data should be a list of file items
            if isinstance(response_data, list):
                return [FileItem(**item) for item in response_data]
            else:
                # Handle case where API wraps list in an object
                files_data = response_data.get('files', response_data)
                return [FileItem(**item) for item in files_data]
                
        except Exception as e:
            raise FileOperationError(f"Failed to list files in {path or 'workspace'}: {str(e)}")
    
    def dir(self, path: Optional[str] = None, offset: Optional[int] = None, 
            limit: Optional[int] = None) -> List[FileItem]:
        """List files and folders in the workspace (alias for list).
        
        This method is an alias for list() to provide a more familiar interface
        for users coming from filesystem operations.
        
        Args:
            path (str, optional): Path to list contents from. See list() for details.
            offset (int, optional): Number of items to skip for pagination.
            limit (int, optional): Maximum number of items to return.
        
        Returns:
            List[FileItem]: List of FileItem objects. Same as list().
        
        Examples:
            >>> files = workspace.dir()  # List all workspace contents
            >>> files = workspace.dir('data')  # List contents of data folder
        """
        return self.list(path, offset, limit)
    
    def put(self, local_path: str, workspace_path: Optional[str] = None) -> FileProxy:
        """Upload a file to the workspace (alias for add).
        
        This method is an alias for add() to provide a more familiar interface
        for users coming from cloud storage and API operations where 'put' is
        the standard terminology for uploading files.
        
        Args:
            local_path (str): Path to the local file to upload. Same as add().
            workspace_path (str, optional): Destination path in workspace.
                Same as add().
        
        Returns:
            FileProxy: Proxy object representing the uploaded file. Same as add().
        
        Examples:
            >>> file_proxy = workspace.put('/local/data.csv')  # Upload to root
            >>> file_proxy = workspace.put('/local/data.csv', 'raw/data.csv')  # Upload with path
        """
        return self.add(local_path, workspace_path)
    
    @property
    def tools(self):
        """Access Intel Module analysis tools scoped to this workspace.
        
        The tools namespace provides workspace-scoped access to bioinformatics
        analysis tools. All tools automatically use relative paths within the
        workspace, eliminating the need to specify full S3 URLs.
        
        Key Features:
            - Automatic path resolution: Use simple relative paths like 'data/input.fasta'
            - Workspace sandboxing: Outputs are automatically confined to your workspace
            - External data support: Can read from external S3 sources while writing to workspace
            - Auto-generated logs: Log files are created automatically if not specified

        Available Tools:
            - ProteinProfiling: Run multiple bioinformatics methods on protein sequences
            - GenomeProfiling: Extract and profile proteins from genome sequences

        Returns:
            WorkspaceToolsNamespace: Namespace for creating workspace-scoped analysis tools

        Examples:
            Basic protein profiling with workspace files:
                >>> workspace = session.workspace("My Project")
                >>> profiler = workspace.tools.ProteinProfiling(
                ...     input='proteins.fasta',
                ...     output='results/profiling.json'
                ... )
                >>> validation = profiler.validate()
                >>> if validation['status'] == 'valid':
                ...     result = profiler.run()

            Get help on specific tools:
                >>> help(workspace.tools.ProteinProfiling)

        See Also:
            help(workspace.tools.ProteinProfiling) for detailed profiling options
        """
        return WorkspaceToolsNamespace(self)
    
    def __repr__(self) -> str:
        return f"WorkspaceProxy(rid='{self.rid}', name='{self.name}', status='{self.status}')"


class WorkspaceToolsNamespace:
    """Bioinformatics analysis tools scoped to a workspace.

    This namespace provides access to various bioinformatics analysis tools
    that are automatically configured to work within a specific workspace.
    All tools use relative paths within the workspace, eliminating the need
    to manage S3 URLs directly.

    Key Benefits:
        - Simplified Paths: Use 'data/proteins.fasta' instead of full S3 URLs
        - Workspace Isolation: Outputs automatically saved to your workspace
        - External Data Support: Can read from public datasets or shared buckets
        - Auto-Generated Logs: Log files created automatically if not specified

    Available Tools:
        ProteinProfiling: Run multiple bioinformatics methods on a single protein
                 Orchestrates various analysis methods (world, cypress_1, etc.)
        GenomeProfiling: Extract and profile proteins from genome sequences
                 Performs ORF detection and runs protein profiling on each protein

    Usage Pattern:
        1. Create tool with relative paths
        2. Validate inputs and get time estimates
        3. Run analysis asynchronously
        4. Results saved automatically to workspace

    Examples:
        Get help on available tools:
            >>> help(workspace.tools.ProteinProfiling)

        Basic workflow:
            >>> profiler = workspace.tools.ProteinProfiling(
            ...     input='proteins.fasta',
            ...     output='results/profiling.json'
            ... )
            >>> validation = profiler.validate()
            >>> estimate = profiler.estimate()
            >>> result = profiler.run()
    """
    
    def __init__(self, workspace: 'WorkspaceProxy'):
        """Initialize the tools namespace with a workspace.

        Args:
            workspace: The WorkspaceProxy to scope tools to
        """
        self.workspace = workspace

    def ProteinProfiling(self, input: str, output: str,
                         log_file: Optional[str] = None, methods: Optional[List[str]] = None,
                         **kwargs):
        """Create a Protein Profiling tool scoped to this workspace.

        Args:
            input: Path to FASTA file containing protein sequence(s) (relative to workspace)
            output: Output path for results (relative to workspace)
            log_file: Path for log file (relative to workspace, auto-generated if not provided)
            methods: List of method names to run (default: ["world"])
            **kwargs: Additional configuration parameters

        Returns:
            ProteinProfiling tool instance configured for this workspace

        Examples:
            >>> # Write a FASTA file to workspace
            >>> workspace.write('proteins/my_protein.fasta',
            ...                 '>protein_001\\nMKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNL\\n')
            >>>
            >>> # Run profiling
            >>> profiler = workspace.tools.ProteinProfiling(
            ...     input='proteins/my_protein.fasta',
            ...     output='results/profiling.json',
            ...     methods=["world"]
            ... )
            >>> validation = profiler.validate()
            >>> result = profiler.run()
        """
        from datetime import datetime
        from typing import List
        from ..tools import ProteinProfiling

        # Auto-generate log file if not provided
        if not log_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f'logs/protein_profiling_{timestamp}.log'

        return ProteinProfiling(
            session=self.workspace._session,
            input=input,
            output=output,
            log_file=log_file,
            methods=methods,
            workspace_rid=self.workspace.rid,
            **kwargs
        )

    def GenomeProfiling(self, input: str, output: str,
                        log_file: Optional[str] = None, methods: Optional[List[str]] = None,
                        min_orf_length: int = 90, include_reverse_strand: bool = True,
                        **kwargs):
        """Create a Genome Profiling tool scoped to this workspace.

        Args:
            input: Path to FASTA file containing genome sequence(s) (relative to workspace)
            output: Output path for results (relative to workspace)
            log_file: Path for log file (relative to workspace, auto-generated if not provided)
            methods: List of method names to run on each protein (default: ["world"])
            min_orf_length: Minimum ORF length in nucleotides (default: 90)
            include_reverse_strand: Whether to find ORFs on reverse strand (default: True)
            **kwargs: Additional configuration parameters

        Returns:
            GenomeProfiling tool instance configured for this workspace

        Examples:
            >>> # Write a genome FASTA file to workspace
            >>> genome_seq = "ATGACTAAATAA" * 100  # Example genome
            >>> workspace.write('genomes/test_genome.fasta',
            ...                 f'>genome_001\\n{genome_seq}\\n')
            >>>
            >>> # Run genome profiling
            >>> profiler = workspace.tools.GenomeProfiling(
            ...     input='genomes/test_genome.fasta',
            ...     output='results/genome_profiling.json',
            ...     methods=["world"],
            ...     min_orf_length=90
            ... )
            >>> validation = profiler.validate()
            >>> result = profiler.run()
        """
        from datetime import datetime
        from typing import List
        from ..tools import GenomeProfiling

        # Auto-generate log file if not provided
        if not log_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f'logs/genome_profiling_{timestamp}.log'

        return GenomeProfiling(
            session=self.workspace._session,
            input=input,
            output=output,
            log_file=log_file,
            methods=methods,
            min_orf_length=min_orf_length,
            include_reverse_strand=include_reverse_strand,
            workspace_rid=self.workspace.rid,
            **kwargs
        )