import os
import base64
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

QUOTE_API = "https://quote.yuri.ly/quote/generate.png"


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

        print(
            "sendMessage:",
            response.status_code,
            response.text
        )

        return response

    except Exception as error:

        print(
            "sendMessage error:",
            error
        )

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

        print(
            "sendPhoto:",
            response.status_code,
            response.text
        )

        return response

    except Exception as error:

        print(
            "sendPhoto error:",
            error
        )

        return None


def create_poetry_card(text, user_id):

    payload = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1e182d",
        "width": 512,
        "height": 768,
        "scale": 2,
        "emojiBrand": "apple",
        "messages": [
            {
                "from": {
                    "id": user_id,
                    "name": "شعرکده"
                },
                "text": text,
                "entities": [],
                "avatar": False
            }
        ]
    }

    try:

        response = requests.post(
            QUOTE_API,
            json=payload,
            timeout=120
        )

        print(
            "QUOTE API:",
            response.status_code,
            response.headers.get("content-type")
        )

        if not response.ok:

            print(
                "QUOTE API ERROR:",
                response.text
            )

            return None

        filename = "/tmp/poetry_card.png"

        with open(filename, "wb") as file:

            file.write(response.content)

        print(
            f"Quote image created: {filename}"
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
            "\u0633\u0644\u0627\u0645 \ud83d\udc4b\n\n"
            "\ud83d\uddbc\ufe0f \u0628\u0647 \u0628\u0627\u062a \u06a9\u0627\u0631\u062a \u0634\u0639\u0631 \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc.\n\n"
            "\u0634\u0639\u0631\u062a \u0631\u0627 \u0647\u0645\u06cc\u0646\u200c\u062c\u0627 \u0628\u0641\u0631\u0633\u062a \u062a\u0627 \u0628\u0631\u0627\u06cc\u062a \u06a9\u0627\u0631\u062a \u0634\u0639\u0631 \u0628\u0633\u0627\u0632\u0645. \u2728"
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
                "\u274c \u0645\u062a\u0623\u0633\u0641\u0627\u0646\u0647 \u062f\u0631 \u0633\u0627\u062e\u062a \u06a9\u0627\u0631\u062a \u0645\u0634\u06a9\u0644\u06cc \u067e\u06cc\u0634 \u0622\u0645\u062f."
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
                "\u2705 \u06a9\u0627\u0631\u062a \u0633\u0627\u062e\u062a\u0647 \u0634\u062f\u060c \u0627\u0645\u0627 \u0627\u0631\u0633\u0627\u0644 \u062a\u0635\u0648\u06cc\u0631 \u0645\u0648\u0641\u0642 \u0646\u0634\u062f."
            )

    except Exception as error:

        print(
            "Webhook error:",
            error
        )

        send_message(
            user_id,
            "\u274c \u0645\u0634\u06a9\u0644\u06cc \u067e\u06cc\u0634 \u0622\u0645\u062f."
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


