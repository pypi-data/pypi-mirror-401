"""Base class for Valthos analysis tools."""

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..sdk.session import Session


class BaseTool:
    """Base class for all Valthos analysis tools.
    
    Provides common functionality for validating inputs, estimating runtime,
    and executing bioinformatics workflows through the Intel Modules API.
    """
    
    def __init__(self, session: "Session", module_type: str, **kwargs):
        """Initialize a tool with session and parameters.
        
        Args:
            session: Authenticated Valthos session
            module_type: Type of intel module (e.g., 'fitness', 'host_adaptation')
            **kwargs: Tool-specific parameters
        """
        self.session = session
        self.client = session.client
        self.module_type = module_type
        
        # Extract workspace context if provided
        self.workspace_rid = kwargs.pop('workspace_rid', None)
        
        # Extract standard API parameters - these now match the API exactly
        self.input_path = kwargs.pop('input', None)
        self.output_path = kwargs.pop('output', None)
        self.log_file = kwargs.pop('log_file', None)
        
        # Validate required parameters
        if not self.input_path:
            raise ValueError("input_path is required")
        if not self.output_path:
            raise ValueError("output_path is required")
        if not self.log_file:
            raise ValueError("log_file is required")
        
        # Validate paths when using workspace context
        if self.workspace_rid:
            # Input can be relative OR S3 path
            if self.input_path.startswith('/'):
                raise ValueError("Absolute paths not supported. Use relative paths or S3 URLs.")
            
            # Output and log_file must be relative (no S3 paths) when using workspace
            for path_key, path_value in [('output_path', self.output_path), ('log_file', self.log_file)]:
                if path_value and (path_value.startswith('/') or path_value.startswith('s3://')):
                    raise ValueError(f"{path_key} must be a relative path within workspace when using workspace context")
        
        # Store remaining kwargs as config (these go into the 'config' field)
        self.config = kwargs
        
        # Ensure we have valid token
        self.session._ensure_valid_token()
    
    def _prepare_api_params(self) -> Dict[str, Any]:
        """Prepare parameters for Intel Module API calls.
        
        Returns:
            Dictionary with input_path, output_path, log_file, config, and optionally workspace_rid
        """
        params = {
            "input_path": self.input_path,
            "output_path": self.output_path,
            "log_file": self.log_file,
            "config": self.config
        }
        
        # Include workspace context if present
        if self.workspace_rid:
            params["workspace_rid"] = self.workspace_rid
            
        return params
    
    def validate(self) -> Dict[str, Any]:
        """Validate inputs and configuration.
        
        Returns:
            Validation result with status and any errors/warnings/hints
            
        Example:
            >>> validation = tool.validate()
            >>> if validation['status'] == 'valid':
            ...     print("Ready to run")
            >>> else:
            ...     print(f"Errors: {validation.get('errors', [])}")
        """
        self.session._ensure_valid_token()
        
        endpoint = f"/api/v1/intel/{self.module_type}/validate"
        response = self.client.post(endpoint, data=self._prepare_api_params())
        return response
    
    def estimate(self) -> Dict[str, Any]:
        """Estimate runtime based on input size.
        
        Returns:
            Estimation result with estimated time and details
            
        Example:
            >>> estimation = tool.estimate()
            >>> print(f"Estimated time: {estimation['estimated_time_minutes']} minutes")
        """
        self.session._ensure_valid_token()
        
        endpoint = f"/api/v1/intel/{self.module_type}/estimate"
        response = self.client.post(endpoint, data=self._prepare_api_params())
        return response
    
    def run(self, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the analysis workflow.
        
        Args:
            additional_params: Optional runtime parameters beyond those provided
                in the constructor
        
        Returns:
            Job submission result with job_id and status
            
        Example:
            >>> result = tool.run()
            >>> print(f"Job ID: {result['job_id']}")
            >>> print(f"Status: {result['status']}")
        """
        self.session._ensure_valid_token()
        
        endpoint = f"/api/v1/intel/{self.module_type}/run"
        
        # Prepare run parameters including any additional ones
        run_params = self._prepare_api_params()
        if additional_params:
            run_params["additional_params"] = additional_params
        
        response = self.client.post(endpoint, data=run_params)
        return response
    
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(module_type='{self.module_type}', output_path='{self.output_path}')"