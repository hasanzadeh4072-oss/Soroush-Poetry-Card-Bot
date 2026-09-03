import os
import random
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"
CHANNEL_URL = "https://splus.ir/life_m23"

# =========================
# Card settings
# =========================

CARD_WIDTH = 1080
CARD_HEIGHT = 1080

TEXT_COLOR = (248, 244, 235)
ACCENT_COLOR = (205, 172, 105)
SUBTITLE_COLOR = (190, 175, 150)
BORDER_COLOR = (150, 120, 70)

POEM_FONT = "BNazanin.ttf"
FALLBACK_FONT = "Vazirmatn-Regular.ttf"
TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"

EMOJI_FONT = "NotoColorEmoji.ttf"
EMOJI_BASE_SIZE = 109

# تناسب عناصر غیر فارسی با متن اصلی
EMOJI_SCALE = 0.78
SYMBOL_SCALE = 0.82

# کش فونت‌ها
_font_cache = {}

# کش ایموجی‌های رندرشده
_emoji_cache = {}


# =========================
# Font helpers
# =========================

def get_font(path, size):
    key = (path, size)

    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)

    return _font_cache[key]


def get_emoji_font():
    """
    NotoColorEmoji یک فونت bitmap است و فقط در اندازه‌های
    مشخصی قابل بارگذاری است. بنابراین همیشه با 109px
    بارگذاری می‌شود و بعد تصویر آن کوچک می‌شود.
    """
    key = ("emoji", EMOJI_BASE_SIZE)

    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(
            EMOJI_FONT,
            EMOJI_BASE_SIZE
        )

    return _font_cache[key]


# =========================
# Character detection
# =========================

def is_persian_char(ch):
    code = ord(ch)

    return (
        0x0600 <= code <= 0x06FF
        or 0x0750 <= code <= 0x077F
        or 0x08A0 <= code <= 0x08FF
        or 0xFB50 <= code <= 0xFDFF
        or 0xFE70 <= code <= 0xFEFF
    )


def is_latin_or_number(ch):
    return (
        ch.isascii()
        and (
            ch.isalnum()
            or ch in "@.-/:+"
        )
    )


def is_symbol(ch):
    return ch in "#_"


def is_variation_selector(ch):
    code = ord(ch)
    return 0xFE00 <= code <= 0xFE0F


def is_skin_tone(ch):
    code = ord(ch)
    return 0x1F3FB <= code <= 0x1F3FF


def is_regional_indicator(ch):
    code = ord(ch)
    return 0x1F1E6 <= code <= 0x1F1FF


def is_emoji_base(ch):
    code = ord(ch)

    return (
        0x1F000 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
        or 0x2300 <= code <= 0x23FF
        or 0x2B00 <= code <= 0x2BFF
    )


# =========================
# Grapheme splitter
# =========================

def split_graphemes(text):
    """
    تقسیم متن به واحدهای قابل رندر.
    حروف فارسی کنار هم باقی می‌مانند.
    ایموجی‌های ZWJ و variation selector نیز یک واحد می‌مانند.
    """

    result = []
    current = ""

    i = 0

    while i < len(text):
        ch = text[i]

        # شروع یک ایموجی یا نماد ویژه
        if is_emoji_base(ch) or is_regional_indicator(ch):

            if current:
                result.append(current)
                current = ""

            cluster = ch
            i += 1

            # variation selector / skin tone
            while i < len(text):
                nxt = text[i]

                if (
                    is_variation_selector(nxt)
                    or is_skin_tone(nxt)
                ):
                    cluster += nxt
                    i += 1
                else:
                    break

            # ZWJ emoji sequence
            while i < len(text) and text[i] == "\u200d":
                cluster += text[i]
                i += 1

                if i < len(text):
                    cluster += text[i]
                    i += 1

                while i < len(text):
                    nxt = text[i]

                    if (
                        is_variation_selector(nxt)
                        or is_skin_tone(nxt)
                    ):
                        cluster += nxt
                        i += 1
                    else:
                        break

            # پرچم‌ها
            if (
                len(cluster) == 1
                and is_regional_indicator(cluster[0])
                and i < len(text)
                and is_regional_indicator(text[i])
            ):
                cluster += text[i]
                i += 1

            result.append(cluster)
            continue

        # ZWJ
        if ch == "\u200d":
            current += ch
            i += 1
            continue

        current += ch
        i += 1

    if current:
        result.append(current)

    return result


