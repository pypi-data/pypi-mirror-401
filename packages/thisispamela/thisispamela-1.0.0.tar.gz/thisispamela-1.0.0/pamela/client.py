"""
Pamela B2B API Client for Python
"""

import time
import json
from typing import Optional, Dict, List, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class PamelaClient:
    """Client for Pamela B2B Voice API."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
    ):
        """
        Initialize Pamela client.

        Args:
            api_key: B2B API key (pk_live_xxx or pk_test_xxx)
            base_url: Optional base URL (defaults to https://api.thisispamela.com)
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.thisispamela.com"
        self.base_api_url = f"{self.base_url}/api/b2b/v1"

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API.

        Args:
            method: HTTP method
            endpoint: API endpoint (without base path)
            data: Request body
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_api_url}{endpoint}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def create_call(
        self,
        to: str,
        task: str,
        country: Optional[str] = None,
        locale: Optional[str] = None,
        instructions: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        end_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new call.

        Args:
            to: Destination phone number (E.164 format)
            task: Task description for the call
            country: Optional ISO 3166-1 alpha-2 country code
            locale: Optional locale (e.g., en-US)
            instructions: Optional additional instructions
            metadata: Optional metadata dict
            tools: Optional list of tools
            webhooks: Optional webhook overrides
            end_user_id: Optional end-user ID for marketplace/tenant isolation (privacy/context)

        Returns:
            Call response with id, status, call_session_id, created_at
        """
        data = {
            "to": to,
            "task": task,
        }
        if country:
            data["country"] = country
        if locale:
            data["locale"] = locale
        if instructions:
            data["instructions"] = instructions
        if metadata:
            data["metadata"] = metadata
        if tools:
            data["tools"] = tools
        if webhooks:
            data["webhooks"] = webhooks
        if end_user_id:
            data["end_user_id"] = end_user_id

        return self._request("POST", "/calls", data=data)

    def get_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get call status and details.

        Args:
            call_id: Call ID

        Returns:
            Call status with transcript, summary, etc.
        """
        return self._request("GET", f"/calls/{call_id}")

    def cancel_call(self, call_id: str) -> Dict[str, Any]:
        """
        Cancel an in-progress call.

        Args:
            call_id: Call ID

        Returns:
            Success response
        """
        return self._request("POST", f"/calls/{call_id}/cancel")

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Optional[Dict[str, Any]] = None,
        timeout_ms: int = 30000,
    ) -> Dict[str, Any]:
        """
        Register a tool for the project.

        Args:
            name: Tool name
            description: Tool description
            input_schema: JSON Schema for inputs
            output_schema: Optional JSON Schema for outputs
            timeout_ms: Timeout in milliseconds

        Returns:
            Tool registration response
        """
        data = {
            "tool": {
                "name": name,
                "description": description,
                "input_schema": input_schema,
                "output_schema": output_schema or {},
                "timeout_ms": timeout_ms,
            }
        }
        return self._request("POST", "/tools", data=data)

    def list_calls(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List calls for the authenticated partner/project.

        Args:
            status: Optional filter by status (queued, ringing, in_progress, completed, failed, cancelled)
            limit: Optional limit number of results (default: 50, max: 100)
            offset: Optional offset for pagination
            start_date: Optional start date filter (ISO 8601 format)
            end_date: Optional end date filter (ISO 8601 format)

        Returns:
            Dictionary with calls list and pagination info
        """
        params = {}
        if status:
            params["status"] = status
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("GET", "/calls", params=params)

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all tools for the project.

        Returns:
            List of tool definitions
        """
        return self._request("GET", "/tools")

    def delete_tool(self, tool_id: str) -> Dict[str, Any]:
        """
        Delete (deactivate) a tool.

        Args:
            tool_id: Tool ID

        Returns:
            Success response
        """
        return self._request("DELETE", f"/tools/{tool_id}")

