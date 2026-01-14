import json
import re
from html import unescape as html_unescape
from html.parser import HTMLParser
from typing import Any, List, Optional
from urllib.parse import urljoin, urlparse


def strip_scripts_styles(html_text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html_text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return " ".join(html_unescape(text).split())


def get_text(html_text: str, separator: str = " ", strip: bool = True) -> str:
    cleaned = strip_scripts_styles(html_text)
    if not separator:
        return cleaned
    parts = cleaned.split()
    return separator.join(parts) if strip else separator.join(cleaned.split(separator))


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_map = {k.lower(): v for k, v in attrs}
        href = attr_map.get("href")
        src = attr_map.get("src")
        if href:
            self.links.append(href)
        if src:
            self.links.append(src)


def extract_links(html_text: str, base: str | None = None, same_host: bool = False, extensions: Optional[list[str]] = None) -> list[str]:
    parser = _LinkParser()
    parser.feed(html_text)
    urls = parser.links
    resolved: list[str] = []
    for u in urls:
        full = urljoin(base, u) if base else u
        if same_host and base:
            if urlparse(full).netloc != urlparse(base).netloc:
                continue
        if extensions:
            if not any(full.lower().endswith(ext.lower()) for ext in extensions):
                continue
        resolved.append(full)
    return resolved


class _FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict[str, Any]] = []
        self._current_form: Optional[dict[str, Any]] = None
        self._current_textarea: Optional[str] = None
        self._textarea_buffer: list[str] = []
        self._in_select: Optional[str] = None
        self._select_options: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_map = {k.lower(): v for k, v in attrs}
        if tag.lower() == "form":
            self._current_form = {
                "action": attr_map.get("action", ""),
                "method": (attr_map.get("method") or "get").lower(),
                "fields": {},
            }
        elif self._current_form and tag.lower() == "input":
            name = attr_map.get("name")
            if not name:
                return
            input_type = (attr_map.get("type") or "text").lower()
            value = attr_map.get("value") or ""
            if input_type in {"checkbox", "radio"} and "checked" not in attr_map:
                return
            self._current_form["fields"][name] = value
        elif self._current_form and tag.lower() == "textarea":
            self._current_textarea = attr_map.get("name")
            self._textarea_buffer = []
        elif self._current_form and tag.lower() == "select":
            self._in_select = attr_map.get("name")
            self._select_options = []
        elif self._current_form and tag.lower() == "option" and self._in_select:
            val = attr_map.get("value") or ""
            selected = "selected" in attr_map
            self._select_options.append((val, selected))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "form" and self._current_form is not None:
            self.forms.append(self._current_form)
            self._current_form = None
        elif tag.lower() == "textarea" and self._current_form is not None and self._current_textarea:
            self._current_form["fields"][self._current_textarea] = "".join(self._textarea_buffer).strip()
            self._current_textarea = None
            self._textarea_buffer = []
        elif tag.lower() == "select" and self._current_form is not None and self._in_select:
            value = ""
            for v, selected in self._select_options:
                if selected:
                    value = v
                    break
            if not value and self._select_options:
                value = self._select_options[0][0]
            self._current_form["fields"][self._in_select] = value
            self._in_select = None
            self._select_options = []

    def handle_data(self, data: str) -> None:
        if self._current_textarea is not None:
            self._textarea_buffer.append(data)


def extract_forms(html_text: str, base: str | None = None) -> list[dict[str, Any]]:
    parser = _FormParser()
    parser.feed(html_text)
    forms = parser.forms
    if base:
        forms = [
            {**f, "action": urljoin(base, f.get("action", ""))}
            for f in forms
        ]
    return forms


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._current_table: Optional[list[list[str]]] = None
        self._current_row: Optional[list[str]] = None
        self._capture_cell: bool = False
        self._cell_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag.lower() == "table":
            self._current_table = []
        elif tag.lower() == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag.lower() in {"td", "th"} and self._current_row is not None:
            self._capture_cell = True
            self._cell_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"td", "th"} and self._capture_cell and self._current_row is not None:
            self._capture_cell = False
            text = "".join(self._cell_buffer).strip()
            self._current_row.append(" ".join(text.split()))
        elif tag.lower() == "tr" and self._current_table is not None and self._current_row is not None:
            self._current_table.append(self._current_row)
            self._current_row = None
        elif tag.lower() == "table" and self._current_table is not None:
            self.tables.append(self._current_table)
            self._current_table = None

    def handle_data(self, data: str) -> None:
        if self._capture_cell:
            self._cell_buffer.append(data)


def extract_tables(html_text: str) -> list[dict[str, Any]]:
    parser = _TableParser()
    parser.feed(html_text)
    result: list[dict[str, Any]] = []
    for table in parser.tables:
        if not table:
            continue
        headers: list[str] = []
        rows_data = table
        if table and len(table[0]) > 0:
            headers = table[0]
            rows_data = table[1:]
        rows: list[Any] = []
        if headers:
            for row in rows_data:
                row_dict = {}
                for idx, header in enumerate(headers):
                    row_dict[header] = row[idx] if idx < len(row) else ""
                rows.append(row_dict)
        else:
            rows = rows_data
        result.append({"headers": headers, "rows": rows})
    return result


def json_in_html(html_text: str) -> list[Any]:
    results: list[Any] = []
    script_json = re.findall(
        r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    inline_json = re.findall(
        r"(?:var|let|const)\s+[A-Za-z0-9_]+\s*=\s*({.*?});",
        html_text,
        flags=re.DOTALL,
    )
    for chunk in script_json + inline_json:
        try:
            results.append(json.loads(chunk))
        except Exception:
            continue
    return results
