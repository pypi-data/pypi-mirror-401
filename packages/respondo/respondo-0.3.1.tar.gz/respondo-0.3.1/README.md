# Respondo

A lightweight Python library for web scraping, text extraction, and AI-powered parsing. Zero external dependencies.

[![PyPI version](https://badge.fury.io/py/respondo.svg)](https://pypi.org/project/respondo/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install respondo
```

## Features

- **Text Extraction** — Extract substrings, regex matches, and structured data
- **HTML Parsing** — Forms, tables, links, and visible text extraction
- **JSON Utilities** — Find embedded JSON, safe traversal, schema validation
- **Response Handling** — Status codes, headers, cookies, charset detection
- **AI Parsing** — 10 LLM providers with structured output support

---

## Quick Start

```python
from respondo import between, extract_links, parse_ai, Response

# Extract text between delimiters
between("<title>Hello World</title>", "<title>", "</title>")
# => "Hello World"

# Parse HTML response
resp = Response(200, {"content-type": "text/html"}, b"<a href='/page'>Link</a>")
extract_links(resp.text, base="https://example.com")
# => ["https://example.com/page"]

# AI-powered extraction
parse_ai("Extract all prices", "Item A: $29.99, Item B: $49.99", provider="openai")
# => "$29.99, $49.99"
```

---

## Text Extraction

```python
from respondo import between, betweens, between_last, between_n

between("Hello [World]!", "[", "]")           # => "World"
betweens("a]x[b]y[c", "[", "]")               # => ["b"]
between_last("[a]x[b]y", "[", "]")            # => "b"
between_n("[a][b][c]", "[", "]", 2)           # => "b" (1-indexed)
```

### Regex

```python
from respondo import regex_first, regex_all

regex_first("Price: $42.99", r"\$[\d.]+")     # => "$42.99"
regex_first("Price: $42.99", r"\$([\d.]+)")   # => "42.99" (capture group)
regex_all("<id>1</id><id>2</id>", r"<id>(\d+)</id>")  # => ["1", "2"]
```

### Text Utilities

```python
from respondo import normalize_space, strip_tags, unescape_html

normalize_space("  hello   world  ")          # => "hello world"
strip_tags("<p>Hello <b>World</b></p>")       # => "Hello World"
unescape_html("&lt;div&gt;")                  # => "<div>"
```

---

## HTML Parsing

```python
from respondo import get_text, extract_links, extract_forms, extract_tables

html = """
<html>
  <body>
    <h1>Welcome</h1>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </body>
</html>
"""

# Extract visible text
get_text(html)  # => "Welcome About Contact"

# Extract links
extract_links(html, base="https://example.com")
# => ["https://example.com/about", "https://example.com/contact"]

# Same-host filtering
extract_links(html, base="https://example.com", same_host=True)

# Extension filtering
extract_links(html, extensions=[".pdf", ".doc"])
```

### Forms

```python
html = '<form action="/login" method="post"><input name="user"><input name="pass" type="password"></form>'

extract_forms(html, base="https://example.com")
# => [{"action": "https://example.com/login", "method": "post", "fields": {"user": "", "pass": ""}}]
```

### Tables

```python
html = "<table><tr><th>Name</th><th>Age</th></tr><tr><td>Alice</td><td>30</td></tr></table>"

extract_tables(html)
# => [{"headers": ["Name", "Age"], "rows": [{"Name": "Alice", "Age": "30"}]}]
```

### CSRF Tokens

```python
from respondo import parse_csrf_token

parse_csrf_token('<input name="csrf_token" value="abc123">')  # => "abc123"
parse_csrf_token('<meta name="csrf-token" content="xyz789">') # => "xyz789"
```

---

## JSON Utilities

```python
from respondo import find_first_json, find_all_json, json_get, json_in_html

# Find JSON in mixed text
find_first_json('callback({"user": "alice", "id": 42})')
# => {"user": "alice", "id": 42}

find_all_json('{"a":1} text {"b":2}')
# => [{"a": 1}, {"b": 2}]

# Safe nested access
data = {"user": {"profile": {"name": "Alice"}}}
json_get(data, "user", "profile", "name")     # => "Alice"
json_get(data, "user", "missing", "key")      # => None

# Array indexing
json_get([{"id": 1}, {"id": 2}], 0, "id")     # => 1

# Extract JSON from HTML
json_in_html('<script type="application/json">{"config": true}</script>')
# => [{"config": true}]
```

---

## Response Handling

```python
from respondo import Response

resp = Response(
    status=200,
    headers={"Content-Type": "application/json; charset=utf-8"},
    body=b'{"success": true}'
)

# Status checks
resp.is_success()        # => True (200-299)
resp.is_redirect()       # => False (300-399)
resp.is_client_error()   # => False (400-499)
resp.is_server_error()   # => False (500-599)

# Body access
resp.body                # => b'{"success": true}'
resp.text                # => '{"success": true}'
resp.json()              # => {"success": True}

# Headers
resp.header("content-type")       # => "application/json; charset=utf-8"
resp.headers_all("set-cookie")    # => ["session=abc", "user=123"]
resp.content_type()               # => ("application/json", "utf-8")

# Hashing
resp.hash()              # => SHA-256 hex digest
resp.hash("md5")         # => MD5 hex digest

# Charset detection
text, charset = resp.charset_sniff()

# Cookie parsing
resp.cookies()
# => [{"name": "session", "value": "abc", "attrs": {"path": "/", "httponly": ""}}]

# HTML shortcuts
resp.extract_links(base="https://example.com")
resp.extract_json()
resp.strip_scripts_styles()
```

---

## Encoding Utilities

```python
from respondo import url_encode, url_decode, b64_encode, b64_decode

# URL encoding
url_encode({"q": "hello world", "page": 1})   # => "q=hello+world&page=1"
url_encode({"tags": ["a", "b"]})              # => "tags=a&tags=b"

# URL decoding
url_decode("a=1&b=2&b=3")                     # => {"a": ["1"], "b": ["2", "3"]}

# Base64
b64_encode("hello")                           # => "aGVsbG8="
b64_decode("aGVsbG8=")                        # => b"hello"

# URL-safe Base64
b64_encode("data", urlsafe=True)
b64_decode("ZGF0YQ", urlsafe=True)
```

---

## AI Parsing

Parse text using LLM APIs. Supports 10 providers with structured output.

```python
from respondo import parse_ai, parse_ai_json, list_providers

# List available providers
list_providers()
# => {"openai": "gpt-4o-mini", "anthropic": "claude-3-5-haiku-latest", ...}

# Basic extraction
parse_ai("Extract all email addresses", "Contact: alice@example.com", provider="openai")
# => "alice@example.com"

# Custom model
parse_ai("Summarize this text", article, provider="anthropic", model="claude-3-5-sonnet-latest")

# JSON response
parse_ai_json("Extract name and age", "John is 30 years old", provider="openai")
# => {"name": "John", "age": 30}

# Structured output with schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string"}
    },
    "required": ["name", "age"],
    "additionalProperties": False
}
parse_ai_json("Extract person data", text, provider="openai", schema=schema)
# => {"name": "John", "age": 30, "email": "john@example.com"}
```

### Supported Providers

| Provider | Environment Variable | Default Model |
|----------|---------------------|---------------|
| `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| `anthropic` | `ANTHROPIC_API_KEY` | `claude-3-5-haiku-latest` |
| `gemini` | `GEMINI_API_KEY` | `gemini-2.0-flash` |
| `grok` | `GROK_API_KEY` | `grok-2-latest` |
| `mistral` | `MISTRAL_API_KEY` | `mistral-small-latest` |
| `groq` | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| `cohere` | `COHERE_API_KEY` | `command-r` |
| `together` | `TOGETHER_API_KEY` | `meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| `deepseek` | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| `perplexity` | `PERPLEXITY_API_KEY` | `sonar` |

---

## Error Handling

All functions return empty values instead of raising exceptions:

```python
between("no match", "<", ">")      # => ""
find_first_json("not json")        # => None
regex_first("abc", r"\d+")         # => ""
json_get({"a": 1}, "b", "c")       # => None
b64_decode("invalid!!!")           # => b""
parse_ai("prompt", "text")         # => "" (if no API key)
```

---

## License

MIT
