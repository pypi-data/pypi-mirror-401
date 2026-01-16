#!/usr/bin/env python3
"""
Tapback Server - Human-in-the-Loop Input Tool
スマホから Yes/No または自由テキストを返せるローカルサーバー
"""

import uuid
import time
import random
import secrets
import threading
from flask import Flask, request, jsonify, render_template_string, make_response

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 状態管理（MVP: メモリ内で1件のみ）
current_question = None
question_lock = threading.Lock()

# セキュリティ: PIN認証
session_pin = None  # サーバー起動時に生成
authenticated_tokens = set()  # 認証済みトークン

# PIN入力UI
PIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tapback - 認証</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container { max-width: 400px; width: 100%; text-align: center; }
        .logo { font-size: 2rem; margin-bottom: 1rem; color: #8b5cf6; }
        .subtitle { color: #888; margin-bottom: 2rem; }
        .pin-input {
            width: 100%;
            padding: 1.5rem;
            font-size: 2rem;
            text-align: center;
            letter-spacing: 1rem;
            border: 2px solid #333;
            border-radius: 12px;
            background: #16213e;
            color: #eee;
            margin-bottom: 1rem;
        }
        .pin-input:focus { outline: none; border-color: #8b5cf6; }
        .btn {
            width: 100%;
            padding: 1.2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            background: #8b5cf6;
            color: white;
            cursor: pointer;
        }
        .btn:active { transform: scale(0.98); }
        .error { color: #ef4444; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Tapback</div>
        <div class="subtitle">ターミナルに表示されたPINを入力</div>
        <form method="POST" action="/auth">
            <input type="text" name="pin" class="pin-input" maxlength="4" pattern="[0-9]{4}"
                   inputmode="numeric" autocomplete="off" placeholder="0000" required>
            <button type="submit" class="btn">認証</button>
        </form>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
    </div>
</body>
</html>
"""

# スマホ用UI HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tapback</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        .logo {
            font-size: 2rem;
            margin-bottom: 2rem;
            color: #8b5cf6;
        }
        .message {
            font-size: 1.5rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: #16213e;
            border-radius: 16px;
            word-break: break-word;
        }
        .no-question {
            color: #888;
            font-size: 1.2rem;
        }
        .buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
        }
        .btn {
            padding: 1.5rem 3rem;
            font-size: 1.5rem;
            font-weight: bold;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: transform 0.1s, opacity 0.1s;
            min-width: 120px;
        }
        .btn:active {
            transform: scale(0.95);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .btn-yes {
            background: #22c55e;
            color: white;
        }
        .btn-no {
            background: #ef4444;
            color: white;
        }
        .btn-submit {
            background: #8b5cf6;
            color: white;
            width: 100%;
        }
        .text-input {
            width: 100%;
            padding: 1rem;
            font-size: 1.2rem;
            border: 2px solid #333;
            border-radius: 12px;
            background: #16213e;
            color: #eee;
            resize: vertical;
            min-height: 120px;
            margin-bottom: 1rem;
        }
        .text-input:focus {
            outline: none;
            border-color: #8b5cf6;
        }
        .status {
            margin-top: 2rem;
            padding: 1rem;
            border-radius: 12px;
            font-size: 1.2rem;
        }
        .status-success {
            background: #22c55e33;
            color: #22c55e;
        }
        .status-error {
            background: #ef444433;
            color: #ef4444;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Tapback</div>

        <div id="question-area">
            {% if question %}
                <div class="message">{{ question.message }}</div>

                {% if question.type == 'yesno' %}
                <div class="buttons">
                    <button class="btn btn-yes" onclick="sendAnswer('yes')">YES</button>
                    <button class="btn btn-no" onclick="sendAnswer('no')">NO</button>
                </div>
                {% else %}
                <textarea class="text-input" id="text-answer" placeholder="回答を入力..."></textarea>
                <button class="btn btn-submit" onclick="sendTextAnswer()">送信</button>
                {% endif %}
            {% else %}
                <div class="no-question">待機中の質問はありません</div>
            {% endif %}
        </div>

        <div id="status" class="status hidden"></div>
    </div>

    <script>
        const questionId = "{{ question.id if question else '' }}";
        const authToken = "{{ token }}";

        async function sendAnswer(answer) {
            if (!questionId) return;

            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(btn => btn.disabled = true);

            try {
                const response = await fetch('/answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: questionId, answer: answer, token: authToken })
                });

                if (response.ok) {
                    showStatus('送信しました', 'success');
                    document.getElementById('question-area').innerHTML =
                        '<div class="no-question">送信済み</div>';
                } else {
                    showStatus('エラーが発生しました', 'error');
                    buttons.forEach(btn => btn.disabled = false);
                }
            } catch (e) {
                showStatus('通信エラー', 'error');
                buttons.forEach(btn => btn.disabled = false);
            }
        }

        function sendTextAnswer() {
            const text = document.getElementById('text-answer').value.trim();
            if (!text) {
                showStatus('テキストを入力してください', 'error');
                return;
            }
            sendAnswer(text);
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status status-' + type;
            status.classList.remove('hidden');
        }

        // 5秒ごとに新しい質問をチェック
        if (!questionId) {
            setInterval(() => location.reload(), 5000);
        }
    </script>
</body>
</html>
"""


def is_authenticated(req):
    """リクエストが認証済みか確認"""
    token = req.cookies.get("tapback_token")
    return token in authenticated_tokens


@app.route("/")
def index():
    """スマホ用UIを表示"""
    # 認証チェック
    if not is_authenticated(request):
        return render_template_string(PIN_TEMPLATE, error=None)

    token = request.cookies.get("tapback_token")
    with question_lock:
        q = (
            current_question
            if current_question and current_question["status"] == "waiting"
            else None
        )
    return render_template_string(HTML_TEMPLATE, question=q, token=token)


@app.route("/auth", methods=["POST"])
def auth():
    """PIN認証"""
    pin = request.form.get("pin", "")

    if pin == session_pin:
        # 認証成功: トークン発行
        token = secrets.token_hex(16)
        authenticated_tokens.add(token)

        response = make_response(
            render_template_string(HTML_TEMPLATE, question=None, token=token)
        )
        response.set_cookie(
            "tapback_token", token, httponly=True, samesite="Strict", max_age=86400
        )
        return response
    else:
        return render_template_string(PIN_TEMPLATE, error="PINが間違っています")


@app.route("/ask", methods=["POST"])
def ask():
    """質問を登録"""
    global current_question

    data = request.get_json()
    message = data.get("message", "")
    q_type = data.get("type", "yesno")
    timeout = data.get("timeout", 300)

    if not message:
        return jsonify({"error": "message is required"}), 400

    if q_type not in ("yesno", "text"):
        return jsonify({"error": "type must be yesno or text"}), 400

    question_id = str(uuid.uuid4())

    with question_lock:
        current_question = {
            "id": question_id,
            "message": message,
            "type": q_type,
            "status": "waiting",
            "answer": None,
            "timeout": timeout,
            "created_at": time.time(),
        }

    return jsonify({"id": question_id})


@app.route("/wait/<question_id>")
def wait(question_id):
    """回答が来るまでブロックして待機"""
    global current_question

    while True:
        with question_lock:
            if current_question is None or current_question["id"] != question_id:
                return jsonify({"error": "question not found"}), 404

            # タイムアウトチェック
            elapsed = time.time() - current_question["created_at"]
            if elapsed > current_question["timeout"]:
                current_question["status"] = "timeout"
                return jsonify({"status": "timeout"}), 408

            # 回答済みチェック
            if current_question["status"] == "answered":
                answer = current_question["answer"]
                current_question = None  # クリア
                return jsonify({"answer": answer})

        time.sleep(0.5)


@app.route("/answer", methods=["POST"])
def answer():
    """スマホからの回答送信"""
    global current_question

    data = request.get_json()
    question_id = data.get("id")
    answer_value = data.get("answer")
    token = data.get("token")

    # 認証チェック
    if token not in authenticated_tokens:
        return jsonify({"error": "unauthorized"}), 401

    if not question_id or answer_value is None:
        return jsonify({"error": "id and answer are required"}), 400

    with question_lock:
        if current_question is None or current_question["id"] != question_id:
            return jsonify({"error": "question not found"}), 404

        if current_question["status"] != "waiting":
            return jsonify({"error": "question already answered or timeout"}), 400

        current_question["status"] = "answered"
        current_question["answer"] = answer_value

    return jsonify({"success": True})


@app.route("/status")
def status():
    """現在の状態を取得（デバッグ用）"""
    with question_lock:
        return jsonify({"question": current_question})


def get_local_ips():
    """全てのローカルIPアドレスとインターフェース名を取得"""
    import subprocess

    ips = []
    try:
        result = subprocess.run(
            ["ifconfig"], capture_output=True, text=True, timeout=5
        )
        current_iface = ""
        for line in result.stdout.split("\n"):
            if line and not line.startswith("\t") and not line.startswith(" "):
                current_iface = line.split(":")[0]
            if "inet " in line and "127.0.0.1" not in line:
                parts = line.strip().split()
                idx = parts.index("inet") + 1
                if idx < len(parts):
                    ip = parts[idx]
                    # インターフェース名をわかりやすく
                    if current_iface.startswith("en"):
                        label = "Wi-Fi"
                    elif current_iface.startswith("utun") or current_iface.startswith("tun"):
                        label = "VPN"
                    elif current_iface.startswith("bridge"):
                        label = "VM"
                    else:
                        label = current_iface
                    # Wi-Fi (192.168.x.x) を優先
                    if ip.startswith("192.168.0."):
                        ips.insert(0, (ip, label))
                    else:
                        ips.append((ip, label))
    except:
        pass

    return ips if ips else [("127.0.0.1", "Local")]


def main():
    """CLI エントリーポイント"""
    global session_pin

    import argparse

    parser = argparse.ArgumentParser(description="Tapback Server")
    parser.add_argument(
        "--port", "-p", type=int, default=8080, help="ポート番号 (default: 8080)"
    )
    parser.add_argument(
        "--host", "-H", type=str, default="0.0.0.0", help="ホスト (default: 0.0.0.0)"
    )
    parser.add_argument("--no-auth", action="store_true", help="PIN認証を無効化")
    args = parser.parse_args()

    # PIN生成
    if args.no_auth:
        session_pin = None
        # 認証なしモード: ダミートークンを追加
        authenticated_tokens.add("no-auth")
    else:
        session_pin = f"{random.randint(0, 9999):04d}"

    local_ips = get_local_ips()
    print(f"\n{'=' * 50}")
    print(f"  Tapback Server")
    print(f"{'=' * 50}")
    print(f"  Local: http://127.0.0.1:{args.port}")
    for ip, label in local_ips:
        print(f"  {label}: http://{ip}:{args.port}")
    if session_pin:
        print(f"{'=' * 50}")
        print(f"  PIN: {session_pin}")
    print(f"{'=' * 50}")
    print(f"  スマホからNetwork URLにアクセスしてください")
    print(f"{'=' * 50}\n")

    app.run(host=args.host, port=args.port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
