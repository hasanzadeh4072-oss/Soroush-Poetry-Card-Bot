import os
import random
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

CHANNEL_URL = "https://splus.ir/life_m23"

CARD_WIDTH = 1080
CARD_HEIGHT = 1080

TEXT_COLOR = (248, 244, 235)
ACCENT_COLOR = (205, 172, 105)
SUBTITLE_COLOR = (190, 175, 150)
BORDER_COLOR = (150, 120, 70)

POEM_FONT = "BNazanin.ttf"
FALLBACK_FONT = "Vazirmatn-Regular.ttf"
EMOJI_FONT = "NotoColorEmoji.ttf"

TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"


def get_font(font_name, size):
    return ImageFont.truetype(font_name, size)


def create_gradient_background():

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT)
    )

    pixels = image.load()

    top = (42, 26, 66)
    middle = (31, 22, 52)
    bottom = (15, 14, 28)

    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        if ratio < 0.55:

            t = ratio / 0.55

            r = int(top[0] * (1 - t) + middle[0] * t)
            g = int(top[1] * (1 - t) + middle[1] * t)
            b = int(top[2] * (1 - t) + middle[2] * t)

        else:

            t = (ratio - 0.55) / 0.45

            r = int(middle[0] * (1 - t) + bottom[0] * t)
            g = int(middle[1] * (1 - t) + bottom[1] * t)
            b = int(middle[2] * (1 - t) + bottom[2] * t)

        for x in range(CARD_WIDTH):
            pixels[x, y] = (r, g, b)

    glow = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.ellipse(
        (-180, -120, 620, 520),
        fill=(135, 95, 180, 32)
    )

    glow_draw.ellipse(
        (650, 650, 1250, 1250),
        fill=(90, 60, 140, 20)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(90)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        glow
    )

    texture = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    texture_pixels = texture.load()

    random.seed(8)

    for _ in range(18000):

        x = random.randrange(CARD_WIDTH)
        y = random.randrange(CARD_HEIGHT)

        value = random.choice(
            [
                (255, 255, 255, 4),
                (0, 0, 0, 5)
            ]
        )

        texture_pixels[x, y] = value

    image = Image.alpha_composite(
        image,
        texture
    )

    return image.convert("RGBA")


def normalize_text(text):
    return text.replace("…", "...")


def is_emoji(char):
    code = ord(char)

    return (
        0x1F000 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
        or 0x2300 <= code <= 0x23FF
        or 0x2B00 <= code <= 0x2BFF
    )


def is_fallback_character(char):

    if is_emoji(char):
        return False

    code = ord(char)

    # Latin
    if (
        0x0041 <= code <= 0x005A
        or 0x0061 <= code <= 0x007A
    ):
        return True

    # Numbers
    if 0x0030 <= code <= 0x0039:
        return True

    # Common symbols
    if char in "#@&%$+-=_*/<>[]{}|\\^~`":
        return True

    return False


def get_text_width(draw, text, primary_font, fallback_font, emoji_font):

    total = 0

    for char in text:

        if is_emoji(char):

            try:
                box = draw.textbbox(
                    (0, 0),
                    char,
                    font=emoji_font,
                    embedded_color=True
                )

                total += box[2] - box[0]

            except Exception:

                box = draw.textbbox(
                    (0, 0),
                    char,
                    font=fallback_font
                )

                total += box[2] - box[0]

        elif is_fallback_character(char):

            box = draw.textbbox(
                (0, 0),
                char,
                font=fallback_font
            )

            total += box[2] - box[0]

        else:

            box = draw.textbbox(
                (0, 0),
                char,
                font=primary_font
            )

            total += box[2] - box[0]

    return total


