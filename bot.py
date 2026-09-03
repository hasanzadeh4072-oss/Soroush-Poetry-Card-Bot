import os
import io
import random
import requests

from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# =========================
# Configuration
# =========================

TOKEN = os.getenv("SOROUSH_TOKEN")

if not TOKEN:
    raise RuntimeError("SOROUSH_TOKEN environment variable is not set.")

API_BASE = f"https://api.splus.ir/bot{TOKEN}"

WIDTH = 1080
HEIGHT = 1080

CHANNEL_URL = "https://splus.ir/life_m23"

FONT_TITLE = "BTitrBd.ttf"
FONT_POEM = "BNazanin.ttf"
FONT_FOOTER = "Vazirmatn-Regular.ttf"


# =========================
# Color Palettes
# =========================

PALETTES = [
    {
        "name": "Royal Purple",
        "bg1": (38, 18, 68),
        "bg2": (73, 32, 102),
        "bg3": (27, 12, 48),
        "panel": (43, 24, 63, 205),
        "panel_inner": (57, 32, 79, 110),
        "text": (249, 244, 235),
        "title": (244, 210, 137),
        "accent": (224, 181, 91),
        "subtitle": (214, 199, 174),
        "footer": (193, 174, 148),
        "border": (194, 148, 72, 95),
        "glow": (213, 166, 83, 75),
    },
    {
        "name": "Midnight Blue",
        "bg1": (12, 28, 59),
        "bg2": (25, 56, 91),
        "bg3": (7, 15, 34),
        "panel": (17, 34, 62, 205),
        "panel_inner": (28, 49, 78, 110),
        "text": (245, 246, 241),
        "title": (239, 210, 139),
        "accent": (218, 177, 91),
        "subtitle": (197, 205, 207),
        "footer": (174, 187, 195),
        "border": (177, 146, 78, 95),
        "glow": (130, 160, 206, 65),
    },
    {
        "name": "Emerald",
        "bg1": (10, 48, 42),
        "bg2": (20, 79, 67),
        "bg3": (5, 25, 23),
        "panel": (14, 48, 43, 205),
        "panel_inner": (22, 66, 57, 110),
        "text": (245, 246, 237),
        "title": (239, 211, 137),
        "accent": (215, 176, 89),
        "subtitle": (194, 207, 196),
        "footer": (171, 190, 179),
        "border": (180, 145, 73, 95),
        "glow": (73, 151, 124, 65),
    },
    {
        "name": "Burgundy",
        "bg1": (63, 15, 30),
        "bg2": (103, 28, 47),
        "bg3": (30, 7, 16),
        "panel": (62, 22, 35, 205),
        "panel_inner": (82, 30, 46, 110),
        "text": (249, 244, 237),
        "title": (241, 210, 139),
        "accent": (218, 174, 88),
        "subtitle": (211, 193, 181),
        "footer": (190, 167, 154),
        "border": (191, 139, 69, 95),
        "glow": (177, 77, 95, 65),
    },
    {
        "name": "Dark Mocha",
        "bg1": (48, 30, 20),
        "bg2": (84, 52, 34),
        "bg3": (25, 15, 10),
        "panel": (53, 35, 25, 205),
        "panel_inner": (70, 46, 33, 110),
        "text": (249, 243, 232),
        "title": (239, 205, 132),
        "accent": (216, 171, 83),
        "subtitle": (211, 195, 174),
        "footer": (190, 169, 145),
        "border": (185, 137, 66, 95),
        "glow": (169, 112, 62, 65),
    },
    {
        "name": "Charcoal Gold",
        "bg1": (20, 20, 22),
        "bg2": (43, 43, 46),
        "bg3": (9, 9, 10),
        "panel": (29, 29, 31, 210),
        "panel_inner": (47, 47, 49, 110),
        "text": (247, 244, 235),
        "title": (240, 208, 133),
        "accent": (219, 174, 83),
        "subtitle": (197, 194, 184),
        "footer": (173, 170, 159),
        "border": (190, 145, 69, 105),
        "glow": (204, 159, 76, 60),
    },
]


# =========================
# Flask
# =========================

app = Flask(__name__)


# =========================
# Font Helpers
# =========================

def load_font(path, size):
    return ImageFont.truetype(path, size)


# =========================
# Background
# =========================

