"""
CronGateway Python Client
"""

import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, quote


class CronGatewayClient:
    """
    Official Python client for the CronGateway AI Platform.
    
    CronGateway is a unified API gateway that provides access to multiple AI models
    including OpenAI, Anthropic, Google Gemini, fal.ai, and more.
    
    Example:
        >>> from crongateway import CronGatewayClient
        >>> client = CronGatewayClient(api_key="your-api-key")
        >>> job = client.create_job("flux-pro", {"prompt": "A beautiful sunset"})
        >>> status = client.get_job(job["id"])
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the CronGateway client.
        
        Args:
            api_key: Your CronGateway API key
            base_url: Optional base URL (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url or "https://gateway.croncodestudio.com/api"
        self.session = requests.Session()
        self.session.headers.update({
            "CronCode": api_key,
            "Content-Type": "application/json",
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make an HTTP request to the API."""
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    # Jobs API
    def create_job(self, tool_id: str, input: Dict[str, Any]) -> Dict[Any, Any]:
        """
        Create a new AI job.
        
        Args:
            tool_id: The model ID to use (e.g., "flux-pro", "gemini-2.5-flash-preview")
            input: Input parameters for the model
            
        Returns:
            Job object with ID and status
        """
        return self._request("POST", "/croncode/jobs", json={"toolId": tool_id, "input": input})
    
    def get_job(self, job_id: str) -> Dict[Any, Any]:
        """
        Get job details by ID.
        
        Args:
            job_id: The job ID
            
        Returns:
            Job object with status and results
        """
        return self._request("GET", f"/croncode/jobs/{job_id}")
    
    def list_jobs(self) -> List[Dict[Any, Any]]:
        """
        List all jobs for the authenticated user.
        
        Returns:
            List of job objects
        """
        return self._request("GET", "/croncode/jobs")
    
    # Tools API
    def list_tools(self) -> List[Dict[Any, Any]]:
        """
        List all available AI models/tools.
        
        Returns:
            List of tool objects
        """
        return self._request("GET", "/croncode/tools")
    
    def get_tool(self, tool_id: str) -> Dict[Any, Any]:
        """
        Get a specific tool by ID.
        
        Args:
            tool_id: The tool ID
            
        Returns:
            Tool object with details
        """
        return self._request("GET", f"/croncode/tools/{tool_id}")
    
    def search_tools(self, query: str) -> List[Dict[Any, Any]]:
        """
        Search tools by name or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching tool objects
        """
        return self._request("GET", f"/croncode/tools/search?q={quote(query)}")
    
    def get_tools_by_category(self, category: str) -> List[Dict[Any, Any]]:
        """
        Get tools filtered by category.
        
        Args:
            category: Category name (Text, Image, Video, Audio)
            
        Returns:
            List of tool objects in the category
        """
        return self._request("GET", f"/croncode/tools/category/{category}")
    
    # Storage API
    def list_artifacts(self) -> List[Dict[Any, Any]]:
        """
        List all generated artifacts (images, videos, etc.).
        
        Returns:
            List of artifact objects
        """
        return self._request("GET", "/storage/artifacts")
    
    def upload_file(self, file_path: str) -> Dict[Any, Any]:
        """
        Upload a file to CronGateway storage.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            File object with URL
        """
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(
                urljoin(self.base_url, "/storage/upload"),
                files=files
            )
            response.raise_for_status()
            return response.json()
    
    # Billing API
    def top_up(self, amount: float) -> Dict[Any, Any]:
        """
        Add credits to your account.
        
        Args:
            amount: Amount in USD to add
            
        Returns:
            Transaction object
        """
        return self._request("POST", "/billing/top-up", json={"amount": amount})
    
    def get_billing_history(self) -> List[Dict[Any, Any]]:
        """
        Get billing transaction history.
        
        Returns:
            List of transaction objects
        """
        return self._request("GET", "/billing/history")
    
    def get_usage_stats(self) -> Dict[Any, Any]:
        """
        Get usage analytics and statistics.
        
        Returns:
            Usage statistics object
        """
        return self._request("GET", "/billing/usage")

