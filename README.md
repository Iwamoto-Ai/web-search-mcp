# web-search-mcp (DuckDuckGo利用Web検索無料MCP-Server)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-blue.svg)](#)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)

Dockerコンテナ仮想化環境からWeb検索する時などに使えます。DuckDuckGoを利用しているので無料です。

## DuckDuckGo (無料)
- 公式検索APIは完全に無料で、APIキーの取得も不要です。
- 登録や面倒な手続きなしで、手軽にAIエージェントにWeb検索機能を組み込むことができます。

- 主なメリットと注意点は以下の通りです： API Key不要: 事前登録が一切不要で、すぐに利用可能。
- 完全無料: 開発時の金銭コストを抑えられる。
- 利用制限: 匿名性を維持するため、1日のクエリ数などに一定の使用制限があります。
- LangChainなどのフレームワークでも「DuckDuckGo Search」として標準サポートされているため、
- AIのRAG（検索拡張生成）システム開発などでもよく利用されています。


## 🦞 OpenClaw への設定

> **⚠️ 重要**: OpenClaw では Claude Desktop の `mcpServers` キーは使用できません。  
> OpenClaw 専用の設定方法を使ってください。

`openclaw.json` を直接編集せず、CLIで登録するのが確実です:

```bash
# Linux / WSL
openclaw mcp set web-search-mcp '{
  "command": "python",
  "args": ["/home/YourName/web-search-mcp/web-search-mcp.py"]
}'


### 🦞 openclaw.json に直接記述する場合

`~/.openclaw/openclaw.json` に追記する場合は **`mcp.servers`** キーを使います（`mcpServers` は無効）:

```json
{
  "mcp": {
    "servers": {
      "web-search-mcp": {
        "command": "python",
        "args": [
          "/home/YourName/web-search-mcp/web-search-mcp.py"
        ]
      }
    }
  }
}
```

## Hermes Agent を WSL (Windows Subsystem for Linux) で動作させている場合の設定
`.hermes/config.yaml` を直接編集。

```yaml
mcp_servers:
 web-search-mcp:
    command: python
    args:
    - /home/YourName/web-search-mcp/web-search-mcp.py
    sessionIdleTtlMs: 600000
```

---

## 📄 ライセンス

Apache License Version 2.0 - 詳細は [LICENSE](LICENSE) を参照

Copyright 2026　岩本 剛　All rights reserved.


---


## 🤝 コントリビュート

Issue・Pull Request 歓迎です。

1. Fork する
2. Feature branch を作成: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Pull Request を作成

---

## 📚 参考資料
- [Model Context Protocol (MCP) 公式](https://modelcontextprotocol.io/)
- [Claude Desktop MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Docker](https://www.docker.com/ja-jp/)
- [DuckDuckGo](https://duckduckgo.com/)
- [🦞OpenClaw](https://openclaw.ai/)
- [Hermes-Agent](https://hermes-agent.nousresearch.com/docs/)
 
