"""Type stubs for never_primp Rust extension module.

This file provides type hints for IDE auto-completion and static type checking.
"""

from typing import Any, Dict, Optional, Tuple, TypedDict

# Request parameters type definition
class RequestParams(TypedDict, total=False):
    """Request-level parameters that can override client defaults.

    All parameters are optional and will be merged with client-level settings.
    """
    params: Dict[str, str]
    """Query parameters to append to the URL."""

    headers: Dict[str, str]
    """HTTP headers to send with the request."""

    cookies: Dict[str, str]
    """Cookies to send with the request."""

    json: Any
    """JSON-serializable data to send in the request body."""

    data: Dict[str, str]
    """Form data to send (application/x-www-form-urlencoded)."""

    content: bytes | str
    """Raw bytes or string content to send in the request body."""

    timeout: float
    """Request-specific timeout in seconds."""

    proxy: str
    """Request-specific proxy URL."""

class Response:
    """HTTP response object with lazy-loaded content.

    Attributes:
        url: Final URL (after redirects)
        status_code: HTTP status code (e.g., 200, 404)
        content: Raw response body as bytes (lazy-loaded)
        text: Response body as decoded string (lazy-loaded)
        encoding: Detected or specified character encoding
        headers: Response headers as dict
        cookies: Response cookies as dict

    Example:
        >>> response = client.get("https://httpbin.org/get")
        >>> print(response.status_code)
        200
        >>> print(response.text)
        '{"args": {}, "headers": {...}}'
        >>> data = response.json()
        >>> print(data['headers'])
    """

    url: str
    """Final URL after following redirects."""

    status_code: int
    """HTTP status code (200, 404, etc.)."""

    @property
    def content(self) -> bytes:
        """Get raw response body as bytes.

        This property is lazy-loaded and cached after first access.

        Returns:
            Raw response content as bytes.

        Example:
            >>> response = client.get("https://httpbin.org/get")
            >>> raw_bytes = response.content
            >>> print(len(raw_bytes))
            425
        """
        ...

    @property
    def text(self) -> str:
        """Get response body as decoded string.

        Automatically detects encoding from Content-Type header or content.
        This property is lazy-loaded and cached after first access.

        Returns:
            Response content as decoded string.

        Example:
            >>> response = client.get("https://httpbin.org/get")
            >>> html = response.text
            >>> print(html[:100])
        """
        ...

    @property
    def encoding(self) -> Optional[str]:
        """Get detected character encoding.

        Detected from Content-Type header or by analyzing content.
        Common values: 'utf-8', 'iso-8859-1', 'gbk', etc.

        Returns:
            Encoding name or None if not detected.

        Example:
            >>> response = client.get("https://example.com")
            >>> print(response.encoding)
            'utf-8'
        """
        ...

    @property
    def headers(self) -> Dict[str, str]:
        """Get response headers as dictionary.

        Header names are case-insensitive but returned in lowercase.
        This property is lazy-loaded and cached after first access.

        Returns:
            Dictionary of header name to value.

        Example:
            >>> response = client.get("https://httpbin.org/get")
            >>> print(response.headers['content-type'])
            'application/json'
            >>> print(response.headers.keys())
            dict_keys(['date', 'content-type', 'content-length', ...])
        """
        ...

    @property
    def cookies(self) -> Dict[str, str]:
        """Get response cookies as dictionary.

        Extracted from Set-Cookie headers.
        This property is lazy-loaded and cached after first access.

        Returns:
            Dictionary of cookie name to value.

        Example:
            >>> response = client.get("https://httpbin.org/cookies/set?session=abc123")
            >>> print(response.cookies['session'])
            'abc123'
        """
        ...

    def json(self) -> Any:
        """Parse response body as JSON.

        Automatically decodes response text and parses as JSON.
        Supports nested objects, arrays, and all JSON types.

        Returns:
            Parsed JSON data (dict, list, str, int, float, bool, or None).

        Raises:
            ValueError: If response body is not valid JSON.

        Example:
            >>> response = client.get("https://httpbin.org/get")
            >>> data = response.json()
            >>> print(data['headers']['User-Agent'])
            'Mozilla/5.0 ...'

            >>> # Access nested data
            >>> response = client.get("https://api.example.com/users")
            >>> users = response.json()
            >>> for user in users:
            ...     print(user['name'], user['email'])
        """
        ...

