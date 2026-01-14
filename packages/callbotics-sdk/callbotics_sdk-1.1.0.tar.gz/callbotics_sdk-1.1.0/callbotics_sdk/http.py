"""
Callbotics SDK HTTP Client.

HTTP client utilities for making API requests.
"""

import json
from typing import Any, BinaryIO, Dict, Optional, Union
from urllib.parse import urljoin

import httpx

from callbotics_sdk.exceptions import (
    AuthenticationError,
    AuthorizationError,
    CallboticsError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)


class HTTPClient:
    """HTTP client for making API requests."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._headers = headers or {}
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    @property
    def headers(self) -> Dict[str, str]:
        """Get current headers."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **self._headers,
        }

    def set_header(self, key: str, value: str) -> None:
        """Set a header value."""
        self._headers[key] = value

    def remove_header(self, key: str) -> None:
        """Remove a header."""
        self._headers.pop(key, None)

    def _get_client(self) -> httpx.Client:
        """Get or create sync HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.headers,
            )
        return self._client

    def _get_async_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.headers,
            )
        return self._async_client

    def _build_url(self, path: str) -> str:
        """Build full URL from path."""
        if path.startswith("http"):
            return path
        return path.lstrip("/")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"message": response.text}

        if response.status_code == 200 or response.status_code == 201:
            return data

        message = data.get("message", data.get("detail", "Unknown error"))

        if response.status_code == 400:
            raise ValidationError(
                message=message,
                status_code=response.status_code,
                response_data=data,
                errors=data.get("errors", []),
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 403:
            raise AuthorizationError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 409:
            raise ConflictError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )
        elif response.status_code == 422:
            raise ValidationError(
                message=message,
                status_code=response.status_code,
                response_data=data,
                errors=data.get("detail", []),
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                message=message,
                status_code=response.status_code,
                response_data=data,
                retry_after=int(retry_after) if retry_after else None,
            )
        elif response.status_code >= 500:
            raise ServerError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )
        else:
            raise CallboticsError(
                message=message,
                status_code=response.status_code,
                response_data=data,
            )

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, BinaryIO]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a synchronous HTTP request."""
        url = self._build_url(path)
        request_headers = {**self.headers, **(headers or {})}

        # Remove Content-Type for file uploads
        if files:
            request_headers.pop("Content-Type", None)

        try:
            client = self._get_client()
            response = client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=data,
                files=files,
                headers=request_headers,
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {e}")
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")

    async def request_async(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, BinaryIO]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an asynchronous HTTP request."""
        url = self._build_url(path)
        request_headers = {**self.headers, **(headers or {})}

        # Remove Content-Type for file uploads
        if files:
            request_headers.pop("Content-Type", None)

        try:
            client = self._get_async_client()
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=data,
                files=files,
                headers=request_headers,
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {e}")
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        return self.request("GET", path, params=params, **kwargs)

    def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return self.request("POST", path, json_data=json_data, **kwargs)

    def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return self.request("PUT", path, json_data=json_data, **kwargs)

    def patch(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self.request("PATCH", path, json_data=json_data, **kwargs)

    def delete(
        self,
        path: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self.request("DELETE", path, **kwargs)

    async def get_async(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make an async GET request."""
        return await self.request_async("GET", path, params=params, **kwargs)

    async def post_async(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make an async POST request."""
        return await self.request_async("POST", path, json_data=json_data, **kwargs)

    async def put_async(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make an async PUT request."""
        return await self.request_async("PUT", path, json_data=json_data, **kwargs)

    async def delete_async(
        self,
        path: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make an async DELETE request."""
        return await self.request_async("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

    async def close_async(self) -> None:
        """Close the async HTTP client."""
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None
