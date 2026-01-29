#!/usr/bin/env python3
"""
Tapback - Human-in-the-Loop Input Tool
Python API & CLI

Usage (CLI):
    tapback "Delete this file?" --type yesno --timeout 300
    tapback "Enter your modifications" --type text --timeout 600

Usage (Python API):
    from tapback import ask
    result = ask("Merge this PR?", type="yesno", timeout=300)
"""

import sys
import argparse
import requests
from typing import Optional, Literal

# Default settings
DEFAULT_SERVER = "http://127.0.0.1:8080"
DEFAULT_TIMEOUT = 300


def get_server_url() -> Optional[str]:
    """
    Get server URL from .tapback/server.json
    Returns None if not found
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
    """Tapback error."""

    pass


class TapbackTimeout(TapbackError):
    """Timeout error."""

    pass


def ask(
    message: str,
    type: Literal["yesno", "text"] = "yesno",
    timeout: int = DEFAULT_TIMEOUT,
    server: str = DEFAULT_SERVER,
) -> Optional[str]:
    """
    Send question to mobile and wait for answer.

    Args:
        message: Question text
        type: Question type ("yesno" or "text")
        timeout: Timeout in seconds
        server: Server URL

    Returns:
        Answer ("yes", "no", or text)

    Raises:
        TapbackTimeout: On timeout
        TapbackError: On other errors
    """
    # Register question
    try:
        response = requests.post(
            f"{server}/ask",
            json={"message": message, "type": type, "timeout": timeout},
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        raise TapbackError(f"Cannot connect to server: {server}")
    except requests.exceptions.Timeout:
        raise TapbackError("Connection to server timed out")

    if response.status_code != 200:
        raise TapbackError(f"Failed to register question: {response.text}")

    question_id = response.json().get("id")
    if not question_id:
        raise TapbackError("Failed to get question ID")

    # Wait for answer
    try:
        wait_response = requests.get(
            f"{server}/wait/{question_id}",
            timeout=timeout + 10,  # Server timeout + margin
        )
    except requests.exceptions.Timeout:
        raise TapbackTimeout("Answer wait timed out")
    except requests.exceptions.ConnectionError:
        raise TapbackError("Connection to server lost")

    if wait_response.status_code == 408:
        raise TapbackTimeout("Timeout: No answer received")

    if wait_response.status_code != 200:
        raise TapbackError(f"Error: {wait_response.text}")

    return wait_response.json().get("answer")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tapback",
        description="Human-in-the-Loop Input Tool - Get answers from mobile",
    )
    parser.add_argument("message", help="Question text")
    parser.add_argument(
        "-t",
        "--type",
        choices=["yesno", "text"],
        default="yesno",
        help="Question type (default: yesno)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "-s",
        "--server",
        default=None,
        help="Server URL (default: from .tapback/server.json)",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Output result only")
    parser.add_argument(
        "--silent", action="store_true", help="Exit silently if server not running"
    )

    args = parser.parse_args()

    # Determine server URL
    server = args.server or get_server_url() or DEFAULT_SERVER

    # --silent mode: exit if no server info
    if args.silent and not get_server_url():
        sys.exit(0)

    if not args.quiet:
        print(f"Sending question: {args.message}", file=sys.stderr)
        print("Please answer on mobile...", file=sys.stderr)

    try:
        result = ask(
            message=args.message,
            type=args.type,
            timeout=args.timeout,
            server=server,
        )

        print(result)

        # Exit code: yes/text input=0, no=1
        if args.type == "yesno" and result == "no":
            sys.exit(1)
        sys.exit(0)

    except TapbackTimeout:
        if not args.quiet:
            print("Timeout", file=sys.stderr)
        sys.exit(2)

    except TapbackError as e:
        if args.silent:
            sys.exit(0)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