class RClient:
    """Low-level HTTP client (Rust implementation).

    This is the Rust-backed client. Use the `Client` class from the main
    module for a more Pythonic interface with context manager support.

    Attributes:
        auth: Basic authentication credentials
        auth_bearer: Bearer token authentication
        params: Default query parameters
        proxy: Proxy URL
        timeout: Request timeout in seconds
        impersonate: Browser to impersonate (read-only)
        impersonate_os: Operating system to impersonate (read-only)
        split_cookies: Cookie splitting behavior
    """

    auth: Optional[Tuple[str, Optional[str]]]
    """Basic authentication (username, password)."""

    auth_bearer: Optional[str]
    """Bearer token authentication."""

    params: Optional[Dict[str, str]]
    """Default query parameters for all requests."""

    proxy: Optional[str]
    """Proxy URL (e.g., 'http://127.0.0.1:8080')."""

    timeout: Optional[float]
    """Request timeout in seconds."""

    impersonate: Optional[str]
    """Browser to impersonate (e.g., 'chrome_143'). Read-only."""

    impersonate_os: Optional[str]
    """Operating system to impersonate (e.g., 'windows'). Read-only."""

    split_cookies: Optional[bool]
    """Send cookies in separate headers (HTTP/2 style) when True."""

    def __init__(
        self,
        auth: Optional[Tuple[str, Optional[str]]] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookie_store: bool = True,
        proxy: Optional[str] = None,
        timeout: Optional[float] = None,
        impersonate: Optional[str] = None,
        impersonate_os: Optional[str] = None,
        follow_redirects: bool = True,
        max_redirects: int = 20,
        verify: bool = True,
    ) -> None:
        """Initialize HTTP client.

        Args:
            auth: Basic authentication (username, password)
            params: Default query parameters
            headers: Default headers
            cookie_store: Enable cookie persistence
            proxy: Proxy URL
            timeout: Request timeout in seconds
            impersonate: Browser to impersonate
            impersonate_os: OS to impersonate
            follow_redirects: Follow redirects
            max_redirects: Maximum redirects
            verify: Verify SSL certificates
        """
        ...

    def get(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP GET request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters (headers, params, cookies, etc.)

        Returns:
            Response object
        """
        ...

    def post(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP POST request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters (json, data, headers, etc.)

        Returns:
            Response object
        """
        ...

    def put(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP PUT request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object
        """
        ...

    def delete(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP DELETE request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object
        """
        ...

    def patch(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP PATCH request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object
        """
        ...

    def head(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP HEAD request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object (no body)
        """
        ...

    def options(self, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP OPTIONS request.

        Args:
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object
        """
        ...

    def request(self, method: str, url: str, **kwargs: RequestParams) -> Response:
        """Send HTTP request with specified method.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            url: Target URL
            **kwargs: Optional request-level parameters

        Returns:
            Response object
        """
        ...

    # Cookie management methods
    def get_cookie(self, name: str, url: str) -> Optional[str]:
        """Get a specific cookie by name for a URL.

        Args:
            name: Cookie name
            url: URL to get cookie for

        Returns:
            Cookie value or None if not found
        """
        ...

    def get_cookies(self, url: str) -> Dict[str, str]:
        """Get all cookies for a specific URL.

        Args:
            url: URL to get cookies for

        Returns:
            Dictionary of cookie name-value pairs
        """
        ...

    def set_cookie(
        self,
        name: str,
        value: str,
        url: str,
        domain: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        """Set a cookie for a specific URL.

        Args:
            name: Cookie name
            value: Cookie value
            url: URL to set cookie for
            domain: Optional domain attribute
            path: Optional path attribute
        """
        ...

    def set_cookies(self, url: str, cookies: Dict[str, str]) -> None:
        """Set multiple cookies for a specific URL.

        Args:
            url: URL to set cookies for
            cookies: Dictionary of cookie name-value pairs
        """
        ...

    def remove_cookie(self, name: str, url: str) -> None:
        """Remove a cookie by name for a specific URL.

        Args:
            name: Cookie name to remove
            url: URL to remove cookie for
        """
        ...

    def clear_cookies(self) -> None:
        """Clear all cookies from the cookie store."""
        ...

    def get_all_cookies(self) -> list[Tuple[str, str]]:
        """Get all cookies in the jar (across all domains).

        Returns:
            List of (name, value) tuples
        """
        ...

    # Header management methods
    def get_headers(self) -> Dict[str, str]:
        """Get all client-level headers.

        Returns:
            Dictionary of header name-value pairs
        """
        ...

    def set_headers(self, headers: Optional[Dict[str, str]]) -> None:
        """Set client-level headers (replaces all existing headers).

        Args:
            headers: Dictionary of header name-value pairs, or None to clear
        """
        ...

    def headers_update(self, headers: Dict[str, str]) -> None:
        """Update client-level headers (merges with existing headers).

        Args:
            headers: Dictionary of headers to add/update
        """
        ...

    def set_header(self, name: str, value: str) -> None:
        """Set a single header.

        Args:
            name: Header name
            value: Header value
        """
        ...

    def get_header(self, name: str) -> Optional[str]:
        """Get a single header value by name.

        Args:
            name: Header name

        Returns:
            Header value or None if not found
        """
        ...

    def delete_header(self, name: str) -> None:
        """Delete a single header by name.

        Args:
            name: Header name to remove
        """
        ...

    def clear_headers(self) -> None:
        """Clear all client-level headers."""
        ...
