import os
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

CARD_WIDTH = 1080
CARD_HEIGHT = 1350

BACKGROUND = (30, 24, 45)
TEXT_COLOR = (245, 240, 230)
ACCENT_COLOR = (190, 160, 100)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def prepare_persian_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)


def create_poetry_card(text):

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT),
        BACKGROUND
    )

    draw = ImageDraw.Draw(image)

    margin = 55

    draw.rounded_rectangle(
        (
            margin,
            margin,
            CARD_WIDTH - margin,
            CARD_HEIGHT - margin
        ),
        radius=35,
        outline=ACCENT_COLOR,
        width=3
    )

    # عنوان
    title_font = get_font(42)

    title = prepare_persian_text(
        "\u0634\u0639\u0631\u06a9\u062f\u0647"
    )

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = bbox[2] - bbox[0]

    draw.text(
        (
            (CARD_WIDTH - title_width) // 2,
            120
        ),
        title,
        font=title_font,
        fill=ACCENT_COLOR
    )

    # متن شعر
    poem_font = get_font(48)

    lines = text.splitlines()

    if len(lines) == 1:

        words = text.split()
        lines = []
        current = ""

        for word in words:

            test = current + " " + word

            if len(test) > 28:

                if current:
                    lines.append(current.strip())

                current = word

            else:
                current = test

        if current:
            lines.append(current.strip())

    prepared_lines = []

    for line in lines:

        if line.strip():

            prepared_lines.append(
                prepare_persian_text(line)
            )

    if not prepared_lines:

        prepared_lines = [
            prepare_persian_text(
                "\u0645\u062a\u0646 \u062e\u0627\u0644\u06cc \u0627\u0633\u062a"
            )
        ]

    line_spacing = 28

    total_height = 0
    heights = []

    for line in prepared_lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=poem_font
        )

        height = bbox[3] - bbox[1]

        heights.append(height)
        total_height += height + line_spacing

    total_height -= line_spacing

    y = (CARD_HEIGHT - total_height) // 2

    for index, line in enumerate(prepared_lines):

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=poem_font
        )

        width = bbox[2] - bbox[0]

        x = (CARD_WIDTH - width) // 2

        draw.text(
            (x, y),
            line,
            font=poem_font,
            fill=TEXT_COLOR
        )

        y += heights[index] + line_spacing

    # پایین کارت
    footer_font = get_font(28)

    footer = prepare_persian_text(
        "\u06a9\u0627\u0631\u062a \u0634\u0639\u0631"
    )

    bbox = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font
    )

    footer_width = bbox[2] - bbox[0]

    draw.text(
        (
            (CARD_WIDTH - footer_width) // 2,
            CARD_HEIGHT - 120
        ),
        footer,
        font=footer_font,
        fill=ACCENT_COLOR
    )

    filename = "/tmp/poetry_card.png"

    image.save(
        filename,
        "PNG"
    )

    return filename


def send_message(chat_id, text):

    try:

        response = requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=20
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


@app.route("/")
def home():

    return "Poetry Card Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json(
        silent=True
    ) or {}

    print("UPDATE:", update)

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

        filename = create_poetry_card(text)

        print(
            f"Poetry card created: {filename}"
        )

        # ارسال تصویر
        photo_response = send_photo(
            user_id,
            filename
        )

        # اگر ارسال عکس موفق بود، پیام موفقیت نمی‌فرستیم
        if photo_response is not None and photo_response.ok:

            print("Poetry card sent successfully.")

        else:

            print("Photo sending failed.")

            send_message(
                user_id,
                "\u2705 \u06a9\u0627\u0631\u062a \u0633\u0627\u062e\u062a\u0647 \u0634\u062f\u060c \u0627\u0645\u0627 \u0627\u0631\u0633\u0627\u0644 \u062a\u0635\u0648\u06cc\u0631 \u0645\u0648\u0641\u0642 \u0646\u0634\u062f."
            )

    except Exception as error:

        print(
            "Card creation error:",
            error
        )

        send_message(
            user_id,
            "\u274c \u0647\u0646\u06af\u0627\u0645 \u0633\u0627\u062e\u062a \u06a9\u0627\u0631\u062a \u0645\u0634\u06a9\u0644\u06cc \u067e\u06cc\u0634 \u0622\u0645\u062f."
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


