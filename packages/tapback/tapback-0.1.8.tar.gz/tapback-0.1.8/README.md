# Tapback

ターミナルをスマホに同期するツール。Claude Codeなどをリモートで操作できます。

## 使い方

インストール不要で直接実行:

```bash
uvx --from tapback tapback-server claude
```

最新版を使いたい場合は `--refresh` を付ける:

```bash
uvx --refresh --from tapback tapback-server claude
```

表示されるURLにスマホでアクセスし、PINを入力。

ターミナルの内容がリアルタイムで同期され、スマホから入力できます。

## インストール（オプション）

```bash
pip install tapback
```

インストール後:

```bash
tapback-server claude
```

## 要件

- tmux (`brew install tmux`)
- スマホとMacが同じWi-Fiネットワーク（または ngrok）

## ローカルで確認

tmuxセッションに直接アタッチして確認:

```bash
tmux attach -t tapback
```

## 外部ネットワークから使う

外出先など別ネットワークから使う場合は ngrok でトンネリング:

```bash
ngrok http 8080
```

表示されるURL（例: `https://xxxx.ngrok.io`）をスマホで開きます。

## オプション

```bash
tapback-server --port 9000 claude   # ポート変更
tapback-server --no-auth claude     # PIN認証を無効化
tapback-server --kill               # 既存セッションを終了
```

## License

MIT
