def create_poetry_card(text, palette, branded=True):

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

    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)

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
    # 4. Header / Footer Branding
    # ------------------------------

    stage_start = time.perf_counter()

    # --------------------------------
    # کارت شعر
    # همان تنظیمات قبلی Footer
    # اما منتقل‌شده به بالا
    # --------------------------------

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
        CARD_WIDTH
        - footer_width
    ) // 2

    # همان فاصله قبلی، اما در بالا
    footer_y = 78

    center_x = CARD_WIDTH // 2

    # همان خط قبلی Footer
    draw.line(
        (
            center_x - 35,
            footer_y - 13,
            center_x + 35,
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

    # --------------------------------
    # شعرکده + سروش پلاس
    # همان تنظیمات قبلی Header
    # اما منتقل‌شده به پایین
    # --------------------------------

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

    # همان فاصله افقی قبلی
    header_center = CARD_WIDTH // 2
    gap = 20

    title_x = header_center + 10

    subtitle_x = (
        title_x
        - subtitle_width
        - gap
    )

    # --------------------------------
    # انتقال کامل Header به پایین
    # با حفظ فضای تنفس
    # --------------------------------

    title_y = 940

    subtitle_y = (
        title_y
        + (
            title_height
            - subtitle_height
        ) // 2
        - 3
    )

    if branded:

        # سایه شعرکده
        draw.text(
            (
                title_x + 2,
                title_y + 3
            ),
            title,
            font=title_font,
            fill=(0, 0, 0, 80)
        )

        # شعرکده
        draw.text(
            (
                title_x,
                title_y
            ),
            title,
            font=title_font,
            fill=palette["accent"]
        )

        # سروش پلاس
        draw.text(
            (
                subtitle_x,
                subtitle_y
            ),
            subtitle,
            font=subtitle_font,
            fill=palette["subtitle"]
        )

        # همان فاصله تنفسی قبلی،
        # اما خط بالای شعرکده قرار می‌گیرد
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

        # برای کارت عمومی فقط تزئین بالایی
        # حفظ می‌شود
        ornament_y = 112
        ornament_width = 82
        center_x = CARD_WIDTH // 2

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
    # 9. Footer timing
    # ------------------------------

    print(
        f"[TIMING] 09 - Footer: "
        f"{0:.4f}s"
    )

    # ------------------------------
    # 10. PNG save
    # ------------------------------

    stage_start = time.perf_counter()

    filename = "/tmp/poetry_card.png"

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

    # ------------------------------
    # Total
    # ------------------------------

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
