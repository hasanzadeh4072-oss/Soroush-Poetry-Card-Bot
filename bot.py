import os

import random

import time

import threading

import requests

import uuid


from flask import Flask, request

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


app = Flask(name)


==================================


Configuration


==================================


TOKEN = os.environ.get("SOROUSH_TOKEN")

API = f"https://api.splus.ir/bot{TOKEN}"


CHANNEL_URL = "https://splus.ir/life_m23"


CARD_WIDTH = 1080

CARD_HEIGHT = 1080


POEM_FONT = "BNazanin.ttf"

TITLE_FONT = "BTitrBd.ttf"

SUBTITLE_FONT = "Vazirmatn-Regular.ttf"

FOOTER_FONT = "Vazirmatn-Regular.ttf"


BACKGROUND_IMAGE = "background.jpg"


PENDING_TIMEOUT = 120


==================================


Line Thickness


==================================


OUTER_FRAME_WIDTH = 3

INNER_FRAME_WIDTH = 2

ORNAMENT_LINE_WIDTH = 2

SIDE_LINE_WIDTH = 2

PANEL_OUTLINE_WIDTH = 2

PANEL_INNER_WIDTH = 1

FOOTER_LINE_WIDTH = 2


==================================


Pending Poems


==================================


PENDING_POEMS = {}


READY_MESSAGES = {}


Lock for shared user state


STATE_LOCK = threading.RLock()


Timer belonging to each pending poem


PENDING_TIMERS = {}


==================================


Monitoring


==================================


MONITOR_LOCK = threading.Lock()


ACTIVE_REQUESTS = 0

MAX_ACTIVE_REQUESTS = 0


TOTAL_REQUESTS = 0

SUCCESSFUL_REQUESTS = 0

FAILED_REQUESTS = 0


TOTAL_REQUEST_TIME = 0.0

MAX_REQUEST_TIME = 0.0


def monitoring_request_started():


global ACTIVE_REQUESTS  
global MAX_ACTIVE_REQUESTS  
global TOTAL_REQUESTS  

with MONITOR_LOCK:  

    ACTIVE_REQUESTS += 1  
    TOTAL_REQUESTS += 1  

    if ACTIVE_REQUESTS > MAX_ACTIVE_REQUESTS:  

        MAX_ACTIVE_REQUESTS = ACTIVE_REQUESTS  

    current_active = ACTIVE_REQUESTS  
    current_max = MAX_ACTIVE_REQUESTS  
    current_total = TOTAL_REQUESTS  

print(  
    f"[MONITOR] Request started | "  
    f"active={current_active} | "  
    f"max_active={current_max} | "  
    f"total={current_total}"  
)  



def monitoring_request_finished(

elapsed,

successful=True

):


global ACTIVE_REQUESTS  
global SUCCESSFUL_REQUESTS  
global FAILED_REQUESTS  
global TOTAL_REQUEST_TIME  
global MAX_REQUEST_TIME  

with MONITOR_LOCK:  

    if ACTIVE_REQUESTS > 0:  

        ACTIVE_REQUESTS -= 1  

    TOTAL_REQUEST_TIME += elapsed  

    if elapsed > MAX_REQUEST_TIME:  

        MAX_REQUEST_TIME = elapsed  

    if successful:  

        SUCCESSFUL_REQUESTS += 1  

    else:  

        FAILED_REQUESTS += 1  

    current_active = ACTIVE_REQUESTS  
    successful_count = SUCCESSFUL_REQUESTS  
    failed_count = FAILED_REQUESTS  
    total_request_time = TOTAL_REQUEST_TIME  
    max_request_time = MAX_REQUEST_TIME  

    completed_requests = (  
        successful_count  
        + failed_count  
    )  

    if completed_requests > 0:  

        average_request_time = (  
            total_request_time  
            / completed_requests  
        )  

    else:  

        average_request_time = 0.0  

print(  
    f"[MONITOR] Request finished | "  
    f"time={elapsed:.4f}s | "  
    f"active={current_active} | "  
    f"success={successful_count} | "  
    f"failed={failed_count} | "  
    f"avg={average_request_time:.4f}s | "  
    f"max_time={max_request_time:.4f}s"  
)  



