#!/usr/bin/env python3
"""
Tapback MCP Server - Claude Code連携用
"""

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tapback")

DEFAULT_SERVER = "http://127.0.0.1:8080"


@mcp.tool()
def ask_yesno(message: str, timeout: int = 300) -> str:
    """
    スマホにYes/No質問を送信し、回答を待つ。

    Args:
        message: 質問文（例: "この変更を適用しますか？"）
        timeout: タイムアウト秒数

    Returns:
        "yes" または "no"
    """
    return _ask(message, "yesno", timeout)


@mcp.tool()
def ask_text(message: str, timeout: int = 600) -> str:
    """
    スマホにテキスト入力を求め、回答を待つ。

    Args:
        message: 質問文（例: "修正内容を入力してください"）
        timeout: タイムアウト秒数

    Returns:
        ユーザーが入力したテキスト
    """
    return _ask(message, "text", timeout)


def _ask(message: str, q_type: str, timeout: int) -> str:
    """内部: 質問を送信して回答を待つ"""
    server = DEFAULT_SERVER

    # 質問を登録
    try:
        response = requests.post(
            f"{server}/ask",
            json={"message": message, "type": q_type, "timeout": timeout},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return "[ERROR] tapback-serverに接続できません。先に 'uv run tapback-server' を実行してください。"

    if response.status_code != 200:
        return f"[ERROR] 質問の登録に失敗: {response.text}"

    question_id = response.json().get("id")

    # 回答を待機
    try:
        wait_response = requests.get(
            f"{server}/wait/{question_id}", timeout=timeout + 10
        )
    except requests.exceptions.Timeout:
        return "[TIMEOUT] 回答がありませんでした"

    if wait_response.status_code == 408:
        return "[TIMEOUT] 回答がありませんでした"

    if wait_response.status_code != 200:
        return f"[ERROR] {wait_response.text}"

    return wait_response.json().get("answer", "")


if __name__ == "__main__":
    mcp.run()
