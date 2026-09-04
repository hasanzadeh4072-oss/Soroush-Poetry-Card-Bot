# ============================================
# Soroush Plus Poetry Card Bot
# ============================================

import os
import time
import threading
import requests

from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================
# CONFIG
# ============================================

TOKEN = os.getenv("SOROUSH_TOKEN")

API_BASE = f"https://api.splus.ir/bot{TOKEN}"

CARD_WIDTH = 1080
CARD_HEIGHT = 1080

BG_IMAGE_PATH = "background.png"

TITLE_FONT = "BTitrBd.ttf"
POEM_FONT = "BNazanin.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"

OUTER_FRAME_WIDTH = 3
INNER_FRAME_WIDTH = 2
ORNAMENT_LINE_WIDTH = 2
SIDE_LINE_WIDTH = 2
PANEL_OUTLINE_WIDTH = 2
PANEL_INNER_WIDTH = 1
FOOTER_LINE_WIDTH = 2


# ============================================
# PALETTES
# ============================================

PALETTES = [
    {
        "name": "بنفش سلطنتی",
        "start": (42, 20, 76),
        "end": (112, 61, 158),
        "frame": (224, 192, 255, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (255, 250, 255, 255),
        "accent": (245, 216, 255, 255),
        "ornament": (220, 175, 255, 190),
        "side_line": (255, 255, 255, 255),
        "side_dot": (255, 220, 255, 255),
        "panel_outline": (255, 255, 255, 255, 38),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "آبی شبانه",
        "start": (10, 30, 65),
        "end": (26, 91, 145),
        "frame": (170, 220, 255, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (245, 252, 255, 255),
        "accent": (185, 230, 255, 255),
        "ornament": (150, 215, 255, 190),
        "side_line": (220, 245, 255, 255),
        "side_dot": (200, 235, 255, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 20),
    },
    {
        "name": "سبز زمردی",
        "start": (8, 48, 39),
        "end": (25, 119, 92),
        "frame": (160, 235, 210, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (242, 255, 250, 255),
        "accent": (185, 255, 225, 255),
        "ornament": (145, 235, 205, 190),
        "side_line": (220, 255, 245, 255),
        "side_dot": (190, 250, 225, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "قرمز شرابی",
        "start": (65, 12, 27),
        "end": (145, 35, 57),
        "frame": (255, 190, 205, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (255, 245, 248, 255),
        "accent": (255, 200, 215, 255),
        "ornament": (255, 160, 185, 190),
        "side_line": (255, 225, 235, 255),
        "side_dot": (255, 195, 215, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "فیروزه‌ای",
        "start": (5, 66, 73),
        "end": (20, 150, 153),
        "frame": (170, 245, 240, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (240, 255, 255, 255),
        "accent": (180, 255, 250, 255),
        "ornament": (145, 235, 230, 190),
        "side_line": (220, 255, 255, 255),
        "side_dot": (190, 250, 245, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "طلایی",
        "start": (75, 50, 12),
        "end": (170, 120, 25),
        "frame": (255, 225, 145, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (255, 250, 225, 255),
        "accent": (255, 220, 125, 255),
        "ornament": (245, 195, 90, 190),
        "side_line": (255, 240, 190, 255),
        "side_dot": (255, 220, 130, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "صورتی ملایم",
        "start": (91, 36, 66),
        "end": (180, 90, 130),
        "frame": (255, 205, 225, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (255, 248, 253, 255),
        "accent": (255, 205, 230, 255),
        "ornament": (255, 175, 215, 190),
        "side_line": (255, 230, 242, 255),
        "side_dot": (255, 205, 225, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "نارنجی گرم",
        "start": (90, 37, 10),
        "end": (190, 93, 25),
        "frame": (255, 215, 160, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (255, 250, 235, 255),
        "accent": (255, 215, 155, 255),
        "ornament": (255, 190, 120, 190),
        "side_line": (255, 235, 200, 255),
        "side_dot": (255, 215, 160, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
    {
        "name": "ذغالی طلایی",
        "start": (25, 25, 27),
        "end": (70, 64, 45),
        "frame": (235, 205, 125, 180),
        "frame_inner": (255, 255, 255, 70),
        "text": (250, 245, 225, 255),
        "accent": (235, 205, 125, 255),
        "ornament": (210, 175, 95, 190),
        "side_line": (245, 225, 170, 255),
        "side_dot": (235, 205, 125, 255),
        "panel_outline": (255, 255, 255, 255),
        "panel_inner": (255, 255, 255, 255, 20),
    },
]


# ============================================
# GLOBAL CACHE
# ============================================

FONT_CACHE = {}
CACHED_CARD_BACKGROUNDS = {}

pending_poems = {}
pending_lock = threading.Lock()


# ============================================
# FONT
# ============================================

def get_font(font_name, size):
    key = (font_name, size)

    if key not in FONT_CACHE:
        FONT_CACHE[key] = ImageFont.truetype(
            font_name,
            size
        )

    return FONT_CACHE[key]


# ============================================
# BACKGROUND
# ============================================

def create_gradient_background(palette):

    image = Image.new(
        "RGB",
        (1, CARD_HEIGHT)
    )

    pixels = image.load()

    start = palette["start"]
    end = palette["end"]

    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        r = int(
            start[0]
            + (end[0] - start[0]) * ratio
        )

        g = int(
            start[1]
            + (end[1] - start[1]) * ratio
        )

        b = int(
            start[2]
            + (end[2] - start[2]) * ratio
        )

        pixels[0, y] = (
            r,
            g,
            b
        )

    image = image.resize(
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
        Image.Resampling.NEAREST
    )

    return image.convert("RGBA")


def build_cached_backgrounds():

    print(
        "Building cached card backgrounds..."
    )

    total_start = time.perf_counter()

    for palette in PALETTES:

        start = time.perf_counter()

        print(
            f"Preparing background: "
            f"{palette['name']}"
        )

        CACHED_CARD_BACKGROUNDS[
            palette["name"]
        ] = create_gradient_background(
            palette
        )

        print(
            f"Background ready: "
            f"{time.perf_counter() - start:.4f}s"
        )

    print(
        "All card backgrounds cached."
    )

    print(
        f"Background cache build time: "
        f"{time.perf_counter() - total_start:.2f}s"
    )


# ============================================
# TEXT HELPERS
# ============================================

def prepare_poem_lines(
    draw,
    text,
    font,
    max_width
):

    result = []

    paragraphs = text.splitlines()

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            result.append(None)
            continue

        words = paragraph.split()

        current = ""

        for word in words:

            test = (
                word
                if not current
                else current + " " + word
            )

            bbox = draw.textbbox(
                (0, 0),
                test,
                font=font
            )

            width = (
                bbox[2]
                - bbox[0]
            )

            if width <= max_width:

                current = test

            else:

                if current:
                    result.append(current)

                current = word

        if current:
            result.append(current)

    return result


def calculate_text_height(
    draw,
    lines,
    font,
    line_spacing,
    blank_line_spacing
):

    total = 0

    for line in lines:

        if line is None:
            total += blank_line_spacing
            continue

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        height = (
            bbox[3]
            - bbox[1]
        )

        total += (
            height
            + line_spacing
        )

    if total > 0:
        total -= line_spacing

    return total


# ============================================
# CARD CREATION
# ============================================

def create_poetry_card(
    text,
    palette,
    branded=True
):

    total_start = time.perf_counter()

    # ----------------------------------------
    # 01 - Background
    # ----------------------------------------

    stage_start = time.perf_counter()

    cached_background = (
        CACHED_CARD_BACKGROUNDS.get(
            palette["name"]
        )
    )

    if cached_background is not None:
        image = cached_background.copy()
    else:
        image = create_gradient_background(
            palette
        )

    image = image.convert("RGBA")

    draw = ImageDraw.Draw(image)

    print(
        f"[TIMING] 01 - Background copy: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 02 - Outer frame
    # ----------------------------------------

    stage_start = time.perf_counter()

    margin = 40

    draw.rounded_rectangle(
        (
            margin,
            margin,
            CARD_WIDTH - margin,
            CARD_HEIGHT - margin
        ),
        radius=42,
        outline=palette["frame"],
        width=OUTER_FRAME_WIDTH
    )

    print(
        f"[TIMING] 02 - Outer frame: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 03 - Inner frame
    # ----------------------------------------

    stage_start = time.perf_counter()

    inner_margin = 49

    draw.rounded_rectangle(
        (
            inner_margin,
            inner_margin,
            CARD_WIDTH - inner_margin,
            CARD_HEIGHT - inner_margin
        ),
        radius=35,
        outline=palette["frame_inner"],
        width=INNER_FRAME_WIDTH
    )

    print(
        f"[TIMING] 03 - Inner frame: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 04 - Header
    # کارت شعر کوچک در بالا
    # ----------------------------------------

    stage_start = time.perf_counter()

    header_font = get_font(
        FOOTER_FONT,
        23
    )

    header_text = "کارت شعر"

    header_bbox = draw.textbbox(
        (0, 0),
        header_text,
        font=header_font
    )

    header_width = (
        header_bbox[2]
        - header_bbox[0]
    )

    header_x = (
        CARD_WIDTH
        - header_width
    ) // 2

    header_y = 78

    draw.text(
        (
            header_x,
            header_y
        ),
        header_text,
        font=header_font,
        fill=palette["accent"]
    )

    # خط تزئینی زیر کارت شعر

    center_x = CARD_WIDTH // 2

    header_line_y = 116

    draw.line(
        (
            center_x - 35,
            header_line_y,
            center_x - 10,
            header_line_y
        ),
        fill=palette["ornament"],
        width=FOOTER_LINE_WIDTH
    )

    draw.line(
        (
            center_x + 10,
            header_line_y,
            center_x + 35,
            header_line_y
        ),
        fill=palette["ornament"],
        width=FOOTER_LINE_WIDTH
    )

    diamond_size = 4

    draw.polygon(
        [
            (
                center_x,
                header_line_y - diamond_size
            ),
            (
                center_x + diamond_size,
                header_line_y
            ),
            (
                center_x,
                header_line_y + diamond_size
            ),
            (
                center_x - diamond_size,
                header_line_y
            )
        ],
        fill=palette["accent"]
    )

    # ----------------------------------------
    # سروش پلاس
    # زیر کارت شعر در بالای کارت
    # ----------------------------------------

    sub_font = get_font(
        FOOTER_FONT,
        23
    )

    subtitle = "( سروش پلاس )"

    subtitle_bbox = draw.textbbox(
        (0, 0),
        subtitle,
        font=sub_font
    )

    subtitle_width = (
        subtitle_bbox[2]
        - subtitle_bbox[0]
    )

    subtitle_x = (
        CARD_WIDTH
        - subtitle_width
    ) // 2

    subtitle_y = 126

    draw.text(
        (
            subtitle_x,
            subtitle_y
        ),
        subtitle,
        font=sub_font,
        fill=palette["accent"]
    )

    print(
        f"[TIMING] 04 - Header: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 05 - Text preparation
    # ----------------------------------------

    stage_start = time.perf_counter()

    text_left = 75
    text_right = 1005

    text_top = 218
    text_bottom = 895

    max_width = (
        text_right
        - text_left
    )

    available_height = (
        text_bottom
        - text_top
    )

    font_size = 62
    min_font_size = 28

    line_spacing = 16
    blank_line_spacing = 44

    lines = []
    font_iterations = 0

    while font_size >= min_font_size:

        font_iterations += 1

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

        total_height = calculate_text_height(
            draw,
            lines,
            poem_font,
            line_spacing,
            blank_line_spacing
        )

        if total_height <= available_height:
            break

        font_size -= 2

    if not lines:

        poem_font = get_font(
            POEM_FONT,
            48
        )

        lines = [
            "متن خالی است"
        ]

    total_height = calculate_text_height(
        draw,
        lines,
        poem_font,
        line_spacing,
        blank_line_spacing
    )

    print(
        f"[TIMING] 05 - Text preparation: "
        f"{time.perf_counter() - stage_start:.4f}s "
        f"| font={font_size} "
        f"| iterations={font_iterations} "
        f"| lines={len(lines)}"
    )

    # ----------------------------------------
    # 06 - Glass panel
    # ----------------------------------------

    stage_start = time.perf_counter()

    panel_top = max(
        text_top - 38,
        160
    )

    panel_bottom = min(
        text_bottom + 38,
        940
    )

    panel = Image.new(
        "RGBA",
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(
        panel
    )

    panel_draw.rounded_rectangle(
        (
            62,
            panel_top + 4,
            1018,
            panel_bottom + 6
        ),
        radius=45,
        fill=(0, 0, 0, 34)
    )

    panel_draw.rounded_rectangle(
        (
            62,
            panel_top,
            1018,
            panel_bottom
        ),
        radius=45,
        fill=(255, 255, 255, 14),
        outline=palette["panel_outline"],
        width=PANEL_OUTLINE_WIDTH
    )

    panel_draw.rounded_rectangle(
        (
            72,
            panel_top + 10,
            1008,
            panel_bottom - 10
        ),
        radius=37,
        outline=palette["panel_inner"],
        width=PANEL_INNER_WIDTH
    )

    panel = panel.filter(
        ImageFilter.GaussianBlur(0.35)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        panel
    )

    draw = ImageDraw.Draw(image)

    print(
        f"[TIMING] 06 - Glass panel: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 07 - Side ornaments
    # ----------------------------------------

    stage_start = time.perf_counter()

    deco_y = (
        text_top
        + available_height // 2
    )

    draw.line(
        (
            79,
            deco_y - 30,
            79,
            deco_y + 30
        ),
        fill=palette["side_line"],
        width=SIDE_LINE_WIDTH
    )

    draw.ellipse(
        (
            76,
            deco_y - 3,
            82,
            deco_y + 3
        ),
        fill=palette["side_dot"]
    )

    draw.line(
        (
            1001,
            deco_y - 30,
            1001,
            deco_y + 30
        ),
        fill=palette["side_line"],
        width=SIDE_LINE_WIDTH
    )

    draw.ellipse(
        (
            998,
            deco_y - 3,
            1004,
            deco_y + 3
        ),
        fill=palette["side_dot"]
    )

    print(
        f"[TIMING] 07 - Side ornaments: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 08 - Poem drawing
    # ----------------------------------------

    stage_start = time.perf_counter()

    y = (
        text_top
        + (
            available_height
            - total_height
        ) // 2
    )

    for line in lines:

        if line is None:

            y += blank_line_spacing

            continue

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=poem_font
        )

        width = (
            bbox[2]
            - bbox[0]
        )

        height = (
            bbox[3]
            - bbox[1]
        )

        x = (
            CARD_WIDTH
            - width
        ) // 2

        draw.text(
            (
                x,
                y
            ),
            line,
            font=poem_font,
            fill=palette["text"]
        )

        y += (
            height
            + line_spacing
        )

    print(
        f"[TIMING] 08 - Poem drawing: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 09 - Footer
    # شعرکده در پایین
    # ----------------------------------------

    stage_start = time.perf_counter()

    if branded:

        brand_font = get_font(
            TITLE_FONT,
            42
        )

        brand_text = "شعرکده"

        brand_bbox = draw.textbbox(
            (0, 0),
            brand_text,
            font=brand_font
        )

        brand_width = (
            brand_bbox[2]
            - brand_bbox[0]
        )

        brand_x = (
            CARD_WIDTH
            - brand_width
        ) // 2

        brand_line_y = 924

        # خط تزئینی بالای شعرکده

        draw.line(
            (
                center_x - 55,
                brand_line_y,
                center_x - 10,
                brand_line_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

        draw.line(
            (
                center_x + 10,
                brand_line_y,
                center_x + 55,
                brand_line_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

        diamond_size = 4

        draw.polygon(
            [
                (
                    center_x,
                    brand_line_y - diamond_size
                ),
                (
                    center_x + diamond_size,
                    brand_line_y
                ),
                (
                    center_x,
                    brand_line_y + diamond_size
                ),
                (
                    center_x - diamond_size,
                    brand_line_y
                )
            ],
            fill=palette["accent"]
        )

        brand_y = 940

        # سایه بسیار ملایم

        draw.text(
            (
                brand_x + 2,
                brand_y + 3
            ),
            brand_text,
            font=brand_font,
            fill=(0, 0, 0, 80)
        )

        draw.text(
            (
                brand_x,
                brand_y
            ),
            brand_text,
            font=brand_font,
            fill=palette["accent"]
        )

    print(
        f"[TIMING] 09 - Footer: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # 10 - PNG save
    # ----------------------------------------

    stage_start = time.perf_counter()

    filename = "/tmp/poetry_card.png"

    image.convert("RGB").save(
        filename,
        "PNG",
        compress_level=1
    )

    save_time = (
        time.perf_counter()
        - stage_start
    )

    file_size = 0

    try:

        file_size = (
            os.path.getsize(filename)
            / 1024
        )

    except Exception:
        pass

    print(
        f"[TIMING] 10 - PNG save: "
        f"{save_time:.4f}s "
        f"| size={file_size:.1f} KB"
    )

    total_time = (
        time.perf_counter()
        - total_start
    )

    print("")
    print("========== CARD TIMING ==========")

    print(
        f"[TIMING] CREATE CARD TOTAL: "
        f"{total_time:.4f}s"
    )

    print(
        f"[TIMING] Palette: "
        f"{palette['name']}"
    )

    print(
        f"[TIMING] Branded: "
        f"{branded}"
    )

    print("=================================")
    print("")

    return filename


# ============================================
# BOT / API
# ============================================

app = Flask(__name__)


def api_post(method, data=None, files=None):

    url = f"{API_BASE}/{method}"

    try:

        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=60
        )

        return response.json()

    except Exception as e:

        print(
            f"API ERROR [{method}]:",
            e
        )

        return None


def send_message(
    chat_id,
    text,
    reply_markup=None
):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup is not None:
        data["reply_markup"] = reply_markup

    return api_post(
        "sendMessage",
        data=data
    )


def delete_message(
    chat_id,
    message_id
):

    return api_post(
        "deleteMessage",
        data={
            "chat_id": chat_id,
            "message_id": message_id
        }
    )


def answer_callback_query(
    callback_id
):

    return api_post(
        "answerCallbackQuery",
        data={
            "callback_query_id": callback_id
        }
    )


def send_photo(
    chat_id,
    filename
):

    try:

        with open(
            filename,
            "rb"
        ) as photo:

            return api_post(
                "sendPhoto",
                data={
                    "chat_id": chat_id
                },
                files={
                    "photo": photo
                }
            )

    except Exception as e:

        print(
            "sendPhoto ERROR:",
            e
        )

        return None


# ============================================
# KEYBOARDS
# ============================================

def card_type_keyboard():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "🖋️ با امضای شعرکده",
                    "callback_data": "type_branded"
                }
            ],
            [
                {
                    "text": "◻️ کارت عمومی، بدون امضا",
                    "callback_data": "type_public"
                }
            ]
        ]
    }


def color_keyboard():

    rows = []

    for index, palette in enumerate(PALETTES):

        rows.append(
            [
                {
                    "text": palette["name"],
                    "callback_data": f"color_{index}"
                }
            ]
        )

    return {
        "inline_keyboard": rows
    }


# ============================================
# PENDING POEMS
# ============================================

PENDING_TIMEOUT = 120


def save_pending_poem(
    chat_id,
    text
):

    with pending_lock:

        pending_poems[chat_id] = {
            "text": text,
            "created_at": time.time(),
            "branded": None
        }


def get_pending_poem(chat_id):

    with pending_lock:

        item = pending_poems.get(
            chat_id
        )

        if not item:
            return None

        if (
            time.time()
            - item["created_at"]
            > PENDING_TIMEOUT
        ):

            del pending_poems[chat_id]

            return None

        return item


def refresh_pending_timer(chat_id):

    with pending_lock:

        if chat_id in pending_poems:

            pending_poems[
                chat_id
            ]["created_at"] = time.time()


def delete_pending_poem(chat_id):

    with pending_lock:

        pending_poems.pop(
            chat_id,
            None
        )


# ============================================
# AFTER CARD MESSAGE
# ============================================

def send_after_card_message(
    chat_id
):

    text = (
        "🌿 کارت شعر شما آماده شد.\n\n"
        "اگر دوست داشتید شعرهای بیشتری ببینید، "
        "به کانال شعرکده سر بزنید."
    )

    return send_message(
        chat_id,
        text
    )


# ============================================
# CALLBACK PROCESSING
# ============================================

def process_type_selection(
    callback
):

    callback_id = callback.get(
        "id"
    )

    data = callback.get(
        "data",
        ""
    )

    message = callback.get(
        "message",
        {}
    )

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    message_id = message.get(
        "message_id"
    )

    if not chat_id:
        return

    answer_start = time.perf_counter()

    answer_callback_query(
        callback_id
    )

    print(
        f"[TIMING] answerCallbackQuery: "
        f"{time.perf_counter() - answer_start:.4f}s"
    )

    item = get_pending_poem(
        chat_id
    )

    if not item:

        send_message(
            chat_id,
            "⏰ زمان انتخاب کارت تمام شده است. لطفاً شعر را دوباره ارسال کنید."
        )

        return

    branded = (
        data == "type_branded"
    )

    with pending_lock:

        if chat_id in pending_poems:

            pending_poems[
                chat_id
            ]["branded"] = branded

            pending_poems[
                chat_id
            ]["created_at"] = time.time()

    delete_start = time.perf_counter()

    delete_message(
        chat_id,
        message_id
    )

    print(
        f"[TIMING] Delete type message: "
        f"{time.perf_counter() - delete_start:.4f}s"
    )

    send_message(
        chat_id,
        "🎨 حالا رنگ کارت را انتخاب کنید:",
        color_keyboard()
    )


def process_color_selection(
    callback
):

    total_start = time.perf_counter()

    callback_id = callback.get(
        "id"
    )

    data = callback.get(
        "data",
        ""
    )

    message = callback.get(
        "message",
        {}
    )

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    message_id = message.get(
        "message_id"
    )

    if not chat_id:
        return

    # ----------------------------------------
    # answer callback
    # ----------------------------------------

    stage_start = time.perf_counter()

    answer_callback_query(
        callback_id
    )

    print(
        f"[TIMING] answerCallbackQuery: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # pending
    # ----------------------------------------

    item = get_pending_poem(
        chat_id
    )

    if not item:

        send_message(
            chat_id,
            "⏰ زمان انتخاب رنگ تمام شده است. لطفاً شعر را دوباره ارسال کنید."
        )

        return

    # ----------------------------------------
    # palette
    # ----------------------------------------

    try:

        index = int(
            data.replace(
                "color_",
                ""
            )
        )

        palette = PALETTES[index]

    except Exception:

        send_message(
            chat_id,
            "رنگ انتخاب‌شده معتبر نیست."
        )

        return

    poem_text = item["text"]
    branded = item["branded"]

    # ----------------------------------------
    # delete color message
    # ----------------------------------------

    stage_start = time.perf_counter()

    delete_message(
        chat_id,
        message_id
    )

    print(
        f"[TIMING] Delete color message: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # building message
    # ----------------------------------------

    stage_start = time.perf_counter()

    building = send_message(
        chat_id,
        "⏳ کارت شعر در حال ساخت است..."
    )

    print(
        f"[TIMING] Send building message: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # create card
    # ----------------------------------------

    filename = create_poetry_card(
        poem_text,
        palette,
        branded
    )

    # ----------------------------------------
    # send photo
    # ----------------------------------------

    stage_start = time.perf_counter()

    send_photo(
        chat_id,
        filename
    )

    print(
        f"[TIMING] sendPhoto: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    # ----------------------------------------
    # delete building
    # ----------------------------------------

    if building:

        building_message_id = (
            building
            .get("result", {})
            .get("message_id")
        )

        if building_message_id:

            stage_start = time.perf_counter()

            delete_message(
                chat_id,
                building_message_id
            )

            print(
                f"[TIMING] Delete building message: "
                f"{time.perf_counter() - stage_start:.4f}s"
            )

    # ----------------------------------------
    # after card
    # ----------------------------------------

    stage_start = time.perf_counter()

    send_after_card_message(
        chat_id
    )

    print(
        f"[TIMING] Send after-card message: "
        f"{time.perf_counter() - stage_start:.4f}s"
    )

    delete_pending_poem(
        chat_id
    )

    # ----------------------------------------
    # total
    # ----------------------------------------

    print("")
    print(
        "======= COLOR SELECTION TOTAL ======="
    )

    print(
        f"[TIMING] Total color click -> finished: "
        f"{time.perf_counter() - total_start:.4f}s"
    )

    print(
        "====================================="
    )
    print("")


# ============================================
# CALLBACK ROUTER
# ============================================

def process_callback(callback):

    data = callback.get(
        "data",
        ""
    )

    if data.startswith(
        "type_"
    ):

        process_type_selection(
            callback
        )

    elif data.startswith(
        "color_"
    ):

        process_color_selection(
            callback
        )


# ============================================
# MESSAGE PROCESSING
# ============================================

def process_message(message):

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    text = message.get(
        "text"
    )

    if not chat_id or not text:
        return

    text = text.strip()

    if not text:
        return

    # ----------------------------------------
    # start
    # ----------------------------------------

    if text in (
        "/start",
        "/start@bot"
    ):

        send_message(
            chat_id,
            (
                "🌿 به شعرکده خوش آمدید.\n\n"
                "شعر خود را ارسال کنید تا برایتان کارت شعر بسازم."
            )
        )

        return

    # ----------------------------------------
    # new poem
    # ----------------------------------------

    save_pending_poem(
        chat_id,
        text
    )

    send_message(
        chat_id,
        "نوع کارت را انتخاب کنید:",
        card_type_keyboard()
    )


# ============================================
# WEBHOOK
# ============================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return "OK"


@app.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    try:

        update = request.get_json(
            silent=True
        )

        if not update:

            return "OK"

        # callback query

        callback = update.get(
            "callback_query"
        )

        if callback:

            process_callback(
                callback
            )

            return "OK"

        # normal message

        message = update.get(
            "message"
        )

        if message:

            process_message(
                message
            )

        return "OK"

    except Exception as e:

        print(
            "WEBHOOK ERROR:",
            e
        )

        return "OK"


# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":

    print(
        "Background image loaded and cached."
    )

    build_cached_backgrounds()

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
