"""Demonstration of type hints and IDE auto-completion.

This file showcases the comprehensive type hints provided by never_primp.
When using an IDE like PyCharm, VSCode with Pylance, or other Python IDEs,
you'll get full auto-completion and type checking support.
"""

import never_primp

# Example 1: Basic request with auto-completion
# Type "response." and your IDE will show all available attributes/methods:
# - response.url
# - response.status_code
# - response.content
# - response.text
# - response.encoding
# - response.headers
# - response.cookies
# - response.json()

response = never_primp.get("https://httpbin.org/get", impersonate="chrome")

# Auto-complete should show: url, status_code, content, text, encoding, headers, cookies, json()
print(f"Status: {response.status_code}")  # IDE knows this is int
print(f"URL: {response.url}")  # IDE knows this is str
print(f"Encoding: {response.encoding}")  # IDE knows this is Optional[str]


# Example 2: Response properties with type hints
# Your IDE will show type information for each property

# response.text is str
html_text: str = response.text
print(f"Text length: {len(html_text)}")

# response.content is bytes
raw_bytes: bytes = response.content
print(f"Content length: {len(raw_bytes)}")

# response.headers is Dict[str, str]
headers: dict = response.headers
print(f"Content-Type: {headers.get('content-type', 'unknown')}")

# response.cookies is Dict[str, str]
cookies: dict = response.cookies
print(f"Cookies: {len(cookies)}")


# Example 3: JSON parsing with type hints
json_response = never_primp.get("https://httpbin.org/get")
data = json_response.json()  # IDE knows this returns Any

# You can add your own type hints for parsed JSON
from typing import Any, Dict

parsed_data: Dict[str, Any] = json_response.json()
print(f"Headers from JSON: {parsed_data['headers']}")


# Example 4: Client class with full auto-completion
# When you type "client.", IDE will show all available methods:
# - get, post, put, delete, patch, head, options

with never_primp.Client(
    impersonate="firefox",  # IDE will show all available browser options
    impersonate_os="windows",  # IDE will show: windows, macos, linux, android, ios
    timeout=30.0,
    verify=True,
) as client:
    # Auto-complete for HTTP methods
    resp1 = client.get("https://httpbin.org/get")
    resp2 = client.post("https://httpbin.org/post")
    resp3 = client.put("https://httpbin.org/put")
    resp4 = client.delete("https://httpbin.org/delete")

    # Each response has full type hints
    print(f"GET status: {resp1.status_code}")
    print(f"POST headers: {resp2.headers}")
    print(f"PUT text length: {len(resp3.text)}")
    print(f"DELETE content length: {len(resp4.content)}")


# Example 5: Async client with type hints
import asyncio


async def async_example():
    """Async client also has full type hints."""
    async with never_primp.AsyncClient(impersonate="safari") as client:
        # Auto-complete works with async methods too
        response = await client.get("https://httpbin.org/get")

        # All response properties available
        print(f"Async status: {response.status_code}")
        print(f"Async text: {response.text[:100]}")
        print(f"Async JSON: {response.json()}")


# Example 6: Type checking with literal types
# The IMPERSONATE type uses Literal, so type checkers will warn about invalid values

# This will work (valid browser):
client_chrome = never_primp.Client(impersonate="chrome_143")

# This would show a warning in type checkers (invalid browser):
# client_invalid = never_primp.Client(impersonate="invalid_browser")  # Type error!


# Example 7: Response attribute access patterns
def process_response(resp: never_primp.Response) -> None:
    """Function parameter with type hint."""
    # IDE knows all methods/attributes available on resp
    print(f"Processing {resp.url}")
    print(f"Status: {resp.status_code}")

    # Check status code
    if resp.status_code == 200:
        # Parse JSON if successful
        try:
            data = resp.json()
            print(f"JSON data: {data}")
        except ValueError:
            # Not JSON, use text
            print(f"Text data: {resp.text}")

    # Access headers
    content_type = resp.headers.get("content-type", "")
    if "json" in content_type:
        print("Response is JSON")
    elif "html" in content_type:
        print("Response is HTML")

    # Check cookies
    if resp.cookies:
        print(f"Received {len(resp.cookies)} cookies")


# Run the demo
if __name__ == "__main__":
    print("=" * 60)
    print("Type Hints and Auto-Completion Demo")
    print("=" * 60)
    print()
    print("This demo shows IDE auto-completion support.")
    print("Open this file in your IDE (PyCharm, VSCode, etc.) and")
    print("type 'response.' to see all available methods/properties!")
    print()
    print("=" * 60)
    print()

    # Run basic examples
    response = never_primp.get("https://httpbin.org/get")
    process_response(response)

    print()
    print("Demo completed! Check your IDE for auto-completion support.")
