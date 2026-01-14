# Respondo

Scraping-friendly Python library for response parsing, text extraction, and JSON detection. Zero external dependencies—standard library only.

## Installation

```bash
pip install respondo
```

## Quick Example

```python
from respondo import between, find_first_json, extract_links, Response

# Extract text between delimiters
between("<title>Hello World</title>", "<title>", "</title>")
# => "Hello World"

# Find JSON embedded in text
find_first_json('callback({"user": "alice", "id": 42})')
# => {"user": "alice", "id": 42}

# Parse HTTP response
resp = Response(200, {"content-type": "text/html"}, b"<a href='/page'>Link</a>")
resp.is_success()  # => True
extract_links(resp.text, base="https://example.com")
# => ["https://example.com/page"]
```

## Error Handling

**All functions return empty values instead of raising exceptions.** This is intentional for scraping where missing data is expected.

```python
between("no match here", "<a>", "</a>")  # => ""
find_first_json("not json")              # => None
regex_first("abc", r"\d+")               # => ""
b64_decode("invalid!!!")                 # => b""
json_get({"a": 1}, "b", "c")             # => None
```

## API Reference

### Text Extraction

```python
from respondo import between, betweens, between_last, between_n

# First match between delimiters
between("a]x[b]y[c", "[", "]")           # => "b"

# All matches
betweens("a[b]c[d]e", "[", "]")          # => ["b", "d"]

# Last occurrence of left delimiter
between_last("a[b]c[d]e", "[", "]")      # => "d"

# Nth match (1-indexed)
between_n("a[b]c[d]e", "[", "]", 2)      # => "d"
```

### Regex

```python
from respondo import regex_first, regex_all

# First match (returns capture group if present)
regex_first("price: $42.99", r"\$(\d+)")      # => "42"
regex_first("abc123def", r"\d+")              # => "123"

# All matches
regex_all("<a>1</a><a>2</a>", r"<a>(\d+)</a>")  # => ["1", "2"]
```

### HTML Processing

```python
from respondo import (
    strip_tags,
    get_text,
    extract_links,
    extract_forms,
    extract_tables,
    parse_csrf_token,
)

html = """
<html>
  <script>var x=1;</script>
  <body>
    <h1>Title</h1>
    <p>Hello &amp; welcome</p>
    <a href="/page1">Link 1</a>
    <a href="/page2">Link 2</a>
  </body>
</html>
"""

# Strip HTML tags (keeps script/style content)
strip_tags("<b>bold</b> text")           # => "bold text"

# Extract visible text (removes scripts/styles, decodes entities)
get_text(html)                           # => "Title Hello & welcome Link 1 Link 2"

# Extract all links
extract_links(html, base="https://example.com")
# => ["https://example.com/page1", "https://example.com/page2"]

# Filter to same host only
extract_links(html, base="https://example.com", same_host=True)

# Filter by extension
extract_links(html, extensions=[".pdf", ".doc"])

# Extract forms with fields
extract_forms('<form action="/login" method="post"><input name="user"></form>')
# => [{"action": "/login", "method": "post", "fields": {"user": ""}}]

# Extract tables as dicts
extract_tables("<table><tr><th>Name</th></tr><tr><td>Alice</td></tr></table>")
# => [{"headers": ["Name"], "rows": [{"Name": "Alice"}]}]

# Find CSRF tokens
parse_csrf_token('<input name="csrf_token" value="abc123">')  # => "abc123"
parse_csrf_token('<meta name="csrf-token" content="xyz">')    # => "xyz"
```

### JSON Utilities