==================================


Cached Backgrounds


==================================


CACHED_BACKGROUND = None

CACHED_CARD_BACKGROUNDS = {}

FONT_CACHE = {}


==================================


Load Original Background


==================================


def load_background_image():


global CACHED_BACKGROUND  

if not os.path.exists(BACKGROUND_IMAGE):  

    print(  
        "Background image not found:",  
        BACKGROUND_IMAGE  
    )  

    return None  

try:  

    background = Image.open(  
        BACKGROUND_IMAGE  
    ).convert("RGB")  

    background_ratio = (  
        background.width  
        / background.height  
    )  

    card_ratio = (  
        CARD_WIDTH  
        / CARD_HEIGHT  
    )  

    if background_ratio > card_ratio:  

        new_height = CARD_HEIGHT  

        new_width = int(  
            background.width  
            * CARD_HEIGHT  
            / background.height  
        )  

    else:  

        new_width = CARD_WIDTH  

        new_height = int(  
            background.height  
            * CARD_WIDTH  
            / background.width  
        )  

    background = background.resize(  
        (  
            new_width,  
            new_height  
        ),  
        Image.Resampling.LANCZOS  
    )  

    left = (  
        new_width  
        - CARD_WIDTH  
    ) // 2  

    top_crop = (  
        new_height  
        - CARD_HEIGHT  
    ) // 2  

    background = background.crop(  
        (  
            left,  
            top_crop,  
            left + CARD_WIDTH,  
            top_crop + CARD_HEIGHT  
        )  
    )  

    background = ImageEnhance.Brightness(  
        background  
    ).enhance(0.48)  

    background = background.filter(  
        ImageFilter.GaussianBlur(4)  
    )  

    background = background.convert(  
        "RGBA"  
    )  

    background.putalpha(42)  

    CACHED_BACKGROUND = background  

    print(  
        "Background image loaded and cached."  
    )  

    return CACHED_BACKGROUND  

except Exception as error:  

    print(  
        "Background image error:",  
        error  
    )  

    return None  



==================================


Color Palettes


==================================


PALETTES = [


# ------------------------------  
# DARK  
# ------------------------------  

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

# ------------------------------  
# MEDIUM  
# ------------------------------  

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

# ------------------------------  
# LIGHT  
# ------------------------------  

{  
    "name": "کرم",  
    "top": (250, 239, 210),  
    "middle": (242, 226, 190),  
    "bottom": (226, 205, 163),  
    "glow1": (255, 252, 230, 55),  
    "glow2": (255, 240, 185, 28),  
    "glow3": (255, 255, 255, 22),  
    "frame": (91, 67, 39),  
    "frame_inner": (126, 96, 58),  
    "text": (49, 40, 31),  
    "accent": (104, 73, 38),  
    "subtitle": (77, 61, 43),  
    "ornament": (113, 80, 42),  
    "panel_outline": (105, 78, 43, 55),  
    "panel_inner": (255, 255, 255, 75),  
    "side_line": (105, 78, 43, 85),  
    "side_dot": (94, 67, 35, 125),  
},  

{  
    "name": "آبی روشن",  
    "top": (205, 235, 248),  
    "middle": (180, 220, 238),  
    "bottom": (153, 201, 225),  
    "glow1": (235, 249, 255, 58),  
    "glow2": (145, 205, 235, 28),  
    "glow3": (255, 255, 255, 24),  
    "frame": (43, 73, 91),  
    "frame_inner": (72, 105, 124),  
    "text": (31, 51, 63),  
    "accent": (48, 82, 101),  
    "subtitle": (54, 77, 91),  
    "ornament": (59, 91, 108),  
    "panel_outline": (58, 91, 110, 55),  
    "panel_inner": (255, 255, 255, 78),  
    "side_line": (58, 91, 110, 85),  
    "side_dot": (46, 79, 99, 125),  
},  

{  
    "name": "مریم‌گلی",  
    "top": (218, 231, 205),  
    "middle": (201, 219, 184),  
    "bottom": (179, 201, 159),  
    "glow1": (242, 249, 230, 58),  
    "glow2": (175, 205, 145, 28),  
    "glow3": (255, 255, 255, 24),  
    "frame": (60, 76, 52),  
    "frame_inner": (91, 108, 78),  
    "text": (39, 54, 35),  
    "accent": (67, 88, 55),  
    "subtitle": (67, 82, 59),  
    "ornament": (75, 96, 62),  
    "panel_outline": (73, 96, 62, 55),  
    "panel_inner": (255, 255, 255, 78),  
    "side_line": (73, 96, 62, 85),  
    "side_dot": (62, 84, 52, 125),  
},  



]


