"""
HTTP Client for Contexere Query API
"""

from typing import Optional, Dict, Any
from contexere.config import get_config

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class QueryClientError(Exception):
    """Error from query client"""
    pass


class QueryClient:
    """HTTP client for query endpoints"""

    def __init__(self, timeout: float = 30.0):
        """
        Initialize query client.

        Args:
            timeout: Request timeout in seconds (default 30s for reads)
        """
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        config = get_config()
        if not config.api_key:
            raise QueryClientError("Contexere not initialized. Call contexere.init() first.")
        return {
            "x-contexere-api-key": config.api_key,
            "Content-Type": "application/json"
        }

    def _get_base_url(self) -> str:
        """Get base URL from config"""
        config = get_config()
        return config.endpoint

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to query endpoint.

        Args:
            path: API path (e.g., "/query/agents")
            params: Query parameters

        Returns:
            Response JSON as dict

        Raises:
            QueryClientError: On request failure
        """
        if not HAS_HTTPX:
            raise QueryClientError("httpx is required for query operations. Install with: pip install httpx")

        url = f"{self._get_base_url()}{path}"
        headers = self._get_headers()

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise QueryClientError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise QueryClientError(f"Request failed: {str(e)}")

    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request to query endpoint.

        Args:
            path: API path
            data: Request body

        Returns:
            Response JSON as dict

        Raises:
            QueryClientError: On request failure
        """
        if not HAS_HTTPX:
            raise QueryClientError("httpx is required for query operations. Install with: pip install httpx")

        url = f"{self._get_base_url()}{path}"
        headers = self._get_headers()

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise QueryClientError(f"HTTP {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise QueryClientError(f"Request failed: {str(e)}")