def create_gradient_background(palette):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()

    top = palette["bg1"]
    middle = palette["bg2"]
    bottom = palette["bg3"]

    for y in range(HEIGHT):
        if y < HEIGHT // 2:
            ratio = y / (HEIGHT // 2)
            c1 = top
            c2 = middle
        else:
            ratio = (y - HEIGHT // 2) / (HEIGHT // 2)
            c1 = middle
            c2 = bottom

        for x in range(WIDTH):
            # Very subtle horizontal variation
            x_ratio = (x - WIDTH / 2) / WIDTH

            r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
            g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
            b = int(c1[2] * (1 - ratio) + c2[2] * ratio)

            variation = int(abs(x_ratio) * 4)

            pixels[x, y] = (
                max(0, min(255, r + variation)),
                max(0, min(255, g + variation)),
                max(0, min(255, b + variation)),
            )

    return image


def add_texture(image):
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    random.seed(17)

    for _ in range(5000):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        alpha = random.randint(3, 12)
        radius = random.choice([0, 0, 1])

        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=(255, 255, 255, alpha),
        )

    overlay = overlay.filter(ImageFilter.GaussianBlur(0.35))

    return Image.alpha_composite(image.convert("RGBA"), overlay)


# =========================
# Drawing Helpers
# =========================

def rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        xy,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )


def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


# =========================
# Poem Processing
# =========================

