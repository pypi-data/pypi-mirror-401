# Tapback

スマホからYes/Noやテキストを返せるHuman-in-the-Loopツール。

Claude CodeなどのLLMツールと連携し、スマホから承認・入力ができます。

## インストール

```bash
uvx tapback-server  # サーバー起動
```

## Claude Code連携

プロジェクトの `.mcp.json` に以下を追加:

```json
{
  "mcpServers": {
    "tapback": {
      "command": "uvx",
      "args": ["tapback"]
    }
  }
}
```

## 使い方

### 1. サーバー起動

```bash
uvx tapback-server
```

表示されるPINをメモし、Network URLにスマホでアクセス。

### 2. Claude Codeで使用

Claude Codeが `ask_yesno` / `ask_text` ツールを呼び出すと、スマホに質問が表示されます。

### CLIとして使用

```bash
uvx tapback "削除しますか？" --type yesno
uvx tapback "修正内容を入力" --type text
```

### Pythonから使用

```python
from tapback import ask

if ask("実行しますか？", type="yesno") == "yes":
    execute()
```

## オプション

```bash
uvx tapback-server --port 9000      # ポート変更
uvx tapback-server --no-auth        # PIN認証を無効化
```

## License

MIT
