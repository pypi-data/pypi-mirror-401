# IDE Auto-Completion and Type Hints Guide

`never_primp` provides comprehensive type hints and IDE auto-completion support for all its APIs. This guide shows you how to get the most out of IDE features.

## Setup

### 1. Install Type Hint Support

The library includes:
- `never_primp.pyi` - Type stub file for the Rust extension module
- `py.typed` - Marker file indicating this is a typed package
- Full type annotations in `__init__.py`

### 2. IDE Configuration

#### PyCharm
- No additional configuration needed
- Type hints work out of the box
- Press `Ctrl+Space` to trigger auto-completion
- Hover over any method/property to see documentation

#### VSCode with Pylance
1. Install Pylance extension
2. Set Python language server to Pylance in settings:
   ```json
   {
       "python.languageServer": "Pylance"
   }
   ```
3. Press `Ctrl+Space` for auto-completion
4. Hover to see type information

#### Sublime Text with LSP-pyright
1. Install LSP and LSP-pyright packages
2. Auto-completion works automatically

## Available Type Hints

### 1. Client Class

```python
import never_primp

# IDE shows all available parameters with types
client = never_primp.Client(
    impersonate="chrome",          # IDE shows all 100+ browser options
    impersonate_os="windows",       # IDE shows: windows, macos, linux, android, ios
    timeout=30.0,                   # float
    verify=True,                    # bool
    proxy="http://127.0.0.1:8080", # Optional[str]
)

# IDE shows all HTTP methods
response = client.get("https://example.com")    # → Response
response = client.post("https://example.com")   # → Response
response = client.put("https://example.com")    # → Response
response = client.delete("https://example.com") # → Response
response = client.patch("https://example.com")  # → Response
response = client.head("https://example.com")   # → Response
response = client.options("https://example.com")# → Response
```

### 2. Response Object

```python
# All properties have type hints and documentation
response.url          # str - Final URL after redirects
response.status_code  # int - HTTP status code (200, 404, etc.)
response.content      # bytes - Raw response body
response.text         # str - Decoded text response
response.encoding     # Optional[str] - Detected encoding
response.headers      # Dict[str, str] - Response headers
response.cookies      # Dict[str, str] - Response cookies
response.json()       # Any - Parsed JSON data
```

### 3. Convenience Functions

```python
import never_primp

# Module-level functions with full type hints
response = never_primp.get(
    url="https://httpbin.org/get",
    impersonate="chrome",           # Literal type - IDE shows all options
    impersonate_os="windows",       # Literal type - IDE shows all options
    verify=True,
    proxy=None,
    timeout=None,
)

# Same for other HTTP methods
never_primp.post(url, ...)
never_primp.put(url, ...)
never_primp.delete(url, ...)
never_primp.patch(url, ...)
never_primp.head(url, ...)
never_primp.options(url, ...)
```

### 4. AsyncClient

```python
import asyncio
import never_primp

async def main():
    # Async client with same type hints as Client
    async with never_primp.AsyncClient(impersonate="firefox") as client:
        response = await client.get("https://example.com")
        # All Response properties available with type hints
        print(response.status_code)  # IDE knows this is int
        print(response.text)         # IDE knows this is str

asyncio.run(main())
```

## IDE Features

### 1. Auto-Completion

Type any object followed by a dot to see available methods/properties:

```python
import never_primp

response = never_primp.get("https://httpbin.org/get")

# Type "response." and IDE will show:
# - url: str
# - status_code: int
# - content: bytes
# - text: str
# - encoding: Optional[str]
# - headers: Dict[str, str]
# - cookies: Dict[str, str]
# - json() → Any
```

### 2. Parameter Hints

When calling functions, IDE shows parameter types and defaults:

```python
# As you type, IDE shows:
# Client(
#     auth: Optional[Tuple[str, Optional[str]]] = None,
#     params: Optional[Dict[str, str]] = None,
#     headers: Optional[Dict[str, str]] = None,
#     cookie_store: bool = True,
#     proxy: Optional[str] = None,
#     timeout: Optional[float] = None,
#     impersonate: Optional[IMPERSONATE] = None,
#     impersonate_os: Optional[IMPERSONATE_OS] = None,
#     follow_redirects: bool = True,
#     max_redirects: int = 20,
#     verify: bool = True,
# )
client = never_primp.Client(...)
```

### 3. Type Checking with Literal Types

The library uses Literal types for browser and OS parameters. Type checkers will warn about invalid values:

```python
# ✓ Valid - type checker happy
client = never_primp.Client(impersonate="chrome_143")

# ✗ Invalid - type checker shows warning
client = never_primp.Client(impersonate="invalid_browser")
# Error: Argument of type "Literal['invalid_browser']" cannot be assigned to
# parameter "impersonate" of type "IMPERSONATE | None"
```

