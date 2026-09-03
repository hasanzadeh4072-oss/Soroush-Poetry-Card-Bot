import os
import io
import re
import math
import requests
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TOKEN = os.environ.get("SOROUSH_TOKEN")
API_BASE = f"https://api.splus.ir/bot{TOKEN}"

WIDTH = 1080
HEIGHT = 1080

BG_TOP = (35, 18, 58)
BG_BOTTOM = (18, 9, 34)

POEM_COLOR = (250, 246, 235, 255)
GOLD = (220, 190, 120, 255)
FOOTER_COLOR = (205, 195, 215, 230)

POEM_FONT = "BNazanin.ttf"
TITLE_FONT = "BTitrBd.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"
EMOJI_FONT = "NotoColorEmoji.ttf"

EMOJI_BASE_SIZE = 109
EMOJI_SCALE = 0.78
SYMBOL_SCALE = 0.82

MARGIN_X = 95
MAX_TEXT_WIDTH = WIDTH - 2 * MARGIN_X

FONT_DIR = os.path.dirname(os.path.abspath(__file__))


def font_path(name):
    return os.path.join(FONT_DIR, name)


@lru_cache(maxsize=100)
def get_font(name, size):
    return ImageFont.truetype(font_path(name), size)


@lru_cache(maxsize=1)
def get_emoji_font():
    return ImageFont.truetype(font_path(EMOJI_FONT), EMOJI_BASE_SIZE)


def normalize_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("…", "...")
    return text


def is_emoji_char(ch):
    cp = ord(ch)

    return (
        0x1F000 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or 0x2300 <= cp <= 0x23FF
        or 0x2B00 <= cp <= 0x2BFF
    )


def split_graphemes(text):
    result = []
    current = ""

    for ch in text:
        cp = ord(ch)

        if not current:
            current = ch
            continue

        if (
            cp == 0xFE0F
            or 0xFE0E
            or 0x200D
            or 0x20E3
            or 0x1F3FB <= cp <= 0x1F3FF
            or 0xE0020 <= cp <= 0xE007F
            or 0xE0001 == cp
            or 0xE007F == cp
        ):
            current += ch
        elif 0x1F1E6 <= cp <= 0x1F1FF and len(current) == 1:
            current += ch
        else:
            result.append(current)
            current = ch

    if current:
        result.append(current)

    return result


def contains_emoji(text):
    return any(is_emoji_char(c) for c in text)


def is_persian_char(ch):
    cp = ord(ch)

    return (
        0x0600 <= cp <= 0x06FF
        or 0x0750 <= cp <= 0x077F
        or 0x08A0 <= cp <= 0x08FF
        or 0xFB50 <= cp <= 0xFDFF
        or 0xFE70 <= cp <= 0xFEFF
    )


def is_latin_or_number(ch):
    return ch.isascii() and (ch.isalnum() or ch in ".,!?;:'\"+-=/()%&@$")


def is_symbol(ch):
    return ch in "#_*-–—|~"


def split_mixed_runs(text):
    runs = []
    current = ""
    current_type = None

    for ch in text:
        if ch.isspace():
            typ = "space"
        elif is_emoji_char(ch):
            typ = "emoji"
        elif is_persian_char(ch):
            typ = "persian"
        elif is_latin_or_number(ch):
            typ = "latin"
        elif is_symbol(ch):
            typ = "symbol"
        else:
            typ = "other"

        if typ == "emoji":
            if current:
                runs.append((current_type, current))
                current = ""
            runs.append(("emoji", ch))
            current_type = None
            continue

        if typ != current_type and current:
            runs.append((current_type, current))
            current = ""

        current_type = typ
        current += ch

    if current:
        runs.append((current_type, current))

    # Merge adjacent Persian runs
    merged = []
    for typ, value in runs:
        if merged and typ == merged[-1][0] and typ != "emoji":
            merged[-1] = (typ, merged[-1][1] + value)
        else:
            merged.append((typ, value))

    return merged


def render_emoji(cluster, target_size):
    font = get_emoji_font()

    bbox = font.getbbox(cluster)

    if bbox is None:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    left, top, right, bottom = bbox

    w = max(1, right - left + 20)
    h = max(1, bottom - top + 20)

    image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.text(
        (10 - left, 10 - top),
        cluster,
        font=font,
        embedded_color=True,
    )

    bbox2 = image.getbbox()

    if bbox2:
        image = image.crop(bbox2)

    scale = target_size / max(image.height, 1)

    new_w = max(1, int(image.width * scale))
    new_h = max(1, int(image.height * scale))

    return image.resize((new_w, new_h), Image.Resampling.LANCZOS)


