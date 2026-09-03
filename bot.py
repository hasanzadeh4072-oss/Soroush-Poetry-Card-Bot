import os
import random
import requests

from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter


app = Flask(__name__)


# =========================================================
# Soroush Plus
# =========================================================

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

CHANNEL_URL = "https://splus.ir/life_m23"


# =========================================================
# Card settings
# =========================================================

CARD_WIDTH = 1080
CARD_HEIGHT = 1080

TEXT_COLOR = (248, 244, 235)
ACCENT_COLOR = (205, 172, 105)
SUBTITLE_COLOR = (190, 175, 150)
BORDER_COLOR = (150, 120, 70)


# =========================================================
# Fonts
# =========================================================

POEM_FONT = "BNazanin.ttf"
FALLBACK_FONT = "Vazirmatn-Regular.ttf"

TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"

EMOJI_FONT = "NotoColorEmoji.ttf"

# IMPORTANT:
# NotoColorEmoji is a bitmap/color font and does not accept
# arbitrary pixel sizes. 109 is the supported base size.
EMOJI_BASE_SIZE = 109


# =========================================================
# Font cache
# =========================================================

_font_cache = {}
_emoji_cache = {}


def get_font(font_name, size):
    """
    Load and cache normal fonts.
    """

    key = (font_name, size)

    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(
            font_name,
            size
        )

    return _font_cache[key]


def get_emoji_font():
    """
    Load NotoColorEmoji ONLY at its supported base size.
    """

    key = (EMOJI_FONT, EMOJI_BASE_SIZE)

    if key not in _font_cache:

        _font_cache[key] = ImageFont.truetype(
            EMOJI_FONT,
            EMOJI_BASE_SIZE
        )

    return _font_cache[key]


# =========================================================
# Background
# =========================================================

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

            r = int(
                top[0] * (1 - t)
                + middle[0] * t
            )

            g = int(
                top[1] * (1 - t)
                + middle[1] * t
            )

            b = int(
                top[2] * (1 - t)
                + middle[2] * t
            )

        else:

            t = (ratio - 0.55) / 0.45

            r = int(
                middle[0] * (1 - t)
                + bottom[0] * t
            )

            g = int(
                middle[1] * (1 - t)
                + bottom[1] * t
            )

            b = int(
                middle[2] * (1 - t)
                + bottom[2] * t
            )

        for x in range(CARD_WIDTH):

            pixels[x, y] = (
                r,
                g,
                b
            )

    # -----------------------------------------------------
    # Soft glow
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Subtle texture
    # -----------------------------------------------------

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


# =========================================================
# Text normalization
# =========================================================

def normalize_text(text):

    # BNazanin may display … incorrectly.
    # Use three normal dots instead.
    return text.replace("…", "...")


# =========================================================
# Character / emoji detection
# =========================================================

def is_emoji_base(char):

    code = ord(char)

    return (
        0x1F000 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
        or 0x2300 <= code <= 0x23FF
        or 0x2B00 <= code <= 0x2BFF
    )


def is_variation_selector(char):

    code = ord(char)

    return (
        0xFE00 <= code <= 0xFE0F
    )


def is_skin_tone(char):

    code = ord(char)

    return (
        0x1F3FB <= code <= 0x1F3FF
    )


def is_regional_indicator(char):

    code = ord(char)

    return (
        0x1F1E6 <= code <= 0x1F1FF
    )


def is_combining_mark(char):

    code = ord(char)

    return (
        0x0300 <= code <= 0x036F
        or 0x1AB0 <= code <= 0x1AFF
        or 0x1DC0 <= code <= 0x1DFF
        or 0x20D0 <= code <= 0x20FF
        or 0xFE20 <= code <= 0xFE2F
    )


