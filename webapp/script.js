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
        name: "بنفش سلطنتی",
        top: [76, 43, 105],
        middle: [50, 34, 73],
        bottom: [25, 18, 40],
        glow1: [175, 120, 215, 42],
        glow2: [120, 85, 175, 25],
        glow3: [115, 80, 160, 12],
        frame: [173, 137, 82],
        frame_inner: [205, 172, 105],
        text: [255, 255, 255],
        accent: [244, 210, 137],
        subtitle: [215, 201, 184],
        ornament: [155, 120, 75],
        panel_outline: [205, 172, 105, 42],
        side_line: [205, 172, 105, 82],
        side_dot: [205, 172, 105, 105]
    },
    {
        name: "آبی شبانه",
        top: [30, 58, 100],
        middle: [25, 43, 76],
        bottom: [12, 20, 38],
        glow1: [85, 130, 205, 40],
        glow2: [60, 100, 175, 25],
        glow3: [65, 105, 165, 12],
        frame: [165, 140, 83],
        frame_inner: [200, 170, 103],
        text: [255, 255, 255],
        accent: [239, 210, 139],
        subtitle: [205, 213, 220],
        ornament: [145, 130, 88],
        panel_outline: [190, 170, 110, 42],
        side_line: [200, 175, 110, 82],
        side_dot: [215, 185, 115, 105]
    },
    {
        name: "شرابی",
        top: [103, 31, 52],
        middle: [65, 21, 36],
        bottom: [31, 10, 19],
        glow1: [195, 82, 105, 42],
        glow2: [155, 55, 78, 25],
        glow3: [145, 55, 70, 12],
        frame: [174, 133, 72],
        frame_inner: [205, 169, 98],
        text: [255, 255, 255],
        accent: [241, 210, 139],
        subtitle: [220, 201, 190],
        ornament: [155, 112, 70],
        panel_outline: [195, 155, 95, 42],
        side_line: [200, 160, 100, 82],
        side_dot: [215, 175, 105, 105]
    },
    {
        name: "فیروزه‌ای تیره",
        top: [16, 80, 88],
        middle: [13, 53, 61],
        bottom: [6, 24, 29],
        glow1: [65, 170, 180, 42],
        glow2: [45, 125, 140, 25],
        glow3: [45, 135, 145, 12],
        frame: [172, 145, 91],
        frame_inner: [205, 177, 112],
        text: [255, 255, 255],
        accent: [224, 199, 132],
        subtitle: [201, 218, 217],
        ornament: [140, 147, 98],
        panel_outline: [185, 170, 110, 42],
        side_line: [185, 175, 110, 82],
        side_dot: [210, 190, 120, 105]
    },
    {
        name: "سبز زمردی",
        top: [18, 76, 64],
        middle: [17, 51, 46],
        bottom: [7, 24, 22],
        glow1: [75, 160, 130, 42],
        glow2: [55, 125, 105, 25],
        glow3: [50, 115, 95, 12],
        frame: [168, 139, 78],
        frame_inner: [200, 169, 99],
        text: [255, 255, 255],
        accent: [239, 211, 137],
        subtitle: [205, 218, 207],
        ornament: [150, 128, 77],
        panel_outline: [190, 165, 100, 42],
        side_line: [190, 170, 105, 82],
        side_dot: [210, 180, 110, 105]
    },
    {
        name: "رزگلد",
        top: [94, 48, 62],
        middle: [60, 31, 43],
        bottom: [27, 13, 20],
        glow1: [205, 120, 135, 40],
        glow2: [165, 85, 105, 25],
        glow3: [150, 80, 95, 12],
        frame: [181, 125, 119],
        frame_inner: [218, 165, 154],
        text: [255, 255, 255],
        accent: [235, 181, 163],
        subtitle: [224, 204, 197],
        ornament: [174, 120, 114],
        panel_outline: [215, 160, 150, 42],
        side_line: [210, 155, 145, 82],
        side_dot: [225, 170, 158, 105]
    },
    {
        name: "کرم",
        top: [250, 239, 210],
        middle: [242, 226, 190],
        bottom: [226, 205, 163],
        glow1: [255, 252, 230, 55],
        glow2: [255, 240, 185, 28],
        glow3: [255, 255, 255, 22],
        frame: [91, 67, 39],
        frame_inner: [126, 96, 58],
        text: [49, 40, 31],
        accent: [104, 73, 38],
        subtitle: [77, 61, 43],
        ornament: [113, 80, 42],
        panel_outline: [105, 78, 43, 55],
        side_line: [105, 78, 43, 85],
        side_dot: [94, 67, 35, 125]
    },
    {
        name: "آبی روشن",
        top: [205, 235, 248],
        middle: [180, 220, 238],
        bottom: [153, 201, 225],
        glow1: [235, 249, 255, 58],
        glow2: [145, 205, 235, 28],
        glow3: [255, 255, 255, 24],
        frame: [43, 73, 91],
        frame_inner: [72, 105, 124],
        text: [31, 51, 63],
        accent: [48, 82, 101],
        subtitle: [54, 77, 91],
        ornament: [59, 91, 108],
        panel_outline: [58, 91, 110, 55],
        side_line: [58, 91, 110, 85],
        side_dot: [46, 79, 99, 125]
    },
    {
        name: "مریم‌گلی",
        top: [218, 231, 205],
        middle: [201, 219, 184],
        bottom: [179, 201, 159],
        glow1: [242, 249, 230, 58],
        glow2: [175, 205, 145, 28],
        glow3: [255, 255, 255, 24],
        frame: [60, 76, 52],
        frame_inner: [91, 108, 78],
        text: [39, 54, 35],
        accent: [67, 88, 55],
        subtitle: [67, 82, 59],
        ornament: [75, 96, 62],
        panel_outline: [73, 96, 62, 55],
        side_line: [73, 96, 62, 85],
        side_dot: [62, 84, 52, 125]
    }
];

