# Tapback

ターミナルをスマホに同期するツール。Claude Codeなどをリモートで操作できます。

## インストール

```bash
pip install tapback
# または
uv add tapback
```

## 使い方

```bash
tapback-server claude
```

表示されるURLにスマホでアクセスし、PINを入力。

ターミナルの内容がリアルタイムで同期され、スマホから入力できます。

## 要件

- tmux (`brew install tmux`)
- スマホとMacが同じWi-Fiネットワーク（または ngrok）

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