def wrap_text(
    draw,
    text,
    primary_font,
    fallback_font,
    emoji_font,
    max_width
):

    words = text.split()

    if not words:
        return []

    lines = []
    current = words[0]

    for word in words[1:]:

        test = current + " " + word

        width = get_text_width(
            draw,
            test,
            primary_font,
            fallback_font,
            emoji_font
        )

        if width <= max_width:

            current = test

        else:

            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def prepare_poem_lines(
    draw,
    text,
    primary_font,
    fallback_font,
    emoji_font,
    max_width
):

    text = normalize_text(text)

    raw_lines = text.splitlines()

    final_lines = []

    for line in raw_lines:

        if not line.strip():

            final_lines.append(None)
            continue

        wrapped = wrap_text(
            draw,
            line.strip(),
            primary_font,
            fallback_font,
            emoji_font,
            max_width
        )

        final_lines.extend(wrapped)

    return final_lines


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

    if lines[-1] is not None:
        total -= line_spacing

    return total


def draw_text_with_fallback(
    draw,
    position,
    text,
    primary_font,
    fallback_font,
    emoji_font,
    fill
):

    x, y = position

    for char in text:

        if is_emoji(char):

            try:

                bbox = draw.textbbox(
                    (0, 0),
                    char,
                    font=emoji_font,
                    embedded_color=True
                )

                draw.text(
                    (x, y),
                    char,
                    font=emoji_font,
                    embedded_color=True
                )

                width = bbox[2] - bbox[0]

            except Exception:

                bbox = draw.textbbox(
                    (0, 0),
                    char,
                    font=fallback_font
                )

                draw.text(
                    (x, y),
                    char,
                    font=fallback_font,
                    fill=fill
                )

                width = bbox[2] - bbox[0]

        elif is_fallback_character(char):

            bbox = draw.textbbox(
                (0, 0),
                char,
                font=fallback_font
            )

            draw.text(
                (x, y),
                char,
                font=fallback_font,
                fill=fill
            )

            width = bbox[2] - bbox[0]

        else:

            bbox = draw.textbbox(
                (0, 0),
                char,
                font=primary_font
            )

            draw.text(
                (x, y),
                char,
                font=primary_font,
                fill=fill
            )

            width = bbox[2] - bbox[0]

        x += width


