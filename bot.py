import os
import io
import random
import requests

from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter


app = Flask(__name__)


# =========================================================
# تنظیمات
# =========================================================

TOKEN = os.getenv("SOROUSH_TOKEN")

if not TOKEN:
    raise RuntimeError("SOROUSH_TOKEN is not set")

API_BASE = f"https://api.splus.ir/bot{TOKEN}"

WIDTH = 1080
HEIGHT = 1080

CHANNEL_URL = "https://splus.ir/life_m23"


# =========================================================
# فونت‌ها
# =========================================================

FONT_TITLE = "BTitrBd.ttf"
FONT_POEM = "BNazanin.ttf"
FONT_FOOTER = "Vazirmatn-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# =========================================================
# پالت‌های رنگی
# =========================================================
# هر پالت کاملاً مستقل است تا تفاوت رنگ‌ها محسوس باشد.
# =========================================================

PALETTES = [

    # 1 ـ بنفش سلطنتی
    {
        "name": "Royal Purple",
        "bg1": (25, 8, 55),
        "bg2": (72, 25, 105),
        "bg3": (125, 55, 145),
        "panel": (42, 20, 65, 150),
        "panel_inner": (120, 80, 150, 25),
        "text": (250, 244, 232),
        "title": (235, 197, 112),
        "accent": (218, 174, 91),
        "subtitle": (221, 211, 196),
        "footer": (195, 180, 157),
        "border": (184, 137, 70, 110),
        "glow": (150, 70, 190),
    },

    # 2 ـ آبی نیمه‌شب
    {
        "name": "Midnight Blue",
        "bg1": (4, 14, 35),
        "bg2": (9, 35, 72),
        "bg3": (18, 73, 105),
        "panel": (8, 28, 53, 155),
        "panel_inner": (75, 135, 170, 25),
        "text": (241, 246, 246),
        "title": (220, 192, 112),
        "accent": (211, 172, 91),
        "subtitle": (202, 218, 226),
        "footer": (169, 193, 205),
        "border": (108, 153, 177, 115),
        "glow": (30, 115, 170),
    },

    # 3 ـ سبز زمردی
    {
        "name": "Emerald",
        "bg1": (3, 25, 22),
        "bg2": (7, 55, 45),
        "bg3": (13, 93, 69),
        "panel": (7, 38, 32, 155),
        "panel_inner": (74, 150, 122, 25),
        "text": (241, 245, 232),
        "title": (226, 195, 111),
        "accent": (211, 174, 87),
        "subtitle": (201, 220, 208),
        "footer": (171, 198, 181),
        "border": (102, 153, 125, 115),
        "glow": (30, 145, 105),
    },

    # 4 ـ شرابی / عنابی
    {
        "name": "Burgundy",
        "bg1": (35, 5, 12),
        "bg2": (78, 13, 29),
        "bg3": (125, 31, 49),
        "panel": (52, 12, 24, 155),
        "panel_inner": (170, 75, 90, 25),
        "text": (249, 239, 230),
        "title": (231, 190, 105),
        "accent": (211, 165, 82),
        "subtitle": (224, 201, 193),
        "footer": (201, 173, 165),
        "border": (170, 103, 89, 115),
        "glow": (170, 35, 60),
    },

    # 5 ـ قهوه‌ای شکلاتی / موکا
    {
        "name": "Dark Mocha",
        "bg1": (25, 14, 8),
        "bg2": (60, 31, 17),
        "bg3": (104, 57, 28),
        "panel": (43, 24, 14, 158),
        "panel_inner": (175, 105, 55, 25),
        "text": (250, 242, 225),
        "title": (231, 191, 109),
        "accent": (214, 169, 86),
        "subtitle": (221, 203, 180),
        "footer": (198, 176, 150),
        "border": (173, 119, 71, 115),
        "glow": (155, 80, 35),
    },

    # 6 ـ ذغالی + طلایی
    {
        "name": "Charcoal Gold",
        "bg1": (5, 6, 7),
        "bg2": (17, 19, 21),
        "bg3": (37, 38, 37),
        "panel": (18, 19, 19, 165),
        "panel_inner": (190, 160, 85, 18),
        "text": (246, 242, 228),
        "title": (239, 202, 112),
        "accent": (221, 180, 89),
        "subtitle": (211, 207, 194),
        "footer": (179, 174, 160),
        "border": (190, 150, 70, 125),
        "glow": (180, 135, 45),
    },
]


# =========================================================
# ابزارهای کمکی
# =========================================================

def lerp(a, b, t):
    return int(a + (b - a) * t)


def interpolate_color(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))