# =========================
# Emoji rendering
# =========================

def render_emoji(emoji, target_size):
    display_size = max(
        int(target_size * EMOJI_SCALE),
        16
    )

    cache_key = (emoji, display_size)

    if cache_key in _emoji_cache:
        return _emoji_cache[cache_key]

    font = get_emoji_font()

    # اندازه امن برای رندر فونت NotoColorEmoji
    temp = Image.new(
        "RGBA",
        (EMOJI_BASE_SIZE * 2, EMOJI_BASE_SIZE * 2),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(temp)

    bbox = draw.textbbox(
        (0, 0),
        emoji,
        font=font
    )

    if not bbox:
        return None

    x1, y1, x2, y2 = bbox

    draw.text(
        (-x1 + 10, -y1 + 10),
        emoji,
        font=font,
        embedded_color=True
    )

    bbox2 = temp.getbbox()

    if not bbox2:
        return None

    temp = temp.crop(bbox2)

    # حفظ نسبت
    ratio = display_size / max(temp.width, temp.height)

    new_w = max(int(temp.width * ratio), 1)
    new_h = max(int(temp.height * ratio), 1)

    temp = temp.resize(
        (new_w, new_h),
        Image.Resampling.LANCZOS
    )

    _emoji_cache[cache_key] = temp

    return temp


# =========================
# Mixed text helpers
# =========================

def contains_emoji(text):
    return any(
        is_emoji_base(ch) or is_regional_indicator(ch)
        for ch in text
    )


def contains_special_symbol(text):
    return any(
        ch in "#_"
        for ch in text
    )


def render_persian_with_symbols(
    image,
    xy,
    text,
    primary_font,
    fallback_font,
    fill
):
    """
    هشتگ را به‌صورت ترکیبی رندر می‌کند:

    حروف فارسی:
        BNazanin

    # و _:
        فونت کمکی

    بنابراین مثلاً:
        #پونه_مقیمی

    حروف فارسی‌اش دقیقاً با فونت شعر باقی می‌ماند.
    """

    draw = ImageDraw.Draw(image)

    x, y = xy

    # اگر هشتگ/نماد ندارد، کل عبارت یکجا رندر شود
    if not contains_special_symbol(text):
        draw.text(
            (x, y),
            text,
            font=primary_font,
            fill=fill,
            direction="rtl"
        )
        return

    # واحدهای متنی را جدا می‌کنیم اما حروف فارسی را
    # دانه‌دانه نمی‌کنیم تا شکل‌دهی فارسی خراب نشود.
    parts = []
    current = ""

    for ch in text:
        if ch in "#_":
            if current:
                parts.append(("text", current))
                current = ""

            parts.append(("symbol", ch))

        else:
            current += ch

    if current:
        parts.append(("text", current))

    # برای حفظ ترتیب راست‌به‌چپ، از انتها به ابتدا می‌چینیم.
    cursor_x = x

    for kind, value in reversed(parts):

        if kind == "text":
            bbox = draw.textbbox(
                (0, 0),
                value,
                font=primary_font,
                direction="rtl"
            )

            width = bbox[2] - bbox[0]

            draw.text(
                (cursor_x - width, y),
                value,
                font=primary_font,
                fill=fill,
                direction="rtl"
            )

            cursor_x -= width

        else:
            symbol_size = max(
                int(primary_font.size * SYMBOL_SCALE),
                14
            )

            symbol_font = get_font(
                fallback_font,
                symbol_size
            )

            bbox = draw.textbbox(
                (0, 0),
                value,
                font=symbol_font
            )

            width = bbox[2] - bbox[0]

            # کمی فاصله ظریف
            cursor_x -= 2

            # تنظیم خط مبنا نسبت به BNazanin
            primary_bbox = draw.textbbox(
                (0, 0),
                "آ",
                font=primary_font
            )

            symbol_bbox = draw.textbbox(
                (0, 0),
                value,
                font=symbol_font
            )

            symbol_y = (
                y
                + primary_bbox[3]
                - symbol_bbox[3]
            )

            draw.text(
                (cursor_x - width, symbol_y),
                value,
                font=symbol_font,
                fill=fill
            )

            cursor_x -= width + 2


def render_token(
    image,
    x,
    y,
    token,
    primary_font,
    fallback_font,
    fill
):
    """
    یک کلمه/توکن را رندر می‌کند.
    فارسی با فونت اصلی.
    هشتگ با ترکیب فونت اصلی و کمکی.
    ایموجی با NotoColorEmoji کوچک‌شده.
    """

    draw = ImageDraw.Draw(image)

    if not token:
        return 0

    # اگر توکن کاملاً فارسی/عادی است
    if not contains_emoji(token) and not contains_special_symbol(token):

        draw.text(
            (x, y),
            token,
            font=primary_font,
            fill=fill,
            direction="rtl"
        )

        bbox = draw.textbbox(
            (0, 0),
            token,
            font=primary_font,
            direction="rtl"
        )

        return bbox[2] - bbox[0]

    # هشتگ
    if contains_special_symbol(token) and not contains_emoji(token):

        # عرض واقعی را با همان روش رندر محاسبه می‌کنیم
        temp = Image.new(
            "RGBA",
            (2000, 300),
            (0, 0, 0, 0)
        )

        render_persian_with_symbols(
            temp,
            (1900, 20),
            token,
            primary_font,
            fallback_font,
            fill
        )

        bbox = temp.getbbox()

        if not bbox:
            return 0

        width = bbox[2] - bbox[0]

        render_persian_with_symbols(
            image,
            (x + width, y),
            token,
            primary_font,
            fallback_font,
            fill
        )

        return width

    # توکن دارای ایموجی
    clusters = split_graphemes(token)

    widths = []

    for cluster in clusters:

        if contains_emoji(cluster):

            emoji_img = render_emoji(
                cluster,
                primary_font.size
            )

            if emoji_img:
                widths.append(
                    emoji_img.width
                )
            else:
                widths.append(0)

        else:

            bbox = draw.textbbox(
                (0, 0),
                cluster,
                font=primary_font,
                direction="rtl"
            )

            widths.append(
                bbox[2] - bbox[0]
            )

    total_width = sum(widths)

    cursor_x = x + total_width

    primary_bbox = draw.textbbox(
        (0, 0),
        "آ",
        font=primary_font
    )

    for cluster, width in zip(clusters, widths):

        cursor_x -= width

        if contains_emoji(cluster):

            emoji_img = render_emoji(
                cluster,
                primary_font.size
            )

            if emoji_img:

                emoji_y = (
                    y
                    + primary_bbox[3]
                    - emoji_img.height
                )

                image.alpha_composite(
                    emoji_img,
                    (
                        int(cursor_x),
                        int(emoji_y)
                    )
                )

        else:

            draw.text(
                (cursor_x, y),
                cluster,
                font=primary_font,
                fill=fill,
                direction="rtl"
            )

    return total_width


# =========================
# Line rendering
# =========================

def render_line(
    image,
    x,
    y,
    text,
    primary_font,
    fallback_font,
    fill
):
    draw = ImageDraw.Draw(image)

    if not text:
        return

    # متن عادی بدون ایموجی و هشتگ:
    # کل جمله یکجا رندر می‌شود تا شکل‌دهی فارسی کاملاً حفظ شود.
    if not contains_emoji(text) and not contains_special_symbol(text):

        draw.text(
            (x, y),
            text,
            font=primary_font,
            fill=fill,
            direction="rtl"
        )

        return

    # برای متن ترکیبی، کلمات جدا می‌شوند.
    tokens = text.split(" ")

    # فاصله بین کلمات
    space_bbox = draw.textbbox(
        (0, 0),
        " ",
        font=primary_font
    )

    space_width = space_bbox[2] - space_bbox[0]

    widths = []

    for token in tokens:

        if not token:
            widths.append(0)
            continue

        if contains_emoji(token):

            token_width = 0

            for cluster in split_graphemes(token):

                if contains_emoji(cluster):
                    emoji_img = render_emoji(
                        cluster,
                        primary_font.size
                    )

                    if emoji_img:
                        token_width += emoji_img.width

                else:
                    bbox = draw.textbbox(
                        (0, 0),
                        cluster,
                        font=primary_font,
                        direction="rtl"
                    )

                    token_width += bbox[2] - bbox[0]

            widths.append(token_width)

        elif contains_special_symbol(token):

            temp = Image.new(
                "RGBA",
                (2000, 300),
                (0, 0, 0, 0)
            )

            render_persian_with_symbols(
                temp,
                (1900, 20),
                token,
                primary_font,
                fallback_font,
                fill
            )

            bbox = temp.getbbox()

            widths.append(
                bbox[2] - bbox[0]
                if bbox else 0
            )

        else:

            bbox = draw.textbbox(
                (0, 0),
                token,
                font=primary_font,
                direction="rtl"
            )

            widths.append(
                bbox[2] - bbox[0]
            )

    total_width = (
        sum(widths)
        + space_width * max(len(tokens) - 1, 0)
    )

    cursor_x = x + total_width

    for i, token in enumerate(tokens):

        if not token:
            cursor_x -= space_width
            continue

        token_width = widths[i]

        cursor_x -= token_width

        render_token(
            image,
            cursor_x,
            y,
            token,
            primary_font,
            fallback_font,
            fill
        )

        if i < len(tokens) - 1:
            cursor_x -= space_width


# =========================
# Text measurement
# =========================

def get_text_width(
    text,
    primary_font,
    fallback_font
):
    temp = Image.new(
        "RGBA",
        (3000, 500),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(temp)

    if not contains_emoji(text) and not contains_special_symbol(text):

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=primary_font,
            direction="rtl"
        )

        return bbox[2] - bbox[0]

    # همان مسیر واقعی رندر
    render_line(
        temp,
        2900,
        20,
        text,
        primary_font,
        fallback_font,
        TEXT_COLOR
    )

    bbox = temp.getbbox()

    if not bbox:
        return 0

    return bbox[2] - bbox[0]


# =========================
# Text wrapping
# =========================

def wrap_text(
    text,
    font,
    fallback_font,
    max_width
):
    lines = []

    paragraphs = text.split("\n")

    for paragraph in paragraphs:

        if paragraph.strip() == "":
            lines.append("")
            continue

        words = paragraph.split()

        current = ""

        for word in words:

            candidate = (
                word
                if not current
                else current + " " + word
            )

            width = get_text_width(
                candidate,
                font,
                fallback_font
            )

            if width <= max_width:
                current = candidate

            else:

                if current:
                    lines.append(current)

                # اگر خود کلمه از عرض مجاز بزرگ‌تر است
                # همان را نگه می‌داریم تا ساختار متن خراب نشود.
                current = word

        if current:
            lines.append(current)

    return lines


# =========================
# Background
# =========================

def create_background():
    image = Image.new(
        "RGBA",
        (CARD_WIDTH, CARD_HEIGHT)
    )

    pixels = image.load()

    top = (42, 26, 66)
    middle = (31, 22, 52)
    bottom = (15, 14, 28)

    for y in range(CARD_HEIGHT):

        t = y / (CARD_HEIGHT - 1)

        if t < 0.55:

            local_t = t / 0.55

            r = int(
                top[0]
                + (middle[0] - top[0]) * local_t
            )

            g = int(
                top[1]
                + (middle[1] - top[1]) * local_t
            )

            b = int(
                top[2]
                + (middle[2] - top[2]) * local_t
            )

        else:

            local_t = (t - 0.55) / 0.45

            r = int(
                middle[0]
                + (bottom[0] - middle[0]) * local_t
            )

            g = int(
                middle[1]
                + (bottom[1] - middle[1]) * local_t
            )

            b = int(
                middle[2]
                + (bottom[2] - middle[2]) * local_t
            )

        for x in range(CARD_WIDTH):
            pixels[x, y] = (r, g, b, 255)

    # نور نرم
    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.ellipse(
        (170, -160, 900, 570),
        fill=(112, 71, 150, 35)
    )

    glow_draw.ellipse(
        (350, 570, 1200, 1250),
        fill=(80, 55, 120, 20)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(90)
    )

    image.alpha_composite(glow)

    # بافت بسیار ظریف
    texture = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    texture_draw = ImageDraw.Draw(texture)

    for _ in range(18000):

        x = random.randrange(CARD_WIDTH)
        y = random.randrange(CARD_HEIGHT)

        alpha = random.randrange(3, 12)

        texture_draw.point(
            (x, y),
            fill=(255, 255, 255, alpha)
        )

    image.alpha_composite(texture)

    return image


# =========================
# Create poetry card
# =========================

def create_card(poem):
    image = create_background()
    draw = ImageDraw.Draw(image)

    # -------------------------
    # Outer border
    # -------------------------

    draw.rounded_rectangle(
        (42, 42, 1038, 1038),
        radius=38,
        outline=(
            BORDER_COLOR[0],
            BORDER_COLOR[1],
            BORDER_COLOR[2],
            150
        ),
        width=2
    )

    # -------------------------
    # Header
    # -------------------------

    title_font = get_font(
        TITLE_FONT,
        48
    )

    subtitle_font = get_font(
        SUBTITLE_FONT,
        24
    )

    title = "شعرکده"
    subtitle = "( سروش پلاس )"

    title_bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font,
        direction="rtl"
    )

    title_width = (
        title_bbox[2] - title_bbox[0]
    )

    subtitle_bbox = draw.textbbox(
        (0, 0),
        subtitle,
        font=subtitle_font,
        direction="rtl"
    )

    subtitle_width = (
        subtitle_bbox[2] - subtitle_bbox[0]
    )

    gap = 18

    total_width = (
        title_width
        + gap
        + subtitle_width
    )

    start_x = (
        CARD_WIDTH - total_width
    ) / 2

    title_x = (
        start_x
        + subtitle_width
        + gap
    )

    subtitle_x = start_x

    title_y = 82
    subtitle_y = 79

    draw.text(
        (title_x, title_y),
        title,
        font=title_font,
        fill=ACCENT_COLOR,
        direction="rtl"
    )

    draw.text(
        (subtitle_x, subtitle_y),
        subtitle,
        font=subtitle_font,
        fill=SUBTITLE_COLOR,
        direction="rtl"
    )

    # خط زیر عنوان
    line_y = (
        title_y
        + (title_bbox[3] - title_bbox[1])
        + 24
    )

    draw.line(
        (
            CARD_WIDTH // 2 - 60,
            line_y,
            CARD_WIDTH // 2 + 60,
            line_y
        ),
        fill=ACCENT_COLOR,
        width=2
    )

    # نقطه وسط خط
    draw.ellipse(
        (
            CARD_WIDTH // 2 - 4,
            line_y - 4,
            CARD_WIDTH // 2 + 4,
            line_y + 4
        ),
        fill=ACCENT_COLOR
    )

    # -------------------------
    # Poem
    # -------------------------

    max_width = 900

    text_top = 220
    text_bottom = 900

    selected_font = None
    selected_lines = None

    for size in range(58, 27, -1):

        font = get_font(
            POEM_FONT,
            size
        )

        lines = wrap_text(
            poem,
            font,
            FALLBACK_FONT,
            max_width
        )

        line_height = size + 20
        blank_spacing = 48

        total_height = 0

        for line in lines:

            if line == "":
                total_height += blank_spacing
            else:
                total_height += line_height

        if total_height <= (
            text_bottom - text_top
        ):
            selected_font = font
            selected_lines = lines
            break

    if selected_font is None:
        selected_font = get_font(
            POEM_FONT,
            28
        )

        selected_lines = wrap_text(
            poem,
            selected_font,
            FALLBACK_FONT,
            max_width
        )

    # -------------------------
    # Glass poem panel
    # -------------------------

    panel_top = text_top - 35

    panel_bottom = text_bottom + 35

    panel = Image.new(
        "RGBA",
        image.size,
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
        outline=(255, 255, 255, 18),
        width=1
    )

    image.alpha_composite(panel)

    # -------------------------
    # Poem text
    # -------------------------

    line_height = selected_font.size + 20
    blank_spacing = 48

    current_y = text_top

    for line in selected_lines:

        if line == "":
            current_y += blank_spacing
            continue

        line_width = get_text_width(
            line,
            selected_font,
            FALLBACK_FONT
        )

        x = (
            CARD_WIDTH / 2
            + line_width / 2
        )

        render_line(
            image,
            x,
            current_y,
            line,
            selected_font,
            FALLBACK_FONT,
            TEXT_COLOR
        )

        current_y += line_height

    # -------------------------
    # Side decorative marks
    # -------------------------

    mark_y = (
        text_top
        + (text_bottom - text_top) / 2
    )

    draw.line(
        (78, mark_y - 18, 78, mark_y + 18),
        fill=(205, 172, 105, 55),
        width=1
    )

    draw.line(
        (1002, mark_y - 18, 1002, mark_y + 18),
        fill=(205, 172, 105, 55),
        width=1
    )

    # -------------------------
    # Footer
    # -------------------------

    footer_font = get_font(
        FOOTER_FONT,
        24
    )

    footer = "کارت شعر"

    footer_bbox = draw.textbbox(
        (0, 0),
        footer,
        font=footer_font,
        direction="rtl"
    )

    footer_width = (
        footer_bbox[2] - footer_bbox[0]
    )

    footer_x = (
        CARD_WIDTH
        / 2
        + footer_width / 2
    )

    draw.text(
        (footer_x, 990),
        footer,
        font=footer_font,
        fill=SUBTITLE_COLOR,
        direction="rtl"
    )

    return image


