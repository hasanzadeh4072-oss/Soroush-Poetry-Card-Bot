const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const previewEmpty = document.getElementById("previewEmpty");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const paletteButtons = document.getElementById("paletteButtons");

const W = 1080;
const H = 1080;

const S = 2;
const RW = W * S;
const RH = H * S;

const LINE_SPACING = 32;
const BLANK_LINE_SPACING = 48;

const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";

const PALETTES = [
    {
        name:"بنفش سلطنتی",
        top:[76,43,105],
        middle:[50,34,73],
        bottom:[25,18,40],
        glow1:[175,120,215,42],
        glow2:[120,85,175,25],
        glow3:[115,80,160,12],
        frame:[173,137,82],
        frame_inner:[205,172,105],
        text:[255,255,255],
        accent:[244,210,137],
        subtitle:[215,201,184],
        ornament:[155,120,75],
        panel_outline:[205,172,105,42],
        side_line:[205,172,105,82],
        side_dot:[205,172,105,105]
    },
    {
        name:"آبی شبانه",
        top:[30,58,100],
        middle:[25,43,76],
        bottom:[12,20,38],
        glow1:[85,130,205,40],
        glow2:[60,100,175,25],
        glow3:[65,105,165,12],
        frame:[165,140,83],
        frame_inner:[200,170,103],
        text:[255,255,255],
        accent:[239,210,139],
        subtitle:[205,213,220],
        ornament:[145,130,88],
        panel_outline:[190,170,110,42],
        side_line:[200,175,110,82],
        side_dot:[215,185,115,105]
    },
    {
        name:"شرابی",
        top:[103,31,52],
        middle:[65,21,36],
        bottom:[31,10,19],
        glow1:[195,82,105,42],
        glow2:[155,55,78,25],
        glow3:[145,55,70,12],
        frame:[174,133,72],
        frame_inner:[205,169,98],
        text:[255,255,255],
        accent:[241,210,139],
        subtitle:[220,201,190],
        ornament:[155,112,70],
        panel_outline:[195,155,95,42],
        side_line:[200,160,100,82],
        side_dot:[215,175,105,105]
    },
    {
        name:"فیروزه‌ای تیره",
        top:[16,80,88],
        middle:[13,53,61],
        bottom:[6,24,29],
        glow1:[65,170,180,42],
        glow2:[45,125,140,25],
        glow3:[45,135,145,12],
        frame:[172,145,91],
        frame_inner:[205,177,112],
        text:[255,255,255],
        accent:[224,199,132],
        subtitle:[201,218,217],
        ornament:[140,147,98],
        panel_outline:[185,170,110,42],
        side_line:[185,175,110,82],
        side_dot:[210,190,120,105]
    },
    {
        name:"سبز زمردی",
        top:[18,76,64],
        middle:[17,51,46],
        bottom:[7,24,22],
        glow1:[75,160,130,42],
        glow2:[55,125,105,25],
        glow3:[50,115,95,12],
        frame:[168,139,78],
        frame_inner:[200,169,99],
        text:[255,255,255],
        accent:[239,211,137],
        subtitle:[205,218,207],
        ornament:[150,128,77],
        panel_outline:[190,165,100,42],
        side_line:[190,170,105,82],
        side_dot:[210,180,110,105]
    },
    {
        name:"رزگلد",
        top:[94,48,62],
        middle:[60,31,43],
        bottom:[27,13,20],
        glow1:[205,120,135,40],
        glow2:[165,85,105,25],
        glow3:[150,80,95,12],
        frame:[181,125,119],
        frame_inner:[218,165,154],
        text:[255,255,255],
        accent:[235,181,163],
        subtitle:[224,204,197],
        ornament:[174,120,114],
        panel_outline:[215,160,150,42],
        side_line:[210,155,145,82],
        side_dot:[225,170,158,105]
    },
    {
        name:"کرم",
        top:[250,239,210],
        middle:[242,226,190],
        bottom:[226,205,163],
        glow1:[255,252,230,55],
        glow2:[255,240,185,28],
        glow3:[255,255,255,22],
        frame:[91,67,39],
        frame_inner:[126,96,58],
        text:[49,40,31],
        accent:[104,73,38],
        subtitle:[77,61,43],
        ornament:[113,80,42],
        panel_outline:[105,78,43,55],
        side_line:[105,78,43,85],
        side_dot:[94,67,35,125]
    },
    {
        name:"آبی روشن",
        top:[205,235,248],
        middle:[180,220,238],
        bottom:[153,201,225],
        glow1:[235,249,255,58],
        glow2:[145,205,235,28],
        glow3:[255,255,255,24],
        frame:[43,73,91],
        frame_inner:[72,105,124],
        text:[31,51,63],
        accent:[48,82,101],
        subtitle:[54,77,91],
        ornament:[59,91,108],
        panel_outline:[58,91,110,55],
        side_line:[58,91,110,85],
        side_dot:[46,79,99,125]
    },
    {
        name:"مریم‌گلی",
        top:[218,231,205],
        middle:[201,219,184],
        bottom:[179,201,159],
        glow1:[242,249,230,58],
        glow2:[175,205,145,28],
        glow3:[255,255,255,24],
        frame:[60,76,52],
        frame_inner:[91,108,78],
        text:[39,54,35],
        accent:[67,88,55],
        subtitle:[67,82,59],
        ornament:[75,96,62],
        panel_outline:[73,96,62,55],
        side_line:[73,96,62,85],
        side_dot:[62,84,52,125]
    }
];