def text_bbox(text, font, direction=None):
    temp = Image.new("RGB", (3000, 500))
    draw = ImageDraw.Draw(temp)

    kwargs = {}
    if direction:
        kwargs["direction"] = direction

    return draw.textbbox((0, 0), text, font=font, **kwargs)


def text_width(text, font, direction=None):
    if not text:
        return 0

    box = text_bbox(text, font, direction)

    return max(0, box[2] - box[0])


def render_run_image(typ, text, font_size):
    if not text:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    if typ == "emoji":
        size = max(18, int(font_size * EMOJI_SCALE))
        return render_emoji(text, size)

    if typ == "persian":
        font = get_font(POEM_FONT, font_size)

        box = text_bbox(text, font, "rtl")

        w = max(1, box[2] - box[0] + 8)
        h = max(1, box[3] - box[1] + 8)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text(
            (4 - box[0], 4 - box[1]),
            text,
            font=font,
            fill=POEM_COLOR,
            direction="rtl",
        )

        return img

    if typ == "latin":
        size = max(18, int(font_size * 0.86))
        font = get_font(FOOTER_FONT, size)

        box = text_bbox(text, font)

        w = max(1, box[2] - box[0] + 8)
        h = max(1, box[3] - box[1] + 8)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text(
            (4 - box[0], 4 - box[1]),
            text,
            font=font,
            fill=POEM_COLOR,
        )

        return img

    if typ == "symbol":
        size = max(18, int(font_size * SYMBOL_SCALE))
        font = get_font(FOOTER_FONT, size)

        box = text_bbox(text, font)

        w = max(1, box[2] - box[0] + 8)
        h = max(1, box[3] - box[1] + 8)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text(
            (4 - box[0], 4 - box[1]),
            text,
            font=font,
            fill=POEM_COLOR,
        )

        return img

    # سایر نویسه‌ها با فونت فارسی
    font = get_font(POEM_FONT, font_size)

    box = text_bbox(text, font, "rtl")

    w = max(1, box[2] - box[0] + 8)
    h = max(1, box[3] - box[1] + 8)

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.text(
        (4 - box[0], 4 - box[1]),
        text,
        font=font,
        fill=POEM_COLOR,
        direction="rtl",
    )

    return img


def is_simple_persian_line(text):
    return not contains_emoji(text) and not any(
        is_latin_or_number(c) or is_symbol(c)
        for c in text
    )


def render_line(text, font_size):
    if not text:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    # حالت عادی شعر: کل جمله یکجا برای حفظ اتصال حروف
    if is_simple_persian_line(text):
        font = get_font(POEM_FONT, font_size)

        box = text_bbox(text, font, "rtl")

        w = max(1, box[2] - box[0] + 16)
        h = max(1, box[3] - box[1] + 16)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text(
            (8 - box[0], 8 - box[1]),
            text,
            font=font,
            fill=POEM_COLOR,
            direction="rtl",
        )

        return img

    runs = split_mixed_runs(text)

    # حذف فاصله‌های ابتدا و انتها
    while runs and runs[0][0] == "space":
        runs.pop(0)

    while runs and runs[-1][0] == "space":
        runs.pop()

    if not runs:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    rendered = []

    for typ, value in runs:
        if typ == "space":
            font = get_font(POEM_FONT, font_size)
            width = max(5, text_width(" ", font))
            rendered.append(
                Image.new(
                    "RGBA",
                    (width, max(10, int(font_size * 1.4))),
                    (0, 0, 0, 0),
                )
            )
        else:
            rendered.append(render_run_image(typ, value, font_size))

    # ترتیب بصری را برای خط RTL کنترل می‌کنیم.
    # هر run به‌صورت یک واحد باقی می‌ماند تا حروف فارسی به‌هم نریزند.
    rendered = rendered[::-1]

    gap = 2

    total_w = sum(img.width for img in rendered)
    total_w += gap * max(0, len(rendered) - 1)

    max_h = max(img.height for img in rendered)

    canvas = Image.new(
        "RGBA",
        (max(1, total_w + 8), max(1, max_h + 8)),
        (0, 0, 0, 0),
    )

    x = 4

    for img in rendered:
        y = 4 + (max_h - img.height) // 2
        canvas.alpha_composite(img, (x, y))
        x += img.width + gap

    return canvas


def measure_line(text, font_size):
    return render_line(text, font_size).width