```python
from respondo import find_first_json, find_all_json, json_get, json_in_html

# Find first valid JSON in text
find_first_json('prefix {"a": 1} middle [1,2,3] suffix')
# => {"a": 1}

# Find all JSON objects/arrays
find_all_json('{"a":1} text [1,2] more {"b":2}')
# => [{"a": 1}, [1, 2], {"b": 2}]

# Safe nested access (returns None if path missing)
data = {"user": {"profile": {"name": "Alice"}}}
json_get(data, "user", "profile", "name")  # => "Alice"
json_get(data, "user", "missing", "key")   # => None

# Array indexing
json_get([{"id": 1}, {"id": 2}], 0, "id")  # => 1

# Extract JSON from HTML script tags
html = '<script type="application/json">{"config": true}</script>'
json_in_html(html)  # => [{"config": true}]
```

### Encoding Utilities

```python
from respondo import url_encode, url_decode, b64_encode, b64_decode

# URL encoding
url_encode({"q": "hello world", "page": 1})  # => "q=hello+world&page=1"
url_encode({"tags": ["a", "b"]})              # => "tags=a&tags=b"

# URL decoding (returns lists for multi-values)
url_decode("a=1&b=2&b=3")  # => {"a": ["1"], "b": ["2", "3"]}

# Base64
b64_encode("hello")           # => "aGVsbG8="
b64_decode("aGVsbG8=")        # => b"hello"

# URL-safe base64
b64_encode("data", urlsafe=True)
b64_decode("ZGF0YQ", urlsafe=True)
```

### Response Class

```python
from respondo import Response

# Create from status, headers, body
resp = Response(
    status=200,
    headers={"Content-Type": "application/json"},
    body=b'{"ok": true}'
)

# Status checks
resp.is_success()       # 200-299
resp.is_redirect()      # 300-399
resp.is_client_error()  # 400-499
resp.is_server_error()  # 500-599

# Headers (case-insensitive)
resp.header("content-type")      # First value: "application/json"
resp.headers_all("set-cookie")   # All values: ["a=1", "b=2"]

# Content type parsing
resp.content_type()  # => ("application/json", "utf-8")

# Body access
resp.body        # Raw bytes
resp.text        # Decoded string (utf-8)
resp.json()      # Parsed JSON

# Hashing
resp.hash()          # SHA-256 of body
resp.hash("md5")     # MD5 of body

# Charset detection (from headers or <meta>)
text, charset = resp.charset_sniff()

# Cookie parsing
resp.cookies()
# => [{"name": "session", "value": "abc", "attrs": {"path": "/", "httponly": ""}}]

# HTML helpers (delegates to htmlutil)
resp.extract_links(base="https://example.com", same_host=True)
resp.extract_json()           # Find JSON in HTML
resp.strip_scripts_styles()   # Clean HTML text
```

## Real-World Examples

### Scrape Hacker News titles

```python
import urllib.request
from respondo import Response, regex_all, normalize_space

req = urllib.request.urlopen("https://news.ycombinator.com")
resp = Response(req.status, dict(req.headers), req.read())

titles = regex_all(resp.text, r'class="titleline"[^>]*><a[^>]*>([^<]+)</a>')
for title in titles[:5]:
    print(normalize_space(title))
```

### Extract data from JSON API

```python
from respondo import Response, json_get

resp = Response(200, {}, b'{"users": [{"name": "Alice"}, {"name": "Bob"}]}')
data = resp.json()

# Safe traversal
first_user = json_get(data, "users", 0, "name")  # => "Alice"
missing = json_get(data, "users", 99, "name")    # => None (no error)
```

### Parse form and submit

```python
from respondo import extract_forms, parse_csrf_token, url_encode

html = '''
<form action="/login" method="post">
  <input name="csrf" value="token123">
  <input name="username">
  <input name="password" type="password">
</form>
'''

forms = extract_forms(html, base="https://example.com")
# => [{"action": "https://example.com/login", "method": "post", "fields": {"csrf": "token123", "username": "", "password": ""}}]

# Or just grab the CSRF token
csrf = parse_csrf_token(html)  # => "token123"
```

## Running Tests

```bash
cd src
python demo_real_sites.py
```

## License

MIT
