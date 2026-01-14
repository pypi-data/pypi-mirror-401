"""
Demo script for header management and property access in never_primp.

This example demonstrates:
1. Setting client-level headers via properties
2. Getting/setting individual headers
3. Updating headers
4. Header ordering and override behavior
5. Client-level vs request-level headers
"""

import never_primp


def demo_property_access():
    """Demonstrate property-based access to client settings."""
    print("=" * 60)
    print("Demo 1: Property Access")
    print("=" * 60)

    client = never_primp.Client()

    # Set proxy via property
    client.proxy = "http://127.0.0.1:8080"
    print(f"Proxy set to: {client.proxy}")

    # Set timeout via property
    client.timeout = 30.0
    print(f"Timeout set to: {client.timeout}")

    # Set auth via property
    client.auth = ("username", "password")
    print(f"Auth set to: {client.auth}")

    # Set bearer token
    client.auth_bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    print(f"Bearer token set: {client.auth_bearer[:20]}...")

    # Set params via property
    client.params = {"api_key": "secret123", "format": "json"}
    print(f"Params set to: {client.params}")

    # Set split_cookies
    client.split_cookies = True
    print(f"Split cookies: {client.split_cookies}")

    print()


def demo_header_management():
    """Demonstrate header management methods."""
    print("=" * 60)
    print("Demo 2: Header Management")
    print("=" * 60)

    client = never_primp.Client()

    # Set headers via property
    print("Setting headers via property:")
    client.headers = {
        "User-Agent": "MyBot/1.0",
        "Accept": "application/json",
        "X-Custom-Header": "value1"
    }
    print(f"Headers: {client.headers}")
    print()

    # Get a single header
    print("Get single header:")
    user_agent = client.get_header("User-Agent")
    print(f"User-Agent: {user_agent}")
    print()

    # Set a single header
    print("Set single header:")
    client.set_header("X-Another-Header", "value2")
    print(f"Headers after set_header: {client.headers}")
    print()

    # Update headers (merge)
    print("Update headers (merge):")
    client.update_headers({
        "Accept-Language": "en-US,en;q=0.9",
        "X-Custom-Header": "updated_value"  # Override existing
    })
    print(f"Headers after update: {client.headers}")
    print()

    # Delete a header
    print("Delete header:")
    client.delete_header("X-Another-Header")
    print(f"Headers after delete: {client.headers}")
    print()

    # Clear all headers
    print("Clear all headers:")
    client.clear_headers()
    print(f"Headers after clear: {client.headers}")
    print()


def demo_header_ordering():
    """Demonstrate header ordering (important for anti-detection)."""
    print("=" * 60)
    print("Demo 3: Header Ordering")
    print("=" * 60)

    # Headers are maintained in insertion order (IndexMap)
    client = never_primp.Client()

    # Set headers in specific order
    client.headers = {
        "accept": "text/html,application/xhtml+xml",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
    }

    print("Client-level headers (in order):")
    for key, value in client.headers.items():
        print(f"  {key}: {value[:50]}...")
    print()


def demo_client_vs_request_headers():
    """Demonstrate client-level vs request-level header override."""
    print("=" * 60)
    print("Demo 4: Client vs Request Level Headers")
    print("=" * 60)

    client = never_primp.Client()

    # Set client-level headers
    client.headers = {
        "User-Agent": "ClientBot/1.0",
        "Accept": "application/json",
        "X-Client-Header": "client-value"
    }

    print("Client-level headers:")
    print(f"  {client.headers}")
    print()

    print("When making request with override headers:")
    print("  Request headers: {'User-Agent': 'RequestBot/2.0', 'X-Request-Header': 'request-value'}")
    print()
    print("  Expected behavior:")
    print("    - User-Agent: RequestBot/2.0 (request overrides client)")
    print("    - Accept: application/json (from client)")
    print("    - X-Client-Header: client-value (from client)")
    print("    - X-Request-Header: request-value (from request)")
    print()

    # Note: Actual HTTP request not made in this demo


def demo_cookie_management():
    """Demonstrate cookie split behavior."""
    print("=" * 60)
    print("Demo 5: Cookie Management")
    print("=" * 60)

    client = never_primp.Client(cookie_store=True)

    # HTTP/1.1 style (merged)
    client.split_cookies = False
    print(f"Split cookies (HTTP/1.1 merged): {client.split_cookies}")
    print("  Cookies will be sent as: Cookie: session=abc; user_id=123")
    print()

    # HTTP/2 style (split)
    client.split_cookies = True
    print(f"Split cookies (HTTP/2 separate): {client.split_cookies}")
    print("  Cookies will be sent as:")
    print("    cookie: session=abc")
    print("    cookie: user_id=123")
    print()


def demo_immutable_properties():
    """Demonstrate read-only properties."""
    print("=" * 60)
    print("Demo 6: Read-Only Properties")
    print("=" * 60)

    client = never_primp.Client(
        impersonate="chrome_143",
        impersonate_os="windows"
    )

    print(f"Browser impersonation: {client.impersonate}")
    print(f"OS impersonation: {client.impersonate_os}")
    print()
    print("Note: These properties are read-only.")
    print("To change browser/OS, create a new client instance.")
    print()


if __name__ == "__main__":
    try:
        demo_property_access()
        demo_header_management()
        demo_header_ordering()
        demo_client_vs_request_headers()
        demo_cookie_management()
        demo_immutable_properties()

        print("=" * 60)
        print("All demos completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
