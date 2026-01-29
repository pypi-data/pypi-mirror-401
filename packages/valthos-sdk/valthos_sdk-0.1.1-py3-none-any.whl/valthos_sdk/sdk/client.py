"""HTTP client for Valthos API."""

import os
import requests
from typing import Dict, Any, Optional, BinaryIO
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import APIError, NetworkError, TokenExpiredError, InvalidTokenError, FileUploadError


class HTTPClient:
    """HTTP client with automatic retry and error handling."""
    
    def __init__(self, base_url: str, access_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def set_access_token(self, access_token: str):
        """Update the access token."""
        self.access_token = access_token
    
    def _get_headers(self, include_content_type: bool = True) -> Dict[str, str]:
        """Get default headers for requests."""
        headers = {
            "User-Agent": "valthos-sdk/0.1.0"
        }
        
        if include_content_type:
            headers["Content-Type"] = "application/json"
        
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            if response.status_code == 401:
                raise TokenExpiredError("Token has expired or is invalid")
            elif response.status_code == 403:
                raise InvalidTokenError("Token does not have required permissions")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = {"message": response.text}
                
                # FastAPI uses 'detail', other APIs may use 'message'
                error_msg = error_data.get('detail') or error_data.get('message', 'Unknown error')
                raise APIError(
                    f"API request failed: {error_msg}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during GET {url}: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            # Use longer timeout for intel module runs which may submit many jobs
            timeout = 120 if "/intel/" in endpoint and "/run" in endpoint else 30
            response = self.session.post(
                url,
                json=data,
                headers=self._get_headers(),
                timeout=timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during POST {url}: {str(e)}")
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.put(
                url,
                json=data,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during PUT {url}: {str(e)}")
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.delete(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during DELETE {url}: {str(e)}")
    
    def upload_file(self, endpoint: str, file_path: str, workspace_path: str, **params) -> Dict[str, Any]:
        """Upload a file to the specified endpoint."""
        # Build URL with query parameters (path is a query param for the backend API)
        query_params = {'path': workspace_path}
        query_params.update(params)
        
        # Use proper URL encoding for query parameters
        query_string = urlencode(query_params)
        url = f"{self.base_url}/{endpoint.lstrip('/')}?{query_string}"
        
        if not os.path.exists(file_path):
            raise FileUploadError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
                
                # Don't include Content-Type for multipart uploads
                headers = self._get_headers(include_content_type=False)
                
                response = self.session.post(
                    url,
                    files=files,
                    headers=headers,
                    timeout=300  # 5 minute timeout for file uploads
                )
                return self._handle_response(response)
        except (OSError, IOError) as e:
            raise FileUploadError(f"Error reading file {file_path}: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during file upload to {url}: {str(e)}")