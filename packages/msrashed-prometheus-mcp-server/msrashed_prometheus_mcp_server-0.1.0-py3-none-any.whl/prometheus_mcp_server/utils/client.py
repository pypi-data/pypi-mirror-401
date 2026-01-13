"""
Prometheus API client.

This module provides a read-only HTTP client for the Prometheus API.
All write operations are blocked by design.
"""

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class PrometheusResponse:
    """Response from Prometheus API."""

    success: bool
    data: dict[str, Any] | list[Any] | None
    error: str | None
    status_code: int
    warnings: list[str] | None = None


class PrometheusClient:
    """
    Read-only Prometheus API client.

    This client only supports GET and specific POST requests
    that are read-only (like queries).

    Authentication:
    - PROM_URL or PROMETHEUS_URL: Prometheus server URL
    - PROM_TOKEN or PROMETHEUS_TOKEN: Bearer token (optional)
    - PROM_USERNAME/PROM_PASSWORD: Basic auth (optional)
    """

    # Endpoints that allow POST but are read-only (query/search)
    ALLOWED_POST_ENDPOINTS = {
        "/api/v1/query",
        "/api/v1/query_range",
        "/api/v1/query_exemplars",
        "/api/v1/series",
        "/api/v1/labels",
    }

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        """
        Initialize Prometheus client.

        Args:
            url: Prometheus server URL (or use PROM_URL env var)
            token: Bearer token for authentication (optional)
            username: Username for basic auth (optional)
            password: Password for basic auth (optional)
            timeout: Request timeout in seconds
            verify_ssl: Verify SSL certificates
        """
        self.url = (
            url
            or os.environ.get("PROM_URL")
            or os.environ.get("PROMETHEUS_URL")
            or "http://localhost:9090"
        )
        self.token = token or os.environ.get("PROM_TOKEN") or os.environ.get("PROMETHEUS_TOKEN")
        self.username = username or os.environ.get("PROM_USERNAME")
        self.password = password or os.environ.get("PROM_PASSWORD")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        # Remove trailing slash
        self.url = self.url.rstrip("/")

        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create HTTP client."""
        if self._client is None:
            headers = {"Content-Type": "application/json"}

            # Add authentication
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            auth = None
            if self.username and self.password:
                auth = (self.username, self.password)

            self._client = httpx.Client(
                base_url=self.url,
                headers=headers,
                auth=auth,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
        return self._client

    def _is_blocked(self, method: str, endpoint: str) -> bool:
        """Check if request is blocked."""
        # Only GET and specific POSTs allowed
        if method == "GET":
            return False

        if method == "POST":
            # Check if it's an allowed read-only POST
            return all(
                not endpoint.startswith(allowed)
                for allowed in self.ALLOWED_POST_ENDPOINTS
            )

        # Block all other methods (PUT, DELETE, PATCH)
        return True

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> PrometheusResponse:
        """
        Make GET request to Prometheus API.

        Args:
            endpoint: API endpoint (e.g., "/api/v1/query")
            params: Query parameters

        Returns:
            PrometheusResponse with data or error
        """
        try:
            response = self.client.get(endpoint, params=params)

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("status") == "success":
                    return PrometheusResponse(
                        success=True,
                        data=json_data.get("data"),
                        error=None,
                        status_code=response.status_code,
                        warnings=json_data.get("warnings"),
                    )
                else:
                    return PrometheusResponse(
                        success=False,
                        data=None,
                        error=json_data.get("error", "Unknown error"),
                        status_code=response.status_code,
                        warnings=json_data.get("warnings"),
                    )
            else:
                error_data = response.json() if response.content else {}
                return PrometheusResponse(
                    success=False,
                    data=None,
                    error=error_data.get("error", response.text),
                    status_code=response.status_code,
                )

        except httpx.TimeoutException:
            return PrometheusResponse(
                success=False,
                data=None,
                error=f"Request timed out after {self.timeout} seconds",
                status_code=0,
            )
        except Exception as e:
            return PrometheusResponse(
                success=False,
                data=None,
                error=str(e),
                status_code=0,
            )

    def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> PrometheusResponse:
        """
        Make POST request for query operations (read-only).

        Args:
            endpoint: API endpoint (must be in ALLOWED_POST_ENDPOINTS)
            data: Form data
            params: Query parameters

        Returns:
            PrometheusResponse with data or error
        """
        if self._is_blocked("POST", endpoint):
            raise ValueError(
                f"POST to {endpoint} is not allowed. "
                f"Only these endpoints support POST: {self.ALLOWED_POST_ENDPOINTS}"
            )

        try:
            response = self.client.post(
                endpoint,
                data=data,
                params=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("status") == "success":
                    return PrometheusResponse(
                        success=True,
                        data=json_data.get("data"),
                        error=None,
                        status_code=response.status_code,
                        warnings=json_data.get("warnings"),
                    )
                else:
                    return PrometheusResponse(
                        success=False,
                        data=None,
                        error=json_data.get("error", "Unknown error"),
                        status_code=response.status_code,
                        warnings=json_data.get("warnings"),
                    )
            else:
                error_data = response.json() if response.content else {}
                return PrometheusResponse(
                    success=False,
                    data=None,
                    error=error_data.get("error", response.text),
                    status_code=response.status_code,
                )

        except httpx.TimeoutException:
            return PrometheusResponse(
                success=False,
                data=None,
                error=f"Request timed out after {self.timeout} seconds",
                status_code=0,
            )
        except Exception as e:
            return PrometheusResponse(
                success=False,
                data=None,
                error=str(e),
                status_code=0,
            )

    def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> "PrometheusClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
