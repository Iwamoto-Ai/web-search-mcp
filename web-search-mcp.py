# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp", "ddgs"]
# ///
"""web-search-mcp

DuckDuckGo を利用した無料の Web 検索 / ページ取得 MCP サーバー。
API キー不要で、Docker コンテナや WSL など隔離環境からの Web 検索に利用できます。
"""

from __future__ import annotations

import urllib.error
import urllib.request
from html.parser import HTMLParser
from typing import Any, Dict
from urllib.parse import urlparse

from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

app = FastMCP("web-search-fetch")

# web_fetch の設定
ALLOWED_SCHEMES = {"http", "https"}
MAX_BYTES = 1_000_000  # 取得する最大バイト数 (1MB)
FETCH_TIMEOUT = 15  # 秒
USER_AGENT = "web-search-mcp/1.0 (+https://github.com/Iwamoto-Ai/web-search-mcp)"


class _TextExtractor(HTMLParser):
    """HTML からテキストだけを抽出する簡易パーサー（標準ライブラリのみ）。"""

    _SKIP_TAGS = {"script", "style", "noscript", "template"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def get_text(self) -> str:
        return "\n".join(self._chunks)


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(html)
    except Exception:
        return html  # パースに失敗したら生のまま返す
    return parser.get_text()


@app.tool()
def web_search(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    DuckDuckGo を使って Web 検索します。

    Args:
        query: 検索クエリ。
        max_results: 取得する結果数 (デフォルト: 10)。
    """
    if not query or not query.strip():
        return {"error": "query is empty."}

    max_results = max(1, min(max_results, 50))  # 1〜50 にクランプ

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return {"results": results, "count": len(results)}
    except Exception as e:
        # DuckDuckGo のレート制限やネットワークエラーを呼び出し側に返す
        return {"error": f"{type(e).__name__}: {e}"}


@app.tool()
def web_fetch(url: str, raw: bool = False) -> Dict[str, Any]:
    """
    Web ページの内容を取得します。

    Args:
        url: 取得する URL (http / https のみ)。
        raw: True の場合は HTML をそのまま返す。False (デフォルト) は本文テキストを抽出して返す。
    """
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        return {"error": "Only http/https URLs are allowed."}
    if not parsed.netloc:
        return {"error": "Invalid URL."}

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read(MAX_BYTES)
            truncated = len(resp.read(1)) > 0  # まだ続きがあるか
        html = data.decode(charset, errors="ignore")
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "url": url}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "url": url}

    content = html if raw else _html_to_text(html)
    return {"url": url, "content": content, "truncated": truncated}


if __name__ == "__main__":
    app.run()
