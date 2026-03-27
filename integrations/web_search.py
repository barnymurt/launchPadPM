"""
DuckDuckGo web search integration.
"""

from typing import Any, Dict, List

try:
    from ddgs import DDGS
    USE_DDGS = True
except ImportError:
    USE_DDGS = False


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not query.strip():
        return results

    if not USE_DDGS:
        return results

    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "snippet": item.get("body", ""),
                    }
                )
    except Exception as e:
        print(f"Web search error: {e}")

    return results
