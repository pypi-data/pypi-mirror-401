"""never_primp - High-performance Python HTTP client with browser impersonation.

Based on wreq/wreq-util, optimized for high-concurrency web scraping and reverse engineering.
"""

from __future__ import annotations

import asyncio
import sys
from functools import partial
from typing import TYPE_CHECKING, Literal, TypedDict

if sys.version_info >= (3, 11):
    from typing import Unpack
else:
    from typing_extensions import Unpack

# Import Rust implementations
from .never_primp import RClient, Response

# Type definitions
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

# Browser types for type hinting
IMPERSONATE = Literal[
    # Chrome versions
    "chrome_100", "chrome_101", "chrome_104", "chrome_105", "chrome_106",
    "chrome_107", "chrome_108", "chrome_109", "chrome_110", "chrome_114",
    "chrome_116", "chrome_117", "chrome_118", "chrome_119", "chrome_120",
    "chrome_123", "chrome_124", "chrome_126", "chrome_127", "chrome_128",
    "chrome_129", "chrome_130", "chrome_131", "chrome_132", "chrome_133",
    "chrome_134", "chrome_135", "chrome_136", "chrome_137", "chrome_138",
    "chrome_139", "chrome_140", "chrome_141", "chrome_142", "chrome_143",
    # Edge versions
    "edge_101", "edge_122", "edge_127", "edge_131", "edge_134", "edge_135",
    "edge_136", "edge_137", "edge_138", "edge_139", "edge_140", "edge_141",
    "edge_142",
    # Opera versions
    "opera_116", "opera_117", "opera_118", "opera_119",
    # Safari versions
    "safari_15.3", "safari_15.5", "safari_15.6.1", "safari_16", "safari_16.5",
    "safari_17.0", "safari_17.2.1", "safari_17.4.1", "safari_17.5", "safari_17.6",
    "safari_18", "safari_18.2", "safari_18.3", "safari_18.3.1", "safari_18.5",
    "safari_26", "safari_26.1", "safari_26.2",
    # Safari iOS versions
    "safari_ios_16.5", "safari_ios_17.2", "safari_ios_17.4.1", "safari_ios_18.1.1",
    "safari_ios_26", "safari_ios_26.2",
    # Safari iPad versions
    "safari_ipad_18", "safari_ipad_26", "safari_ipad_26.2",
    # Firefox versions
    "firefox_109", "firefox_117", "firefox_128", "firefox_133", "firefox_135",
    "firefox_136", "firefox_139", "firefox_142", "firefox_143", "firefox_144",
    "firefox_145", "firefox_146",
    # Firefox Private/Android versions
    "firefox_private_135", "firefox_private_136", "firefox_android_135",
    # OkHttp versions
    "okhttp_3.9", "okhttp_3.11", "okhttp_3.13", "okhttp_3.14",
    "okhttp_4.9", "okhttp_4.10", "okhttp_4.12", "okhttp_5",
    # Generic browser names (latest versions)
    "chrome", "firefox", "safari", "edge", "opera", "okhttp",
]

IMPERSONATE_OS = Literal["windows", "macos", "linux", "android", "ios"]


# Request parameters TypedDict for type hints
class RequestParams(TypedDict, total=False):
    """Type definition for request-level parameters.

    These parameters can be passed to individual requests to override
    client-level settings or add request-specific configuration.
    """
    params: dict[str, str]
    """Query parameters to append to the URL"""

    headers: dict[str, str]
    """HTTP headers to send with the request"""

    cookies: dict[str, str]
    """Cookies to send with the request"""

    json: any
    """JSON data to send in request body (will be serialized to JSON)"""

    data: dict[str, str] | bytes | str
    """Form data to send in request body. Can be dict (form-encoded), bytes, or string"""

    content: bytes
    """Raw bytes content to send in request body"""

    files: dict[str, str]
    """Files to upload (multipart/form-data). Map of field name to file path"""

    timeout: float
    """Request-specific timeout in seconds"""

    read_timeout: float
    """Read timeout in seconds (time to wait for response data)"""

    proxy: str
    """Request-specific proxy URL"""

    auth: tuple[str, str | None]
    """Basic authentication (username, password)"""

    auth_bearer: str
    """Bearer token authentication"""

    impersonate: IMPERSONATE
    """Browser to impersonate for this request"""

    impersonate_os: IMPERSONATE_OS
    """OS to impersonate for this request"""

    verify: bool
    """Verify SSL certificates for this request"""

    ca_cert_file: str
    """Path to CA certificate file for this request"""

    follow_redirects: bool
    """Follow redirects for this request"""

    max_redirects: int
    """Maximum redirects for this request"""

    https_only: bool
    """Restrict to HTTPS only for this request"""

    http1_only: bool
    """Force HTTP/1.1 for this request"""

    http2_only: bool
    """Force HTTP/2 for this request"""

    split_cookies: bool
    """Send cookies in separate headers (HTTP/2 style)"""


