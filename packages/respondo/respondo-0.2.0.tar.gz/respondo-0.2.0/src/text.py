import base64
import html
import re
import urllib.parse
from typing import Any, Mapping, Sequence


def between(s: str, left: str, right: str) -> str:
    if not left or not right:
        return ""
    start = s.find(left)
    if start == -1:
        return ""
    start += len(left)
    end = s.find(right, start)
    if end == -1:
        return ""
    return s[start:end]


def betweens(s: str, left: str, right: str) -> list[str]:
    if not left or not right:
        return []
    res: list[str] = []
    pos = 0
    while True:
        start = s.find(left, pos)
        if start == -1:
            break
        start += len(left)
        end = s.find(right, start)
        if end == -1:
            break
        res.append(s[start:end])
        pos = end + len(right)
    return res


def between_last(s: str, left: str, right: str) -> str:
    if not left or not right:
        return ""
    start = s.rfind(left)
    if start == -1:
        return ""
    start += len(left)
    end = s.find(right, start)
    if end == -1:
        return ""
    return s[start:end]


def between_n(s: str, left: str, right: str, n: int) -> str:
    if n < 1:
        return ""
    matches = betweens(s, left, right)
    if n - 1 < len(matches):
        return matches[n - 1]
    return ""


def normalize_space(s: str) -> str:
    return " ".join(s.split())


def strip_tags(html_text: str) -> str:
    cleaned = re.sub(r"<[^>]*>", " ", html_text, flags=re.DOTALL)
    return normalize_space(cleaned)


def unescape_html(s: str) -> str:
    return html.unescape(s)


def regex_first(s: str, pattern: str) -> str:
    try:
        compiled = re.compile(pattern)
    except re.error:
        return ""
    match = compiled.search(s)
    if not match:
        return ""
    if match.groups():
        return match.group(1)
    return match.group(0)


def regex_all(s: str, pattern: str) -> list[str]:
    try:
        compiled = re.compile(pattern)
    except re.error:
        return []
    results: list[str] = []
    for m in compiled.finditer(s):
        if m.groups():
            results.append(m.group(1))
        else:
            results.append(m.group(0))
    return results


def parse_csrf_token(html_text: str) -> str:
    """
    Extracts a CSRF token from common hidden input, meta, or inline script patterns.
    Returns empty string when not found.
    """
    patterns = [
        r'<input[^>]*name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
        r'<input[^>]*name=["\']_csrf["\'][^>]*value=["\']([^"\']+)["\']',
        r'<meta[^>]*name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)["\']',
        r'<meta[^>]*name=["\']csrf_token["\'][^>]*content=["\']([^"\']+)["\']',
        r"csrfToken\s*[:=]\s*['\"]([^'\"]+)['\"]",
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
    return ""


def url_encode(params: Mapping[str, Any] | Sequence[tuple[str, Any]]) -> str:
    clean_params: Mapping[str, Any] | Sequence[tuple[str, Any]] = params
    if isinstance(params, Mapping):
        clean_params = {k: "" if v is None else v for k, v in params.items()}
    return urllib.parse.urlencode(clean_params, doseq=True)


def url_decode(query: str) -> dict[str, list[str]]:
    return urllib.parse.parse_qs(query, keep_blank_values=True)


def b64_encode(data: str | bytes, *, urlsafe: bool = False) -> str:
    raw = data.encode("utf-8") if isinstance(data, str) else data
    if urlsafe:
        return base64.urlsafe_b64encode(raw).decode("ascii")
    return base64.b64encode(raw).decode("ascii")


def b64_decode(data: str, *, urlsafe: bool = False) -> bytes:
    if not data:
        return b""
    padded = data + "=" * (-len(data) % 4)
    try:
        if urlsafe:
            return base64.urlsafe_b64decode(padded)
        return base64.b64decode(padded)
    except Exception:
        return b""
