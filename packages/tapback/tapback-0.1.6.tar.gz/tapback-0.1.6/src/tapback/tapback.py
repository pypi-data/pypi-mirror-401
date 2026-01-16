#!/usr/bin/env python3
"""
Tapback - Human-in-the-Loop Input Tool
Python API & CLI

Usage (CLI):
    tapback "本当に削除しますか？" --type yesno --timeout 300
    tapback "修正内容を入力してください" --type text --timeout 600

Usage (Python API):
    from tapback import ask
    result = ask("このPRをマージしますか？", type="yesno", timeout=300)
"""

import sys
import argparse
import requests
from typing import Optional, Literal

# デフォルト設定
DEFAULT_SERVER = "http://127.0.0.1:8080"
DEFAULT_TIMEOUT = 300


def get_server_url() -> Optional[str]:
    """
    .tapback/server.jsonからサーバーURLを取得
    存在しなければNoneを返す
    """
    import os
    import json

    info_path = os.path.join(os.getcwd(), ".tapback", "server.json")
    if not os.path.exists(info_path):
        return None

    try:
        with open(info_path) as f:
            info = json.load(f)
            return info.get("url")
    except Exception:
        return None


class TapbackError(Exception):
    """Tapback エラー"""

    pass


class TapbackTimeout(TapbackError):
    """タイムアウトエラー"""

    pass


def ask(
    message: str,
    type: Literal["yesno", "text"] = "yesno",
    timeout: int = DEFAULT_TIMEOUT,
    server: str = DEFAULT_SERVER,
) -> Optional[str]:
    """
    スマホに質問を送信し、回答を待機する

    Args:
        message: 質問文
        type: 質問タイプ ("yesno" or "text")
        timeout: タイムアウト秒数
        server: サーバーURL

    Returns:
        回答 ("yes", "no", またはテキスト)

    Raises:
        TapbackTimeout: タイムアウト時
        TapbackError: その他のエラー時
    """
    # 質問を登録
    try:
        response = requests.post(
            f"{server}/ask",
            json={"message": message, "type": type, "timeout": timeout},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        raise TapbackError(f"サーバーに接続できません: {server}")
    except requests.exceptions.Timeout:
        raise TapbackError("サーバーへの接続がタイムアウトしました")

    if response.status_code != 200:
        raise TapbackError(f"質問の登録に失敗: {response.text}")

    question_id = response.json().get("id")
    if not question_id:
        raise TapbackError("質問IDが取得できませんでした")

    # 回答を待機
    try:
        wait_response = requests.get(
            f"{server}/wait/{question_id}",
            timeout=timeout + 10,  # サーバー側タイムアウト + マージン
        )
    except requests.exceptions.Timeout:
        raise TapbackTimeout("回答待機がタイムアウトしました")
    except requests.exceptions.ConnectionError:
        raise TapbackError("サーバーとの接続が切断されました")

    if wait_response.status_code == 408:
        raise TapbackTimeout("タイムアウト: 回答がありませんでした")

    if wait_response.status_code != 200:
        raise TapbackError(f"エラー: {wait_response.text}")

    return wait_response.json().get("answer")


def main():
    """CLI エントリーポイント"""
    parser = argparse.ArgumentParser(
        prog="tapback",
        description="Human-in-the-Loop Input Tool - スマホから回答を受け取る",
    )
    parser.add_argument("message", help="質問文")
    parser.add_argument(
        "-t",
        "--type",
        choices=["yesno", "text"],
        default="yesno",
        help="質問タイプ (default: yesno)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"タイムアウト秒数 (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "-s",
        "--server",
        default=None,
        help="サーバーURL (default: .tapback/server.jsonから取得)",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="結果のみ出力")
    parser.add_argument(
        "--silent", action="store_true", help="サーバー未起動時は静かに終了"
    )

    args = parser.parse_args()

    # サーバーURLを決定
    server = args.server or get_server_url() or DEFAULT_SERVER

    # --silent モード: サーバー情報がなければ終了
    if args.silent and not get_server_url():
        sys.exit(0)

    if not args.quiet:
        print(f"質問を送信中: {args.message}", file=sys.stderr)
        print("スマホで回答してください...", file=sys.stderr)

    try:
        result = ask(
            message=args.message,
            type=args.type,
            timeout=args.timeout,
            server=server,
        )

        print(result)

        # 終了コード: yes/text入力あり=0, no=1
        if args.type == "yesno" and result == "no":
            sys.exit(1)
        sys.exit(0)

    except TapbackTimeout:
        if not args.quiet:
            print("タイムアウト", file=sys.stderr)
        sys.exit(2)

    except TapbackError as e:
        if args.silent:
            sys.exit(0)
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(3)

    except KeyboardInterrupt:
        print("\n中断されました", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
