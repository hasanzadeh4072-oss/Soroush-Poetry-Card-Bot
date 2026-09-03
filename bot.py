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
    title = prepare_persian_text("شعرکده")

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

    # اگر شعر یک‌خطی باشد، آن را به چند خط تقسیم می‌کنیم
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
            prepare_persian_text("متن خالی است")
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
        "کارت شعر"
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

    # شروع بات
    if text == "/start":

        send_message(
            user_id,
            "سلام 👋\n\n"
            "🖼️
