"""Comprehensive Response object usage examples.

This script demonstrates all properties and methods of the Response object,
with full type hints and IDE auto-completion support.
"""

import never_primp


def demo_response_properties():
    """Demonstrate all Response object properties."""
    print("=" * 70)
    print("Response Properties Demo")
    print("=" * 70)

    # Make a request
    response = never_primp.get("https://httpbin.org/get", impersonate="chrome")

    # 1. url property (str)
    print(f"\n1. URL Property (type: str)")
    print(f"   Final URL: {response.url}")
    print(f"   Type: {type(response.url)}")

    # 2. status_code property (int)
    print(f"\n2. Status Code Property (type: int)")
    print(f"   Status: {response.status_code}")
    print(f"   Type: {type(response.status_code)}")
    print(f"   Is success: {200 <= response.status_code < 300}")

    # 3. content property (bytes) - lazy loaded
    print(f"\n3. Content Property (type: bytes, lazy-loaded)")
    content = response.content
    print(f"   Content length: {len(content)} bytes")
    print(f"   Type: {type(content)}")
    print(f"   First 50 bytes: {content[:50]}")

    # 4. text property (str) - lazy loaded with encoding detection
    print(f"\n4. Text Property (type: str, lazy-loaded)")
    text = response.text
    print(f"   Text length: {len(text)} characters")
    print(f"   Type: {type(text)}")
    print(f"   First 100 chars: {text[:100]}...")

    # 5. encoding property (Optional[str]) - auto-detected
    print(f"\n5. Encoding Property (type: Optional[str])")
    encoding = response.encoding
    print(f"   Detected encoding: {encoding}")
    print(f"   Type: {type(encoding)}")

    # 6. headers property (Dict[str, str]) - lazy loaded
    print(f"\n6. Headers Property (type: Dict[str, str], lazy-loaded)")
    headers = response.headers
    print(f"   Number of headers: {len(headers)}")
    print(f"   Type: {type(headers)}")
    print(f"   Headers:")
    for key, value in headers.items():
        print(f"     {key}: {value}")

    # 7. cookies property (Dict[str, str]) - lazy loaded
    print(f"\n7. Cookies Property (type: Dict[str, str], lazy-loaded)")
    cookies = response.cookies
    print(f"   Number of cookies: {len(cookies)}")
    print(f"   Type: {type(cookies)}")
    if cookies:
        print(f"   Cookies:")
        for name, value in cookies.items():
            print(f"     {name}: {value}")
    else:
        print(f"   No cookies in this response")


def demo_json_method():
    """Demonstrate the json() method."""
    print("\n" + "=" * 70)
    print("Response.json() Method Demo")
    print("=" * 70)

    # Get JSON response
    response = never_primp.get("https://httpbin.org/get", impersonate="firefox")

    # Parse JSON
    print(f"\n1. Parse JSON (returns: Any)")
    data = response.json()
    print(f"   Type: {type(data)}")
    print(f"   Keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")

    # Access nested data
    print(f"\n2. Access nested JSON data")
    if isinstance(data, dict):
        print(f"   URL from JSON: {data.get('url', 'N/A')}")
        print(f"   Headers from JSON: {data.get('headers', {})}")
        print(f"   Args from JSON: {data.get('args', {})}")

    # Handle different JSON types
    print(f"\n3. Different JSON response types")

    # Dictionary response
    dict_response = never_primp.get("https://httpbin.org/get")
    dict_data = dict_response.json()
    print(f"   Dict: {type(dict_data)} with {len(dict_data)} keys")

    # List/array response (example)
    print(f"   JSON can return: dict, list, str, int, float, bool, None")


def demo_header_access():
    """Demonstrate different ways to access headers."""
    print("\n" + "=" * 70)
    print("Header Access Patterns")
    print("=" * 70)

    response = never_primp.get("https://httpbin.org/response-headers?foo=bar")

    headers = response.headers

    # 1. Direct access (KeyError if not exists)
    print(f"\n1. Direct access (headers['key'])")
    try:
        content_type = headers["content-type"]
        print(f"   Content-Type: {content_type}")
    except KeyError as e:
        print(f"   Key not found: {e}")

    # 2. Safe access with get()
    print(f"\n2. Safe access (headers.get('key', default))")
    server = headers.get("server", "Unknown")
    print(f"   Server: {server}")
    custom = headers.get("custom-header", "Not present")
    print(f"   Custom-Header: {custom}")

    # 3. Check if header exists
    print(f"\n3. Check existence (key in headers)")
    print(f"   Has 'content-type': {'content-type' in headers}")
    print(f"   Has 'x-custom': {'x-custom' in headers}")

    # 4. Iterate over all headers
    print(f"\n4. Iterate over headers")
    print(f"   All headers:")
    for name, value in headers.items():
        print(f"     {name}: {value[:50]}..." if len(value) > 50 else f"     {name}: {value}")


