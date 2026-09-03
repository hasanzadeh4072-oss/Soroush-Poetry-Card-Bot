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
ACCENT_COLOR = (214, 181, 112)
SUBTITLE_COLOR = (190, 175, 150)
BORDER_COLOR = (145, 112, 68)

POEM_FONT = "BNazanin.ttf"
TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"


def get_font(font_name, size):
    return ImageFont.truetype(font_name, size)


# ==================================
# Luxury Background
# ==================================

def create_gradient_background():

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT)
    )

    pixels = image.load()

    top = (47, 27, 70)
    middle = (29, 20, 49)
    bottom = (12, 11, 23)

    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        if ratio < 0.52:

            t = ratio / 0.52

            r = int(top[0] * (1 - t) + middle[0] * t)
            g = int(top[1] * (1 - t) + middle[1] * t)
            b = int(top[2] * (1 - t) + middle[2] * t)

        else:

            t = (ratio - 0.52) / 0.48

            r = int(middle[0] * (1 - t) + bottom[0] * t)
            g = int(middle[1] * (1 - t) + bottom[1] * t)
            b = int(middle[2] * (1 - t) + bottom[2] * t)

        for x in range(CARD_WIDTH):

            pixels[x, y] = (r, g, b)

    # --------------------------------
    # Large soft glow
    # --------------------------------

    glow = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.ellipse(
        (-260, -180, 650, 560),
        fill=(150, 105, 190, 38)
    )

    glow_draw.ellipse(
        (690, 690, 1250, 1250),
        fill=(105, 70, 160, 22)
    )

    glow_draw.ellipse(
        (250, 350, 850, 950),
        fill=(100, 65, 145, 10)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(110)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        glow
    )

    # --------------------------------
    # Very subtle texture
    # --------------------------------

    texture = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    texture_pixels = texture.load()

    random.seed(8)

    for _ in range(14000):

        x = random.randrange(CARD_WIDTH)
        y = random.randrange(CARD_HEIGHT)

        value = random.choice(
            [
                (255, 255, 255, 3),
                (0, 0, 0, 4)
            ]
        )

        texture_pixels[x, y] = value

    image = Image.alpha_composite(
        image,
        texture
    )

    return image.convert("RGB")


# ==================================
# Text Helpers
# ==================================

def normalize_text(text):

    return text.replace("…", "...")


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