def normalize_poem(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # BNazanin may display the single ellipsis character incorrectly.
    text = text.replace("…", "...")

    return text.strip()


def wrap_line(draw, line, font, max_width):
    if not line:
        return [""]

    words = line.split()

    if not words:
        return [""]

    result = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word

        if text_width(draw, test, font) <= max_width:
            current = test
        else:
            if current:
                result.append(current)

            # Handle a single very long word
            if text_width(draw, word, font) <= max_width:
                current = word
            else:
                part = ""

                for char in word:
                    test_part = part + char

                    if text_width(draw, test_part, font) <= max_width:
                        part = test_part
                    else:
                        if part:
                            result.append(part)
                        part = char

                current = part

    if current:
        result.append(current)

    return result


def prepare_poem_lines(draw, poem, font, max_width):
    raw_lines = poem.split("\n")
    final_lines = []

    for line in raw_lines:
        if line.strip() == "":
            final_lines.append("")
        else:
            final_lines.extend(
                wrap_line(
                    draw,
                    line.strip(),
                    font,
                    max_width,
                )
            )

    return final_lines


def fit_poem(draw, poem, max_width, max_height):
    blank_spacing = 44
    line_spacing = 16

    for size in range(62, 27, -2):
        font = load_font(FONT_POEM, size)

        lines = prepare_poem_lines(
            draw,
            poem,
            font,
            max_width,
        )

        line_heights = []

        for line in lines:
            if line == "":
                line_heights.append(blank_spacing)
            else:
                bbox = draw.textbbox(
                    (0, 0),
                    line,
                    font=font,
                )
                line_heights.append(
                    bbox[3] - bbox[1]
                )

        total_height = 0

        for index, height in enumerate(line_heights):
            total_height += height

            if index < len(line_heights) - 1:
                if lines[index] == "" or lines[index + 1] == "":
                    total_height += blank_spacing
                else:
                    total_height += line_spacing

        if total_height <= max_height:
            return font, lines, line_heights, total_height

    # Fallback
    font = load_font(FONT_POEM, 28)

    lines = prepare_poem_lines(
        draw,
        poem,
        font,
        max_width,
    )

    line_heights = []

    for line in lines:
        if line == "":
            line_heights.append(blank_spacing)
        else:
            bbox = draw.textbbox(
                (0, 0),
                line,
                font=font,
            )
            line_heights.append(
                bbox[3] - bbox[1]
            )

    total_height = sum(line_heights)

    return font, lines, line_heights, total_height


# =========================
# Poetry Card
# =========================

def create_poetry_card(poem):
    palette = random.choice(PALETTES)

    background = create_gradient_background(palette)
    image = add_texture(background)

    draw = ImageDraw.Draw(image)

    # ---------------------------------
    # Outer decorative frame
    # ---------------------------------

    draw.rounded_rectangle(
        (24, 24, WIDTH - 24, HEIGHT - 24),
        radius=34,
        outline=palette["border"],
        width=2,
    )

    draw.rounded_rectangle(
        (34, 34, WIDTH - 34, HEIGHT - 34),
        radius=28,
        outline=(
            palette["border"][0],
            palette["border"][1],
            palette["border"][2],
            45,
        ),
        width=1,
    )

    # ---------------------------------
    # Header
    # ---------------------------------

    title_font = load_font(FONT_TITLE, 50)
    subtitle_font = load_font(FONT_FOOTER, 23)

    title = "شعرکده"
    subtitle = "( سروش پلاس )"

    title_bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font,
    )

    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    title_x = (WIDTH - title_width) // 2
    title_y = 63

    draw.text(
        (title_x, title_y),
        title,
        font=title_font,
        fill=palette["title"],
    )

    subtitle_bbox = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font,
    )

    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]

    subtitle_x = (WIDTH - subtitle_width) // 2

    # Original subtitle spacing/offset preserved
    subtitle_y = (
        title_y
        + title_height
        + 18
        - 3
    )

    draw.text(
        (subtitle_x, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=palette["subtitle"],
    )

    # ---------------------------------
    # Header ornament
    # ---------------------------------

    ornament_y = 178

    line_width = 125
    center_x = WIDTH // 2

    draw.line(
        (
            center_x - line_width,
            ornament_y,
            center_x - 18,
            ornament_y,
        ),
        fill=palette["accent"],
        width=2,
    )

    draw.line(
        (
            center_x + 18,
            ornament_y,
            center_x + line_width,
            ornament_y,
        ),
        fill=palette["accent"],
        width=2,
    )

    draw.ellipse(
        (
            center_x - 4,
            ornament_y - 4,
            center_x + 4,
            ornament_y + 4,
        ),
        fill=palette["accent"],
    )

    # ---------------------------------
    # Poetry panel
    # ---------------------------------

    panel_x1 = 58
    panel_y1 = 214
    panel_x2 = 1022
    panel_y2 = 900

    # Soft glow behind panel
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    glow_draw.rounded_rectangle(
        (
            panel_x1 - 8,
            panel_y1 - 8,
            panel_x2 + 8,
            panel_y2 + 8,
        ),
        radius=44,
        fill=palette["glow"],
    )

    glow = glow.filter(ImageFilter.GaussianBlur(18))
    image = Image.alpha_composite(image, glow)

    draw = ImageDraw.Draw(image)

    # Main panel
    rounded_rectangle(
        draw,
        (
            panel_x1,
            panel_y1,
            panel_x2,
            panel_y2,
        ),
        radius=38,
        fill=palette["panel"],
        outline=palette["border"],
        width=1,
    )

    # Inner translucent panel
    rounded_rectangle(
        draw,
        (
            panel_x1 + 8,
            panel_y1 + 8,
            panel_x2 - 8,
            panel_y2 - 8,
        ),
        radius=32,
        fill=palette["panel_inner"],
    )

    # ---------------------------------
    # Small side marks
    # ---------------------------------

    mark_y = panel_y1 + 54

    draw.line(
        (
            panel_x1 + 20,
            mark_y,
            panel_x1 + 43,
            mark_y,
        ),
        fill=palette["accent"],
        width=2,
    )

    draw.line(
        (
            panel_x2 - 43,
            mark_y,
            panel_x2 - 20,
            mark_y,
        ),
        fill=palette["accent"],
        width=2,
    )

    # ---------------------------------
    # Poem
    # ---------------------------------

    text_x1 = 105
    text_x2 = 975

    max_text_width = text_x2 - text_x1
    max_text_height = 625

    poem = normalize_poem(poem)

    font, lines, line_heights, total_height = fit_poem(
        draw,
        poem,
        max_text_width,
        max_text_height,
    )

    # Original vertical positioning preserved
    poem_top = panel_y1 + 62

    if total_height < max_text_height:
        poem_top += (
            max_text_height - total_height
        ) // 2

    current_y = poem_top

    line_spacing = 16
    blank_spacing = 44

    for index, line in enumerate(lines):
        if line == "":
            current_y += blank_spacing

            if index < len(lines) - 1:
                current_y += blank_spacing

            continue

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font,
        )

        width = bbox[2] - bbox[0]

        # IMPORTANT:
        # Center alignment — preserved from the original design.
        x = (WIDTH - width) // 2

        draw.text(
            (x, current_y),
            line,
            font=font,
            fill=palette["text"],
        )

        current_y += line_heights[index]

        if index < len(lines) - 1:
            if lines[index + 1] == "":
                current_y += blank_spacing
            else:
                current_y += line_spacing

    # ---------------------------------
    # Footer separator
    # ---------------------------------

    separator_y = 934

    draw.line(
        (
            380,
            separator_y,
            700,
            separator_y,
        ),
        fill=palette["border"],
        width=1,
    )

    # ---------------------------------
    # Footer
    # ---------------------------------

    footer_font = load_font(FONT_FOOTER, 21)
    footer = "کارت شعر"

    footer_bbox = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font,
    )

    footer_width = (
        footer_bbox[2] - footer_bbox[0]
    )

    footer_x = (WIDTH - footer_width) // 2
    footer_y = 956

    draw.text(
        (footer_x, footer_y),
        footer,
        font=footer_font,
        fill=palette["footer"],
    )

    # ---------------------------------
    # Final image
    # ---------------------------------

    output = io.BytesIO()

    image.convert("RGB").save(
        output,
        format="PNG",
        optimize=True,
    )

    output.seek(0)

    return output