def split_graphemes(text):

    """
    A lightweight Unicode grapheme/emoji cluster splitter.

    This keeps sequences such as:
        ❤️
        👩‍💻
        👍🏽
        🇮🇷
        #️⃣

    together instead of treating every Unicode codepoint
    as a separate character.
    """

    clusters = []

    i = 0

    while i < len(text):

        char = text[i]

        # -------------------------------------------------
        # Newline
        # -------------------------------------------------

        if char == "\n":

            clusters.append("\n")
            i += 1
            continue

        cluster = char

        # -------------------------------------------------
        # Regional indicator pair (flags)
        # -------------------------------------------------

        if is_regional_indicator(char):

            if (
                i + 1 < len(text)
                and is_regional_indicator(text[i + 1])
            ):

                cluster += text[i + 1]
                i += 2

                clusters.append(cluster)
                continue

        # -------------------------------------------------
        # Variation selector / skin tone / combining mark
        # -------------------------------------------------

        j = i + 1

        while j < len(text):

            next_char = text[j]

            if (
                is_variation_selector(next_char)
                or is_skin_tone(next_char)
                or is_combining_mark(next_char)
            ):

                cluster += next_char
                j += 1
                continue

            break

        # -------------------------------------------------
        # ZWJ emoji sequence
        # -------------------------------------------------

        while (
            j < len(text)
            and text[j] == "\u200d"
        ):

            cluster += text[j]
            j += 1

            if j < len(text):

                cluster += text[j]
                j += 1

            while j < len(text):

                next_char = text[j]

                if (
                    is_variation_selector(next_char)
                    or is_skin_tone(next_char)
                    or is_combining_mark(next_char)
                ):

                    cluster += next_char
                    j += 1

                else:

                    break

        clusters.append(cluster)

        i = max(j, i + 1)

    return clusters


def is_emoji_cluster(cluster):

    if not cluster:
        return False

    for char in cluster:

        if is_emoji_base(char):
            return True

    # Keycap emoji:
    # #️⃣  *️⃣  1️⃣
    if (
        "\ufe0f" in cluster
        and "\u20e3" in cluster
    ):

        return True

    return False


def is_fallback_character(char):

    if is_emoji_base(char):
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


# =========================================================
# Emoji rendering
# =========================================================

def render_emoji(cluster, target_size):

    """
    Render one emoji cluster using NotoColorEmoji at its
    fixed supported size (109px), then resize it.

    This completely avoids the:
        OSError: invalid pixel size
    """

    cache_key = (
        cluster,
        target_size
    )

    if cache_key in _emoji_cache:

        return _emoji_cache[cache_key]

    try:

        emoji_font = get_emoji_font()

        # Large transparent canvas
        canvas_size = EMOJI_BASE_SIZE * 2

        canvas = Image.new(
            "RGBA",
            (
                canvas_size,
                canvas_size
            ),
            (0, 0, 0, 0)
        )

        emoji_draw = ImageDraw.Draw(canvas)

        emoji_draw.text(
            (
                EMOJI_BASE_SIZE // 2,
                EMOJI_BASE_SIZE // 2
            ),
            cluster,
            font=emoji_font,
            embedded_color=True
        )

        bbox = canvas.getbbox()

        if bbox is None:

            return None

        cropped = canvas.crop(bbox)

        # Keep emoji proportional.
        max_height = max(
            int(target_size * 1.05),
            1
        )

        scale = (
            max_height
            / cropped.height
        )

        new_width = max(
            int(cropped.width * scale),
            1
        )

        new_height = max(
            int(cropped.height * scale),
            1
        )

        resized = cropped.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.LANCZOS
        )

        _emoji_cache[cache_key] = resized

        return resized

    except Exception as error:

        print(
            "Emoji render error:",
            repr(error),
            "cluster:",
            repr(cluster)
        )

        return None


