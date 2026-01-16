#!/usr/bin/env python3
"""
Tapback Server - tmuxセッション経由でターミナルを同期
"""

import sys
import subprocess
import secrets
import random
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

app = FastAPI()

SESSION_NAME = "tapback"
terminal_output = []
MAX_BUFFER = 200
connected_clients: list[WebSocket] = []
session_pin = None
authenticated_tokens = set()

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Tapback</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,monospace;background:#0d1117;color:#c9d1d9;display:flex;flex-direction:column}
#h{padding:10px 14px;background:#161b22;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}
#h .t{color:#8b5cf6;font-weight:bold;font-size:18px}
#h .s{font-size:13px}
.on{color:#3fb950}.off{color:#f85149}
#term{flex:1;overflow-y:auto;padding:14px;font-size:13px;line-height:1.5;white-space:pre-wrap;word-break:break-all;min-height:0;font-family:monospace}
#in{padding:12px;background:#161b22;border-top:1px solid #30363d;flex-shrink:0}
.row{display:flex;gap:8px;align-items:center}
#txt{flex:1;padding:12px 14px;font-size:16px;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:10px;min-width:0}
#txt:focus{outline:none;border-color:#8b5cf6}
.btn{padding:12px 18px;font-size:15px;font-weight:600;border:none;border-radius:10px;cursor:pointer}
.bsend{background:#8b5cf6;color:#fff}
.benter{background:#30363d;color:#c9d1d9}
</style></head>
<body>
<div id="h"><span class="t">Tapback</span><span class="s" id="st">...</span></div>
<div id="term"></div>
<div id="in">
<div class="row">
<input type="text" id="txt" placeholder="入力..." autocomplete="off">
<button class="btn bsend" id="b4">送信</button>
<button class="btn benter" id="b3">⏎</button>
</div>
</div>
<script>
const term=document.getElementById('term'),txt=document.getElementById('txt'),st=document.getElementById('st');
let ws;
function connect(){
const p=location.protocol==='https:'?'wss:':'ws:';
ws=new WebSocket(p+'//'+location.host+'/ws');
ws.onopen=()=>{st.textContent='接続済';st.className='s on'};
ws.onmessage=(e)=>{const d=JSON.parse(e.data);if(d.t==='o'){term.textContent=d.c;term.scrollTop=term.scrollHeight}};
ws.onclose=()=>{st.textContent='再接続...';st.className='s off';setTimeout(connect,2000)};
ws.onerror=()=>ws.close();
}
function send(v){if(ws&&ws.readyState===1)ws.send(JSON.stringify({t:'i',c:v}))}
document.getElementById('b3').onclick=()=>send('');
document.getElementById('b4').onclick=()=>{send(txt.value);txt.value=''};
txt.onkeypress=(e)=>{if(e.key==='Enter'){send(txt.value);txt.value=''}};
connect();
</script>
</body></html>"""

PIN_HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tapback</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh;display:flex;align-items:center;justify-content:center}}
.c{{max-width:320px;width:100%;padding:20px;text-align:center}}
.l{{font-size:2rem;margin-bottom:1.5rem;color:#8b5cf6}}
.p{{width:100%;padding:1.2rem;font-size:2rem;text-align:center;letter-spacing:0.8rem;border:1px solid #30363d;border-radius:8px;background:#161b22;color:#c9d1d9;margin-bottom:1rem}}
.b{{width:100%;padding:1rem;font-size:1.1rem;border:none;border-radius:8px;background:#8b5cf6;color:#fff;cursor:pointer}}
.e{{color:#f85149;margin-top:1rem}}
</style></head>
<body><div class="c">
<div class="l">Tapback</div>
<form method="POST" action="/auth">
<input type="text" name="pin" class="p" maxlength="4" inputmode="numeric" placeholder="----" required autofocus>
<button type="submit" class="b">認証</button>
</form>{error}
</div></body></html>"""


def tmux_send(text: str):
    """tmuxセッションにキー入力を送信"""
    result = subprocess.run(
        ["tmux", "send-keys", "-t", SESSION_NAME, text, "Enter"],
        capture_output=True,
        text=True,
    )
    print(f"[tapback] send '{text}' -> rc={result.returncode}, err={result.stderr}")


def tmux_capture() -> str:
    """tmuxセッションの出力を取得"""
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
    return HTMLResponse(PIN_HTML.format(error='<div class="e">PINが違います</div>'))


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    print("[tapback] WebSocket接続要求")
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
        print("[tapback] 認証失敗、接続を閉じます")
        await websocket.close(code=4001)
        return

    connected_clients.append(websocket)
    print(f"[tapback] クライアント追加、合計{len(connected_clients)}人")

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

        poll_task.cancel()
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"[tapback] エラー: {e}")
    finally:
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
    # tmuxセッションを終了
    subprocess.run(["tmux", "kill-session", "-t", SESSION_NAME], capture_output=True)


def main():
    global session_pin
    import argparse
    import atexit

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8080)
    parser.add_argument("--no-auth", action="store_true")
    parser.add_argument("--kill", "-k", action="store_true")
    parser.add_argument("command", nargs="*")
    args = parser.parse_args()

    if args.kill:
        cleanup()
        print("終了しました")
        return

    # 常にクリーンアップしてから開始
    cleanup()

    if not args.command:
        print("Usage: tapback-server claude")
        return

    # tmuxがインストールされているか確認
    if subprocess.run(["which", "tmux"], capture_output=True).returncode != 0:
        print("エラー: tmuxがインストールされていません")
        print("  brew install tmux")
        sys.exit(1)

    # 既存のセッションを終了
    subprocess.run(["tmux", "kill-session", "-t", SESSION_NAME], capture_output=True)

    # 新しいtmuxセッションを作成してコマンドを実行
    cmd = " ".join(args.command)
    subprocess.run(["tmux", "new-session", "-d", "-s", SESSION_NAME, cmd])

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
    print(f"  tmux attach -t {SESSION_NAME}  # ローカルで確認")
    print(f"{'=' * 50}\n")

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
