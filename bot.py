import os
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter


app = Flask(__name__)


TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

CHANNEL_URL = "https://splus.ir/life_m23"


CARD_WIDTH = 1080
CARD_HEIGHT = 1080


POEM_FONT = "BNazanin.ttf"
TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"


# ==================================
# Pending Poems
# ==================================

# هر کاربر یک شعر در انتظار انتخاب رنگ دارد.
# با ارسال شعر جدید، شعر قبلی جایگزین می‌شود.
PENDING_POEMS = {}


# ==================================
# Color Palettes
# فقط رنگ‌ها تغییر می‌کنند
# ==================================

PALETTES = [

    # 1. Royal Purple
    {
        "name": "بنفش سلطنتی",

        "top": (55, 25, 82),
        "middle": (32, 21, 53),
        "bottom": (13, 10, 25),

        "glow1": (160, 105, 200, 38),
        "glow2": (105, 70, 160, 22),
        "glow3": (100, 65, 145, 10),

        "frame": (173, 137, 82),
        "frame_inner": (205, 172, 105),

        "text": (248, 244, 235),
        "accent": (244, 210, 137),
        "subtitle": (205, 191, 168),
        "ornament": (145, 112, 68),

        "panel_outline": (205, 172, 105, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (205, 172, 105, 75),
        "side_dot": (205, 172, 105, 100),
    },


    # 2. Midnight Blue
    {
        "name": "آبی شبانه",

        "top": (18, 39, 76),
        "middle": (16, 27, 53),
        "bottom": (7, 11, 23),

        "glow1": (75, 115, 185, 32),
        "glow2": (50, 80, 150, 22),
        "glow3": (55, 85, 140, 10),

        "frame": (165, 140, 83),
        "frame_inner": (200, 170, 103),

        "text": (246, 246, 241),
        "accent": (239, 210, 139),
        "subtitle": (195, 204, 211),
        "ornament": (140, 125, 82),

        "panel_outline": (190, 170, 110, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (200, 175, 110, 75),
        "side_dot": (215, 185, 115, 100),
    },


    # 3. Emerald
    {
        "name": "سبز زمردی",

        "top": (12, 59, 51),
        "middle": (13, 38, 35),
        "bottom": (5, 18, 17),

        "glow1": (65, 145, 120, 35),
        "glow2": (45, 110, 95, 20),
        "glow3": (40, 100, 85, 10),

        "frame": (168, 139, 78),
        "frame_inner": (200, 169, 99),

        "text": (246, 246, 238),
        "accent": (239, 211, 137),
        "subtitle": (194, 207, 197),
        "ornament": (140, 118, 70),

        "panel_outline": (190, 165, 100, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (190, 170, 105, 75),
        "side_dot": (210, 180, 110, 100),
    },


    # 4. Burgundy
    {
        "name": "شرابی",

        "top": (76, 19, 37),
        "middle": (45, 14, 26),
        "bottom": (20, 6, 13),

        "glow1": (175, 70, 90, 35),
        "glow2": (135, 45, 65, 20),
        "glow3": (130, 45, 60, 10),

        "frame": (174, 133, 72),
        "frame_inner": (205, 169, 98),

        "text": (249, 244, 237),
        "accent": (241, 210, 139),
        "subtitle": (211, 193, 181),
        "ornament": (145, 105, 65),

        "panel_outline": (195, 155, 95, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (200, 160, 100, 75),
        "side_dot": (215, 175, 105, 100),
    },


    # 5. Dark Mocha
    {
        "name": "قهوه‌ای شکلاتی",

        "top": (59, 37, 24),
        "middle": (39, 26, 19),
        "bottom": (17, 10, 7),

        "glow1": (170, 110, 60, 32),
        "glow2": (125, 75, 40, 20),
        "glow3": (110, 65, 38, 10),

        "frame": (174, 133, 70),
        "frame_inner": (202, 166, 98),

        "text": (249, 243, 232),
        "accent": (239, 205, 132),
        "subtitle": (211, 195, 174),
        "ornament": (145, 105, 62),

        "panel_outline": (195, 155, 90, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (200, 160, 95, 75),
        "side_dot": (215, 175, 105, 100),
    },


    # 6. Charcoal Gold
    {
        "name": "ذغالی طلایی",

        "top": (28, 28, 30),
        "middle": (19, 19, 21),
        "bottom": (7, 7, 8),

        "glow1": (190, 145, 70, 25),
        "glow2": (135, 100, 50, 15),
        "glow3": (120, 90, 45, 8),

        "frame": (170, 140, 78),
        "frame_inner": (198, 165, 98),

        "text": (247, 244, 235),
        "accent": (240, 208, 133),
        "subtitle": (197, 194, 184),
        "ornament": (140, 115, 68),

        "panel_outline": (190, 150, 85, 24),
        "panel_inner": (255, 255, 255, 8),

        "side_line": (195, 160, 95, 75),
        "side_dot": (215, 175, 105, 100),
    },
]


# ==================================
# Font
# ==================================

def get_font(font_name, size):
    return ImageFont.truetype(font_name, size)


# ==================================
# Luxury Background
# ==================================

def create_gradient_background(palette):

    image = Image.new(
        "RGB",
        (CARD_WIDTH, CARD_HEIGHT)
    )

    pixels = image.load()

    top = palette["top"]
    middle = palette["middle"]
    bottom = palette["bottom"]


    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        if ratio < 0.52:

            t = ratio / 0.52

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

            t = (ratio - 0.52) / 0.48

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
        fill=palette["glow1"]
    )


    glow_draw.ellipse(
        (690, 690, 1250, 1250),
        fill=palette["glow2"]
    )


    glow_draw.ellipse(
        (250, 350, 850, 950),
        fill=palette["glow3"]
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


    # ثابت نگه داشتن بافت
    # تا ظاهر اصلی قالب تغییر نکند.
    import random

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

    return text.replace(
        "…",
        "..."
    )


def wrap_text(
    draw,
    text,
    font,
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

            lines.append(
                current
            )

            current = word


    if current:

        lines.append(
            current
        )


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


        final_lines.extend(
            wrapped
        )


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


        height = (
            bbox[3]
            - bbox[1]
        )


        total += (
            height
            + line_spacing
        )


    if lines[-1] is not None:

        total -= line_spacing


    return total


# ==================================
# Create Poetry Card
# ==================================

def create_poetry_card(
    text,
    palette
):

    image = create_gradient_background(
        palette
    )


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
        outline=palette["frame"],
        width=2
    )


    # ==================================
    # Inner subtle frame
    # ==================================

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
        title_bbox[2]
        - title_bbox[0]
    )


    title_height = (
        title_bbox[3]
        - title_bbox[1]
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
        subtitle_bbox[2]
        - subtitle_bbox[0]
    )


    subtitle_height = (
        subtitle_bbox[3]
        - subtitle_bbox[1]
    )


    title_y = 78


    header_center = (
        CARD_WIDTH // 2
    )


    gap = 20


    title_x = (
        header_center + 10
    )


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
        fill=palette["accent"]
    )


    draw.text(
        (
            subtitle_x,
            subtitle_y
        ),
        subtitle,
        font=subtitle_font,
        fill=palette["subtitle"]
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


    center_x = (
        CARD_WIDTH // 2
    )


    # left line

    draw.line(
        (
            center_x - line_width,
            line_y,
            center_x - 12,
            line_y
        ),
        fill=palette["ornament"],
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
        fill=palette["ornament"],
        width=1
    )


    # center diamond

    diamond_size = 5


    draw.polygon(
        [
            (
                center_x,
                line_y - diamond_size
            ),
            (
                center_x + diamond_size,
                line_y
            ),
            (
                center_x,
                line_y + diamond_size
            ),
            (
                center_x - diamond_size,
                line_y
            )
        ],
        fill=palette["accent"]
    )


    # ==================================
    # Poem Area
    # ==================================

    text_left = 75
    text_right = 1005


    max_width = (
        text_right
        - text_left
    )


    text_top = 218
    text_bottom = 895


    available_height = (
        text_bottom
        - text_top
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


    panel_draw = ImageDraw.Draw(
        panel
    )


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
        outline=palette["panel_outline"],
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
        outline=palette["panel_inner"],
        width=1
    )


    panel = panel.filter(
        ImageFilter.GaussianBlur(0.35)
    )


    image = Image.alpha_composite(
        image.convert("RGBA"),
        panel
    )


    draw = ImageDraw.Draw(
        image
    )


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
        fill=palette["side_line"],
        width=1
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


    # right

    draw.line(
        (
            1001,
            deco_y - 30,
            1001,
            deco_y + 30
        ),
        fill=palette["side_line"],
        width=1
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


        width = (
            bbox[2]
            - bbox[0]
        )


        height = (
            bbox[3]
            - bbox[1]
        )


        # وسط‌چین

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
            fill=palette["text"]
        )


        y += (
            height
            + line_spacing
        )


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
        footer_bbox[2]
        - footer_bbox[0]
    )


    footer_x = (
        CARD_WIDTH - footer_width
    ) // 2


    footer_y = (
        CARD_HEIGHT - 86
    )


    # tiny separator

    draw.line(
        (
            center_x - 35,
            footer_y - 13,
            center_x + 35,
            footer_y - 13
        ),
        fill=palette["ornament"],
        width=1
    )


    draw.text(
        (
            footer_x,
            footer_y
        ),
        footer,
        font=footer_font,
        fill=palette["accent"]
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

def send_message(
    chat_id,
    text,
    reply_markup=None
):

    try:

        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }


        if reply_markup is not None:

            data["reply_markup"] = reply_markup


        response = requests.post(
            f"{API}/sendMessage",
            json=data,
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

def send_photo(
    chat_id,
    filename
):

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


# ==================================
# Answer Callback Query
# ==================================

def answer_callback_query(
    callback_query_id
):

    try:

        response = requests.post(
            f"{API}/answerCallbackQuery",
            json={
                "callback_query_id":
                    callback_query_id
            },
            timeout=20
        )


        print(
            "answerCallbackQuery:",
            response.status_code,
            response.text
        )


        return response


    except Exception as error:

        print(
            "answerCallbackQuery error:",
            error
        )


        return None


# ==================================
# Color Keyboard
# ==================================

def get_color_keyboard():

    return {
        "inline_keyboard": [

            [
                {
                    "text": "🟣 بنفش سلطنتی",
                    "callback_data": "color_0"
                },
                {
                    "text": "🔵 آبی شبانه",
                    "callback_data": "color_1"
                }
            ],

            [
                {
                    "text": "🟢 سبز زمردی",
                    "callback_data": "color_2"
                },
                {
                    "text": "🔴 شرابی",
                    "callback_data": "color_3"
                }
            ],

            [
                {
                    "text": "🟤 قهوه‌ای شکلاتی",
                    "callback_data": "color_4"
                },
                {
                    "text": "⚫ ذغالی طلایی",
                    "callback_data": "color_5"
                }
            ]

        ]
    }


# ==================================
# Ask For Color
# ==================================

def send_color_selection(
    chat_id
):

    text = (
        "🎨 رنگ کارت شعر را انتخاب کن:"
    )


    return send_message(
        chat_id,
        text,
        get_color_keyboard()
    )


# ==================================
# Start Message
# ==================================

def send_start_message(
    chat_id
):

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

def send_after_card_message(
    chat_id
):

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
# Process Selected Color
# ==================================

def process_color_selection(
    update
):

    callback_query = (
        update.get("callback_query")
        or {}
    )


    callback_id = (
        callback_query.get("id")
    )


    data = (
        callback_query.get("data")
        or ""
    )


    callback_message = (
        callback_query.get("message")
        or {}
    )


    chat = (
        callback_message.get("chat")
        or {}
    )


    chat_id = chat.get("id")


    # --------------------------------
    # همیشه Callback را تأیید می‌کنیم
    # --------------------------------

    if callback_id:

        answer_callback_query(
            callback_id
        )


    if not chat_id:

        return


    # --------------------------------
    # بررسی رنگ
    # --------------------------------

    if not data.startswith(
        "color_"
    ):

        return


    try:

        palette_index = int(
            data.replace(
                "color_",
                ""
            )
        )

    except ValueError:

        return


    if (
        palette_index < 0
        or palette_index >= len(PALETTES)
    ):

        send_message(
            chat_id,
            "❌ انتخاب رنگ نامعتبر است."
        )

        return


    # --------------------------------
    # پیدا کردن شعر ذخیره‌شده
    # --------------------------------

    poem = PENDING_POEMS.get(
        chat_id
    )


    if not poem:

        send_message(
            chat_id,
            "⚠️ شعر در انتظار انتخاب رنگ پیدا نشد.\n\n"
            "لطفاً دوباره شعرت را ارسال کن."
        )

        return


    palette = PALETTES[
        palette_index
    ]


    # --------------------------------
    # حذف شعر از حالت انتظار
    # --------------------------------

    PENDING_POEMS.pop(
        chat_id,
        None
    )


    # --------------------------------
    # ساخت کارت
    # --------------------------------

    try:

        filename = create_poetry_card(
            poem,
            palette
        )


        print(
            "Poetry card created:",
            filename,
            "Palette:",
            palette["name"]
        )


        photo_response = send_photo(
            chat_id,
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
                chat_id
            )


        else:

            print(
                "Photo sending failed."
            )


            send_message(
                chat_id,
                "✅ کارت ساخته شد، "
                "اما ارسال تصویر موفق نشد."
            )


    except Exception as error:

        print(
            "Card creation error:",
            error
        )


        send_message(
            chat_id,
            "❌ هنگام ساخت کارت مشکلی پیش آمد."
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


    # ==================================
    # Callback Query
    # ==================================

    if update.get(
        "callback_query"
    ):

        process_color_selection(
            update
        )

        return "OK", 200


    # ==================================
    # Message
    # ==================================

    message = (
        update.get("message")
        or {}
    )


    text = message.get(
        "text"
    )


    chat = (
        message.get("chat")
        or {}
    )


    user_id = chat.get(
        "id"
    )


    if not user_id:

        return "OK", 200


    if not text:

        return "OK", 200


    # ==================================
    # /start
    # ==================================

    if text == "/start":

        # اگر شعری در انتظار بوده،
        # پاک شود.

        PENDING_POEMS.pop(
            user_id,
            None
        )


        send_start_message(
            user_id
        )


        return "OK", 200


    # ==================================
    # Receive Poem
    # ==================================

    # شعر را ذخیره می‌کنیم.
    # هنوز کارت ساخته نمی‌شود.

    PENDING_POEMS[
        user_id
    ] = text


    # ==================================
    # Ask Color
    # ==================================

    send_color_selection(
        user_id
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
