"""SonarQube API client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx


if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class SonarAPIError(Exception):
    """Exception raised for SonarQube API errors.

    Attributes:
        message: Error message.
        status_code: HTTP status code if available.
        response_body: Response body if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        """Initialize SonarAPIError.

        Args:
            message: Error message.
            status_code: HTTP status code.
            response_body: Response body from API.
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class SonarClient:
    """Async HTTP client for SonarQube API.

    This client handles authentication, request building, and response
    parsing for the SonarQube REST API.

    Attributes:
        base_url: Base URL of the SonarQube server.
        organization: Organization key for SonarCloud (optional).
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        organization: str | None = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize SonarClient.

        Args:
            base_url: Base URL of the SonarQube server.
            token: API authentication token.
            organization: Organization key for SonarCloud.
            timeout: Request timeout in seconds.
            verify_ssl: Whether to verify SSL certificates.
        """
        self.base_url = base_url.rstrip("/")
        self._token = token
        self.organization = organization
        self.timeout = timeout
        self._verify_ssl = verify_ssl
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> SonarClient:
        """Enter async context manager."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._build_headers(),
            timeout=self.timeout,
            verify=self._verify_ssl,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for requests.

        Returns:
            Dictionary of HTTP headers.
        """
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }

    def _add_organization(self, params: dict[str, Any] | None) -> dict[str, Any]:
        """Add organization to params if configured.

        Args:
            params: Existing query parameters.

        Returns:
            Updated parameters with organization if applicable.
        """
        if params is None:
            params = {}
        if self.organization and "organization" not in params:
            params["organization"] = self.organization
        return params

    def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized.

        Returns:
            The HTTP client instance.

        Raises:
            RuntimeError: If client is used outside context manager.
        """
        if self._client is None:
            msg = "SonarClient must be used as async context manager"
            raise RuntimeError(msg)
        return self._client

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle error responses from the API.

        Args:
            response: HTTP response object.

        Raises:
            SonarAPIError: If response indicates an error.
        """
        if response.status_code >= 400:
            try:
                body = response.json()
                errors = body.get("errors", [])
                if errors:
                    messages = [e.get("msg", str(e)) for e in errors]
                    message = "; ".join(messages)
                else:
                    message = response.text
            except Exception:
                message = response.text or f"HTTP {response.status_code}"

            raise SonarAPIError(
                message=message,
                status_code=response.status_code,
                response_body=body if "body" in dir() else None,
            )

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a GET request to the API.

        Args:
            path: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response as dictionary.

        Raises:
            SonarAPIError: If request fails.
        """
        client = self._ensure_client()
        params = self._add_organization(params)

        response = await client.get(path, params=params)
        self._handle_error_response(response)

        result: dict[str, Any] = response.json()
        return result

    async def post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the API.

        Args:
            path: API endpoint path.
            data: Form data to send.
            params: Query parameters.

        Returns:
            JSON response as dictionary.

        Raises:
            SonarAPIError: If request fails.
        """
        client = self._ensure_client()
        params = self._add_organization(params)

        response = await client.post(path, data=data, params=params)
        self._handle_error_response(response)

        result: dict[str, Any] = response.json()
        return result

    async def get_paginated(
        self,
        path: str,
        items_key: str,
        params: dict[str, Any] | None = None,
        page_size: int = 100,
        max_results: int | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Iterate over paginated API responses.

        Args:
            path: API endpoint path.
            items_key: Key in response containing items array.
            params: Additional query parameters.
            page_size: Number of items per page.
            max_results: Maximum total items to return.

        Yields:
            Individual items from paginated responses.
        """
        if params is None:
            params = {}

        page = 1
        count = 0

        while True:
            page_params = {**params, "ps": page_size, "p": page}
            response = await self.get(path, params=page_params)

            items = response.get(items_key, [])
            paging = response.get("paging", {})

            for item in items:
                if max_results is not None and count >= max_results:
                    return
                yield item
                count += 1

            # Check if there are more pages
            total = paging.get("total", 0)
            current_page = paging.get("pageIndex", page)
            items_so_far = current_page * page_size

            if items_so_far >= total or not items:
                break

            page += 1