def wrap_text(text, font_size, max_width):
    lines = text.split("\n")
    result = []

    for original_line in lines:
        if not original_line.strip():
            result.append("")
            continue

        words = original_line.split()

        current = ""

        for word in words:
            candidate = word if not current else current + " " + word

            if measure_line(candidate, font_size) <= max_width:
                current = candidate
            else:
                if current:
                    result.append(current)

                # اگر خود کلمه هم بزرگ بود، آن را مجبور به خط‌شکنی می‌کنیم
                if measure_line(word, font_size) <= max_width:
                    current = word
                else:
                    partial = ""

                    for ch in split_graphemes(word):
                        test = partial + ch

                        if measure_line(test, font_size) <= max_width:
                            partial = test
                        else:
                            if partial:
                                result.append(partial)
                            partial = ch

                    current = partial

        if current:
            result.append(current)

    return result


def calculate_text_layout(poem):
    for size in range(58, 27, -2):
        lines = wrap_text(poem, size, MAX_TEXT_WIDTH)

        if not lines:
            continue

        line_height = int(size * 1.55)
        spacing = 20
        blank_height = 48

        total_height = 0

        for line in lines:
            if line == "":
                total_height += blank_height
            else:
                total_height += line_height

        if len(lines) > 1:
            total_height += spacing * (len(lines) - 1)

        if total_height <= 690:
            return size, lines, line_height, spacing, blank_height

    size = 28
    lines = wrap_text(poem, size, MAX_TEXT_WIDTH)

    line_height = int(size * 1.55)
    spacing = 14
    blank_height = 40

    return size, lines, line_height, spacing, blank_height


def create_background():
    image = Image.new("RGBA", (WIDTH, HEIGHT))

    px = image.load()

    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)

        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)

        for x in range(WIDTH):
            dx = abs(x - WIDTH / 2) / (WIDTH / 2)
            glow = max(0, 1 - dx) * 4

            px[x, y] = (
                min(255, r + int(glow)),
                min(255, g + int(glow)),
                min(255, b + int(glow)),
                255,
            )

    return image


def add_texture(image):
    texture = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)

    step = 8

    for y in range(0, HEIGHT, step):
        for x in range(0, WIDTH, step):
            value = ((x * 17 + y * 31) % 23)

            if value < 3:
                draw.point(
                    (x, y),
                    fill=(255, 255, 255, 7),
                )

    texture = texture.filter(ImageFilter.GaussianBlur(0.5))
    image.alpha_composite(texture)


