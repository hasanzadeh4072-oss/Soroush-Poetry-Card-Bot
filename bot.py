import os
import requests
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

TOKEN = os.environ.get("SOROUSH_TOKEN")
API = f"https://api.splus.ir/bot{TOKEN}"

# =========================
# اندازه کارت
# =========================

CARD_WIDTH = 1080
CARD_HEIGHT = 1080

# =========================
# رنگ‌ها
# =========================

BACKGROUND_TOP = (48, 30, 72)
BACKGROUND_BOTTOM = (22, 18, 38)

TEXT_COLOR = (248, 244, 235)
ACCENT_COLOR = (205, 172, 105)
SUBTITLE_COLOR = (190, 175, 150)
BORDER_COLOR = (150, 120, 70)

# =========================
# فونت‌ها
# =========================

POEM_FONT = "BNazanin.ttf"
TITLE_FONT = "BTitrBd.ttf"
SUBTITLE_FONT = "Vazirmatn-Regular.ttf"
FOOTER_FONT = "Vazirmatn-Regular.ttf"


def get_font(font_name, size):
    return ImageFont.truetype(font_name, size)


# =========================
# پس‌زمینه
# =========================

def create_gradient_background():
    image = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT))
    pixels = image.load()

    for y in range(CARD_HEIGHT):
        ratio = y / (CARD_HEIGHT - 1)

        r = int(
            BACKGROUND_TOP[0] * (1 - ratio)
            + BACKGROUND_BOTTOM[0] * ratio
        )

        g = int(
            BACKGROUND_TOP[1] * (1 - ratio)
            + BACKGROUND_BOTTOM[1] * ratio
        )

        b = int(
            BACKGROUND_TOP[2] * (1 - ratio)
            + BACKGROUND_BOTTOM[2] * ratio
        )

        for x in range(CARD_WIDTH):
            pixels[x, y] = (r, g, b)

    return image


# =========================
# اصلاح علائم مشکل‌دار
# =========================

def normalize_text(text):
    # فونت BNazanin بعضی نسخه‌ها کاراکتر … را ندارد
    # بنابراین آن را به سه نقطه معمولی تبدیل می‌کنیم.
    text = text.replace("…", "...")

    return text


# =========================
# شکستن خطوط بر اساس عرض واقعی
# =========================

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


# =========================
# آماده‌سازی شعر
# =========================

def prepare_poem_lines(draw, text, font, max_width):

    text = normalize_text(text)

    raw_lines = text.splitlines()

    final_lines = []

    for line in raw_lines:

        # خط خالی واقعی کاربر حفظ شود
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


# =========================
# محاسبه ارتفاع شعر
# =========================

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

    # فاصله آخر حذف شود
    last_line = lines[-1]

    if last_line is not None:
        total -= line_spacing

    return total


# =========================
# ساخت کارت شعر
# =========================

def create_poetry_card(text):

    image = create_gradient_background()
    draw = ImageDraw.Draw(image)

    # =========================
    # کادر
    # =========================

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

    # =========================
    # عنوان
    # =========================

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

    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    # =========================
    # زیرعنوان
    # =========================

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

    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

    # =========================
    # چیدمان هدر
    #
    # شعرکده سمت راست
    # سروش پلاس سمت چپ آن
    # =========================

    title_y = 82

    header_center = CARD_WIDTH // 2

    # فاصله کمتر بین دو نوشته
    gap = 18

    # عنوان در سمت راست مرکز
    title_x = header_center + 10

    # زیرعنوان در سمت چپ عنوان
    subtitle_x = title_x - subtitle_width - gap

    # اصلاح تراز عمودی
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

    # =========================
    # خط تزئینی
    # =========================

    line_width = 120

    line_y = title_y + title_height + 24

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

    # =========================
    # محدوده شعر
    # =========================

    text_left = 90
    text_right = 990

    max_width = text_right - text_left

    text_top = 220
    text_bottom = 900

    available_height = text_bottom - text_top

    # =========================
    # تنظیم خودکار اندازه فونت
    # =========================

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

    # =========================
    # متن خالی
    # =========================

    if not lines:

        poem_font = get_font(
            POEM_FONT,
            48
        )

        lines = ["متن خالی است"]

    # =========================
    # ارتفاع نهایی
    # =========================

    total_height = calculate_text_height(
        draw,
        lines,
        poem_font,
        line_spacing,
        blank_line_spacing
    )

    # وسط‌چین عمودی
    y = (
        text_top
        + (available_height - total_height) // 2
    )

    # =========================
    # رسم شعر
    # =========================

    for line in lines:

        # خط خالی واقعی
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

        x = (CARD_WIDTH - width) // 2

        draw.text(
            (x, y),
            line,
            font=poem_font,
            fill=TEXT_COLOR
        )

        y += height + line_spacing

    # =========================
    # پایین کارت
    # =========================

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

    # =========================
    # ذخیره
    # =========================

    filename = "/tmp/poetry_card.png"

    image.save(
        filename,
        "PNG",
        optimize=True
    )

    return filename


# =========================
# ارسال پیام
# =========================

def send_message(chat_id, text):

    try:

        response = requests.post(
            f"{API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
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


# =========================
# ارسال عکس
# =========================

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


# =========================
# صفحه اصلی
# =========================

@app.route("/")
def home():

    return (
        "Poetry Card Bot is running",
        200
    )


# =========================
# Webhook
# =========================

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

    # =========================
    # start
    # =========================

    if text == "/start":

        send_message(
            user_id,
            "سلام 👋\n\n"
            "🖼️ به بات کارت شعر خوش آمدی.\n\n"
            "شعرت را همین‌جا بفرست "
            "تا برایت کارت شعر بسازم. ✨"
        )

        return "OK", 200

    # =========================
    # ساخت کارت
    # =========================

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


# =========================
# اجرای برنامه
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


