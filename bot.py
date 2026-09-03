import os
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

CARD_WIDTH = 1080
CARD_HEIGHT = 1350

# =========================
# تنظیمات ظاهری
# =========================

BACKGROUND_TOP = (48, 30, 72)
BACKGROUND_BOTTOM = (22, 18, 38)

TEXT_COLOR = (248, 244, 235)
ACCENT_COLOR = (205, 172, 105)
SUBTITLE_COLOR = (190, 175, 150)

BORDER_COLOR = (150, 120, 70)

# فونت‌ها
POEM_FONT = "BNazanin.ttf"
TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"


# =========================
# فونت
# =========================

def get_font(font_name, size):
    return ImageFont.truetype(
        font_name,
        size
    )


# =========================
# پس زمینه گرادیانی
# =========================

def create_gradient_background():

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT)
    )

    pixels = image.load()

    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        r = int(
            BACKGROUND_TOP[0] * (1 - ratio)
            + BACKGROUND_BOTTOM[0] * ratio
        )

        g = int(
            BACKGROUND_TOP[1] * (1 - ratio)
            + BACKGROUND_BOTTOM[1] * ratio
        )

        b = int(
            BACKGROUND_TOP[2] * (1 - ratio)
            + BACKGROUND_BOTTOM[2] * ratio
        )

        for x in range(CARD_WIDTH):
            pixels[x, y] = (r, g, b)

    return image


# =========================
# شکستن خط بر اساس عرض واقعی
# =========================

def wrap_text(draw, text, font, max_width):

    words = text.split()

    if not words:
        return []

    lines = []
    current = words[0]

    for word in words[1:]:

        test = current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test

        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


# =========================
# آماده سازی خطوط شعر
#
# نکته:
# خطوط خالی کاربر حفظ می‌شوند.
# =========================

def prepare_poem_lines(draw, text, font, max_width):

    raw_lines = text.splitlines()

    final_lines = []

    for line in raw_lines:

        # اگر خط کاملاً خالی است،
        # همان خط خالی را نگه می‌داریم.
        if not line.strip():

            final_lines.append(None)

            continue

        wrapped = wrap_text(
            draw,
            line.strip(),
            font,
            max_width
        )

        final_lines.extend(wrapped)

    return final_lines


# =========================
# محاسبه ارتفاع شعر
# =========================

def calculate_text_height(
    draw,
    lines,
    font,
    line_spacing,
    blank_line_spacing
):

    if not lines:
        return 0

    total = 0

    for line in lines:

        # خط خالی
        if line is None:

            total += blank_line_spacing

            continue

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        height = bbox[3] - bbox[1]

        total += height + line_spacing

    # فاصله آخرین خط حذف شود
    if lines:

        last_line = lines[-1]

        if last_line is not None:
            total -= line_spacing

    return total


# =========================
# ساخت کارت شعر
# =========================

def create_poetry_card(text):

    image = create_gradient_background()

    draw = ImageDraw.Draw(image)

    # =========================
    # حاشیه
    # =========================

    margin = 48

    draw.rounded_rectangle(
        (
            margin,
            margin,
            CARD_WIDTH - margin,
            CARD_HEIGHT - margin
        ),
        radius=38,
        outline=BORDER_COLOR,
        width=2
    )

    # =========================
    # عنوان
    # =========================

    title_font = get_font(
        TITLE_FONT,
        48
    )

    title = "شعرکده"

    title_bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = (
        title_bbox[2] - title_bbox[0]
    )

    title_height = (
        title_bbox[3] - title_bbox[1]
    )

    # =========================
    # سروش پلاس
    # =========================

    subtitle_font = get_font(
        SUBTITLE_FONT,
        24
    )

    subtitle = "( سروش پلاس )"

    subtitle_bbox = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )

    subtitle_width = (
        subtitle_bbox[2] - subtitle_bbox[0]
    )

    subtitle_height = (
        subtitle_bbox[3] - subtitle_bbox[1]
    )

    gap = 22

    total_header_width = (
        title_width
        + gap
        + subtitle_width
    )

    header_x = (
        CARD_WIDTH - total_header_width
    ) // 2

    title_y = 105

    # عنوان
    draw.text(
        (
            header_x,
            title_y
        ),
        title,
        font=title_font,
        fill=ACCENT_COLOR
    )

    # سروش پلاس
    subtitle_x = (
        header_x
        + title_width
        + gap
    )

    subtitle_y = (
        title_y
        + title_height
        - subtitle_height
        - 2
    )

    draw.text(
        (
            subtitle_x,
            subtitle_y
        ),
        subtitle,
        font=subtitle_font,
        fill=SUBTITLE_COLOR
    )

    # =========================
    # خط تزئینی
    # =========================

    line_width = 110

    line_y = (
        title_y
        + title_height
        + 25
    )

    draw.line(
        (
            (CARD_WIDTH - line_width) // 2,
            line_y,
            (CARD_WIDTH + line_width) // 2,
            line_y
        ),
        fill=BORDER_COLOR,
        width=2
    )

    # =========================
    # محدوده شعر
    # =========================

    text_left = 100
    text_right = 980

    max_width = text_right - text_left

    text_top = 270
    text_bottom = 1110

    available_height = (
        text_bottom - text_top
    )

    # =========================
    # تنظیمات فاصله
    # =========================

    font_size = 58
    min_font_size = 28

    # فاصله معمول بین خطوط
    line_spacing = 24

    # فاصله‌ای که یک خط خالی ایجاد می‌کند
    blank_line_spacing = 55

    # =========================
    # اندازه خودکار فونت
    # =========================

    while font_size >= min_font_size:

        poem_font = get_font(
            POEM_FONT,
            font_size
        )

        lines = prepare_poem_lines(
            draw,
            text,
            poem_font,
            max_width
        )

        total