def prepare_poem_lines(
    draw,
    text,
    font,
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
            font,
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


# ==================================
# Create Poetry Card
# ==================================

def create_poetry_card(text):

    image = create_gradient_background()

    draw = ImageDraw.Draw(image)

    # ==================================
    # Outer frame
    # ==================================

    margin = 40

    draw.rounded_rectangle(
        (
            margin,
            margin,
            CARD_WIDTH - margin,
            CARD_HEIGHT - margin
        ),
        radius=42,
        outline=(173, 137, 82),
        width=2
    )

    # Inner subtle frame

    inner_margin = 49

    draw.rounded_rectangle(
        (
            inner_margin,
            inner_margin,
            CARD_WIDTH - inner_margin,
            CARD_HEIGHT - inner_margin
        ),
        radius=35,
        outline=(205, 172, 105),
        width=1
    )

    # ==================================
    # Header
    # ==================================

    title_font = get_font(
        TITLE_FONT,
        50
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
        23
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

    title_y = 78

    header_center = CARD_WIDTH // 2

    gap = 20

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

    # Very soft title shadow

    draw.text(
        (
            title_x + 2,
            title_y + 3
        ),
        title,
        font=title_font,
        fill=(0, 0, 0, 80)
    )

    draw.text(
        (
            title_x,
            title_y
        ),
        title,
        font=title_font,
        fill=ACCENT_COLOR
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

    # ==================================
    # Header Ornament
    # ==================================

    line_y = (
        title_y
        + title_height
        + 25
    )

    line_width = 150

    center_x = CARD_WIDTH // 2

    # left line

    draw.line(
        (
            center_x - line_width,
            line_y,
            center_x - 12,
            line_y
        ),
        fill=(145, 112, 68),
        width=1
    )

    # right line

    draw.line(
        (
            center_x + 12,
            line_y,
            center_x + line_width,
            line_y
        ),
        fill=(145, 112, 68),
        width=1
    )

    # center diamond

    diamond_size = 5

    draw.polygon(
        [
            (center_x, line_y - diamond_size),
            (center_x + diamond_size, line_y),
            (center_x, line_y + diamond_size),
            (center_x - diamond_size, line_y)
        ],
        fill=ACCENT_COLOR
    )

    # ==================================
    # Poem Area
    # ==================================

    text_left = 75
    text_right = 1005

    max_width = text_right - text_left

    text_top = 218
    text_bottom = 895

    available_height = (
        text_bottom - text_top
    )

    font_size = 62
    min_font_size = 28

    line_spacing = 16
    blank_line_spacing = 44

    lines = []

    # ==================================
    # Smart Font Sizing
    # ==================================

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

        lines = ["متن خالی است"]

    total_height = calculate_text_height(
        draw,
        lines,
        poem_font,
        line_spacing,
        blank_line_spacing
    )

    # ==================================
    # Luxury Glass Panel
    # ==================================

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
        (CARD_WIDTH, CARD_HEIGHT),
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(panel)

    # Outer shadow

    panel_draw.rounded_rectangle(
        (
            62,
            panel_top + 4,
            1018,
            panel_bottom + 6
        ),
        radius=45,
        fill=(0, 0, 0, 28)
    )

    # Main panel

    panel_draw.rounded_rectangle(
        (
            62,
            panel_top,
            1018,
            panel_bottom
        ),
        radius=45,
        fill=(255, 255, 255, 8),
        outline=(205, 172, 105, 24),
        width=1
    )

    # Inner highlight

    panel_draw.rounded_rectangle(
        (
            72,
            panel_top + 10,
            1008,
            panel_bottom - 10
        ),
        radius=37,
        outline=(255, 255, 255, 8),
        width=1
    )

    panel = panel.filter(
        ImageFilter.GaussianBlur(0.35)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        panel
    )

    draw = ImageDraw.Draw(image)

    # ==================================
    # Side Ornaments
    # ==================================

    deco_y = (
        text_top
        + available_height // 2
    )

    # left

    draw.line(
        (
            79,
            deco_y - 30,
            79,
            deco_y + 30
        ),
        fill=(205, 172, 105, 75),
        width=1
    )

    draw.ellipse(
        (
            76,
            deco_y - 3,
            82,
            deco_y + 3
        ),
        fill=(205, 172, 105, 100)
    )

    # right

    draw.line(
        (
            1001,
            deco_y - 30,
            1001,
            deco_y + 30
        ),
        fill=(205, 172, 105, 75),
        width=1
    )

    draw.ellipse(
        (
            998,
            deco_y - 3,
            1004,
            deco_y + 3
        ),
        fill=(205, 172, 105, 100)
    )

    # ==================================
    # Poem
    # ==================================

    y = (
        text_top
        + (available_height - total_height) // 2
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

        width = bbox[2] - bbox[0]

        height = bbox[3] - bbox[1]

        x = (
            CARD_WIDTH - width
        ) // 2

        draw.text(
            (
                x,
                y
            ),
            line,
            font=poem_font,
            fill=TEXT_COLOR
        )

        y += height + line_spacing

    # ==================================
    # Footer
    # ==================================

    footer_font = get_font(
        FOOTER_FONT,
        23
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

    footer_y = CARD_HEIGHT - 86

    # tiny separator

    draw.line(
        (
            center_x - 35,
            footer_y - 13,
            center_x + 35,
            footer_y - 13
        ),
        fill=(145, 112, 68),
        width=1
    )

    draw.text(
        (
            footer_x,
            footer_y
        ),
        footer,
        font=footer_font,
        fill=ACCENT_COLOR
    )

    # ==================================
    # Save
    # ==================================

    filename = "/tmp/poetry_card.png"

    image.convert("RGB").save(
        filename,
        "PNG",
        optimize=True
    )

    return filename


# ==================================
# Send Message
# ==================================

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


# ==================================
# Send Photo
# ==================================

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


# ==================================
# Start Message
# ==================================

def send_start_message(chat_id):

    text = (
        "سلام 👋\n\n"
        "🖼️ به بات کارت شعر خوش آمدی.\n\n"
        "شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨\n\n"
        "📖 برای دیدن شعرهای بیشتر، "
        f'<a href="{CHANNEL_URL}">شعرکده</a> '
        "در سروش پلاس را دنبال کن."
    )

    return send_message(
        chat_id,
        text
    )


# ==================================
# After Card Message
# ==================================

def send_after_card_message(chat_id):

    text = (
        "✨ کارت شعر شما آماده شد.\n\n"
        "اگر باز هم شعری دارید، همین‌جا ارسال کنید "
        "تا آن را هم به کارت شعر تبدیل کنیم. 🖼️\n\n"
        "📖 برای دیدن شعرهای بیشتر، "
        f'<a href="{CHANNEL_URL}">«شعرکده»</a> '
        "در سروش پلاس بزنید."
    )

    return send_message(
        chat_id,
        text
    )


# ==================================
# Home
# ==================================

@app.route("/")
def home():

    return (
        "Poetry Card Bot is running",
        200
    )


# ==================================
# Webhook
# ==================================

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

    # --------------------------------
    # /start
    # --------------------------------

    if text == "/start":

        send_start_message(
            user_id
        )

        return "OK", 200

    # --------------------------------
    # Create Card
    # --------------------------------

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


# ==================================
# Run
# ==================================

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