==================================


Fonts


==================================


def get_font(

font_name,

size

):


key = (  
    font_name,  
    size  
)  

if key not in FONT_CACHE:  

    FONT_CACHE[key] = ImageFont.truetype(  
        font_name,  
        size  
    )  

return FONT_CACHE[key]  



==================================


Background


==================================


def create_gradient_background(

palette

):


gradient = Image.new(  
    "RGB",  
    (  
        1,  
        CARD_HEIGHT  
    )  
)  

pixels = gradient.load()  

top = palette["top"]  
middle = palette["middle"]  
bottom = palette["bottom"]  

for y in range(  
    CARD_HEIGHT  
):  

    ratio = (  
        y  
        / (CARD_HEIGHT - 1)  
    )  

    if ratio < 0.52:  

        t = (  
            ratio  
            / 0.52  
        )  

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

        t = (  
            ratio - 0.52  
        ) / 0.48  

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

    pixels[  
        0,  
        y  
    ] = (  
        r,  
        g,  
        b  
    )  

image = gradient.resize(  
    (  
        CARD_WIDTH,  
        CARD_HEIGHT  
    ),  
    Image.Resampling.NEAREST  
)  

if CACHED_BACKGROUND is not None:  

    image = Image.alpha_composite(  
        image.convert("RGBA"),  
        CACHED_BACKGROUND  
    )  

else:  

    image = image.convert(  
        "RGBA"  
    )  

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

glow_draw.ellipse(  
    (  
        -260,  
        -180,  
        650,  
        560  
    ),  
    fill=palette["glow1"]  
)  

glow_draw.ellipse(  
    (  
        690,  
        690,  
        1250,  
        1250  
    ),  
    fill=palette["glow2"]  
)  

glow_draw.ellipse(  
    (  
        250,  
        350,  
        850,  
        950  
    ),  
    fill=palette["glow3"]  
)  

glow = glow.filter(  
    ImageFilter.GaussianBlur(110)  
)  

image = Image.alpha_composite(  
    image,  
    glow  
)  

texture = Image.new(  
    "RGBA",  
    (  
        CARD_WIDTH,  
        CARD_HEIGHT  
    ),  
    (0, 0, 0, 0)  
)  

texture_pixels = texture.load()  

random_generator = random.Random(8)  

for _ in range(  
    14000  
):  

    x = random_generator.randrange(  
        CARD_WIDTH  
    )  

    y = random_generator.randrange(  
        CARD_HEIGHT  
    )  

    value = random_generator.choice(  
        [  
            (255, 255, 255, 3),  
            (0, 0, 0, 4)  
        ]  
    )  

    texture_pixels[  
        x,  
        y  
    ] = value  

image = Image.alpha_composite(  
    image,  
    texture  
)  

return image.convert(  
    "RGB"  
)  



==================================


Build All Cached Card Backgrounds


==================================


def build_cached_card_backgrounds():


global CACHED_CARD_BACKGROUNDS  

print(  
    "Building cached card backgrounds..."  
)  

start_time = time.perf_counter()  

CACHED_CARD_BACKGROUNDS = {}  

for palette in PALETTES:  

    palette_name = palette["name"]  

    print(  
        f"Preparing background: "  
        f"{palette_name}"  
    )  

    palette_start = time.perf_counter()  

    CACHED_CARD_BACKGROUNDS[  
        palette_name  
    ] = create_gradient_background(  
        palette  
    )  

    print(  
        f"[TIMING] Background "  
        f"{palette_name}: "  
        f"{time.perf_counter() - palette_start:.4f}s"  
    )  