def create_card(poem):
    poem = normalize_text(poem.strip())

    image = create_background()
    add_texture(image)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Header
    title_font = get_font(TITLE_FONT, 66)
    subtitle_font = get_font(FOOTER_FONT, 25)

    title = "شعرکده"
    subtitle = "( سروش پلاس )"

    title_box = draw.textbbox(
        (0, 0),
        title,
        font=title_font,
        direction="rtl",
    )

    title_w = title_box[2] - title_box[0]
    title_h = title_box[3] - title_box[1]

    title_x = (WIDTH - title_w) // 2
    title_y = 72

    draw.text(
        (title_x, title_y),
        title,
        font=title_font,
        fill=GOLD,
        direction="rtl",
    )

    subtitle_box = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font,
        direction="rtl",
    )

    subtitle_w = subtitle_box[2] - subtitle_box[0]

    subtitle_x = (WIDTH - subtitle_w) // 2
    subtitle_y = title_y + title_h + 18 - 3

    draw.text(
        (subtitle_x, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=FOOTER_COLOR,
        direction="rtl",
    )

    # خط ظریف زیر عنوان
    line_y = subtitle_y + 45

    draw.line(
        (WIDTH // 2 - 120, line_y, WIDTH // 2 + 120, line_y),
        fill=(220, 190, 120, 90),
        width=2,
    )

    draw.ellipse(
        (
            WIDTH // 2 - 4,
            line_y - 4,
            WIDTH // 2 + 4,
            line_y + 4,
        ),
        fill=(220, 190, 120, 190),
    )

    # علائم کناری بسیار ظریف
    draw.line(
        (70, line_y - 18, 70, line_y + 18),
        fill=(220, 190, 120, 45),
        width=2,
    )

    draw.line(
        (WIDTH - 70, line_y - 18, WIDTH - 70, line_y + 18),
        fill=(220, 190, 120, 45),
        width=2,
    )

    image.alpha_composite(overlay)

    # متن شعر
    font_size, lines, line_height, spacing, blank_height = calculate_text_layout(
        poem
    )

    rendered_lines = []

    for line in lines:
        if line == "":
            rendered_lines.append(None)
        else:
            rendered_lines.append(render_line(line, font_size))

    content_height = 0

    for img in rendered_lines:
        if img is None:
            content_height += blank_height
        else:
            content_height += img.height

    if len(rendered_lines) > 1:
        content_height += spacing * (len(rendered_lines) - 1)

    top_limit = 265
    bottom_limit = 870

    available = bottom_limit - top_limit

    if content_height > available:
        scale = available / content_height

        if scale < 1:
            # در حالت نادر، کل متن را کمی کوچک می‌کنیم
            new_lines = []

            for img in rendered_lines:
                if img is None:
                    new_lines.append(None)
                else:
                    new_lines.append(
                        img.resize(
                            (
                                max(1, int(img.width * scale)),
                                max(1, int(img.height * scale)),
                            ),
                            Image.Resampling.LANCZOS,
                        )
                    )

            rendered_lines = new_lines
            content_height = available

    # پنل نیمه‌شفاف شعر
    panel_top = max(235, top_limit - 28)
    panel_bottom = min(
        HEIGHT - 115,
        top_limit + content_height + 45,
    )

    panel = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    panel_draw = ImageDraw.Draw(panel)

    panel_draw.rounded_rectangle(
        (
            48,
            panel_top,
            WIDTH - 48,
            panel_bottom,
        ),
        radius=34,
        fill=(255, 255, 255, 13),
        outline=(220, 190, 120, 30),
        width=1,
    )

    panel = panel.filter(ImageFilter.GaussianBlur(0.15))
    image.alpha_composite(panel)

    # دوباره متن روی پنل
    y = top_limit

    for img in rendered_lines:
        if img is None:
            y += blank_height
            continue

        x = (WIDTH - img.width) // 2

        image.alpha_composite(
            img,
            (x, int(y)),
        )

        y += img.height + spacing

    # Footer
    footer = "کارت شعر"

    footer_font = get_font(FOOTER_FONT, 22)

    footer_box = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font,
        direction="rtl",
    )

    footer_w = footer_box[2] - footer_box[0]

    footer_x = (WIDTH - footer_w) // 2
    footer_y = HEIGHT - 75

    footer_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    footer_draw = ImageDraw.Draw(footer_layer)

    footer_draw.text(
        (footer_x, footer_y),
        footer,
        font=footer_font,
        fill=FOOTER_COLOR,
        direction="rtl",
    )

    image.alpha_composite(footer_layer)

    return image.convert("RGB")


def send_message(chat_id, text, reply_markup=None):
    url = f"{API_BASE}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup:
        data["reply_markup"] = reply_markup

    try:
        response = requests.post(
            url,
            json=data,
            timeout=30,
        )

        print(
            "sendMessage:",
            response.status_code,
            response.text[:500],
        )

        return response
    except Exception as e:
        print("sendMessage error:", e)
        return None


def send_photo(chat_id, image):
    url = f"{API_BASE}/sendPhoto"

    buffer = io.BytesIO()
    image.save(
        buffer,
        format="JPEG",
        quality=95,
    )
    buffer.seek(0)

    files = {
        "photo": (
            "poetry_card.jpg",
            buffer,
            "image/jpeg",
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

        print(
            "sendPhoto:",
            response.status_code,
            response.text[:500],
        )

        return response
    except Exception as e:
        print("sendPhoto error:", e)
        return None


def process_update(update):
    message = update.get("message", {})

    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id:
        return

    text = message.get("text", "")

    if not text:
        return

    if text.strip() == "/start":
        welcome = """سلام 👋

🖼️ به بات کارت شعر خوش آمدی.

شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨

📖 برای دیدن شعرهای بیشتر، <a href="https://splus.ir/life_m23">شعرکده</a> در سروش پلاس را دنبال کن."""

        send_message(chat_id, welcome)
        return

    try:
        image = create_card(text)

        result = send_photo(
            chat_id,
            image,
        )

        if result is not None and result.ok:
            success = """✨ کارت شعر شما آماده شد.

اگر باز هم شعری دارید، همین‌جا ارسال کنید تا آن را هم به کارت شعر تبدیل کنیم. 🖼️

📖 برای دیدن شعرهای بیشتر، سری هم به کانال «<a href="https://splus.ir/life_m23">شعرکده</a>» در سروش پلاس بزنید."""

            send_message(chat_id, success)
        else:
            send_message(
                chat_id,
                "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد.",
            )

    except Exception as e:
        print("Card creation error:", e)

        send_message(
            chat_id,
            "❌ هنگام ساخت کارت مشکلی پیش آمد.",
        )


from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Soroush Poetry Card Bot is running."


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(silent=True)

        if update:
            print("UPDATE:", update)
            process_update(update)

        return "OK", 200

    except Exception as e:
        print("Webhook error:", e)
        return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
    )
