# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp", "duckduckgo-search"]
# ///

from __future__ import annotations
from typing import Any, Dict
from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

app = FastMCP('web-search-fetch')

@app.tool()
def web_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Web search using DuckDuckGo.
    Args:
        query: Search query.
        max_results: Number of results (default: 10).
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return {"results": results}

@app.tool()
def web_fetch(url: str) -> Dict[str, Any]:
    """
    Fetch the content of a web page.
    Args:
        url: The URL to fetch.
    """
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return {"content": response.read().decode("utf-8", errors="ignore")}

if __name__ == '__main__':
    app.run()
