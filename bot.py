import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"


@app.route("/")
def home():
    return "Poetry Card Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message") or {}
    text = message.get("text")
    chat = message.get("chat") or {}
    user_id = chat.get("id")

    if text == "/start":
        requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": user_id,
                "text": (
                    "سلام 👋\n\n"
                    "🖼️ به بات کارت شعر خوش آمدی.\n\n"
                    "شعرت را بفرست تا برایت یک کارت زیبا بسازم. ✨"
                )
            },
            timeout=20
        )

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