def create_gradient_background(palette):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()

    c1 = palette["bg1"]
    c2 = palette["bg2"]
    c3 = palette["bg3"]

    for y in range(HEIGHT):
        vertical = y / (HEIGHT - 1)

        if vertical < 0.55:
            t = vertical / 0.55
            base = interpolate_color(c1, c2, t)
        else:
            t = (vertical - 0.55) / 0.45
            base = interpolate_color(c2, c3, t)

        for x in range(WIDTH):
            # نور بسیار ملایم از مرکز
            dx = (x - WIDTH * 0.52) / WIDTH
            dy = (y - HEIGHT * 0.38) / HEIGHT

            glow_strength = max(
                0,
                1 - ((dx * dx + dy * dy) ** 0.5) * 2.2
            )

            glow = palette["glow"]

            r = min(255, int(base[0] + glow[0] * glow_strength * 0.055))
            g = min(255, int(base[1] + glow[1] * glow_strength * 0.055))
            b = min(255, int(base[2] + glow[2] * glow_strength * 0.055))

            # وینیت بسیار ملایم
            edge = abs(x - WIDTH / 2) / (WIDTH / 2)
            edge += abs(y - HEIGHT / 2) / (HEIGHT / 2)
            darken = max(0, edge - 0.85) * 8

            pixels[x, y] = (
                max(0, int(r - darken)),
                max(0, int(g - darken)),
                max(0, int(b - darken)),
            )

    return image


def add_texture(image):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    random.seed(18)

    for _ in range(9000):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)

        value = random.choice([
            (255, 255, 255, 4),
            (255, 255, 255, 3),
            (0, 0, 0, 4),
            (0, 0, 0, 3),
        ])

        draw.point((x, y), fill=value)

    return Image.alpha_composite(image.convert("RGBA"), overlay)


def rounded_rectangle(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width
    )


def text_width(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0]