let selectedPalette = 0;
let branded = true;
let backgroundImage = null;

function rgb(c) {
    return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
}

function rgba(c) {
    return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${c[3] / 255})`;
}

function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();

        img.crossOrigin = "anonymous";

        img.onload = () => resolve(img);
        img.onerror = reject;

        img.src = src;
    });
}

function roundedRect(c, x1, y1, x2, y2, radius) {
    c.beginPath();

    c.moveTo(x1 + radius, y1);
    c.lineTo(x2 - radius, y1);

    c.quadraticCurveTo(
        x2,
        y1,
        x2,
        y1 + radius
    );

    c.lineTo(x2, y2 - radius);

    c.quadraticCurveTo(
        x2,
        y2,
        x2 - radius,
        y2
    );

    c.lineTo(x1 + radius, y2);

    c.quadraticCurveTo(
        x1,
        y2,
        x1,
        y2 - radius
    );

    c.lineTo(x1, y1 + radius);

    c.quadraticCurveTo(
        x1,
        y1,
        x1 + radius,
        y1
    );

    c.closePath();
}

function drawGradient(c, p) {
    const gradient = c.createLinearGradient(
        0,
        0,
        0,
        RH
    );

    gradient.addColorStop(
        0,
        rgb(p.top)
    );

    gradient.addColorStop(
        0.52,
        rgb(p.middle)
    );

    gradient.addColorStop(
        1,
        rgb(p.bottom)
    );

    c.fillStyle = gradient;
    c.fillRect(0, 0, RW, RH);
}

function drawBackground(c) {
    if (!backgroundImage) {
        return;
    }

    c.save();

    c.globalAlpha = 42 / 255;
    c.filter = "brightness(48%) blur(8px)";

    const iw = backgroundImage.naturalWidth;
    const ih = backgroundImage.naturalHeight;

    const ratio = iw / ih;
    const target = RW / RH;

    let dw;
    let dh;

    if (ratio > target) {
        dh = RH;
        dw = iw * RH / ih;
    } else {
        dw = RW;
        dh = ih * RW / iw;
    }

    const dx = (RW - dw) / 2;
    const dy = (RH - dh) / 2;

    c.drawImage(
        backgroundImage,
        dx,
        dy,
        dw,
        dh
    );

    c.restore();
}

function drawGlow(c, p) {
    const glow = document.createElement("canvas");

    glow.width = RW;
    glow.height = RH;

    const g = glow.getContext("2d");

    g.filter = "blur(220px)";

    g.fillStyle = rgba(p.glow1);

    g.beginPath();
    g.ellipse(
        195 * S,
        190 * S,
        455 * S,
        370 * S,
        0,
        0,
        Math.PI * 2
    );
    g.fill();

    g.fillStyle = rgba(p.glow2);

    g.beginPath();
    g.ellipse(
        970 * S,
        970 * S,
        280 * S,
        280 * S,
        0,
        0,
        Math.PI * 2
    );
    g.fill();

    g.fillStyle = rgba(p.glow3);

    g.beginPath();
    g.ellipse(
        550 * S,
        650 * S,
        300 * S,
        300 * S,
        0,
        0,
        Math.PI * 2
    );
    g.fill();

    c.drawImage(
        glow,
        0,
        0
    );
}

function drawTexture(c) {
    const texture = document.createElement("canvas");

    texture.width = RW;
    texture.height = RH;

    const t = texture.getContext("2d");

    let seed = 8;

    function random() {
        seed |= 0;
        seed = Math.imul(
            seed ^ (seed >>> 16),
            2246822507
        );

        seed = Math.imul(
            seed ^ (seed >>> 13),
            3266489909
        );

        return (
            (seed ^= seed >>> 16) >>> 0
        ) / 4294967296;
    }

    for (let i = 0; i < 56000; i++) {

        const x =
            Math.floor(random() * RW);

        const y =
            Math.floor(random() * RH);

        t.fillStyle =
            random() < 0.5
                ? "rgba(255,255,255,0.0117647059)"
                : "rgba(0,0,0,0.0156862745)";

        t.fillRect(
            x,
            y,
            1,
            1
        );
    }

    c.drawImage(
        texture,
        0,
        0
    );
}

function drawPanel(c, p) {
    c.save();

    roundedRect(
        c,
        100 * S,
        164 * S,
        980 * S,
        896 * S,
        45 * S
    );

    c.fillStyle =
        "rgba(0,0,0,0.1764705882)";

    c.fill();

    roundedRect(
        c,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    c.fillStyle =
        "rgba(255,255,255,0.0941176471)";

    c.fill();

    roundedRect(
        c,
        110 * S,
        170 * S,
        970 * S,
        880 * S,
        37 * S
    );

    c.strokeStyle =
        "rgba(255,255,255,0.0470588235)";

    c.lineWidth = 1 * S;
    c.stroke();

    c.restore();

    c.save();

    roundedRect(
        c,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    c.strokeStyle =
        rgba(p.panel_outline);

    c.lineWidth = 2 * S;
    c.stroke();

    c.restore();
}

function drawFrame(c, p) {
    c.save();

    roundedRect(
        c,
        40 * S,
        40 * S,
        1040 * S,
        1040 * S,
        42 * S
    );

    c.strokeStyle =
        rgb(p.frame);

    c.lineWidth = 3 * S;
    c.stroke();

    roundedRect(
        c,
        49 * S,
        49 * S,
        1031 * S,
        1031 * S,
        35 * S
    );

    c.strokeStyle =
        rgb(p.frame_inner);

    c.lineWidth = 2 * S;
    c.stroke();

    c.restore();
}

function drawOrnament(c, p, y) {
    const center = W / 2;
    const width = 150;

    c.save();

    c.strokeStyle =
        rgb(p.ornament);

    c.lineWidth = 2 * S;

    c.beginPath();

    c.moveTo(
        (center - width) * S,
        y * S
    );

    c.lineTo(
        (center - 12) * S,
        y * S
    );

    c.stroke();

    c.beginPath();

    c.moveTo(
        (center + 12) * S,
        y * S
    );

    c.lineTo(
        (center + width) * S,
        y * S
    );

    c.stroke();

    c.fillStyle =
        rgb(p.accent);

    c.beginPath();

    c.moveTo(
        center * S,
        (y - 5) * S
    );

    c.lineTo(
        (center + 5) * S,
        y * S
    );

    c.lineTo(
        center * S,
        (y + 5) * S
    );

    c.lineTo(
        (center - 5) * S,
        y * S
    );

    c.closePath();
    c.fill();

    c.restore();
}

function font(size, family, weight = 400) {
    return `${weight} ${size * S}px "${family}"`;
}

function textSize(c, text, f) {
    c.font = f;

    const b = c.measureText(text);

    return {
        width:
            b.width / S,

        height:
            (
                (b.actualBoundingBoxAscent || 0) +
                (b.actualBoundingBoxDescent || 0)
            ) / S,

        top:
            -(b.actualBoundingBoxAscent || 0) / S,

        bottom:
            (b.actualBoundingBoxDescent || 0) / S
    };
}

function wrapText(c, text, f, maxWidth) {
    c.font = f;

    const words = text.split(/\s+/);

    if (!words.length) {
        return [];
    }

    const lines = [];

    let current = words[0];

    for (let i = 1; i < words.length; i++) {

        const candidate =
            current + " " + words[i];

        const width =
            c.measureText(candidate).width / S;

        if (width <= maxWidth) {
            current = candidate;
        } else {
            lines.push(current);
            current = words[i];
        }
    }

    lines.push(current);

    return lines;
}

function prepareLines(c, text, f, maxWidth) {
    const result = [];

    const normalized =
        text
            .replace(/\r\n/g, "\n")
            .replace(/\r/g, "\n")
            .replace(/…/g, "...");

    for (const raw of normalized.split("\n")) {

        if (!raw.trim()) {
            result.push(null);
            continue;
        }

        result.push(
            ...wrapText(
                c,
                raw.trim(),
                f,
                maxWidth
            )
        );
    }

    return result;
}

function calculateHeight(c, lines, f) {
    let total = 0;

    for (const line of lines) {

        if (line === null) {
            total += BLANK_LINE_SPACING;
            continue;
        }

        const s =
            textSize(
                c,
                line,
                f
            );

        total +=
            s.height +
            LINE_SPACING;
    }

    if (
        lines.length &&
        lines[lines.length - 1] !== null
    ) {
        total -= LINE_SPACING;
    }

    return total;
}

function drawPoem(c, p, text) {
    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;

    const maxWidth =
        right - left;

    const availableHeight =
        bottom - top;

    let fontSize = 66;
    let poemFont;
    let lines = [];

    while (fontSize >= 28) {

        poemFont =
            font(
                fontSize,
                "Parastoo",
                600
            );

        lines =
            prepareLines(
                c,
                text,
                poemFont,
                maxWidth
            );

        const height =
            calculateHeight(
                c,
                lines,
                poemFont
            );

        if (
            height <= availableHeight
        ) {
            break;
        }

        fontSize -= 2;
    }

    if (!lines.length) {
        poemFont =
            font(
                46,
                "Parastoo",
                600
            );

        lines = [
            "متن خالی است"
        ];
    }

    const items = [];
    let totalHeight = 0;

    for (
        let index = 0;
        index < lines.length;
        index++
    ) {

        const line = lines[index];

        if (line === null) {

            items.push({
                line: null,
                height: BLANK_LINE_SPACING
            });

            totalHeight +=
                BLANK_LINE_SPACING;

            continue;
        }

        const m =
            textSize(
                c,
                line,
                poemFont
            );

        items.push({
            line,
            width: m.width,
            height: m.height,
            top: m.top
        });

        totalHeight += m.height;

        if (
            index !== lines.length - 1
        ) {
            totalHeight += LINE_SPACING;
        }
    }

    let y =
        top +
        (
            availableHeight -
            totalHeight
        ) / 2;

    y = Math.max(
        top,
        y
    );

    if (
        y + totalHeight >
        bottom
    ) {
        y =
            bottom -
            totalHeight;
    }

    c.save();

    c.font = poemFont;
    c.textAlign = "left";
    c.textBaseline = "alphabetic";

    for (const item of items) {

        if (item.line === null) {

            y += BLANK_LINE_SPACING;
            continue;
        }

        const x =
            left +
            (
                maxWidth -
                item.width
            ) / 2;

        /*
         * معادل:
         * d.text((x, y - bbox[1]), ...)
         */
        const drawY =
            y -
            item.top;

        c.fillStyle =
            rgb(p.text);

        c.strokeStyle =
            rgb(p.text);

        c.lineWidth = 1 * S;

        c.fillText(
            item.line,
            x * S,
            drawY * S
        );

        c.strokeText(
            item.line,
            x * S,
            drawY * S
        );

        y +=
            item.height +
            LINE_SPACING;
    }

    c.restore();

    const centerY =
        top +
        (
            availableHeight / 2
        );

    c.save();

    c.strokeStyle =
        rgba(p.side_line);

    c.fillStyle =
        rgba(p.side_dot);

    c.lineWidth = 2 * S;

    for (const x of [65, 1015]) {

        c.beginPath();

        c.moveTo(
            x * S,
            (centerY - 30) * S
        );

        c.lineTo(
            x * S,
            (centerY + 30) * S
        );

        c.stroke();

        c.beginPath();

        c.arc(
            x * S,
            centerY * S,
            3 * S,
            0,
            Math.PI * 2
        );

        c.fill();
    }

    c.restore();
}

function drawBranding(c, p) {
    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";
    const footer = "کارت شعر";

    const titleFont =
        font(
            50,
            "BTitrBd",
            700
        );

    const subtitleFont =
        font(
            23,
            "Vazirmatn",
            400
        );

    const footerFont =
        font(
            23,
            "Vazirmatn",
            400
        );

    const titleSize =
        textSize(
            c,
            title,
            titleFont
        );

    const subtitleSize =
        textSize(
            c,
            subtitle,
            subtitleFont
        );

    const footerSize =
        textSize(
            c,
            footer,
            footerFont
        );

    const tw = titleSize.width;
    const th = titleSize.height;

    const sw = subtitleSize.width;
    const sh = subtitleSize.height;

    const fw = footerSize.width;
    const fh = footerSize.height;

    const center = W / 2;

    const footerY = 78;
    const footerX =
        (W - fw) / 2;

    const titleY =
        H - 78 - th;

    const titleX =
        center + 10;

    const subtitleX =
        titleX -
        sw -
        20;

    const subtitleY =
        titleY +
        Math.floor(
            (th - sh) / 2
        ) -
        3;

    c.save();

    /*
     * footer
     */
    c.font = footerFont;
    c.textAlign = "left";
    c.textBaseline = "top";

    c.fillStyle =
        "rgba(0,0,0,0.2352941176)";

    c.fillText(
        footer,
        (footerX + 1) * S,
        (footerY + 2) * S
    );

    c.fillStyle =
        rgb(p.accent);

    c.fillText(
        footer,
        footerX * S,
        footerY * S
    );

    c.restore();

    /*
     * خط زیر «کارت شعر»
     * دقیقاً از footer_y + fh + 25
     */
    drawOrnament(
        c,
        p,
        footerY + fh + 25
    );

    if (branded) {

        c.save();

        /*
         * شعرکده
         */
        c.font = titleFont;
        c.textAlign = "left";
        c.textBaseline = "top";

        c.fillStyle =
            "rgba(0,0,0,0.3137254902)";

        c.fillText(
            title,
            (titleX + 2) * S,
            (titleY + 3) * S
        );

        c.fillStyle =
            rgb(p.accent);

        c.fillText(
            title,
            titleX * S,
            titleY * S
        );

        /*
         * سروش پلاس
         */
        c.font = subtitleFont;

        c.fillStyle =
            rgb(p.subtitle);

        c.fillText(
            subtitle,
            subtitleX * S,
            subtitleY * S
        );

        c.restore();

        /*
         * خط بالای شعرکده
         * دقیقاً title_y - 25
         */
        drawOrnament(
            c,
            p,
            titleY - 25
        );

    } else {

        drawOrnament(
            c,
            p,
            H - 112
        );
    }
}

function renderCard(text) {
    const p =
        PALETTES[selectedPalette];

    const highCanvas =
        document.createElement("canvas");

    highCanvas.width = RW;
    highCanvas.height = RH;

    const highCtx =
        highCanvas.getContext("2d");

    highCtx.imageSmoothingEnabled = true;
    highCtx.imageSmoothingQuality = "high";

    /*
     * دقیقاً ترتیب create_card:
     *
     * background آماده
     * frame
     * footer / branding
     * panel
     * poem
     */

    drawGradient(
        highCtx,
        p
    );

    drawBackground(
        highCtx
    );

    drawGlow(
        highCtx,
        p
    );

    drawTexture(
        highCtx
    );

    drawFrame(
        highCtx,
        p
    );

    drawBranding(
        highCtx,
        p
    );

    drawPanel(
        highCtx,
        p
    );

    drawPoem(
        highCtx,
        p,
        text
    );

    canvas.width = W;
    canvas.height = H;

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    /*
     * معادل resize(..., LANCZOS)
     */
    ctx.drawImage(
        highCanvas,
        0,
        0,
        RW,
        RH,
        0,
        0,
        W,
        H
    );
}

function createPaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach(
        (palette, index) => {

            const button =
                document.createElement(
                    "button"
                );

            button.type = "button";
            button.className =
                "palette-btn";

            button.textContent =
                palette.name;

            button.style.background =
                `linear-gradient(135deg,
                    ${rgb(palette.top)},
                    ${rgb(palette.bottom)}
                )`;

            /*
             * رنگ دکمه فقط مربوط به UI است.
             * خود کارت از PALETTES اصلی استفاده می‌کند.
             */
            const luminance =
                (
                    0.299 * palette.top[0] +
                    0.587 * palette.top[1] +
                    0.114 * palette.top[2]
                );

            button.style.color =
                luminance < 145
                    ? "#ffffff"
                    : "#1f2933";

            if (
                index === selectedPalette
            ) {
                button.classList.add(
                    "active"
                );
            }

            button.addEventListener(
                "click",
                () => {

                    selectedPalette =
                        index;

                    document
                        .querySelectorAll(
                            ".palette-btn"
                        )
                        .forEach(
                            btn =>
                                btn.classList.remove(
                                    "active"
                                )
                        );

                    button.classList.add(
                        "active"
                    );

                    drawPreview();
                }
            );

            paletteButtons.appendChild(
                button
            );
        }
    );
}

function drawPreview() {
    const text =
        poemInput.value.trim();

    if (!text) {

        canvas.style.display =
            "none";

        previewEmpty.style.display =
            "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        return;
    }

    canvas.style.display =
        "block";

    previewEmpty.style.display =
        "none";

    downloadBtn.disabled = false;
    shareBtn.disabled = false;

    renderCard(text);
}

document
    .querySelectorAll(".option-btn")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(
                        ".option-btn"
                    )
                    .forEach(
                        btn =>
                            btn.classList.remove(
                                "active"
                            )
                    );

                button.classList.add(
                    "active"
                );

                branded =
                    button.dataset.branded ===
                    "true";

                drawPreview();
            }
        );
    });

poemInput.addEventListener(
    "input",
    drawPreview
);

downloadBtn.addEventListener(
    "click",
    () => {

        if (!poemInput.value.trim()) {
            return;
        }

        const link =
            document.createElement("a");

        link.download =
            "kart-sh3r.png";

        link.href =
            canvas.toDataURL(
                "image/png"
            );

        link.click();
    }
);

shareBtn.addEventListener(
    "click",
    async () => {

        if (!poemInput.value.trim()) {
            return;
        }

        try {

            const blob =
                await new Promise(
                    resolve =>
                        canvas.toBlob(
                            resolve,
                            "image/png"
                        )
                );

            if (!blob) {
                return;
            }

            const file =
                new File(
                    [blob],
                    "kart-sh3r.png",
                    {
                        type:
                            "image/png"
                    }
                );

            if (
                navigator.share &&
                navigator.canShare &&
                navigator.canShare({
                    files: [file]
                })
            ) {

                await navigator.share({
                    files: [file],
                    title: "کارت شعر"
                });

            } else {

                const url =
                    URL.createObjectURL(
                        blob
                    );

                const link =
                    document.createElement(
                        "a"
                    );

                link.href = url;
                link.download =
                    "kart-sh3r.png";

                link.click();

                setTimeout(
                    () =>
                        URL.revokeObjectURL(
                            url
                        ),
                    1000
                );
            }

        } catch (error) {

            if (
                error.name !==
                "AbortError"
            ) {
                console.error(error);
            }
        }
    }
);

createPaletteButtons();

(async () => {

    try {
        backgroundImage =
            await loadImage(
                BG_URL
            );
    } catch (error) {
        console.error(
            "Background load error:",
            error
        );

        backgroundImage = null;
    }

    try {
        await Promise.all([
            document.fonts.load(
                '50px "BTitrBd"'
            ),
            document.fonts.load(
                '23px "Vazirmatn"'
            ),
            document.fonts.load(
                '66px "Parastoo"'
            )
        ]);
    } catch (error) {
        console.error(
            "Font load error:",
            error
        );
    }

    drawPreview();

})();