const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

canvas.width = RW;
canvas.height = RH;

const poemInput = document.getElementById("poemInput");
const paletteButtons = document.getElementById("paletteButtons");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const previewEmpty = document.getElementById("previewEmpty");

let selectedPalette = 0;
let branded = true;
let hasText = false;

const backgroundCache = new Map();

function rgba(c) {
    if (c.length === 3) {
        return `rgb(${c[0]},${c[1]},${c[2]})`;
    }

    return `rgba(${c[0]},${c[1]},${c[2]},${c[3] / 255})`;
}

function scaleRect(x, y, w, h) {
    return {
        x: x * S,
        y: y * S,
        w: w * S,
        h: h * S
    };
}

function roundedRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.roundRect(
        x * S,
        y * S,
        w * S,
        h * S,
        r * S
    );
}

function drawRoundedRect(
    x,
    y,
    w,
    h,
    radius,
    fill = null,
    stroke = null,
    lineWidth = 1
) {
    roundedRect(x, y, w, h, radius);

    if (fill) {
        ctx.fillStyle = fill;
        ctx.fill();
    }

    if (stroke) {
        ctx.strokeStyle = stroke;
        ctx.lineWidth = lineWidth * S;
        ctx.stroke();
    }
}

function drawLine(x1, y1, x2, y2, color, width = 1) {
    ctx.beginPath();
    ctx.moveTo(x1 * S, y1 * S);
    ctx.lineTo(x2 * S, y2 * S);
    ctx.strokeStyle = color;
    ctx.lineWidth = width * S;
    ctx.stroke();
}

function drawTextTop(text, x, y, font, color, align = "left") {
    ctx.font = font;
    ctx.textAlign = align;
    ctx.textBaseline = "top";
    ctx.direction = "rtl";

    ctx.fillStyle = color;
    ctx.fillText(text, x * S, y * S);
}

function textMetrics(text, font) {
    ctx.font = font;

    const m = ctx.measureText(text);

    const ascent =
        Number.isFinite(m.actualBoundingBoxAscent)
            ? m.actualBoundingBoxAscent
            : 40;

    const descent =
        Number.isFinite(m.actualBoundingBoxDescent)
            ? m.actualBoundingBoxDescent
            : 10;

    return {
        width: m.width / S,
        height: (ascent + descent) / S,
        ascent: ascent / S,
        descent: descent / S
    };
}