# =========================
# Soroush Plus API
# =========================

def send_message(chat_id, text):
    url = f"{API_BASE}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30,
        )

        return response

    except Exception as e:
        print("send_message error:", e)
        return None


def send_photo(chat_id, photo_bytes):
    url = f"{API_BASE}/sendPhoto"

    files = {
        "photo": (
            "poetry_card.png",
            photo_bytes,
            "image/png",
        )
    }

    data = {
        "chat_id": chat_id,
    }

    try:
        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=60,
        )

        return response

    except Exception as e:
        print("send_photo error:", e)
        return None


# =========================
# Webhook
# =========================

@app.route("/", methods=["GET"])
def home():
    return "Soroush Poetry Card Bot is running."


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(silent=True)

        if not update:
            return jsonify({"ok": True})

        message = update.get("message")

        if not message:
            return jsonify({"ok": True})

        chat = message.get("chat", {})
        chat_id = chat.get("id")

        if not chat_id:
            return jsonify({"ok": True})

        text = message.get("text", "")

        # -------------------------
        # /start
        # -------------------------

        if text.strip().lower() == "/start":
            start_text = (
                "سلام 👋\n\n"
                "🖼️ به بات کارت شعر خوش آمدی.\n\n"
                "شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨\n\n"
                f'📖 برای دیدن شعرهای بیشتر، '
                f'<a href="{CHANNEL_URL}">شعرکده</a> '
                "در سروش پلاس را دنبال کن."
            )

            send_message(
                chat_id,
                start_text,
            )

            return jsonify({"ok": True})

        # -------------------------
        # Empty message
        # -------------------------

        if not text.strip():
            return jsonify({"ok": True})

        # -------------------------
        # Create card
        # -------------------------

        try:
            photo = create_poetry_card(text)

        except Exception as e:
            print("Card creation error:", e)

            send_message(
                chat_id,
                "❌ هنگام ساخت کارت مشکلی پیش آمد.",
            )

            return jsonify({"ok": True})

        # -------------------------
        # Send photo
        # -------------------------

        response = send_photo(
            chat_id,
            photo,
        )

        if response is not None:
            try:
                result = response.json()
            except Exception:
                result = {}

            if result.get("ok") is True:
                success_text = (
                    "✨ کارت شعر شما آماده شد.\n\n"
                    "اگر باز هم شعری دارید، همین‌جا ارسال کنید "
                    "تا آن را هم به کارت شعر تبدیل کنیم. 🖼️\n\n"
                    f'📖 برای دیدن شعرهای بیشتر، '
                    f'سری هم به کانال «<a href="{CHANNEL_URL}">شعرکده</a>» '
                    "در سروش پلاس بزنید."
                )

                send_message(
                    chat_id,
                    success_text,
                )

            else:
                print(
                    "sendPhoto failed:",
                    response.text,
                )

                send_message(
                    chat_id,
                    "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد.",
                )

        else:
            send_message(
                chat_id,
                "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد.",
            )

        return jsonify({"ok": True})

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"ok": True})


# =========================
# Run
# =========================

if __name__ == "__main__":
    port = int(
        os.getenv("PORT", "5000")
    )

    app.run(
        host="0.0.0.0",
        port=port,
    )
