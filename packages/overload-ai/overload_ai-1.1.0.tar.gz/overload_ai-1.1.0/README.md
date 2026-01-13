# Overload AI Client

AI-powered Python bug identification client library.

## Installation

```bash
pip install overload-ai
```

## Usage

```python
from overload_ai import analyze_code

# Analyze code string
code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
"""

bugs = analyze_code(code)
for bug in bugs:
    print(f"{bug['severity']}: {bug['description']}")
```

### File Analysis

You can also analyze Python files directly:

```python
from overload import analyze_code

# Analyze a Python file
bugs = analyze_code("my_script.py")
for bug in bugs:
    print(f"{bug['severity']}: {bug['description']}")
```

## Features

- Detect syntax bugs, runtime exceptions, logic flaws, security vulnerabilities
- Simple API with automatic file/code detection
- Custom timeout and error handling

## Configuration

Set environment variables:

- `OVERLOAD_BASE_URL`: Custom API base URL (default: https://overload-api.onrender.com)
- `OVERLOAD_API_KEY`: API key if required (future feature)

## License

MIT License