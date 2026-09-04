import os
import random
import requests

from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont, ImageFilter


app = Flask(__name__)


# ==================================
# Configuration
# ==================================

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
# Line Thickness
# ==================================

OUTER_FRAME_WIDTH = 3
INNER_FRAME_WIDTH = 2
ORNAMENT_LINE_WIDTH = 2
SIDE_LINE_WIDTH = 2
PANEL_OUTLINE_WIDTH = 2
PANEL_INNER_WIDTH = 1
FOOTER_LINE_WIDTH = 2


# ==================================
# Pending Poems
# ==================================

PENDING_POEMS = {}


# ==================================
# Color Palettes
# ==================================

PALETTES = [

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
        "panel_outline": (205, 172, 105, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (205, 172, 105, 75),
        "side_dot": (205, 172, 105, 100),
    },

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
        "panel_outline": (190, 170, 110, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (200, 175, 110, 75),
        "side_dot": (215, 185, 115, 100),
    },

    {
        "name": "فیروزه‌ای تیره",
        "top": (10, 61, 67),
        "middle": (9, 39, 45),
        "bottom": (4, 17, 21),
        "glow1": (55, 155, 165, 34),
        "glow2": (35, 110, 125, 20),
        "glow3": (40, 120, 130, 10),
        "frame": (172, 145, 91),
        "frame_inner": (205, 177, 112),
        "text": (242, 247, 244),
        "accent": (224, 199, 132),
        "subtitle": (188, 209, 208),
        "ornament": (130, 137, 91),
        "panel_outline": (185, 170, 110, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (185, 175, 110, 75),
        "side_dot": (210, 190, 120, 100),
    },

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
        "panel_outline": (190, 165, 100, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (190, 170, 105, 75),
        "side_dot": (210, 180, 110, 100),
    },

    {
        "name": "زیتونی تیره",
        "top": (55, 57, 27),
        "middle": (35, 37, 20),
        "bottom": (14, 15, 8),
        "glow1": (145, 145, 65, 30),
        "glow2": (105, 110, 45, 20),
        "glow3": (95, 100, 40, 10),
        "frame": (174, 151, 79),
        "frame_inner": (204, 178, 99),
        "text": (247, 245, 232),
        "accent": (226, 201, 128),
        "subtitle": (204, 199, 171),
        "ornament": (143, 127, 67),
        "panel_outline": (190, 170, 100, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (195, 175, 100, 75),
        "side_dot": (215, 190, 110, 100),
    },

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
        "panel_outline": (195, 155, 95, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (200, 160, 100, 75),
        "side_dot": (215, 175, 105, 100),
    },

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
        "panel_outline": (195, 155, 90, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (200, 160, 95, 75),
        "side_dot": (215, 175, 105, 100),
    },

    {
        "name": "رزگلد",
        "top": (72, 35, 48),
        "middle": (45, 23, 32),
        "bottom": (19, 9, 14),
        "glow1": (190, 105, 120, 32),
        "glow2": (150, 75, 95, 20),
        "glow3": (135, 70, 85, 10),
        "frame": (181, 125, 119),
        "frame_inner": (218, 165, 154),
        "text": (250, 243, 238),
        "accent": (235, 181, 163),
        "subtitle": (216, 194, 187),
        "ornament": (164, 112, 106),
        "panel_outline": (215, 160, 150, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (210, 155, 145, 75),
        "side_dot": (225, 170, 158, 100),
    },

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
        "panel_outline": (190, 150, 85, 38),
        "panel_inner": (255, 255, 255, 12),
        "side_line": (195, 160, 95, 75),
        "side_dot": (215, 175, 105, 100),
    },
]


# ==================================
# Fonts
# ==================================

def get_font(font_name, size):

    return ImageFont.truetype(
        font_name,
        size
    )


# ==================================
# Background
# ==================================

def create_gradient_background(palette):

    image = Image.new(
        "RGB",
        (
            CARD_WIDTH,
            CARD_HEIGHT
        )
    )

    pixels = image.load()

    top = palette["top"]
    middle = palette["middle"]
    bottom = palette["bottom"]

    for y in range(CARD_HEIGHT):

        ratio = y / (CARD_HEIGHT - 1)

        if ratio < 0.50:

            t = ratio / 0.50

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

            t = (ratio - 0.50) / 0.50

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

    # ==================================
    # Soft Atmospheric Glow
    # ==================================

    glow = Image.new(
        "RGBA",
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(
        glow
    )

    # Main upper glow
    glow_draw.ellipse(
        (-320, -240, 680, 600),
        fill=palette["glow1"]
    )

    # Lower secondary glow
    glow_draw.ellipse(
        (650, 650, 1280, 1280),
        fill=palette["glow2"]
    )

    # Very soft central atmosphere
    glow_draw.ellipse(
        (220, 300, 860, 980),
        fill=palette["glow3"]
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(125)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        glow
    )

    # ==================================
    # Very Subtle Texture
    # ==================================

    texture = Image.new(
        "RGBA",
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
        (0, 0, 0, 0)
    )

    texture_pixels = texture.load()

    random.seed(8)

    for _ in range(16000):

        x = random.randrange(
            CARD_WIDTH
        )

        y = random.randrange(
            CARD_HEIGHT
        )

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

        test = current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        width = (
            bbox[2] - bbox[0]
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

    text = normalize_text(
        text
    )

    raw_lines = text.splitlines()

    final_lines = []

    for line in raw_lines:

        if not line.strip():

            final_lines.append(
                None
            )

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
            bbox[3] - bbox[1]
        )

        total += (
            height
            + line_spacing
        )

    if lines[-1] is not None:

        total -= line_spacing

    return total


# ==================================
# Outer Corner Details
# ==================================

def draw_outer_corner_details(
    draw,
    palette
):

    """
    Minimal decorative details for the four
    outer corners of the main frame.

    The design intentionally stays geometric
    and restrained; it is not tazhib.
    """

    color = palette["accent"]
    secondary = palette["ornament"]

    margin = 40

    # Distance from each corner
    inset = 18

    # Length of decorative arms
    arm = 30

    # Small center diamond
    diamond = 3

    # ----------------------------------
    # Top-left
    # ----------------------------------

    x = margin + inset
    y = margin + inset

    draw.line(
        (
            x,
            y + arm,
            x,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x,
            y,
            x + arm,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x + 7,
            y + 7,
            x + 20,
            y + 20
        ),
        fill=color,
        width=1
    )

    draw.polygon(
        [
            (x + 20, y + 20 - diamond),
            (x + 20 + diamond, y + 20),
            (x + 20, y + 20 + diamond),
            (x + 20 - diamond, y + 20),
        ],
        fill=color
    )

    # ----------------------------------
    # Top-right
    # ----------------------------------

    x = CARD_WIDTH - margin - inset
    y = margin + inset

    draw.line(
        (
            x,
            y + arm,
            x,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x,
            y,
            x - arm,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x - 7,
            y + 7,
            x - 20,
            y + 20
        ),
        fill=color,
        width=1
    )

    draw.polygon(
        [
            (x - 20, y + 20 - diamond),
            (x - 20 - diamond, y + 20),
            (x - 20, y + 20 + diamond),
            (x - 20 + diamond, y + 20),
        ],
        fill=color
    )

    # ----------------------------------
    # Bottom-left
    # ----------------------------------

    x = margin + inset
    y = CARD_HEIGHT - margin - inset

    draw.line(
        (
            x,
            y - arm,
            x,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x,
            y,
            x + arm,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x + 7,
            y - 7,
            x + 20,
            y - 20
        ),
        fill=color,
        width=1
    )

    draw.polygon(
        [
            (x + 20, y - 20 - diamond),
            (x + 20 + diamond, y - 20),
            (x + 20, y - 20 + diamond),
            (x + 20 - diamond, y - 20),
        ],
        fill=color
    )

    # ----------------------------------
    # Bottom-right
    # ----------------------------------

    x = CARD_WIDTH - margin - inset
    y = CARD_HEIGHT - margin - inset

    draw.line(
        (
            x,
            y - arm,
            x,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x,
            y,
            x - arm,
            y
        ),
        fill=secondary,
        width=2
    )

    draw.line(
        (
            x - 7,
            y - 7,
            x - 20,
            y - 20
        ),
        fill=color,
        width=1
    )

    draw.polygon(
        [
            (x - 20, y - 20 - diamond),
            (x - 20 - diamond, y - 20),
            (x - 20, y - 20 + diamond),
            (x - 20 + diamond, y - 20),
        ],
        fill=color
    )


# ==================================
# Create Poetry Card
# ==================================

def create_poetry_card(
    text,
    palette,
    branded=True
):

    image = create_gradient_background(
        palette
    )

    draw = ImageDraw.Draw(
        image
    )

    # ==================================
    # Outer Frame
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
        width=OUTER_FRAME_WIDTH
    )

    # ==================================
    # Outer Corner Details
    # ==================================

    draw_outer_corner_details(
        draw,
        palette
    )

    # ==================================
    # Inner Frame
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
        width=INNER_FRAME_WIDTH
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

    title_y = 77

    header_center = (
        CARD_WIDTH // 2
    )

    gap = 18

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
        + (
            title_height
            - subtitle_height
        ) // 2
        - 3
    )

    # ==================================
    # Branded Header
    # ==================================

    if branded:

        # Very subtle title shadow
        draw.text(
            (
                title_x + 2,
                title_y + 3
            ),
            title,
            font=title_font,
            fill=(0, 0, 0)
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
            + 23
        )

        line_width = 145

        center_x = (
            CARD_WIDTH // 2
        )

        draw.line(
            (
                center_x - line_width,
                line_y,
                center_x - 13,
                line_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

        draw.line(
            (
                center_x + 13,
                line_y,
                center_x + line_width,
                line_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

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

    else:

        # ==================================
        # Public Card Top Ornament
        # ==================================

        ornament_y = 112

        ornament_width = 82

        center_x = (
            CARD_WIDTH // 2
        )

        draw.line(
            (
                center_x - ornament_width,
                ornament_y,
                center_x - 14,
                ornament_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

        draw.line(
            (
                center_x + 14,
                ornament_y,
                center_x + ornament_width,
                ornament_y
            ),
            fill=palette["ornament"],
            width=ORNAMENT_LINE_WIDTH
        )

        diamond_size = 4

        draw.polygon(
            [
                (
                    center_x,
                    ornament_y - diamond_size
                ),
                (
                    center_x + diamond_size,
                    ornament_y
                ),
                (
                    center_x,
                    ornament_y + diamond_size
                ),
                (
                    center_x - diamond_size,
                    ornament_y
                )
            ],
            fill=palette["accent"]
        )

    # ==================================
    # Poem Area
    # ==================================

    text_left = 78
    text_right = 1002

    max_width = (
        text_right - text_left
    )

    text_top = 220
    text_bottom = 892

    available_height = (
        text_bottom - text_top
    )

    font_size = 62
    min_font_size = 28

    line_spacing = 15
    blank_line_spacing = 42

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

    # ==================================
    # Empty Text Fallback
    # ==================================

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
    # Glass Panel
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
        (
            CARD_WIDTH,
            CARD_HEIGHT
        ),
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(
        panel
    )

    # Soft panel shadow
    panel_draw.rounded_rectangle(
        (
            62,
            panel_top + 5,
            1018,
            panel_bottom + 7
        ),
        radius=45,
        fill=(0, 0, 0, 30)
    )

    # Main glass surface
    panel_draw.rounded_rectangle(
        (
            62,
            panel_top,
            1018,
            panel_bottom
        ),
        radius=45,
        fill=(255, 255, 255, 13),
        outline=palette["panel_outline"],
        width=PANEL_OUTLINE_WIDTH
    )

    # Inner glass edge
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

    draw.line(
        (
            79,
            deco_y - 28,
            79,
            deco_y + 28
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
            deco_y - 28,
            1001,
            deco_y + 28
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

    # ==================================
    # Poem
    # ==================================

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

    center_x = (
        CARD_WIDTH // 2
    )

    draw.line(
        (
            center_x - 34,
            footer_y - 13,
            center_x + 34,
            footer_y - 13
        ),
        fill=palette["ornament"],
        width=FOOTER_LINE_WIDTH
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
# Card Type Keyboard
# ==================================

def get_card_type_keyboard():

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


# ==================================
# Send Card Type Selection
# ==================================

def send_card_type_selection(
    chat_id
):

    text = (
        "🖼️ <b>نوع کارت شعر را انتخاب کن:</b>\n\n"
        "🖋️ با امضای شعرکده\n"
        "کارت با عنوان و امضای شعرکده ساخته می‌شود.\n\n"
        "◻️ کارت عمومی\n"
        "کارت بدون نام و امضای شعرکده ساخته می‌شود."
    )

    return send_message(
        chat_id,
        text,
        reply_markup=get_card_type_keyboard()
    )


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
                },
                {
                    "text": "🩵 فیروزه‌ای تیره",
                    "callback_data": "color_2"
                }
            ],
            [
                {
                    "text": "🟢 سبز زمردی",
                    "callback_data": "color_3"
                },
                {
                    "text": "🫒 زیتونی تیره",
                    "callback_data": "color_4"
                },
                {
                    "text": "🔴 شرابی",
                    "callback_data": "color_5"
                }
            ],
            [
                {
                    "text": "🟤 قهوه‌ای شکلاتی",
                    "callback_data": "color_6"
                },
                {
                    "text": "🩷 رزگلد",
                    "callback_data": "color_7"
                },
                {
                    "text": "⚫ ذغالی طلایی",
                    "callback_data": "color_8"
                }
            ]
        ]
    }


# ==================================
# Send Color Selection
# ==================================

def send_color_selection(
    chat_id
):

    text = (
        "🎨 <b>حالا رنگ کارت شعر را انتخاب کن:</b>"
    )

    return send_message(
        chat_id,
        text,
        reply_markup=get_color_keyboard()
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
        "شعرت را همین‌جا بفرست تا برایت "
        "کارت شعر بسازم. ✨\n\n"
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
        "📖 برای شعرهای بیشتر، سری به "
        f'<a href="{CHANNEL_URL}">«شعرکده»</a> '
        "در سروش پلاس بزنید."
    )

    return send_message(
        chat_id,
        text
    )


# ==================================
# Process Card Type Selection
# ==================================

def process_card_type_selection(
    update
):

    callback_query = (
        update.get("callback_query")
        or {}
    )

    callback_query_id = (
        callback_query.get("id")
    )

    if callback_query_id:

        answer_callback_query(
            callback_query_id
        )

    data = callback_query.get(
        "data"
    )

    if data not in (
        "type_branded",
        "type_public"
    ):

        return "OK", 200

    callback_message = (
        callback_query.get("message")
        or {}
    )

    chat = (
        callback_message.get("chat")
        or {}
    )

    chat_id = chat.get("id")

    if not chat_id:

        return "OK", 200

    pending = PENDING_POEMS.get(
        chat_id
    )

    if not pending:

        send_message(
            chat_id,
            "⚠️ شعر در انتظار انتخاب پیدا نشد.\n\n"
            "لطفاً دوباره شعرت را ارسال کن."
        )

        return "OK", 200

    if data == "type_branded":

        pending["branded"] = True

    else:

        pending["branded"] = False

    PENDING_POEMS[chat_id] = pending

    print(
        f"Card type selected: "
        f"{'branded' if pending['branded'] else 'public'}"
    )

    send_color_selection(
        chat_id
    )

    return "OK", 200


# ==================================
# Process Color Selection
# ==================================

def process_color_selection(
    update
):

    callback_query = (
        update.get("callback_query")
        or {}
    )

    callback_query_id = (
        callback_query.get("id")
    )

    if callback_query_id:

        answer_callback_query(
            callback_query_id
        )

    data = callback_query.get(
        "data"
    )

    if not data:

        return "OK", 200

    if not data.startswith(
        "color_"
    ):

        return "OK", 200

    callback_message = (
        callback_query.get("message")
        or {}
    )

    chat = (
        callback_message.get("chat")
        or {}
    )

    chat_id = chat.get("id")

    if not chat_id:

        return "OK", 200

    try:

        palette_index = int(
            data.replace(
                "color_",
                ""
            )
        )

    except ValueError:

        send_message(
            chat_id,
            "❌ رنگ انتخاب‌شده معتبر نیست."
        )

        return "OK", 200

    if (
        palette_index < 0
        or palette_index >= len(PALETTES)
    ):

        send_message(
            chat_id,
            "❌ رنگ انتخاب‌شده معتبر نیست."
        )

        return "OK", 200

    pending = PENDING_POEMS.pop(
        chat_id,
        None
    )

    if not pending:

        send_message(
            chat_id,
            "⚠️ شعر در انتظار انتخاب پیدا نشد.\n\n"
            "لطفاً دوباره شعرت را ارسال کن."
        )

        return "OK", 200

    poem = pending.get(
        "poem"
    )

    branded = pending.get(
        "branded",
        True
    )

    if not poem:

        send_message(
            chat_id,
            "⚠️ متن شعر پیدا نشد.\n\n"
            "لطفاً دوباره شعرت را ارسال کن."
        )

        return "OK", 200

    palette = PALETTES[
        palette_index
    ]

    print(
        f"Selected palette: "
        f"{palette['name']}"
    )

    print(
        f"Branded card: "
        f"{branded}"
    )

    try:

        filename = create_poetry_card(
            poem,
            palette,
            branded=branded
        )

        print(
            f"Poetry card created: "
            f"{filename}"
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

    return "OK", 200


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

        callback_query = (
            update.get("callback_query")
            or {}
        )

        data = callback_query.get(
            "data"
        )

        if data in (
            "type_branded",
            "type_public"
        ):

            return process_card_type_selection(
                update
            )

        if (
            data
            and data.startswith("color_")
        ):

            return process_color_selection(
                update
            )

        return "OK", 200

    # ==================================
    # Normal Message
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

    chat_id = chat.get(
        "id"
    )

    if not chat_id:

        return "OK", 200

    if not text:

        return "OK", 200

    # ==================================
    # /start
    # ==================================

    if text == "/start":

        PENDING_POEMS.pop(
            chat_id,
            None
        )

        send_start_message(
            chat_id
        )

        return "OK", 200

    # ==================================
    # New Poem
    # ==================================

    PENDING_POEMS[chat_id] = {

        "poem": text,

        "branded": True
    }

    print(
        f"Pending poem stored "
        f"for chat {chat_id}"
    )

    send_card_type_selection(
        chat_id
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
