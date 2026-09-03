import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

QUOTE_API = os.environ.get(
    "QUOTE_API",
    "https://quote-api-0szx.onrender.com/generate.png"
)


def send_message(chat_id, text):

    try:
        response = requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=30
        )

        print("sendMessage:", response.status_code, response.text)

        return response

    except Exception as error:
        print("sendMessage error:", error)
        return None


def send_photo(chat_id, filename):

    try:

        with open(filename, "rb") as photo:

            response = requests.post(
                f"{API}/sendPhoto",
                data={
                    "chat_id": chat_id
                },
                files={
                    "photo": (
                        "poetry_card.png",
                        photo,
                        "image/png"
                    )
                },
                timeout=60
            )

        print("sendPhoto:", response.status_code, response.text)

        return response

    except Exception as error:
        print("sendPhoto error:", error)
        return None


def create_poetry_card(text, user_id):

    payload = {
        "type": "quote",
        "format": "png",

        # پس‌زمینه گرادیانی به‌جای مشکی ساده
        "backgroundColor": "#17122b/#4b245f",

        # کارت تقریباً مربعی
        "width": 600,
        "height": 600,

        # کیفیت خروجی
        "scale": 2,

        "emojiBrand": "apple",

        "messages": [
            {
                "from": {
                    "id": user_id,
                    "name": "شعرکده"
                },

                "text": text,

                # کل شعر بولد و خواناتر
                "entities": [
                    {
                        "type": "bold",
                        "offset": 0,
                        "length": len(text)
                    }
                ],

                # بدون آواتار
                "avatar": False
            }
        ]
    }

    try:

        print("QUOTE API:", QUOTE_API)
        print("QUOTE PAYLOAD:", payload)

        response = requests.post(
            QUOTE_API,
            json=payload,
            timeout=120
        )

        print(
            "QUOTE API RESPONSE:",
            response.status_code,
            response.headers.get("content-type")
        )

        if not response.ok:

            print(
                "QUOTE API ERROR:",
                response.text
            )

            return None

        content_type = response.headers.get(
            "content-type",
            ""
        )

        if "image" not in content_type:

            print(
                "QUOTE API returned non-image:",
                response.text
            )

            return None

        filename = "/tmp/poetry_card.png"

        with open(filename, "wb") as file:
            file.write(response.content)

        print(
            "Quote image created:",
            filename
        )

        return filename

    except Exception as error:

        print(
            "Quote API error:",
            error
        )

        return None


@app.route("/")
def home():

    return "Poetry Card Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json(
        silent=True
    ) or {}

    print(
        "UPDATE:",
        update
    )

    message = update.get("message") or {}

    text = message.get("text")

    chat = message.get("chat") or {}

    user_id = chat.get("id")

    if not user_id:
        return "OK", 200

    if not text:
        return "OK", 200

    if text == "/start":

        send_message(
            user_id,
            "سلام 👋\n\n"
            "🖼️ به بات کارت شعر خوش آمدی.\n\n"
            "شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨"
        )

        return "OK", 200

    try:

        filename = create_poetry_card(
            text,
            user_id
        )

        if not filename:

            send_message(
                user_id,
                "❌ متأسفانه در ساخت کارت مشکلی پیش آمد."
            )

            return "OK", 200

        photo_response = send_photo(
            user_id,
            filename
        )

        if photo_response is not None and photo_response.ok:

            print(
                "Poetry card sent successfully."
            )

        else:

            print(
                "Poetry card sending failed."
            )

            send_message(
                user_id,
                "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد."
            )

    except Exception as error:

        print(
            "Webhook error:",
            error
        )

        send_message(
            user_id,
            "❌ مشکلی پیش آمد."
        )

    return "OK", 200


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
            )