def get_cluster_width(
    cluster,
    primary_font,
    fallback_font,
    target_size
):

    # -----------------------------------------------------
    # Emoji
    # -----------------------------------------------------

    if is_emoji_cluster(cluster):

        emoji_image = render_emoji(
            cluster,
            target_size
        )

        if emoji_image is not None:

            return emoji_image.width

        # Safe fallback if emoji rendering fails.
        fallback_bbox = fallback_font.getbbox(
            cluster
        )

        return max(
            fallback_bbox[2] - fallback_bbox[0],
            target_size // 2
        )

    # -----------------------------------------------------
    # Fallback characters
    # -----------------------------------------------------

    if len(cluster) == 1 and is_fallback_character(cluster):

        bbox = fallback_font.getbbox(
            cluster
        )

        return bbox[2] - bbox[0]

    # -----------------------------------------------------
    # Normal Persian text
    # -----------------------------------------------------

    bbox = primary_font.getbbox(
        cluster
    )

    return bbox[2] - bbox[0]


def get_text_width(
    text,
    primary_font,
    fallback_font,
    target_size
):

    total = 0

    clusters = split_graphemes(text)

    for cluster in clusters:

        if cluster == "\n":
            continue

        total += get_cluster_width(
            cluster,
            primary_font,
            fallback_font,
            target_size
        )

    return total


# =========================================================
# Text wrapping
# =========================================================

def wrap_text(
    text,
    primary_font,
    fallback_font,
    target_size,
    max_width
):

    words = text.split()

    if not words:
        return []

    lines = []

    current = words[0]

    for word in words[1:]:

        test = (
            current
            + " "
            + word
        )

        width = get_text_width(
            test,
            primary_font,
            fallback_font,
            target_size
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
    text,
    primary_font,
    fallback_font,
    target_size,
    max_width
):

    text = normalize_text(text)

    raw_lines = text.splitlines()

    final_lines = []

    for line in raw_lines:

        # Preserve user's blank lines.
        if not line.strip():

            final_lines.append(None)
            continue

        wrapped = wrap_text(
            line.strip(),
            primary_font,
            fallback_font,
            target_size,
            max_width
        )

        final_lines.extend(wrapped)

    return final_lines


# =========================================================
# Text height
# =========================================================

