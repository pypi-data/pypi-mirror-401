#!/usr/bin/env python3
"""Tapback Server - Sync terminal via tmux session."""

import sys
import subprocess
import secrets
import random
import json
import uvicorn
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from tapback.constants import SESSION_NAME, HTML, PIN_HTML

app = FastAPI()

connected_clients: list[WebSocket] = []
session_pin = None
authenticated_tokens = set()


def tmux_send(text: str):
    """Send key input to tmux session."""
    if text:
        subprocess.run(
            ["tmux", "send-keys", "-t", SESSION_NAME, "-l", text],
            capture_output=True,
            text=True,
        )
    result = subprocess.run(
        ["tmux", "send-keys", "-t", SESSION_NAME, "Enter"],
        capture_output=True,
        text=True,
    )
    print(f"[tapback] send '{text}' -> rc={result.returncode}, err={result.stderr}")


def tmux_capture() -> str:
    """Capture tmux session output."""
    result = subprocess.run(
        ["tmux", "capture-pane", "-t", SESSION_NAME, "-p", "-S", "-100"],
        capture_output=True,
        text=True,
    )
    return result.stdout


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    token = request.cookies.get("tapback_token", "")
    if token not in authenticated_tokens:
        return HTMLResponse(PIN_HTML.format(error=""))
    return HTMLResponse(HTML)


@app.post("/auth")
async def auth(pin: str = Form(...)):
    if pin == session_pin:
        token = secrets.token_hex(16)
        authenticated_tokens.add(token)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie("tapback_token", token, httponly=True, max_age=86400)
        return response
    return HTMLResponse(PIN_HTML.format(error='<div class="e">Invalid PIN</div>'))


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    print("[tapback] WebSocket connection request")
    await websocket.accept()
    print("[tapback] WebSocket accepted")

    token = ""
    for h in websocket.headers.raw:
        if h[0] == b"cookie":
            for c in h[1].decode().split(";"):
                if "tapback_token=" in c:
                    token = c.split("=")[1].strip()

    print(
        f"[tapback] token={token[:8] if token else 'none'}..., authenticated={token in authenticated_tokens}"
    )

    if token not in authenticated_tokens:
        print("[tapback] Auth failed, closing connection")
        await websocket.close(code=4001)
        return

    connected_clients.append(websocket)
    print(f"[tapback] Client added, total {len(connected_clients)}")

    try:
        output = tmux_capture()
        await websocket.send_json({"t": "o", "c": output})
        last_output = output

        import asyncio

        async def poll_output():
            nonlocal last_output
            while True:
                await asyncio.sleep(1)
                output = tmux_capture()
                if output != last_output:
                    last_output = output
                    try:
                        await websocket.send_json({"t": "o", "c": output})
                    except Exception:
                        break

        poll_task = asyncio.create_task(poll_output())

        while True:
            data = await websocket.receive_json()
            if data.get("t") == "i":
                content = data.get("c", "")
                tmux_send(content)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[tapback] Error: {e}")
    finally:
        poll_task.cancel()
        if websocket in connected_clients:
            connected_clients.remove(websocket)


def get_local_ip():
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split("\n"):
            if "inet " in line and "127.0.0.1" not in line:
                parts = line.strip().split()
                idx = parts.index("inet") + 1
                if idx < len(parts):
                    ip = parts[idx]
                    if ip.startswith("192.168."):
                        return ip
        return "127.0.0.1"
    except Exception:
        return "127.0.0.1"


def save_server_info(port: int):
    tapback_dir = Path.cwd() / ".tapback"
    tapback_dir.mkdir(exist_ok=True)
    (tapback_dir / "server.json").write_text(json.dumps({"port": port}))


def cleanup():
    info_path = Path.cwd() / ".tapback" / "server.json"
    if info_path.exists():
        info_path.unlink()
    # Kill tmux session
    subprocess.run(["tmux", "kill-session", "-t", SESSION_NAME], capture_output=True)


def main():
    global session_pin
    import argparse
    import atexit

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8080)
    parser.add_argument("--no-auth", action="store_true")
    parser.add_argument("--kill", "-k", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.kill:
        cleanup()
        print("Stopped")
        return

    # Always cleanup before start
    cleanup()

    if not args.command:
        print("Usage: tapback-server claude")
        return

    # Check if tmux is installed
    if subprocess.run(["which", "tmux"], capture_output=True).returncode != 0:
        print("Error: tmux is not installed")
        print("  brew install tmux")
        sys.exit(1)

    # Kill existing session
    subprocess.run(["tmux", "kill-session", "-t", SESSION_NAME], capture_output=True)

    # Create new tmux session (shell persists after command exit)
    cmd = " ".join(args.command)
    subprocess.run(["tmux", "new-session", "-d", "-s", SESSION_NAME])
    subprocess.run(["tmux", "send-keys", "-t", SESSION_NAME, cmd, "Enter"])

    save_server_info(args.port)
    atexit.register(cleanup)

    if args.no_auth:
        session_pin = None
        authenticated_tokens.add("no-auth")
    else:
        session_pin = f"{random.randint(0, 9999):04d}"

    ip = get_local_ip()
    print(f"\n{'=' * 50}")
    print("  Tapback")
    print(f"{'=' * 50}")
    print(f"  http://{ip}:{args.port}")
    if session_pin:
        print(f"  PIN: {session_pin}")
    print(f"{'=' * 50}")
    print(f"  tmux attach -t {SESSION_NAME}  # Local access")
    print(f"{'=' * 50}\n")

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