# =========================
# Soroush API
# =========================

def send_message(chat_id, text):
    url = f"{API}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=30
        )

        print(
            "sendMessage:",
            response.status_code,
            response.text
        )

        return response

    except Exception as e:
        print(
            "sendMessage error:",
            e
        )

        return None


def send_photo(chat_id, image):
    url = f"{API}/sendPhoto"

    image_path = "/tmp/poetry_card.png"

    image.convert("RGB").save(
        image_path,
        "PNG",
        optimize=True
    )

    try:

        with open(image_path, "rb") as photo:

            files = {
                "photo": (
                    "poetry_card.png",
                    photo,
                    "image/png"
                )
            }

            data = {
                "chat_id": chat_id
            }

            response = requests.post(
                url,
                data=data,
                files=files,
                timeout=60
            )

        print(
            "sendPhoto:",
            response.status_code,
            response.text
        )

        return response

    except Exception as e:

        print(
            "sendPhoto error:",
            e
        )

        return None


# =========================
# Messages
# =========================

def send_start_message(chat_id):

    text = """سلام 👋

🖼️ به بات کارت شعر خوش آمدی.

شعرت را همین‌جا بفرست تا برایت کارت شعر بسازم. ✨

📖 برای دیدن شعرهای بیشتر، شعرکده در سروش پلاس را دنبال کن."""

    # لینک فقط روی «شعرکده»
    text = text.replace(
        "شعرکده در سروش پلاس",
        f'<a href="{CHANNEL_URL}">شعرکده</a> در سروش پلاس'
    )

    return send_message(
        chat_id,
        text
    )


