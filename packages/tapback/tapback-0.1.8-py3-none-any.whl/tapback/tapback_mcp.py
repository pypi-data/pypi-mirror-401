#!/usr/bin/env python3
"""Tapback MCP Server - Claude Code integration."""

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tapback")

DEFAULT_SERVER = "http://127.0.0.1:8080"


@mcp.tool()
def ask_yesno(message: str, timeout: int = 300) -> str:
    """
    Send Yes/No question to mobile and wait for answer.

    Args:
        message: Question text (e.g. "Apply this change?")
        timeout: Timeout in seconds

    Returns:
        "yes" or "no"
    """
    return _ask(message, "yesno", timeout)


@mcp.tool()
def ask_text(message: str, timeout: int = 600) -> str:
    """
    Request text input from mobile and wait for answer.

    Args:
        message: Question text (e.g. "Enter your modifications")
        timeout: Timeout in seconds

    Returns:
        User input text
    """
    return _ask(message, "text", timeout)


def _ask(message: str, q_type: str, timeout: int) -> str:
    """Internal: Send question and wait for answer."""
    server = DEFAULT_SERVER

    # Register question
    try:
        response = requests.post(
            f"{server}/ask",
            json={"message": message, "type": q_type, "timeout": timeout},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        return "[ERROR] Cannot connect to tapback-server. Run 'uv run tapback-server' first."

    if response.status_code != 200:
        return f"[ERROR] Failed to register question: {response.text}"

    question_id = response.json().get("id")

    # Wait for answer
    try:
        wait_response = requests.get(
            f"{server}/wait/{question_id}", timeout=timeout + 10
        )
    except requests.exceptions.Timeout:
        return "[TIMEOUT] No answer received"

    if wait_response.status_code == 408:
        return "[TIMEOUT] No answer received"

    if wait_response.status_code != 200:
        return f"[ERROR] {wait_response.text}"

    return wait_response.json().get("answer", "")


if __name__ == "__main__":
    mcp.run()