elapsed = time.perf_counter() - start_time  

print(  
    "All card backgrounds cached."  
)  

print(  
    f"Background cache build time: "  
    f"{elapsed:.4f} seconds"  
)  



==================================


Initialize Caches


==================================


load_background_image()


build_cached_card_backgrounds()


==================================


Text Helpers


==================================


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



==================================


Pending Poem Timeout


==================================


def expire_pending_poem(

chat_id,

created_at

):


try:  

    with STATE_LOCK:  

        pending = PENDING_POEMS.get(  
            chat_id  
        )  

        if not pending:  

            PENDING_TIMERS.pop(  
                chat_id,  
                None  
            )  

            return  

        current_created_at = (  
            pending.get(  
                "created_at"  
            )  
        )  

        if current_created_at != created_at:  

            return  

        if (  
            time.time()  
            - created_at  
            >= PENDING_TIMEOUT  
        ):  

            PENDING_POEMS.pop(  
                chat_id,  
                None  
            )  

            PENDING_TIMERS.pop(  
                chat_id,  
                None  
            )  

            print(  
                f"Pending poem expired "  
                f"for chat {chat_id}"  
            )  

except Exception as error:  

    print(  
        "Pending poem expiration error:",  
        error  
    )  



def cancel_pending_timer(

chat_id

):


timer = None  

with STATE_LOCK:  

    timer = PENDING_TIMERS.pop(  
        chat_id,  
        None  
    )  

if timer is not None:  

    try:  

        timer.cancel()  

    except Exception as error:  

        print(  
            "Pending timer cancel error:",  
            error  
        )  



def store_pending_poem(

chat_id,

poem

):


created_at = time.time()  

with STATE_LOCK:  

    old_timer = PENDING_TIMERS.pop(  
        chat_id,  
        None  
    )  

    if old_timer is not None:  

        try:  

            old_timer.cancel()  

        except Exception as error:  

            print(  
                "Old pending timer cancel error:",  
                error  
            )  

    PENDING_POEMS[chat_id] = {  
        "poem": poem,  
        "branded": True,  
        "created_at": created_at  
    }  

    timer = threading.Timer(  
        PENDING_TIMEOUT,  
        expire_pending_poem,  
        args=(  
            chat_id,  
            created_at  
        )  
    )  

    timer.daemon = True  

    PENDING_TIMERS[  
        chat_id  
    ] = timer  

    timer.start()  

print(  
    f"Pending poem stored "  
    f"for chat {chat_id}"  
)  



def refresh_pending_timeout(

chat_id

):


created_at = time.time()  

with STATE_LOCK:  

    pending = PENDING_POEMS.get(  
        chat_id  
    )  

    if not pending:  

        return  

    old_timer = PENDING_TIMERS.pop(  
        chat_id,  
        None  
    )  

    if old_timer is not None:  

        try:  

            old_timer.cancel()  

        except Exception as error:  

            print(  
                "Old pending timer cancel error:",  
                error  
            )  

    pending["created_at"] = created_at  

    PENDING_POEMS[chat_id] = pending  

    timer = threading.Timer(  
        PENDING_TIMEOUT,  
        expire_pending_poem,  
        args=(  
            chat_id,  
            created_at  
        )  
    )  

    timer.daemon = True  

    PENDING_TIMERS[  
        chat_id  
    ] = timer  

    timer.start()  

print(  
    f"Pending timeout refreshed "  
    f"for chat {chat_id}"  
)  



==================================


Delete Previous Ready Message


==================================


def delete_previous_ready_message(

chat_id

):