def send_success_message(chat_id):

    text = """✨ کارت شعر شما آماده شد.

اگر باز هم شعری دارید، همین‌جا ارسال کنید تا آن را هم به کارت شعر تبدیل کنیم. 🖼️

📖 برای دیدن شعرهای بیشتر، سری هم به کانال «شعرکده» در سروش پلاس بزنید."""

    text = text.replace(
        "«شعرکده»",
        f'<a href="{CHANNEL_URL}">«شعرکده»</a>'
    )

    return send_message(
        chat_id,
        text
    )


# =========================
# Webhook
# =========================

@app.route("/", methods=["GET"])
def home():
    return "Poetry Card Bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        update = request.get_json(
            silent=True
        ) or {}

        print(
            "UPDATE:",
            update
        )

        message = update.get(
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

        text = message.get(
            "text"
        )

        if not chat_id or text is None:
            return "OK", 200

        # -------------------------
        # /start
        # -------------------------

        if text.strip() == "/start":

            send_start_message(
                chat_id
            )

            return "OK", 200

        # -------------------------
        # Create card
        # -------------------------

        try:

            card = create_card(
                text
            )

        except Exception as e:

            print(
                "Card creation error:",
                e
            )

            send_message(
                chat_id,
                "❌ هنگام ساخت کارت مشکلی پیش آمد."
            )

            return "OK", 200

        # -------------------------
        # Send card
        # -------------------------

        response = send_photo(
            chat_id,
            card
        )

        # پیام موفقیت فقط زمانی ارسال شود
        # که خود تصویر با موفقیت ارسال شده باشد.
        if response is not None and response.ok:

            send_success_message(
                chat_id
            )

        else:

            send_message(
                chat_id,
                "✅ کارت ساخته شد، اما ارسال تصویر موفق نشد."
            )

        return "OK", 200

    except Exception as e:

        print(
            "Webhook error:",
            e
        )

        return "OK", 200


# =========================
# Run
# =========================

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
