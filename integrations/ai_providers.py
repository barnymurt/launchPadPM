"""
AI provider clients for OpenAI, Anthropic, and Perplexity.
"""

import os
from typing import List, Optional

from anthropic import Anthropic
from openai import OpenAI


def _require_key(key_name: str, override_key: Optional[str] = None) -> str:
    if override_key and override_key.strip():
        return override_key.strip()
    api_key = os.getenv(key_name, "").strip()
    if not api_key:
        raise RuntimeError(f"Missing {key_name} environment variable")
    return api_key


def call_openai(
    messages: List[dict],
    model: Optional[str] = None,
    max_tokens: int = 800,
    api_key: Optional[str] = None,
) -> str:
    api_key = _require_key("OPENAI_API_KEY", api_key)
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens)
    return response.choices[0].message.content or ""


def call_anthropic(
    messages: List[dict],
    model: Optional[str] = None,
    max_tokens: int = 800,
    api_key: Optional[str] = None,
) -> str:
    api_key = _require_key("ANTHROPIC_API_KEY", api_key)
    model_name = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
    client = Anthropic(api_key=api_key)
    system = ""
    user_messages = []
    for message in messages:
        if message.get("role") == "system":
            system += f"{message.get('content', '')}\n"
        else:
            user_messages.append({"role": message.get("role", "user"), "content": message.get("content", "")})
    response = client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        system=system.strip(),
        messages=user_messages,
    )
    return response.content[0].text if response.content else ""


def call_perplexity(
    messages: List[dict],
    model: Optional[str] = None,
    max_tokens: int = 800,
    api_key: Optional[str] = None,
) -> str:
    api_key = _require_key("PERPLEXITY_API_KEY", api_key)
    model_name = model or os.getenv("PERPLEXITY_MODEL", "sonar-pro")
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens)
    return response.choices[0].message.content or ""