def create_poetry_card(text):

    image = create_gradient_background()

    draw = ImageDraw.Draw(image)

    margin = 42

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

    title_y = 82

    header_center = CARD_WIDTH // 2

    gap = 18

    title_x = header_center + 10

    subtitle_x = (
        title_x
        - subtitle_width
        - gap
    )

    subtitle_y = (
        title_y
        + (title_height - subtitle_height) // 2
        - 3
    )

    draw.text(
        (title_x, title_y),
        title,
        font=title_font,
        fill=ACCENT_COLOR
    )

    draw.text(
        (subtitle_x, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=SUBTITLE_COLOR
    )

    line_width = 120

    line_y = (
        title_y
        + title_height
        + 24
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

    center_x = CARD_WIDTH // 2

    draw.ellipse(
        (
            center_x - 4,
            line_y - 4,
            center_x + 4,
            line_y + 4
        ),
        fill=ACCENT_COLOR
    )

    text_left = 90
    text_right = 990

    max_width = text_right - text_left

    text_top = 220
    text_bottom = 900

    available_height = (
        text_bottom - text_top
    )

    font_size = 58

    min_font_size = 28

    line_spacing = 20

    blank_line_spacing = 48

    lines = []

    while font_size >= min_font_size:

        poem_font = get_font(
            POEM_FONT,
            font_size
        )

        fallback_font = get_font(
            FALLBACK_FONT,
            font_size
        )

        emoji_font = get_font(
            EMOJI_FONT,
            font_size
        )

        lines = prepare_poem_lines(
            draw,
            text,
            poem_font,
            fallback_font,
            emoji_font,
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

        fallback_font = get_font(
            FALLBACK_FONT,
            48
        )

        emoji_font = get_font(
            EMOJI_FONT,
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

    panel_top = max(
        text_top - 35,
        160
    )

    panel_bottom = min(
        text_bottom + 35,
        940
    )

    panel = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(panel)

    panel_draw.rounded_rectangle(
        (
            65,
            panel_top,
            1015,
            panel_bottom
        ),
        radius=42,
        fill=(255, 255, 255, 7),
        outline=(205, 172, 105, 18),
        width=1
    )

    panel = panel.filter(
        ImageFilter.GaussianBlur(0.5)
    )

    image = Image.alpha_composite(
        image,
        panel
    )

    draw = ImageDraw.Draw(image)

    deco_y = (
        text_top
        + available_height // 2
    )

    draw.line(
        (
            78,
            deco_y - 28,
            78,
            deco_y + 28
        ),
        fill=(205, 172, 105, 90),
        width=1
    )

    draw.line(
        (
            1002,
            deco_y - 28,
            1002,
            deco_y + 28
        ),
        fill=(205, 172, 105, 90),
        width=1
    )

    y = (
        text_top
        + (available_height - total_height) // 2
    )

    for line in lines:

        if line is None:

            y += blank_line_spacing

            continue

        width = get_text_width(
            draw,
            line,
            poem_font,
            fallback_font,
            emoji_font
        )

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=poem_font
        )

        height = bbox[3] - bbox[1]

        x = (
            CARD_WIDTH - width
        ) // 2

        draw_text_with_fallback(
            draw,
            (x, y),
            line,
            poem_font,
            fallback_font,
            emoji_font,
            TEXT_COLOR
        )

        y += height + line_spacing

    footer_font = get_font(
        FOOTER_FONT,
        24
    )

    footer = "کارت شعر"

    footer_bbox = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font
    )

    footer_width = (
        footer_bbox[2] - footer_bbox[0]
    )

    footer_x = (
        CARD_WIDTH - footer_width
    ) // 2

    draw.text(
        (
            footer_x,
            CARD_HEIGHT - 90
        ),
        footer,
        font=footer_font,
        fill=ACCENT_COLOR
    )

    filename = "/tmp/poetry_card.png"

    image.convert("RGB").save(
        filename,
        "PNG",
        optimize=True
    )

    return filename


def send_message(chat_id, text):

    try:

        response = requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
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


def send_start_message(chat_id):

    text = (
        "سلام 👋\n\n"
        "🖼️ به بات کارت شعر خوش آمدی.\n\n"
        "شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨\n\n"
        f'📖 برای دیدن شعرهای بیشتر، '
        f'<a href="{CHANNEL_URL}">شعرکده</a> '
        f'در سروش پلاس را دنبال کن.'
    )

    return send_message(
        chat_id,
        text
    )


def send_after_card_message(chat_id):

    text = (
        "✨ کارت شعر شما آماده شد.\n\n"
        "اگر باز هم شعری دارید، همین‌جا ارسال کنید "
        "تا آن را هم به کارت شعر تبدیل کنیم. 🖼️\n\n"
        f'📖 برای دیدن شعرهای بیشتر، '
        f'سری هم به کانال <a href="{CHANNEL_URL}">'
        f'«شعرکده»</a> در سروش پلاس بزنید.'
    )

    return send_message(
        chat_id,
        text
    )


@app.route("/")
def home():

    return (
        "Poetry Card Bot is running",
        200
    )


@app.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    update = request.get_json(
        silent=True
    ) or {}

    print(
        "UPDATE:",
        update
    )

    message = (
        update.get("message")
        or {}
    )

    text = message.get("text")

    chat = (
        message.get("chat")
        or {}
    )

    user_id = chat.get("id")

    if not user_id:
        return "OK", 200

    if not text:
        return "OK", 200

    if text == "/start":

        send_start_message(
            user_id
        )

        return "OK", 200

    try:

        filename = create_poetry_card(
            text
        )

        print(
            f"Poetry card created: {filename}"
        )

        photo_response = send_photo(
            user_id,
            filename
        )

        if (
            photo_response is not None
            and photo_response.ok
        ):

            print(
                "Poetry card sent successfully."
            )

            send_after_card_message(
                user_id
            )

        else:

            print(
                "Photo sending failed."
            )

            send_message(
                user_id,
                "✅ کارت ساخته شد، "
                "اما ارسال تصویر موفق نشد."
            )

    except Exception as error:

        print(
            "Card creation error:",
            error
        )

        send_message(
            user_id,
            "❌ هنگام ساخت کارت مشکلی پیش آمد."
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