def normalize_poem(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # BNazanin با کاراکتر سه‌نقطه مشکل نمایش داشت.
    text = text.replace("…", "...")

    return text.strip()


# =========================================================
# شکستن خطوط شعر بر اساس عرض واقعی
# =========================================================

def wrap_line(draw, line, font_obj, max_width):
    if not line:
        return [""]

    words = line.split()

    if not words:
        return [""]

    result = []
    current = words[0]

    for word in words[1:]:
        candidate = current + " " + word

        if text_width(draw, candidate, font_obj) <= max_width:
            current = candidate
        else:
            result.append(current)
            current = word

    result.append(current)

    return result


def prepare_poem_lines(draw, poem, font_obj, max_width):
    raw_lines = poem.split("\n")
    final_lines = []

    for line in raw_lines:
        if line.strip() == "":
            final_lines.append("")
            continue

        wrapped = wrap_line(
            draw,
            line.strip(),
            font_obj,
            max_width
        )

        final_lines.extend(wrapped)

    return final_lines


# =========================================================
# اندازه مناسب فونت شعر
# =========================================================

def fit_poem(draw, poem, max_width, max_height):
    for size in range(62, 27, -2):
        poem_font = font(FONT_POEM, size)

        lines = prepare_poem_lines(
            draw,
            poem,
            poem_font,
            max_width
        )

        line_spacing = 16
        blank_spacing = 44

        total_height = 0

        for line in lines:
            if line == "":
                total_height += blank_spacing
            else:
                bbox = draw.textbbox(
                    (0, 0),
                    line,
                    font=poem_font
                )
                line_height = bbox[3] - bbox[1]
                total_height += line_height + line_spacing

        if total_height <= max_height:
            return poem_font, lines

    poem_font = font(FONT_POEM, 28)

    return (
        poem_font,
        prepare_poem_lines(
            draw,
            poem,
            poem_font,
            max_width
        )
    )


# =========================================================
# کارت شعر
# =========================================================

def create_poetry_card(poem):
    poem = normalize_poem(poem)

    palette = random.choice(PALETTES)

    image = create_gradient_background(palette)
    image = add_texture(image)

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # قاب بیرونی
    # -----------------------------------------------------

    outer_border = palette["border"]

    draw.rounded_rectangle(
        (24, 24, WIDTH - 24, HEIGHT - 24),
        radius=34,
        outline=outer_border,
        width=2
    )

    draw.rounded_rectangle(
        (34, 34, WIDTH - 34, HEIGHT - 34),
        radius=29,
        outline=(
            outer_border[0],
            outer_border[1],
            outer_border[2],
            max(30, outer_border[3] // 2)
        ),
        width=1
    )

    # -----------------------------------------------------
    # عنوان
    # -----------------------------------------------------

    title_font = font(FONT_TITLE, 50)
    subtitle_font = font(FONT_FOOTER, 23)

    title = "شعرکده"
    subtitle = "( سروش پلاس )"

    title_box = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = title_box[2] - title_box[0]
    title_height = title_box[3] - title_box[1]

    title_x = (WIDTH - title_width) // 2
    title_y = 63

    # سایه عنوان
    draw.text(
        (title_x + 2, title_y + 4),
        title,
        font=title_font,
        fill=(0, 0, 0, 115)
    )

    draw.text(
        (title_x, title_y),
        title,
        font=title_font,
        fill=palette["title"]
    )

    # زیرعنوان
    subtitle_box = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font
    )

    subtitle_width = subtitle_box[2] - subtitle_box[0]

    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + title_height + 18 - 3

    draw.text(
        (subtitle_x, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=palette["subtitle"]
    )

    # -----------------------------------------------------
    # خط تزئینی زیر عنوان
    # -----------------------------------------------------

    ornament_y = 178

    center_x = WIDTH // 2

    draw.line(
        (125, ornament_y, center_x - 22, ornament_y),
        fill=palette["accent"],
        width=2
    )

    draw.line(
        (center_x + 22, ornament_y, WIDTH - 125, ornament_y),
        fill=palette["accent"],
        width=2
    )

    # الماس کوچک وسط
    diamond = [
        (center_x, ornament_y - 6),
        (center_x + 6, ornament_y),
        (center_x, ornament_y + 6),
        (center_x - 6, ornament_y),
    ]

    draw.polygon(
        diamond,
        fill=palette["accent"]
    )

    # -----------------------------------------------------
    # پنل شعر
    # -----------------------------------------------------

    panel_x1 = 58
    panel_y1 = 214
    panel_x2 = WIDTH - 58
    panel_y2 = 900

    # سایه پنل
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.rounded_rectangle(
        (
            panel_x1 + 8,
            panel_y1 + 12,
            panel_x2 + 8,
            panel_y2 + 12
        ),
        radius=38,
        fill=(0, 0, 0, 85)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(18)
    )

    image = Image.alpha_composite(image, shadow)
    draw = ImageDraw.Draw(image)

    # پنل اصلی
    rounded_rectangle(
        draw,
        (
            panel_x1,
            panel_y1,
            panel_x2,
            panel_y2
        ),
        38,
        palette["panel"]
    )

    # هایلایت داخلی
    rounded_rectangle(
        draw,
        (
            panel_x1 + 2,
            panel_y1 + 2,
            panel_x2 - 2,
            panel_y2 - 2
        ),
        36,
        None,
        outline=palette["panel_inner"],
        width=2
    )

    # قاب طلایی بسیار ظریف
    draw.rounded_rectangle(
        (
            panel_x1,
            panel_y1,
            panel_x2,
            panel_y2
        ),
        radius=38,
        outline=palette["border"],
        width=1
    )

    # -----------------------------------------------------
    # تزئینات کناری پنل
    # -----------------------------------------------------

    side_y1 = 360
    side_y2 = 755

    side_color = palette["accent"]

    # چپ
    draw.line(
        (78, side_y1, 78, side_y2),
        fill=(
            side_color[0],
            side_color[1],
            side_color[2],
            70
        ),
        width=1
    )

    # راست
    draw.line(
        (WIDTH - 78, side_y1, WIDTH - 78, side_y2),
        fill=(
            side_color[0],
            side_color[1],
            side_color[2],
            70
        ),
        width=1
    )

    # -----------------------------------------------------
    # شعر
    # -----------------------------------------------------

    text_x1 = 105
    text_x2 = WIDTH - 105

    max_text_width = text_x2 - text_x1
    max_text_height = 625

    poem_font, lines = fit_poem(
        draw,
        poem,
        max_text_width,
        max_text_height
    )

    # محاسبه ارتفاع واقعی شعر
    line_spacing = 16
    blank_spacing = 44

    line_heights = []

    total_height = 0

    for line in lines:
        if line == "":
            h = blank_spacing
        else:
            bbox = draw.textbbox(
                (0, 0),
                line,
                font=poem_font
            )
            h = (bbox[3] - bbox[1]) + line_spacing

        line_heights.append(h)
        total_height += h

    poem_top = panel_y1 + 62

    # اگر شعر کوتاه است، کمی پایین‌تر و وسط‌تر قرار بگیرد
    available_height = panel_y2 - panel_y1 - 100

    if total_height < available_height:
        poem_top += int(
            (available_height - total_height) / 2
        ) - 8

    current_y = poem_top

    for line, line_height in zip(lines, line_heights):

        if line == "":
            current_y += blank_spacing
            continue

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=poem_font
        )

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        # راست‌چین
        x = text_x2 - width

        # سایه بسیار ملایم
        draw.text(
            (x + 1, current_y + 2),
            line,
            font=poem_font,
            fill=(0, 0, 0, 80)
        )

        draw.text(
            (x, current_y),
            line,
            font=poem_font,
            fill=palette["text"]
        )

        current_y += height + line_spacing

    # -----------------------------------------------------
    # جداکننده پایین
    # -----------------------------------------------------

    footer_line_y = 934

    draw.line(
        (300, footer_line_y, WIDTH - 300, footer_line_y),
        fill=palette["border"],
        width=1
    )

    # نقطه وسط
    draw.ellipse(
        (
            WIDTH // 2 - 3,
            footer_line_y - 3,
            WIDTH // 2 + 3,
            footer_line_y + 3
        ),
        fill=palette["accent"]
    )

    # -----------------------------------------------------
    # فوتر
    # -----------------------------------------------------

    footer = "کارت شعر"

    footer_font = font(FONT_FOOTER, 24)

    footer_box = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font
    )

    footer_width = footer_box[2] - footer_box[0]

    footer_x = (WIDTH - footer_width) // 2
    footer_y = 956

    draw.text(
        (footer_x, footer_y),
        footer,
        font=footer_font,
        fill=palette["footer"]
    )

    # -----------------------------------------------------
    # خروجی
    # -----------------------------------------------------

    output = io.BytesIO()

    image = image.convert("RGB")

    image.save(
        output,
        format="JPEG",
        quality=95,
        optimize=True
    )

    output.seek(0)

    return output, palette["name"]