class Client:
    """
    Synchronous HTTP client with browser impersonation capabilities.

    This client wraps the Rust-based RClient with a more Pythonic interface,
    adding context manager support and comprehensive documentation.

    Optimized for high-concurrency web scraping with:
    - Connection pool: 512 connections per host
    - Multi-threaded Tokio runtime (4 workers)
    - GIL-free async I/O operations
    - 100+ browser fingerprint profiles

    Example:
        >>> client = Client(impersonate="chrome", timeout=30.0)
        >>> response = client.get("https://httpbin.org/get")
        >>> print(response.json())

        >>> # Using context manager
        >>> with Client(impersonate="firefox") as client:
        ...     response = client.get("https://example.com")
        ...     print(response.status_code)
    """

    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookie_store: bool = True,
        referer: bool = True,
        proxy: str | None = None,
        timeout: float | None = None,
        impersonate: IMPERSONATE | None = None,
        impersonate_os: IMPERSONATE_OS | None = None,
        follow_redirects: bool = True,
        max_redirects: int = 20,
        verify: bool = True,
        ca_cert_file: str | None = None,
        https_only: bool = False,
        http1_only: bool = False,
        http2_only: bool = False,
        split_cookies: bool | None = True,
    ):
        """
        Initialize HTTP client with browser impersonation.

        Args:
            auth: Tuple of (username, password) for basic authentication. Default is None.
            auth_bearer: Bearer token for authentication. Default is None.
            params: Default query parameters to append to all URLs. Default is None.
            headers: Default HTTP headers to send with all requests. Default is None.
            cookie_store: Enable persistent cookie storage. Cookies will be preserved
                across requests. Default is True.
            referer: Auto-set Referer header. Default is True.
            proxy: Proxy URL (e.g., "http://127.0.0.1:8080", "socks5://127.0.0.1:1080").
                Default is None.
            timeout: Request timeout in seconds. Default is None (no timeout).
            impersonate: Browser to impersonate. Supported browsers include:
                - Chrome: "chrome_100" through "chrome_143", or "chrome" for latest
                - Firefox: "firefox_109" through "firefox_146", or "firefox" for latest
                - Safari: "safari_15.3" through "safari_26.2", or "safari" for latest
                - Edge: "edge_101" through "edge_142", or "edge" for latest
                - Opera: "opera_116" through "opera_119", or "opera" for latest
                - OkHttp: "okhttp_3.9" through "okhttp_5", or "okhttp" for latest
                Default is None (no impersonation).
            impersonate_os: Operating system to impersonate. Supported:
                "windows", "macos", "linux", "android", "ios". Default is None.
            follow_redirects: Enable automatic redirect following. Default is True.
            max_redirects: Maximum number of redirects to follow. Default is 20.
            verify: Verify SSL certificates. Set to False to disable verification.
                Default is True.
            ca_cert_file: Path to CA certificate file. Default is None.
            https_only: Restrict to HTTPS only requests. Default is False.
            http1_only: Force HTTP/1.1 only. Default is False.
            http2_only: Force HTTP/2 only. Default is False.
            split_cookies: Send cookies in separate Cookie headers (HTTP/2 style).
                If False, combine cookies in one header (HTTP/1.1 style).
                Default is None (auto-detect based on protocol).

        Example:
            >>> # Basic client
            >>> client = Client()

            >>> # Chrome impersonation with proxy
            >>> client = Client(
            ...     impersonate="chrome_143",
            ...     impersonate_os="windows",
            ...     proxy="http://127.0.0.1:8080",
            ...     timeout=30.0
            ... )

            >>> # Firefox with custom headers and HTTP/2
            >>> client = Client(
            ...     impersonate="firefox",
            ...     headers={"X-Custom-Header": "value"},
            ...     http2_only=True,
            ...     split_cookies=True
            ... )
        """
        self._client = RClient(
            auth=auth,
            auth_bearer=auth_bearer,
            params=params,
            headers=headers,
            cookie_store=cookie_store,
            referer=referer,
            proxy=proxy,
            timeout=timeout,
            impersonate=impersonate,
            impersonate_os=impersonate_os,
            follow_redirects=follow_redirects,
            max_redirects=max_redirects,
            verify=verify,
            ca_cert_file=ca_cert_file,
            https_only=https_only,
            http1_only=http1_only,
            http2_only=http2_only,
            split_cookies=split_cookies,
        )

    def __enter__(self) -> Client:
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        pass

    def get_cookie(self, name: str, url: str) -> str | None:
        """
        Get a specific cookie by name for a URL.

        Args:
            name: Cookie name
            url: URL to get cookie for

        Returns:
            Cookie value or None if not found

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookie("session", "abc123", "https://example.com")
            >>> value = client.get_cookie("session", "https://example.com")
            >>> print(value)  # "abc123"
        """
        return self._client.get_cookie(name, url)

    def get_cookies(self, url: str) -> dict[str, str]:
        """
        Get all cookies for a specific URL.

        Args:
            url: URL to get cookies for

        Returns:
            Dictionary of cookie name-value pairs

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.get("https://httpbin.org/cookies/set?session=abc123")
            >>> cookies = client.get_cookies("https://httpbin.org")
            >>> print(cookies)
        """
        return self._client.get_cookies(url)

    def set_cookie(
        self,
        name: str,
        value: str,
        url: str,
        domain: str | None = None,
        path: str | None = None,
    ) -> None:
        """
        Set a cookie for a specific URL.

        Args:
            name: Cookie name
            value: Cookie value
            url: URL to set cookie for
            domain: Optional domain attribute
            path: Optional path attribute

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookie("session", "abc123", "https://example.com")
            >>> client.set_cookie("user_id", "456", "https://example.com",
            ...                   domain=".example.com", path="/")
        """
        self._client.set_cookie(name, value, url, domain, path)

    def set_cookies(self, url: str, cookies: dict[str, str]) -> None:
        """
        Set multiple cookies for a specific URL.

        Args:
            url: URL to set cookies for
            cookies: Dictionary of cookie name-value pairs

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookies("https://example.com", {
            ...     "session": "abc123",
            ...     "user_id": "456"
            ... })
        """
        self._client.set_cookies(url, cookies)

    def remove_cookie(self, name: str, url: str) -> None:
        """
        Remove a cookie by name for a specific URL.

        Args:
            name: Cookie name to remove
            url: URL to remove cookie for

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookie("session", "abc123", "https://example.com")
            >>> client.remove_cookie("session", "https://example.com")
        """
        self._client.remove_cookie(name, url)

    def clear_cookies(self) -> None:
        """
        Clear all cookies from the cookie store.

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookies("https://example.com", {"a": "1", "b": "2"})
            >>> client.clear_cookies()
        """
        self._client.clear_cookies()

    def get_all_cookies(self) -> list[tuple[str, str]]:
        """
        Get all cookies in the jar (across all domains).

        Returns:
            List of (name, value) tuples

        Example:
            >>> client = Client(cookie_store=True)
            >>> client.set_cookies("https://example.com", {"a": "1", "b": "2"})
            >>> all_cookies = client.get_all_cookies()
            >>> print(all_cookies)  # [('a', '1'), ('b', '2')]
        """
        return self._client.get_all_cookies()

    # ===== Property Accessors for Client Configuration =====

    @property
    def proxy(self) -> str | None:
        """
        Get or set the proxy URL.

        Example:
            >>> client = Client()
            >>> client.proxy = "http://127.0.0.1:8080"
            >>> print(client.proxy)  # "http://127.0.0.1:8080"
        """
        return self._client.proxy

    @proxy.setter
    def proxy(self, value: str | None) -> None:
        """Set proxy URL."""
        self._client.proxy = value

    @property
    def headers(self) -> dict[str, str]:
        """
        Get or set client-level headers.

        These headers will be sent with all requests unless overridden
        at the request level.

        Example:
            >>> client = Client()
            >>> client.headers = {"User-Agent": "MyBot/1.0", "Accept": "application/json"}
            >>> print(client.headers)
            >>> # Update a single header
            >>> headers = client.headers
            >>> headers["X-Custom"] = "value"
            >>> client.headers = headers
        """
        return self._client.get_headers()

    @headers.setter
    def headers(self, value: dict[str, str] | None) -> None:
        """Set client-level headers (replaces all existing headers)."""
        self._client.set_headers(value)

    @property
    def auth(self) -> tuple[str, str | None] | None:
        """
        Get or set basic authentication credentials.

        Example:
            >>> client = Client()
            >>> client.auth = ("username", "password")
            >>> print(client.auth)  # ("username", "password")
        """
        return self._client.auth

    @auth.setter
    def auth(self, value: tuple[str, str | None] | None) -> None:
        """Set basic authentication."""
        self._client.auth = value

    @property
    def auth_bearer(self) -> str | None:
        """
        Get or set bearer token authentication.

        Example:
            >>> client = Client()
            >>> client.auth_bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            >>> print(client.auth_bearer)
        """
        return self._client.auth_bearer

    @auth_bearer.setter
    def auth_bearer(self, value: str | None) -> None:
        """Set bearer token."""
        self._client.auth_bearer = value

    @property
    def params(self) -> dict[str, str] | None:
        """
        Get or set default query parameters.

        These parameters will be appended to all request URLs.

        Example:
            >>> client = Client()
            >>> client.params = {"api_key": "secret123", "format": "json"}
            >>> # This will request: https://api.example.com/data?api_key=secret123&format=json
            >>> response = client.get("https://api.example.com/data")
        """
        return self._client.params

    @params.setter
    def params(self, value: dict[str, str] | None) -> None:
        """Set default query parameters."""
        self._client.params = value

    @property
    def timeout(self) -> float | None:
        """
        Get or set request timeout in seconds.

        Example:
            >>> client = Client()
            >>> client.timeout = 30.0
            >>> print(client.timeout)  # 30.0
        """
        return self._client.timeout

    @timeout.setter
    def timeout(self, value: float | None) -> None:
        """Set timeout."""
        self._client.timeout = value

    @property
    def split_cookies(self) -> bool | None:
        """
        Get or set cookie splitting behavior.

        - True: Send each cookie in a separate Cookie header (HTTP/2 style)
        - False: Combine all cookies in one Cookie header (HTTP/1.1 style)
        - None: Auto-detect based on protocol

        Example:
            >>> client = Client()
            >>> client.split_cookies = True  # HTTP/2 style
            >>> print(client.split_cookies)  # True
        """
        return self._client.split_cookies

    @split_cookies.setter
    def split_cookies(self, value: bool | None) -> None:
        """Set cookie splitting behavior."""
        self._client.split_cookies = value

    @property
    def impersonate(self) -> str | None:
        """
        Get browser impersonation setting (read-only).

        To change browser impersonation, create a new client.

        Example:
            >>> client = Client(impersonate="chrome_143")
            >>> print(client.impersonate)  # "chrome_143"
        """
        return self._client.impersonate

    @property
    def impersonate_os(self) -> str | None:
        """
        Get OS impersonation setting (read-only).

        To change OS impersonation, create a new client.

        Example:
            >>> client = Client(impersonate_os="windows")
            >>> print(client.impersonate_os)  # "windows"
        """
        return self._client.impersonate_os

    # ===== Header Management Methods =====

    def get_header(self, name: str) -> str | None:
        """
        Get a single header value by name.

        Args:
            name: Header name

        Returns:
            Header value or None if not found

        Example:
            >>> client = Client(headers={"User-Agent": "MyBot/1.0"})
            >>> print(client.get_header("User-Agent"))  # "MyBot/1.0"
        """
        return self._client.get_header(name)

    def set_header(self, name: str, value: str) -> None:
        """
        Set a single header.

        Args:
            name: Header name
            value: Header value

        Example:
            >>> client = Client()
            >>> client.set_header("User-Agent", "MyBot/1.0")
            >>> client.set_header("Accept", "application/json")
        """
        self._client.set_header(name, value)

    def update_headers(self, headers: dict[str, str]) -> None:
        """
        Update headers (merges with existing headers).

        Args:
            headers: Dictionary of headers to add/update

        Example:
            >>> client = Client(headers={"User-Agent": "MyBot/1.0"})
            >>> client.update_headers({"Accept": "application/json", "X-Custom": "value"})
            >>> # Client now has all three headers
        """
        self._client.headers_update(headers)

    def delete_header(self, name: str) -> None:
        """
        Delete a single header by name.

        Args:
            name: Header name to remove

        Example:
            >>> client = Client(headers={"User-Agent": "MyBot/1.0"})
            >>> client.delete_header("User-Agent")
        """
        self._client.delete_header(name)

    def clear_headers(self) -> None:
        """
        Clear all client-level headers.

        Example:
            >>> client = Client(headers={"User-Agent": "MyBot/1.0", "Accept": "application/json"})
            >>> client.clear_headers()
            >>> print(client.headers)  # {}
        """
        self._client.clear_headers()

    def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a GET request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters (params, headers, cookies, etc.)

        Returns:
            Response object containing server response.

        Example:
            >>> client = Client(impersonate="chrome")
            >>> response = client.get("https://httpbin.org/get")
            >>> print(response.status_code)  # 200

            >>> # With request-level parameters
            >>> response = client.get(
            ...     "https://httpbin.org/get",
            ...     headers={"User-Agent": "Custom"},
            ...     params={"key": "value"}
            ... )
        """
        return self._client.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a POST request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters (json, data, headers, etc.)

        Returns:
            Response object.

        Example:
            >>> client = Client()
            >>> # Send JSON data
            >>> response = client.post(
            ...     "https://httpbin.org/post",
            ...     json={"key": "value"}
            ... )

            >>> # Send form data
            >>> response = client.post(
            ...     "https://httpbin.org/post",
            ...     data={"username": "user", "password": "pass"}
            ... )

            >>> # Send raw bytes
            >>> response = client.post(
            ...     "https://httpbin.org/post",
            ...     content=b"raw bytes data"
            ... )
        """
        return self._client.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a PUT request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object.

        Example:
            >>> response = client.put(
            ...     "https://httpbin.org/put",
            ...     json={"updated": "data"}
            ... )
        """
        return self._client.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a DELETE request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object.

        Example:
            >>> response = client.delete("https://httpbin.org/delete")
        """
        return self._client.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a PATCH request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object.

        Example:
            >>> response = client.patch(
            ...     "https://httpbin.org/patch",
            ...     json={"field": "new_value"}
            ... )
        """
        return self._client.request("PATCH", url, **kwargs)

    def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send a HEAD request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object (no body content).

        Example:
            >>> response = client.head("https://httpbin.org/get")
            >>> print(response.headers)
        """
        return self._client.request("HEAD", url, **kwargs)

    def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Send an OPTIONS request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object.

        Example:
            >>> response = client.options("https://httpbin.org/get")
            >>> print(response.headers.get("Allow"))
        """
        return self._client.request("OPTIONS", url, **kwargs)


class AsyncClient(Client):
    """
    Asynchronous HTTP client with browser impersonation capabilities.

    Wraps the synchronous Client with asyncio support using run_in_executor.
    Provides the same browser impersonation and connection pooling benefits
    as the synchronous client, but with async/await syntax.

    Note: This is a wrapper around the synchronous client using threading.
    For true async I/O, consider using the synchronous client with multiple
    threads via ThreadPoolExecutor.

    Example:
        >>> import asyncio
        >>>
        >>> async def main():
        ...     async with AsyncClient(impersonate="chrome") as client:
        ...         response = await client.get("https://httpbin.org/get")
        ...         print(response.json())
        ...
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookie_store: bool = True,
        referer: bool = True,
        proxy: str | None = None,
        timeout: float | None = None,
        impersonate: IMPERSONATE | None = None,
        impersonate_os: IMPERSONATE_OS | None = None,
        follow_redirects: bool = True,
        max_redirects: int = 20,
        verify: bool = True,
        ca_cert_file: str | None = None,
        https_only: bool = False,
        http1_only: bool = False,
        http2_only: bool = False,
        split_cookies: bool | None = None,
    ):
        """
        Initialize asynchronous HTTP client.

        Args are the same as the synchronous Client class.
        See Client.__init__ for detailed documentation.
        """
        super().__init__(
            auth=auth,
            auth_bearer=auth_bearer,
            params=params,
            headers=headers,
            cookie_store=cookie_store,
            referer=referer,
            proxy=proxy,
            timeout=timeout,
            impersonate=impersonate,
            impersonate_os=impersonate_os,
            follow_redirects=follow_redirects,
            max_redirects=max_redirects,
            verify=verify,
            ca_cert_file=ca_cert_file,
            https_only=https_only,
            http1_only=http1_only,
            http2_only=http2_only,
            split_cookies=split_cookies,
        )

    async def __aenter__(self) -> AsyncClient:
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit async context manager."""
        pass

    async def _run_sync_asyncio(self, fn, *args, **kwargs):
        """Run synchronous function in executor to make it async."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

    async def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Asynchronously send a GET request.

        Args:
            url: URL to request
            **kwargs: Additional request parameters

        Returns:
            Response object.

        Example:
            >>> async with AsyncClient(impersonate="chrome") as client:
            ...     response = await client.get("https://httpbin.org/get")
            ...     print(response.json())
        """
        return await self._run_sync_asyncio(super().get, url, **kwargs)

    async def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send a POST request."""
        return await self._run_sync_asyncio(super().post, url, **kwargs)

    async def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send a PUT request."""
        return await self._run_sync_asyncio(super().put, url, **kwargs)

    async def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send a DELETE request."""
        return await self._run_sync_asyncio(super().delete, url, **kwargs)

    async def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send a PATCH request."""
        return await self._run_sync_asyncio(super().patch, url, **kwargs)

    async def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send a HEAD request."""
        return await self._run_sync_asyncio(super().head, url, **kwargs)

    async def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """Asynchronously send an OPTIONS request."""
        return await self._run_sync_asyncio(super().options, url, **kwargs)