try:  

    with STATE_LOCK:  

        message_id = READY_MESSAGES.get(  
            chat_id  
        )  

    if not message_id:  

        return  

    print(  
        f"Deleting previous ready message "  
        f"{message_id} for chat {chat_id}"  
    )  

    response = delete_message(  
        chat_id,  
        message_id  
    )  

    if (  
        response is not None  
        and response.ok  
    ):  

        with STATE_LOCK:  

            current_message_id = (  
                READY_MESSAGES.get(  
                    chat_id  
                )  
            )  

            if (  
                current_message_id  
                == message_id  
            ):  

                READY_MESSAGES.pop(  
                    chat_id,  
                    None  
                )  

        print(  
            f"Previous ready message "  
            f"{message_id} deleted."  
        )  

    else:  

        print(  
            "Previous ready message "  
            "could not be deleted. "  
            "Continuing normally."  
        )  

except Exception as error:  

    print(  
        "Previous ready message deletion "  
        "error:",  
        error  
    )  



==================================


Create Poetry Card


==================================


def create_poetry_card(

text,

palette,

branded=True

):


total_start = time.perf_counter()  

# ------------------------------  
# 1. Background  
# ------------------------------  

stage_start = time.perf_counter()  

cached_background = CACHED_CARD_BACKGROUNDS.get(  
    palette["name"]  
)  

if cached_background is not None:  

    image = cached_background.copy()  

else:  

    image = create_gradient_background(  
        palette  
    )  

image = image.convert(  
    "RGBA"  
)  

draw = ImageDraw.Draw(  
    image  
)  

print(  
    f"[TIMING] 01 - Background copy: "  
    f"{time.perf_counter() - stage_start:.4f}s"  
)  

# ------------------------------  
# 2. Outer frame  
# ------------------------------  

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

# ------------------------------  
# 3. Inner frame  
# ------------------------------  

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

# ------------------------------  
# 4. Header / Branding  
# ------------------------------  

stage_start = time.perf_counter()  

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

footer_height = (  
    footer_bbox[3]  
    - footer_bbox[1]  
)  

footer_x = (  
    CARD_WIDTH  
    - footer_width  
) // 2  

footer_y = 78  

title_y = (  
    CARD_HEIGHT  
    - 78  
    - title_height  
)  

header_center = CARD_WIDTH // 2  

gap = 20  

