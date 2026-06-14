# web-search-mcp (DuckDuckGo利用Web検索無料MCP-Server)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20WSL2-blue.svg)](https://github.com/Iwamoto-Ai/web-search-mcp)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)

Docker コンテナや WSL などの仮想化・隔離環境から Web 検索する時などに使えます。DuckDuckGo を利用しているので無料です。

## ✨ 機能

| ツール | 説明 |
| --- | --- |
| `web_search` | DuckDuckGo で Web 検索し、結果一覧を返します。 |
| `web_fetch` | 指定 URL のページを取得します。デフォルトでは本文テキストを抽出して返し、`raw=true` で生 HTML を返します。 |

`web_fetch` には次の安全策が組み込まれています。

- `http` / `https` 以外のスキーム（`file://` など）を拒否し、ローカルファイル読み取りを防止
- タイムアウト（15 秒）と取得サイズ上限（1MB）
- User-Agent の付与
- 例外を `{"error": ...}` として返すため、エージェント側で扱いやすい

## DuckDuckGo (無料)

- 検索に API キーの取得は不要です。
- 登録や面倒な手続きなしで、手軽に AI エージェントに Web 検索機能を組み込めます。
- 主なメリットと注意点:
  - **API Key 不要**: 事前登録が一切不要で、すぐに利用可能。
  - **完全無料**: 開発時の金銭コストを抑えられる。
  - **利用制限**: 匿名性を維持するため、1 日のクエリ数などに一定の使用制限があります。
- LangChain などのフレームワークでも標準サポートされており、RAG（検索拡張生成）システム開発でもよく利用されています。

## 📦 必要環境

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)（推奨。インラインスクリプトメタデータから依存を自動解決します）

依存パッケージ（`mcp`, `ddgs`）はスクリプト冒頭のメタデータに記載されているため、`uv run` で自動的にインストールされます。手動でインストールする場合:

```bash
pip install mcp ddgs
```

## 🚀 セットアップ

```bash
git clone https://github.com/Iwamoto-Ai/web-search-mcp.git
cd web-search-mcp

# 動作確認（uv が依存を解決して起動します）
uv run web-search-mcp.py
```

> **Note**: `uv` は単体ではスクリプトを実行できません。必ず `uv run <スクリプト>` の形式で呼び出してください。

## 🧩 各クライアントへの設定

### Claude Desktop

`claude_desktop_config.json` に追記します（`mcpServers` キー）:

```json
{
  "mcpServers": {
    "web-search-mcp": {
      "command": "uv",
      "args": ["run", "/home/YourName/web-search-mcp/web-search-mcp.py"]
    }
  }
}
```

### 🦞 OpenClaw

> **⚠️ 重要**: OpenClaw では Claude Desktop の `mcpServers` キーは使用できません。OpenClaw 専用の設定方法を使ってください。

CLI で登録するのが確実です:

```bash
# Linux / WSL
openclaw mcp set web-search-mcp '{
  "command": "uv",
  "args": ["run", "/home/YourName/web-search-mcp/web-search-mcp.py"]
}'
```

`~/.openclaw/openclaw.json` に直接記述する場合は **`mcp.servers`** キーを使います（`mcpServers` は無効）:

```json
{
  "mcp": {
    "servers": {
      "web-search-mcp": {
        "command": "uv",
        "args": ["run", "/home/YourName/web-search-mcp/web-search-mcp.py"]
      }
    }
  }
}
```

### Hermes Agent を WSL (Windows Subsystem for Linux) で動作させている場合

`.hermes/config.yaml` を直接編集します:

```yaml
web_search_and_fetch:
  command: /home/YourName/web-search-mcp/.venv/bin/python
  args:
    - /home/YourName/web-search-mcp/web-search-mcp.py
  type: stdio
```

> パスはご自身の環境に合わせて変更してください。

## 📄 ライセンス

Licensed under the Apache License, Version 2.0 - 詳細は [LICENSE](LICENSE) を参照してください。

Copyright 2026 岩本 剛    All rights reserved.

## 🤝 コントリビュート

Issue・Pull Request 歓迎です。

1. Fork する
2. Feature branch を作成: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Pull Request を作成

## 📚 参考資料

- [Model Context Protocol (MCP) 公式](https://modelcontextprotocol.io/)
- [Claude Desktop MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Docker](https://www.docker.com/ja-jp/)
- [DuckDuckGo](https://duckduckgo.com/)
- [🦞 OpenClaw](https://openclaw.ai/)
- [Hermes-Agent](https://hermes-agent.nousresearch.com/docs/)
