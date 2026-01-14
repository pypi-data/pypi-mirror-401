"""
AI-powered text parsing using LLM APIs.
Supports OpenAI, Anthropic, and Grok (xAI).
No external dependencies - uses urllib only.
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any, Optional


def _get_api_key(provider: str) -> str:
    """Get API key from environment variable."""
    env_vars = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "grok": "GROK_API_KEY",
    }
    var_name = env_vars.get(provider, "")
    return os.environ.get(var_name, "")


def _call_openai(prompt: str, text: str, api_key: str, model: str) -> str:
    """Call OpenAI API."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ],
    }
    return _http_post(url, headers, payload, ["choices", 0, "message", "content"])


def _call_anthropic(prompt: str, text: str, api_key: str, model: str) -> str:
    """Call Anthropic API."""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ],
    }
    return _http_post(url, headers, payload, ["content", 0, "text"])


def _call_grok(prompt: str, text: str, api_key: str, model: str) -> str:
    """Call Grok (xAI) API - OpenAI compatible."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ],
    }
    return _http_post(url, headers, payload, ["choices", 0, "message", "content"])


def _http_post(url: str, headers: dict, payload: dict, response_path: list) -> str:
    """Make HTTP POST request and extract response."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            # Navigate response path
            for key in response_path:
                if isinstance(key, int):
                    if isinstance(result, list) and 0 <= key < len(result):
                        result = result[key]
                    else:
                        return ""
                else:
                    if isinstance(result, dict) and key in result:
                        result = result[key]
                    else:
                        return ""
            return str(result) if result else ""
    except Exception:
        return ""


def parse_ai(
    prompt: str,
    text: str,
    provider: str = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Parse text using an LLM API.

    Args:
        prompt: Instructions for the LLM (e.g., "Extract all email addresses")
        text: The text to parse
        provider: "openai", "anthropic", or "grok"
        model: Optional model override (defaults to provider's default)
        api_key: Optional API key override (defaults to environment variable)

    Returns:
        LLM response as string, or empty string on error.

    Environment variables:
        OPENAI_API_KEY - for OpenAI
        ANTHROPIC_API_KEY - for Anthropic
        GROK_API_KEY - for Grok (xAI)

    Example:
        >>> parse_ai("Extract the price", "The item costs $29.99", provider="openai")
        "$29.99"
    """
    if not prompt or not text:
        return ""

    key = api_key or _get_api_key(provider)
    if not key:
        return ""

    default_models = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-latest",
        "grok": "grok-2-latest",
    }
    model = model or default_models.get(provider, "")

    providers = {
        "openai": _call_openai,
        "anthropic": _call_anthropic,
        "grok": _call_grok,
    }

    handler = providers.get(provider)
    if not handler:
        return ""

    return handler(prompt, text, key, model)


def parse_ai_json(
    prompt: str,
    text: str,
    provider: str = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Any:
    """
    Parse text using an LLM and return JSON.

    Same as parse_ai() but attempts to parse the response as JSON.
    Returns None if parsing fails or response is not valid JSON.

    Example:
        >>> parse_ai_json("Extract name and age as JSON", "John is 30 years old")
        {"name": "John", "age": 30}
    """
    result = parse_ai(prompt, text, provider, model, api_key)
    if not result:
        return None

    # Try to extract JSON from response (LLMs sometimes wrap in markdown)
    result = result.strip()
    if result.startswith("```"):
        lines = result.split("\n")
        # Remove first and last lines (```json and ```)
        if len(lines) >= 2:
            result = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])

    try:
        return json.loads(result)
    except Exception:
        return None