def demo_encoding_detection():
    """Demonstrate encoding detection."""
    print("\n" + "=" * 70)
    print("Encoding Detection Demo")
    print("=" * 70)

    # Get a response with specified encoding
    response = never_primp.get("https://httpbin.org/get")

    print(f"\n1. Automatic encoding detection")
    print(f"   Detected encoding: {response.encoding}")
    print(f"   Detection method: From Content-Type header or content analysis")

    # Show how encoding affects text
    print(f"\n2. Text decoding with detected encoding")
    text = response.text
    print(f"   Text is properly decoded: {text[:100]}...")

    # Content-Type header
    content_type = response.headers.get("content-type", "")
    print(f"\n3. Content-Type header")
    print(f"   Content-Type: {content_type}")
    if "charset=" in content_type:
        charset = content_type.split("charset=")[1].split(";")[0].strip()
        print(f"   Charset from header: {charset}")


def demo_cookie_handling():
    """Demonstrate cookie handling."""
    print("\n" + "=" * 70)
    print("Cookie Handling Demo")
    print("=" * 70)

    # Set cookies
    print(f"\n1. Setting cookies via URL")
    response = never_primp.get(
        "https://httpbin.org/cookies/set?session=abc123&user=testuser"
    )

    # Access cookies
    print(f"\n2. Accessing cookies from response")
    cookies = response.cookies
    print(f"   Number of cookies: {len(cookies)}")

    if cookies:
        print(f"   Cookies received:")
        for name, value in cookies.items():
            print(f"     {name}: {value}")

    # Cookie persistence with client
    print(f"\n3. Cookie persistence with Client instance")
    with never_primp.Client(cookie_store=True) as client:
        # First request sets cookie
        resp1 = client.get("https://httpbin.org/cookies/set?persistent=value123")
        print(f"   First request cookies: {resp1.cookies}")

        # Second request should include the cookie
        resp2 = client.get("https://httpbin.org/cookies")
        print(f"   Second request cookies: {resp2.json().get('cookies', {})}")


def demo_error_handling():
    """Demonstrate error handling with responses."""
    print("\n" + "=" * 70)
    print("Error Handling Demo")
    print("=" * 70)

    # 1. Check status code
    print(f"\n1. Check HTTP status code")
    response = never_primp.get("https://httpbin.org/status/404")
    print(f"   Status code: {response.status_code}")
    if response.status_code >= 400:
        print(f"   Error: HTTP {response.status_code}")

    # 2. Handle JSON parse errors
    print(f"\n2. Handle JSON parse errors")
    html_response = never_primp.get("https://httpbin.org/html")
    try:
        data = html_response.json()
    except ValueError as e:
        print(f"   JSON parse error (expected): Response is not JSON")
        print(f"   Using .text instead: {html_response.text[:100]}...")

    # 3. Check content type before parsing
    print(f"\n3. Check content type before parsing")
    response = never_primp.get("https://httpbin.org/get")
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        print(f"   Content is JSON, safe to parse")
        data = response.json()
        print(f"   Parsed successfully: {type(data)}")
    else:
        print(f"   Content is not JSON: {content_type}")


def demo_lazy_loading():
    """Demonstrate lazy loading of properties."""
    print("\n" + "=" * 70)
    print("Lazy Loading Demo")
    print("=" * 70)

    print(f"\n1. Properties are lazy-loaded (computed on first access)")
    response = never_primp.get("https://httpbin.org/get")

    print(f"   Response object created")
    print(f"   url and status_code are available immediately")
    print(f"   - url: {response.url}")
    print(f"   - status_code: {response.status_code}")

    print(f"\n2. content, text, headers, cookies are lazy-loaded")
    print(f"   First access computes and caches the value")

    print(f"   Accessing .text (will decode and cache)...")
    text = response.text
    print(f"   ✓ Text loaded and cached ({len(text)} chars)")

    print(f"   Accessing .text again (returns cached value)...")
    text2 = response.text
    print(f"   ✓ Returned from cache (instant)")

    print(f"\n3. This improves performance:")
    print(f"   - Only compute what you need")
    print(f"   - No overhead if you only check status_code")
    print(f"   - Automatic caching prevents redundant work")


if __name__ == "__main__":
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "never_primp Response Object Guide" + " " * 19 + "║")
    print("║" + " " * 13 + "Complete guide with type hints and examples" + " " * 12 + "║")
    print("╚" + "═" * 68 + "╝")

    # Run all demos
    demo_response_properties()
    demo_json_method()
    demo_header_access()
    demo_encoding_detection()
    demo_cookie_handling()
    demo_error_handling()
    demo_lazy_loading()

    print("\n" + "=" * 70)
    print("All demos completed!")
    print("=" * 70)
    print()
    print("💡 Tips for IDE auto-completion:")
    print("   • Type 'response.' to see all available properties and methods")
    print("   • Hover over properties to see their types")
    print("   • Use Ctrl+Space (or Cmd+Space on Mac) to trigger auto-complete")
    print("   • Type hints work in PyCharm, VSCode, Sublime Text, and more!")
    print()