# Convenience functions - create temporary client for single requests
def get(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """
    Send a GET request using a temporary client.

    Args:
        url: URL to request
        impersonate: Browser to impersonate (optional)
        impersonate_os: OS to impersonate (optional)
        verify: Verify SSL certificates. Default is True
        proxy: Proxy URL (optional)
        timeout: Request timeout in seconds (optional)
        **kwargs: Additional request parameters

    Returns:
        Response object.

    Example:
        >>> import never_primp
        >>> response = never_primp.get("https://httpbin.org/get")
        >>> print(response.json())

        >>> # With browser impersonation
        >>> response = never_primp.get(
        ...     "https://httpbin.org/headers",
        ...     impersonate="chrome",
        ...     timeout=10.0
        ... )
    """
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.get(url, **kwargs)


def post(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send a POST request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.post(url, **kwargs)


def put(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send a PUT request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.put(url, **kwargs)


def delete(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send a DELETE request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.delete(url, **kwargs)


def patch(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send a PATCH request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.patch(url, **kwargs)


def head(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send a HEAD request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.head(url, **kwargs)


def options(
    url: str,
    impersonate: IMPERSONATE | None = None,
    impersonate_os: IMPERSONATE_OS | None = None,
    verify: bool = True,
    proxy: str | None = None,
    timeout: float | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """Send an OPTIONS request using a temporary client."""
    with Client(
        impersonate=impersonate,
        impersonate_os=impersonate_os,
        verify=verify,
        proxy=proxy,
        timeout=timeout,
    ) as client:
        return client.options(url, **kwargs)


# Export public API
__all__ = [
    # Classes
    "Client",
    "AsyncClient",
    "Response",
    # Convenience functions
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "head",
    "options",
    # Types
    "IMPERSONATE",
    "IMPERSONATE_OS",
    "HttpMethod",
    "RequestParams",
]

__version__ = "2.1.8"