function drawOrnament(p, y) {
    const center = W / 2;
    const width = 150;

    drawLine(
        center - width,
        y,
        center - 12,
        y,
        rgba(p.ornament),
        2
    );

    drawLine(
        center + 12,
        y,
        center + width,
        y,
        rgba(p.ornament),
        2
    );

    ctx.fillStyle = rgba(p.accent);
    ctx.beginPath();
    ctx.moveTo(center * S, (y - 5) * S);
    ctx.lineTo((center + 5) * S, y * S);
    ctx.lineTo(center * S, (y + 5) * S);
    ctx.lineTo((center - 5) * S, y * S);
    ctx.closePath();
    ctx.fill();
}

function buildGradient(p) {
    const gradient = ctx.createLinearGradient(
        0,
        0,
        0,
        RH
    );

    gradient.addColorStop(
        0,
        rgba([...p.top, 255])
    );

    gradient.addColorStop(
        0.52,
        rgba([...p.middle, 255])
    );

    gradient.addColorStop(
        1,
        rgba([...p.bottom, 255])
    );

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, RW, RH);
}

function drawGlow(x1, y1, x2, y2, color) {
    const g = ctx.createRadialGradient(
        ((x1 + x2) / 2) * S,
        ((y1 + y2) / 2) * S,
        0,
        ((x1 + x2) / 2) * S,
        ((y1 + y2) / 2) * S,
        Math.max(
            (x2 - x1) * S,
            (y2 - y1) * S
        ) / 2
    );

    const alpha = color[3] / 255;

    g.addColorStop(
        0,
        `rgba(${color[0]},${color[1]},${color[2]},${alpha})`
    );

    g.addColorStop(
        1,
        `rgba(${color[0]},${color[1]},${color[2]},0)`
    );

    ctx.fillStyle = g;

    ctx.beginPath();
    ctx.ellipse(
        ((x1 + x2) / 2) * S,
        ((y1 + y2) / 2) * S,
        ((x2 - x1) / 2) * S,
        ((y2 - y1) / 2) * S,
        0,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

async function loadTazhib() {
    if (backgroundCache.has("tazhib")) {
        return backgroundCache.get("tazhib");
    }

    try {
        const response = await fetch(BG_URL, {
            mode: "cors"
        });

        if (!response.ok) {
            throw new Error("Background fetch failed");
        }

        const svgText = await response.text();

        const svgBlob = new Blob(
            [svgText],
            { type: "image/svg+xml" }
        );

        const url = URL.createObjectURL(svgBlob);

        const img = new Image();

        await new Promise((resolve, reject) => {
            img.onload = resolve;
            img.onerror = reject;
            img.src = url;
        });

        URL.revokeObjectURL(url);

        const c = document.createElement("canvas");
        c.width = RW;
        c.height = RH;

        const cctx = c.getContext("2d");

        const scale = Math.max(
            RW / img.width,
            RH / img.height
        );

        const iw = img.width * scale;
        const ih = img.height * scale;

        const x = (RW - iw) / 2;
        const y = (RH - ih) / 2;

        cctx.drawImage(
            img,
            x,
            y,
            iw,
            ih
        );

        const imageData = cctx.getImageData(
            0,
            0,
            RW,
            RH
        );

        const data = imageData.data;

        /*
         * معادل تقریبی:
         * Brightness(.48)
         * سپس alpha = 42
         */
        for (let i = 0; i < data.length; i += 4) {
            data[i] = Math.min(
                255,
                data[i] * 0.48
            );

            data[i + 1] = Math.min(
                255,
                data[i + 1] * 0.48
            );

            data[i + 2] = Math.min(
                255,
                data[i + 2] * 0.48
            );

            data[i + 3] =
                Math.round(
                    data[i + 3] * (42 / 255)
                );
        }

        cctx.putImageData(imageData, 0, 0);

        backgroundCache.set(
            "tazhib",
            c
        );

        return c;

    } catch (error) {
        console.warn(
            "Tazhib could not be loaded:",
            error
        );

        backgroundCache.set(
            "tazhib",
            null
        );

        return null;
    }
}

function buildTexture() {
    const texture = document.createElement("canvas");

    texture.width = RW;
    texture.height = RH;

    const tctx = texture.getContext("2d");

    const image = tctx.createImageData(
        RW,
        RH
    );

    /*
     * بافت بسیار ظریف، مشابه نسخه بات.
     * عمداً کم‌رنگ نگه داشته شده است.
     */
    let seed = 8;

    function random() {
        seed =
            (seed * 1664525 + 1013904223)
            >>> 0;

        return seed / 4294967296;
    }

    for (let i = 0; i < 56000; i++) {
        const x =
            Math.floor(random() * RW);

        const y =
            Math.floor(random() * RH);

        const index =
            (y * RW + x) * 4;

        if (random() < 0.5) {
            image.data[index] = 255;
            image.data[index + 1] = 255;
            image.data[index + 2] = 255;
            image.data[index + 3] = 3;
        } else {
            image.data[index] = 0;
            image.data[index + 1] = 0;
            image.data[index + 2] = 0;
            image.data[index + 3] = 4;
        }
    }

    tctx.putImageData(image, 0, 0);

    return texture;
}

const textureCanvas = buildTexture();

async function buildBackground(p) {
    buildGradient(p);

    drawGlow(
        -260,
        -180,
        650,
        560,
        p.glow1
    );

    drawGlow(
        690,
        690,
        1250,
        1250,
        p.glow2
    );

    drawGlow(
        250,
        350,
        850,
        950,
        p.glow3
    );

    /*
     * تیره‌سازی کنترل‌شده‌ی بسیار ملایم برای جلوگیری
     * از روشن شدن بیش از حد پالت‌ها در Canvas.
     */
    ctx.fillStyle = "rgba(0,0,0,0.08)";
    ctx.fillRect(0, 0, RW, RH);

    const tazhib = await loadTazhib();

    if (tazhib) {
        ctx.globalAlpha = 1;
        ctx.drawImage(
            tazhib,
            0,
            0,
            RW,
            RH
        );
    }

    ctx.drawImage(
        textureCanvas,
        0,
        0,
        RW,
        RH
    );
}

function drawFrame(p) {
    drawRoundedRect(
        40,
        40,
        1000,
        1000,
        42,
        null,
        rgba(p.frame),
        3
    );

    drawRoundedRect(
        49,
        49,
        982,
        982,
        35,
        null,
        rgba(p.frame_inner),
        2
    );
}

function drawPanel(p) {
    drawRoundedRect(
        100,
        164,
        880,
        732,
        45,
        "rgba(0,0,0,0.1764705882)"
    );

    drawRoundedRect(
        100,
        160,
        880,
        730,
        45,
        "rgba(255,255,255,0.0941176471)"
    );

    drawRoundedRect(
        110,
        170,
        860,
        710,
        37,
        null,
        "rgba(255,255,255,0.0470588235)",
        1
    );

    drawRoundedRect(
        100,
        160,
        880,
        730,
        45,
        null,
        rgba(p.panel_outline),
        2
    );
}

function drawBranding(p) {
    const titleFont =
        `700 ${50 * S}px "BTitrBd", sans-serif`;

    const subFont =
        `400 ${23 * S}px "Vazirmatn", sans-serif`;

    const footerFont =
        `400 ${23 * S}px "Vazirmatn", sans-serif`;

    const footer = "کارت شعر";

    const footerM =
        textMetrics(
            footer,
            footerFont
        );

    const footerY = 78;
    const footerX =
        (W - footerM.width) / 2;

    ctx.shadowColor =
        "rgba(0,0,0,0.2352941176)";
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 1 * S;
    ctx.shadowOffsetY = 2 * S;

    drawTextTop(
        footer,
        footerX,
        footerY,
        footerFont,
        rgba(p.accent),
        "left"
    );

    ctx.shadowColor = "transparent";
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    drawOrnament(
        p,
        footerY + footerM.height + 25
    );

    if (!branded) {
        drawOrnament(
            p,
            H - 112
        );

        return;
    }

    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";

    const titleM =
        textMetrics(
            title,
            titleFont
        );

    const subM =
        textMetrics(
            subtitle,
            subFont
        );

    /*
     * دقیقاً بر اساس منطق بات:
     *
     * title_x = center + 10
     * subtitle_x = title_x - sw - 20
     *
     * بنابراین شعرکده سمت راست
     * و سروش پلاس دقیقاً روبه‌روی آن قرار می‌گیرد.
     */
    const titleX =
        W / 2 + 10;

    const subtitleX =
        titleX - subM.width - 20;

    const titleY =
        H - 78 - titleM.height;

    const subtitleY =
        titleY +
        (titleM.height - subM.height) / 2 -
        3;

    ctx.shadowColor =
        "rgba(0,0,0,0.3137254902)";
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 2 * S;
    ctx.shadowOffsetY = 3 * S;

    drawTextTop(
        title,
        titleX,
        titleY,
        titleFont,
        rgba(p.accent),
        "left"
    );

    ctx.shadowColor = "transparent";
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    drawTextTop(
        subtitle,
        subtitleX,
        subtitleY,
        subFont,
        rgba(p.subtitle),
        "left"
    );

    drawOrnament(
        p,
        titleY - 25
    );
}

function prepareLines(text, fontSize) {
    ctx.font =
        `400 ${fontSize * S}px "Parastoo", sans-serif`;

    const maxWidth = 790;
    const lines = [];

    const rawLines =
        text.replace(/…/g, "...").split("\n");

    for (const raw of rawLines) {
        if (!raw.trim()) {
            lines.push(null);
            continue;
        }

        const words =
            raw.trim().split(/\s+/);

        let current = "";

        for (const word of words) {
            const test =
                current
                    ? `${current} ${word}`
                    : word;

            const width =
                ctx.measureText(test).width / S;

            if (
                width <= maxWidth ||
                !current
            ) {
                current = test;
            } else {
                lines.push(current);
                current = word;
            }
        }

        if (current) {
            lines.push(current);
        }
    }

    return lines;
}

function calculateLineHeight(line, fontSize) {
    if (line === null) {
        return BLANK_LINE_SPACING;
    }

    ctx.font =
        `400 ${fontSize * S}px "Parastoo", sans-serif`;

    const m =
        ctx.measureText(line);

    const ascent =
        Number.isFinite(m.actualBoundingBoxAscent)
            ? m.actualBoundingBoxAscent / S
            : fontSize * 0.8;

    const descent =
        Number.isFinite(m.actualBoundingBoxDescent)
            ? m.actualBoundingBoxDescent / S
            : fontSize * 0.2;

    return ascent + descent;
}

function calculateTotalHeight(lines, fontSize) {
    let total = 0;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        if (line === null) {
            total += BLANK_LINE_SPACING;
            continue;
        }

        const h =
            calculateLineHeight(
                line,
                fontSize
            );

        if (i < lines.length - 1) {
            total += h + LINE_SPACING;
        } else {
            total += h;
        }
    }

    return total;
}

function drawPoem(p, text) {
    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;

    const maxWidth = 790;
    const availableHeight = 640;

    let fontSize = 66;
    let lines = [];

    while (fontSize >= 28) {
        lines =
            prepareLines(
                text,
                fontSize
            );

        const total =
            calculateTotalHeight(
                lines,
                fontSize
            );

        if (total <= availableHeight) {
            break;
        }

        fontSize -= 2;
    }

    if (!lines.length) {
        fontSize = 46;
        lines = ["متن خالی است"];
    }

    ctx.font =
        `400 ${fontSize * S}px "Parastoo", sans-serif`;

    const totalHeight =
        calculateTotalHeight(
            lines,
            fontSize
        );

    let y =
        top +
        (availableHeight - totalHeight) / 2;

    if (y < top) {
        y = top;
    }

    if (
        y + totalHeight >
        bottom
    ) {
        y =
            bottom -
            totalHeight;
    }

    for (const line of lines) {
        if (line === null) {
            y += BLANK_LINE_SPACING;
            continue;
        }

        ctx.font =
            `400 ${fontSize * S}px "Parastoo", sans-serif`;

        ctx.textAlign = "left";
        ctx.textBaseline = "top";
        ctx.direction = "rtl";

        const width =
            ctx.measureText(line).width / S;

        let x =
            left +
            (maxWidth - width) / 2;

        if (x < left) {
            x = left;
        }

        ctx.fillStyle =
            rgba(p.text);

        ctx.strokeStyle =
            rgba(p.text);

        ctx.lineWidth =
            1 * S;

        ctx.fillText(
            line,
            x * S,
            y * S
        );

        ctx.strokeText(
            line,
            x * S,
            y * S
        );

        const h =
            calculateLineHeight(
                line,
                fontSize
            );

        y += h + LINE_SPACING;
    }

    /*
     * خطوط کناری دقیقاً مطابق بات:
     * x = 65 و 1015
     * y = 495 تا 555
     */
    const centerY =
        top +
        Math.floor(
            availableHeight / 2
        );

    drawLine(
        65,
        centerY - 30,
        65,
        centerY + 30,
        rgba(p.side_line),
        2
    );

    drawLine(
        1015,
        centerY - 30,
        1015,
        centerY + 30,
        rgba(p.side_line),
        2
    );

    ctx.fillStyle =
        rgba(p.side_dot);

    for (const x of [65, 1015]) {
        for (
            const yy of [
                centerY - 30,
                centerY + 30
            ]
        ) {
            ctx.beginPath();
            ctx.arc(
                x * S,
                yy * S,
                3 * S,
                0,
                Math.PI * 2
            );
            ctx.fill();
        }
    }
}

async function createCard() {
    const text =
        poemInput.value.trim();

    const p =
        PALETTES[selectedPalette];

    ctx.clearRect(
        0,
        0,
        RW,
        RH
    );

    await buildBackground(p);

    drawFrame(p);

    drawBranding(p);

    drawPanel(p);

    if (text) {
        drawPoem(
            p,
            text
        );
    }

    hasText = Boolean(text);

    canvas.style.display =
        "block";

    previewEmpty.style.display =
        "none";

    downloadBtn.disabled =
        !hasText;

    shareBtn.disabled =
        !hasText;
}

function renderWhenReady() {
    createCard().catch(
        console.error
    );
}

async function loadFonts() {
    try {
        await Promise.all([
            document.fonts.load(
                `700 ${50 * S}px "BTitrBd"`
            ),
            document.fonts.load(
                `400 ${23 * S}px "Vazirmatn"`
            ),
            document.fonts.load(
                `400 ${66 * S}px "Parastoo"`
            )
        ]);

        await document.fonts.ready;

    } catch (error) {
        console.warn(
            "Font loading warning:",
            error
        );
    }
}

function createPaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach(
        (palette, index) => {
            const button =
                document.createElement("button");

            button.type = "button";
            button.className =
                "palette-btn";

            button.textContent =
                palette.name;

            button.style.background =
                `linear-gradient(135deg,
                    rgb(${palette.top.join(",")}),
                    rgb(${palette.bottom.join(",")})
                )`;

            button.style.color =
                "white";

            if (index === selectedPalette) {
                button.classList.add(
                    "active"
                );
            }

            button.addEventListener(
                "click",
                () => {
                    selectedPalette = index;

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

                    renderWhenReady();
                }
            );

            paletteButtons.appendChild(
                button
            );
        }
    );
}

document
    .querySelectorAll(
        ".option-btn"
    )
    .forEach(button => {
        button.addEventListener(
            "click",
            () => {
                branded =
                    button.dataset.branded ===
                    "true";

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

                renderWhenReady();
            }
        );
    });

poemInput.addEventListener(
    "input",
    renderWhenReady
);

downloadBtn.addEventListener(
    "click",
    () => {
        if (!hasText) return;

        const link =
            document.createElement("a");

        link.download =
            "kart-shere.png";

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
        if (!hasText) return;

        try {
            const blob =
                await new Promise(
                    resolve =>
                        canvas.toBlob(
                            resolve,
                            "image/png"
                        )
                );

            const file =
                new File(
                    [blob],
                    "kart-shere.png",
                    {
                        type: "image/png"
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
                alert(
                    "اشتراک‌گذاری فایل در این مرورگر پشتیبانی نمی‌شود."
                );
            }

        } catch (error) {
            if (
                error &&
                error.name !== "AbortError"
            ) {
                console.error(error);
            }
        }
    }
);

createPaletteButtons();

(async () => {
    await loadFonts();
    await createCard();
})();