title_x = (  
    header_center  
    + 10  
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

if branded:  

    draw.text(  
        (  
            footer_x + 1,  
            footer_y + 2  
        ),  
        footer,  
        font=footer_font,  
        fill=(0, 0, 0, 60)  
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

    line_y = (  
        footer_y  
        + footer_height  
        + 25  
    )  

    line_width = 150  

    center_x = CARD_WIDTH // 2  

    draw.line(  
        (  
            center_x - line_width,  
            line_y,  
            center_x - 12,  
            line_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    draw.line(  
        (  
            center_x + 12,  
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

    line_y = (  
        title_y  
        - 25  
    )  

    line_width = 150  

    center_x = CARD_WIDTH // 2  

    draw.line(  
        (  
            center_x - line_width,  
            line_y,  
            center_x - 12,  
            line_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    draw.line(  
        (  
            center_x + 12,  
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

    draw.text(  
        (  
            footer_x + 1,  
            footer_y + 2  
        ),  
        footer,  
        font=footer_font,  
        fill=(0, 0, 0, 60)  
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

    ornament_y = (  
        footer_y  
        + footer_height  
        + 25  
    )  

    ornament_width = 150  

    center_x = CARD_WIDTH // 2  

    draw.line(  
        (  
            center_x - ornament_width,  
            ornament_y,  
            center_x - 12,  
            ornament_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    draw.line(  
        (  
            center_x + 12,  
            ornament_y,  
            center_x + ornament_width,  
            ornament_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    diamond_size = 5  

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

    bottom_ornament_y = (  
        CARD_HEIGHT  
        - 112  
    )  

    draw.line(  
        (  
            center_x - ornament_width,  
            bottom_ornament_y,  
            center_x - 12,  
            bottom_ornament_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    draw.line(  
        (  
            center_x + 12,  
            bottom_ornament_y,  
            center_x + ornament_width,  
            bottom_ornament_y  
        ),  
        fill=palette["ornament"],  
        width=ORNAMENT_LINE_WIDTH  
    )  

    draw.polygon(  
        [  
            (  
                center_x,  
                bottom_ornament_y - diamond_size  
            ),  
            (  
                center_x + diamond_size,  
                bottom_ornament_y  
            ),  
            (  
                center_x,  
                bottom_ornament_y + diamond_size  
            ),  
            (  
                center_x - diamond_size,  
                bottom_ornament_y  
            )  
        ],  
        fill=palette["accent"]  
    )  

print(  
    f"[TIMING] 04 - Header: "  
    f"{time.perf_counter() - stage_start:.4f}s"  
)  

# ------------------------------  
# 5. Text wrapping / font sizing  
# ------------------------------  

stage_start = time.perf_counter()  

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

# ------------------------------  
# 6. Glass panel  
# ------------------------------  

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

draw = ImageDraw.Draw(  
    image  
)  

print(  
    f"[TIMING] 06 - Glass panel: "  
    f"{time.perf_counter() - stage_start:.4f}s"  
)  

# ------------------------------  
# 7. Side ornaments  
# ------------------------------  

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

# ------------------------------  
# 8. Poem drawing  
# ------------------------------  

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

# ------------------------------  
# 9. Footer  
# ------------------------------  

stage_start = time.perf_counter()  

print(  
    f"[TIMING] 09 - Footer: "  
    f"{time.perf_counter() - stage_start:.4f}s"  
)  

# ------------------------------  
# 10. PNG save  
# ------------------------------  

stage_start = time.perf_counter()  

# IMPORTANT:  
# Every card gets its own unique file.  
filename = (  
    "/tmp/poetry_card_"  
    + uuid.uuid4().hex  
    + ".png"  
)  

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



==================================


Send Message


==================================


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

        data["reply_markup"] = (  
            reply_markup  
        )  

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



==================================


Delete Message


==================================


def delete_message(

chat_id,

message_id

):


try:  

    response = requests.post(  
        f"{API}/deleteMessage",  
        json={  
            "chat_id": chat_id,  
            "message_id": message_id  
        },  
        timeout=20  
    )  

    print(  
        "deleteMessage:",  
        response.status_code,  
        response.text  
    )  

    return response  

except Exception as error:  

    print(  
        "deleteMessage error:",  
        error  
    )  

    return None  



==================================


Send Photo


==================================


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



==================================


Answer Callback Query


==================================


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



==================================


Card Type Keyboard


==================================


def get_card_type_keyboard():


return {  
    "inline_keyboard": [  
        [  
            {  
                "text": "🖋️ با امضای شعرکده",  
                "callback_data":  
                    "type_branded"  
            }  
        ],  
        [  
            {  
                "text": "◻️ کارت عمومی، بدون امضا",  
                "callback_data":  
                    "type_public"  
            }  
        ]  
    ]  
}  



==================================


Send Card Type Selection


==================================


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



==================================


Color Keyboard


==================================


def get_color_keyboard():


return {  
    "inline_keyboard": [  

        # تیره  
        [  
            {  
                "text": "🟣 سلطنتی",  
                "callback_data": "color_0"  
            },  
            {  
                "text": "🔵 آبی شبانه",  
                "callback_data": "color_1"  
            },  
            {  
                "text": "🔴 شرابی",  
                "callback_data": "color_2"  
            }  
        ],  

        # متوسط  
        [  
            {  
                "text": "🩵 فیروزه‌ای تیره",  
                "callback_data": "color_3"  
            },  
            {  
                "text": "🟢 سبز زمردی",  
                "callback_data": "color_4"  
            },  
            {  
                "text": "🩷 رزگلد",  
                "callback_data": "color_5"  
            }  
        ],  

        # روشن  
        [  
            {  
                "text": "🟡 کرم",  
                "callback_data": "color_6"  
            },  
            {  
                "text": "🔵 آبی روشن",  
                "callback_data": "color_7"  
            },  
            {  
                "text": "🌿 مریم‌گلی",  
                "callback_data": "color_8"  
            }  
        ]  

    ]  
}  



==================================


Send Color Selection


==================================


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



==================================


Start Message


==================================


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



==================================


After Card Message


==================================


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



==================================


Process Card Type Selection


==================================


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

type_message_id = (  
    callback_message.get(  
        "message_id"  
    )  
)  

if chat_id and type_message_id:  

    delete_message(  
        chat_id,  
        type_message_id  
    )  

if not chat_id:  

    return "OK", 200  

with STATE_LOCK:  

    pending = PENDING_POEMS.get(  
        chat_id  
    )  

    if pending:  

        pending = dict(  
            pending  
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

with STATE_LOCK:  

    # Only update if the same pending item  
    # still exists.  
    current_pending = (  
        PENDING_POEMS.get(  
            chat_id  
        )  
    )  

    if current_pending:  

        current_pending["branded"] = (  
            pending["branded"]  
        )  

        PENDING_POEMS[  
            chat_id  
        ] = current_pending  

    else:  

        return "OK", 200  

refresh_pending_timeout(  
    chat_id  
)  

print(  
    f"Card type selected: "  
    f"{'branded' if pending['branded'] else 'public'}"  
)  

send_color_selection(  
    chat_id  
)  

return "OK", 200  



==================================


Process Color Selection


==================================


def process_color_selection(

update

):


overall_start = time.perf_counter()  

callback_query = (  
    update.get("callback_query")  
    or {}  
)  

callback_query_id = (  
    callback_query.get("id")  
)  

if callback_query_id:  

    stage_start = time.perf_counter()  

    answer_callback_query(  
        callback_query_id  
    )  

    print(  
        f"[TIMING] answerCallbackQuery: "  
        f"{time.perf_counter() - stage_start:.4f}s"  
    )  

data = callback_query.get(  
    "data"  
)  

if not data:  

    return "OK", 200  

if not data.startswith("color_"):  

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

color_message_id = (  
    callback_message.get(  
        "message_id"  
    )  
)  

if chat_id and color_message_id:  

    stage_start = time.perf_counter()  

    delete_message(  
        chat_id,  
        color_message_id  
    )  

    print(  
        f"[TIMING] Delete color message: "  
        f"{time.perf_counter() - stage_start:.4f}s"  
    )  

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

# Atomically take the pending poem.  
with STATE_LOCK:  

    pending = PENDING_POEMS.pop(  
        chat_id,  
        None  
    )  

    pending_timer = PENDING_TIMERS.pop(  
        chat_id,  
        None  
    )  

if pending_timer is not None:  

    try:  

        pending_timer.cancel()  

    except Exception as error:  

        print(  
            "Pending timer cancel error:",  
            error  
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

# ------------------------------  
# Send building message  
# ------------------------------  

stage_start = time.perf_counter()  

building_response = send_message(  
    chat_id,  
    "⏳ <b>کارت شعر در حال ساخت است...</b>"  
)  

print(  
    f"[TIMING] Send building message: "  
    f"{time.perf_counter() - stage_start:.4f}s"  
)  

building_message_id = None  

if (  
    building_response is not None  
    and building_response.ok  
):  

    try:  

        building_result = (  
            building_response.json()  
        )  

        result = (  
            building_result.get("result")  
            or {}  
        )  

        building_message_id = (  
            result.get("message_id")  
        )  

    except Exception as error:  

        print(  
            "Building message parse error:",  
            error  
        )  

filename = None  

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

    stage_start = time.perf_counter()  

    photo_response = send_photo(  
        chat_id,  
        filename  
    )  

    photo_time = (  
        time.perf_counter()  
        - stage_start  
    )  

    print(  
        f"[TIMING] sendPhoto: "  
        f"{photo_time:.4f}s"  
    )  

    if (  
        photo_response is not None  
        and photo_response.ok  
    ):  

        print(  
            "Poetry card sent successfully."  
        )  

        if building_message_id:  

            stage_start = (  
                time.perf_counter()  
            )  

            delete_message(  
                chat_id,  
                building_message_id  
            )  

            print(  
                f"[TIMING] Delete building message: "  
                f"{time.perf_counter() - stage_start:.4f}s"  
            )  

        stage_start = (  
            time.perf_counter()  
        )  

        after_card_response = (  
            send_after_card_message(  
                chat_id  
            )  
        )  

        print(  
            f"[TIMING] Send after-card message: "  
            f"{time.perf_counter() - stage_start:.4f}s"  
        )  

        if (  
            after_card_response is not None  
            and after_card_response.ok  
        ):  

            try:  

                after_card_result = (  
                    after_card_response.json()  
                )  

                result = (  
                    after_card_result.get(  
                        "result"  
                    )  
                    or {}  
                )  

                ready_message_id = (  
                    result.get(  
                        "message_id"  
                    )  
                )  

                if ready_message_id:  

                    with STATE_LOCK:  

                        READY_MESSAGES[  
                            chat_id  
                        ] = ready_message_id  

                    print(  
                        f"Ready message saved: "  
                        f"{ready_message_id} "  
                        f"for chat {chat_id}"  
                    )  

                else:  

                    print(  
                        "Ready message ID "  
                        "not found. "  
                        "Continuing normally."  
                    )  

            except Exception as error:  

                print(  
                    "Ready message parse error:",  
                    error  
                )  

    else:  

        print(  
            "Photo sending failed."  
        )  

        if building_message_id:  

            stage_start = (  
                time.perf_counter()  
            )  

            delete_message(  
                chat_id,  
                building_message_id  
            )  

            print(  
                f"[TIMING] Delete building message: "  
                f"{time.perf_counter() - stage_start:.4f}s"  
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

    if building_message_id:  

        stage_start = (  
            time.perf_counter()  
        )  

        delete_message(  
            chat_id,  
            building_message_id  
        )  

        print(  
            f"[TIMING] Delete building message: "  
            f"{time.perf_counter() - stage_start:.4f}s"  
        )  

    send_message(  
        chat_id,  
        "❌ هنگام ساخت کارت مشکلی پیش آمد."  
    )  

finally:  

    # IMPORTANT:  
    # Remove the unique temporary file after use.  
    if filename:  

        try:  

            if os.path.exists(filename):  

                os.remove(  
                    filename  
                )  

                print(  
                    f"Temporary card file removed: "  
                    f"{filename}"  
                )  

        except Exception as error:  

            print(  
                "Temporary card file cleanup error:",  
                error  
            )  

overall_time = (  
    time.perf_counter()  
    - overall_start  
)  

print("")  
print("======= COLOR SELECTION TOTAL =======")  
print(  
    f"[TIMING] Total color click -> finished: "  
    f"{overall_time:.4f}s"  
)  
print("=====================================")  
print("")  

return "OK", 200  



==================================


Home


==================================


@app.route("/")

def home():


return (  
    "Poetry Card Bot is running",  
    200  
)  



==================================


Webhook


==================================


@app.route(

"/webhook",

methods=["POST"]

)

def webhook():


request_start = time.perf_counter()  

monitoring_request_started()  

request_successful = True  

try:  

    update = request.get_json(  
        silent=True  
    ) or {}  

    print(  
        "UPDATE:",  
        update  
    )  

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

    if text != "/start":  

        delete_previous_ready_message(  
            chat_id  
        )  

    if text == "/start":  

        with STATE_LOCK:  

            old_timer = PENDING_TIMERS.pop(  
                chat_id,  
                None  
            )  

            PENDING_POEMS.pop(  
                chat_id,  
                None  
            )  

            READY_MESSAGES.pop(  
                chat_id,  
                None  
            )  

        if old_timer is not None:  

            try:  

                old_timer.cancel()  

            except Exception as error:  

                print(  
                    "Start timer cancel error:",  
                    error  
                )  

        send_start_message(  
            chat_id  
        )  

        return "OK", 200  

    store_pending_poem(  
        chat_id,  
        text  
    )  

    send_card_type_selection(  
        chat_id  
    )  

    return "OK", 200  

except Exception as error:  

    request_successful = False  

    print(  
        "[MONITOR] Webhook unhandled error:",  
        error  
    )  

    raise  

finally:  

    request_time = (  
        time.perf_counter()  
        - request_start  
    )  

    monitoring_request_finished(  
        request_time,  
        successful=request_successful  
    )  



==================================


Run


==================================


if name == "main":


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