# =========================================================
# ارسال پیام
# =========================================================

def send_message(chat_id, text):
    url = f"{API_BASE}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        return response.json()

    except Exception as e:
        print("send_message error:", e)
        return None


# =========================================================
# ارسال عکس
# =========================================================

def send_photo(chat_id, photo):
    url = f"{API_BASE}/sendPhoto"

    files = {
        "photo": (
            "poetry_card.jpg",
            photo,
            "image/jpeg"
        )
    }

    data = {
        "chat_id": chat_id
    }

    try:
        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=60
        )

        print("sendPhoto status:", response.status_code)
        print("sendPhoto response:", response.text)

        return response.json()

    except Exception as e:
        print("send_photo error:", e)
        return None


# =========================================================
# پیام خوش‌آمد
# =========================================================

def welcome_message(chat_id):
    text = """سلام 👋

🖼️ به بات کارت شعر خوش آمدی.

شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨

📖 برای دیدن شعرهای بیشتر، شعرکده در سروش پلاس را دنبال کن."""

    return send_message(chat_id, text)


# =========================================================
# پیام بعد از ساخت کارت
# =========================================================

def success_message(chat_id):
    text = """✨ کارت شعر شما آماده شد.

اگر باز هم شعری دارید، همین‌جا ارسال کنید تا آن را هم به کارت شعر تبدیل کنیم. 🖼️

📖 برای دیدن شعرهای بیشتر، سری هم به کانال «شعرکده» در سروش پلاس بزنید."""

    return send_message(chat_id, text)


# =========================================================
# Webhook
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return "Soroush Poetry Card Bot is running."


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(silent=True) or {}

        print("UPDATE:", update)

        message = update.get("message") or update.get("edited_message")

        if not message:
            return jsonify({"ok": True})

        chat = message.get("chat") or {}
        chat_id = chat.get("id")

        if not chat_id:
            return jsonify({"ok": True})

        text = message.get("text")

        if not text:
            return jsonify({"ok": True})

        text = text.strip()

        # -------------------------------------------------
        # /start
        # -------------------------------------------------

        if text.startswith("/start"):
            welcome_message(chat_id)
            return jsonify({"ok": True})

        # -------------------------------------------------
        # ساخت کارت
        # -------------------------------------------------

        try:
            photo, palette_name = create_poetry_card(text)

            print("Selected palette:", palette_name)

        except Exception as e:
            print("CARD CREATION ERROR:", e)

            send_message(
                chat_id,
                "❌ هنگام ساخت کارت مشکلی پیش آمد."
            )

            return jsonify({"ok": True})

        # -------------------------------------------------
        # ارسال عکس
        # -------------------------------------------------

        result = send_photo(
            chat_id,
            photo
        )

        if result and result.get("ok") is True:
            success_message(chat_id)
        else:
            send_message(
                chat_id,
                "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد."
            )

        return jsonify({"ok": True})

    except Exception as e:
        print("WEBHOOK ERROR:", e)

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 200


# =========================================================
# اجرای برنامه
# =========================================================

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