def calculate_text_height(
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

        bbox = font.getbbox(
            line
        )

        height = (
            bbox[3] - bbox[1]
        )

        total += (
            height
            + line_spacing
        )

    if lines[-1] is not None:

        total -= line_spacing

    return total


# =========================================================
# Draw mixed Persian + fallback + emoji
# =========================================================

def draw_text_with_fallback(
    image,
    position,
    text,
    primary_font,
    fallback_font,
    target_size,
    fill
):

    draw = ImageDraw.Draw(image)

    x, y = position

    clusters = split_graphemes(text)

    # Primary font metrics for approximate baseline.
    primary_bbox = primary_font.getbbox("آ")

    primary_bottom = primary_bbox[3]

    for cluster in clusters:

        if cluster == "\n":
            continue

        # -------------------------------------------------
        # Emoji
        # -------------------------------------------------

        if is_emoji_cluster(cluster):

            emoji_image = render_emoji(
                cluster,
                target_size
            )

            if emoji_image is not None:

                # Align emoji visually with text baseline.
                emoji_y = (
                    y
                    + primary_bottom
                    - emoji_image.height
                )

                image.alpha_composite(
                    emoji_image,
                    (
                        int(x),
                        int(emoji_y)
                    )
                )

                x += emoji_image.width

                continue

            # If emoji rendering failed,
            # safely fall through to fallback font.

        # -------------------------------------------------
        # Fallback
        # -------------------------------------------------

        if len(cluster) == 1 and is_fallback_character(cluster):

            bbox = fallback_font.getbbox(
                cluster
            )

            draw.text(
                (x, y),
                cluster,
                font=fallback_font,
                fill=fill
            )

            x += (
                bbox[2]
                - bbox[0]
            )

            continue

        # -------------------------------------------------
        # Normal Persian
        # -------------------------------------------------

        bbox = primary_font.getbbox(
            cluster
        )

        draw.text(
            (x, y),
            cluster,
            font=primary_font,
            fill=fill
        )

        x += (
            bbox[2]
            - bbox[0]
        )


# =========================================================
# Create poetry card
# =========================================================

def create_poetry_card(text):

    image = create_gradient_background()

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # Outer border
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

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
        title_bbox[2]
        - title_bbox[0]
    )

    title_height = (
        title_bbox[3]
        - title_bbox[1]
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
        subtitle_bbox[2]
        - subtitle_bbox[0]
    )

    subtitle_height = (
        subtitle_bbox[3]
        - subtitle_bbox[1]
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

    # -----------------------------------------------------
    # Header line
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Poem area
    # -----------------------------------------------------

    text_left = 90
    text_right = 990

    max_width = (
        text_right
        - text_left
    )

    text_top = 220
    text_bottom = 900

    available_height = (
        text_bottom
        - text_top
    )

    font_size = 58
    min_font_size = 28

    line_spacing = 20
    blank_line_spacing = 48

    lines = []

    # -----------------------------------------------------
    # Adaptive font size
    # -----------------------------------------------------

    while font_size >= min_font_size:

        poem_font = get_font(
            POEM_FONT,
            font_size
        )

        fallback_font = get_font(
            FALLBACK_FONT,
            font_size
        )

        lines = prepare_poem_lines(
            text,
            poem_font,
            fallback_font,
            font_size,
            max_width
        )

        total_height = calculate_text_height(
            lines,
            poem_font,
            line_spacing,
            blank_line_spacing
        )

        if total_height <= available_height:
            break

        font_size -= 2

    # -----------------------------------------------------
    # Empty text safety
    # -----------------------------------------------------

    if not lines:

        poem_font = get_font(
            POEM_FONT,
            48
        )

        fallback_font = get_font(
            FALLBACK_FONT,
            48
        )

        font_size = 48

        lines = [
            "متن خالی است"
        ]

    # -----------------------------------------------------
    # Final poem height
    # -----------------------------------------------------

    total_height = calculate_text_height(
        lines,
        poem_font,
        line_spacing,
        blank_line_spacing
    )

    # -----------------------------------------------------
    # Glass poem panel
    # -----------------------------------------------------

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
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
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

    # -----------------------------------------------------
    # Decorative side marks
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Draw poem
    # -----------------------------------------------------

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

        width = get_text_width(
            line,
            poem_font,
            fallback_font,
            font_size
        )

        bbox = poem_font.getbbox(
            line
        )

        height = (
            bbox[3]
            - bbox[1]
        )

        x = (
            CARD_WIDTH
            - width
        ) // 2

        draw_text_with_fallback(
            image,
            (
                x,
                y
            ),
            line,
            poem_font,
            fallback_font,
            font_size,
            TEXT_COLOR
        )

        y += (
            height
            + line_spacing
        )

    # -----------------------------------------------------
    # Footer
    # -----------------------------------------------------

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
        footer_bbox[2]
        - footer_bbox[0]
    )

    footer_x = (
        CARD_WIDTH
        - footer_width
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

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    filename = "/tmp/poetry_card.png"

    image.convert("RGB").save(
        filename,
        "PNG",
        optimize=True
    )

    return filename


# =========================================================
# Soroush Plus messaging
# =========================================================

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

        with open(
            filename,
            "rb"
        ) as photo:

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


# =========================================================
# Start message
# =========================================================

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


# =========================================================
# After card message
# =========================================================

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


# =========================================================
# Home
# =========================================================

@app.route("/")
def home():

    return (
        "Poetry Card Bot is running",
        200
    )


# =========================================================
# Webhook
# =========================================================

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

    # -----------------------------------------------------
    # /start
    # -----------------------------------------------------

    if text == "/start":

        send_start_message(
            user_id
        )

        return "OK", 200

    # -----------------------------------------------------
    # Create and send card
    # -----------------------------------------------------

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
            repr(error)
        )

        send_message(
            user_id,
            "❌ هنگام ساخت کارت مشکلی پیش آمد."
        )

    return "OK", 200


# =========================================================
# Run
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
