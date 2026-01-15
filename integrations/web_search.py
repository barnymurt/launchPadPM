"""
DuckDuckGo web search integration.
"""

from typing import Any, Dict, List

from duckduckgo_search import DDGS


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not query.strip():
        return results

    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                }
            )

    return results