### 4. Documentation on Hover

Hover over any method or parameter to see full documentation:

```python
response = client.get("https://example.com")
#                 ↑ hover here to see:
# """
# Send HTTP GET request.
#
# Args:
#     url: Target URL
#
# Returns:
#     Response object containing server response.
# """
```

### 5. Go to Definition

Click on any method while holding Ctrl/Cmd to jump to its definition:

```python
response.json()  # Ctrl+Click to see implementation and docs
```

## Type Hints in Your Code

### Adding Type Hints to Your Functions

```python
from typing import Optional, Dict
import never_primp

def fetch_api(
    url: str,
    headers: Optional[Dict[str, str]] = None
) -> Dict:
    """Fetch JSON from API with type hints."""
    with never_primp.Client(headers=headers) as client:
        response: never_primp.Response = client.get(url)
        data: Dict = response.json()
        return data

# IDE knows the return type is Dict
result = fetch_api("https://api.example.com/data")
```

### Type Checking with mypy

Run mypy to catch type errors:

```bash
pip install mypy
mypy your_script.py
```

Example:

```python
import never_primp

# mypy will catch this error:
response = never_primp.get("https://example.com")
code: str = response.status_code  # Error: Incompatible types (int vs str)
```

## Common Patterns

### 1. Checking Response Type

```python
response = never_primp.get("https://httpbin.org/get")

# Type checker knows status_code is int
if response.status_code == 200:
    # Type checker knows json() returns Any
    data = response.json()
    print(data)
elif response.status_code >= 400:
    # Type checker knows text is str
    error_html = response.text
    print(f"Error: {error_html}")
```

### 2. Working with Headers

```python
response = never_primp.get("https://example.com")

# Type checker knows headers is Dict[str, str]
headers: Dict[str, str] = response.headers

# Dict methods available with type hints
content_type: str = headers.get("content-type", "")
if "json" in content_type:
    data = response.json()
```

### 3. Custom Response Handler

```python
from typing import Union, Dict, List

def handle_response(
    response: never_primp.Response
) -> Union[Dict, List, str]:
    """Handle response based on content type."""
    content_type = response.headers.get("content-type", "")

    if "json" in content_type:
        return response.json()  # Returns Any, but we narrow to Dict/List
    else:
        return response.text    # Returns str
```

## IDE-Specific Tips

### PyCharm

- **Quick Documentation**: `Ctrl+Q` (Windows/Linux) or `F1` (Mac)
- **Parameter Info**: `Ctrl+P`
- **Type Info**: `Ctrl+Shift+P`
- **Find Usages**: `Alt+F7`

### VSCode

- **Trigger Suggest**: `Ctrl+Space`
- **Parameter Hints**: `Ctrl+Shift+Space`
- **Show Hover**: Hover with mouse or `Ctrl+K Ctrl+I`
- **Go to Definition**: `F12` or `Ctrl+Click`

### Sublime Text

- **Auto Complete**: `Ctrl+Space`
- **Goto Definition**: `F12`
- **Hover**: Hover with mouse when LSP is active

## Troubleshooting

### Auto-completion Not Working?

1. **Check Python interpreter**: Make sure IDE is using the correct Python environment where `never_primp` is installed

2. **Rebuild index**:
   - PyCharm: File → Invalidate Caches / Restart
   - VSCode: Reload window (`Ctrl+Shift+P` → "Reload Window")

3. **Verify installation**:
   ```python
   import never_primp
   print(never_primp.__file__)  # Should show installed location
   ```

4. **Check for .pyi file**:
   ```bash
   ls -la $(python -c "import never_primp; import os; print(os.path.dirname(never_primp.__file__))")
   # Should see never_primp.pyi and py.typed
   ```

### Type Hints Not Showing?

1. **Update IDE**: Make sure you're using the latest version
2. **Install type checker**: `pip install mypy` or `pip install pyright`
3. **Check language server**: VSCode users should use Pylance for best results

## Examples

See these example files for more:
- `example/type_hints_demo.py` - Complete type hints demo
- `example/response_guide.py` - Response object comprehensive guide
- `example/basic_usage.py` - Basic usage patterns

## Summary

With proper IDE setup, `never_primp` provides:

✓ Auto-completion for all methods and properties
✓ Parameter hints with types and defaults
✓ Inline documentation on hover
✓ Type checking to catch errors before runtime
✓ Go to definition for easy navigation
✓ Literal types for browser/OS validation
✓ Full mypy/pyright compatibility

Enjoy the enhanced developer experience!
