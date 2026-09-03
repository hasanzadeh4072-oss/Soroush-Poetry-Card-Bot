import os
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"


# -----------------------------
# تنظیمات کارت
# -----------------------------

CARD_WIDTH = 1080
CARD_HEIGHT = 1350

BACKGROUND = (30, 24, 45)
TEXT_COLOR = (245, 240, 230)
ACCENT_COLOR = (190, 160, 100)


# -----------------------------
# فونت
# -----------------------------

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def prepare_persian_text(text):
    """
    آماده‌سازی متن فارسی برای نمایش صحیح
    """
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)


# -----------------------------
# ساخت کارت شعر
# -----------------------------

def create_poetry_card(text):

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT),
        BACKGROUND
    )

    draw = ImageDraw.Draw(image)

    # حاشیه
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

    title = prepare_persian_text("شعر
