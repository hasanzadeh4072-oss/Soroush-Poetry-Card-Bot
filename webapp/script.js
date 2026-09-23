const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const paletteButtons = document.getElementById("paletteButtons");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const previewEmpty = document.getElementById("previewEmpty");

const W = 1080;
const H = 1080;

const S = 2;
const RW = W * S;
const RH = H * S;

canvas.width = RW;
canvas.height = RH;

const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";

const FONT_BASE =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "085a674b15bd74787ca00701a8ce9780342e3fd9/";

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

let selectedPalette = PALETTES[0];
let branded = true;

let backgroundImage = null;
let textureCanvas = null;
let panelCanvas = null;
let backgroundCache = new Map();

function rgba(c) {
    return `rgba(${c[0]},${c[1]},${c[2]},${c.length > 3 ? c[3] / 255 : 1})`;
}

function rgb(c) {
    return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function scale(v) {
    return Math.round(v * S);
}

function createOffscreen(w = RW, h = RH) {
    const c = document.createElement("canvas");
    c.width = w;
    c.height = h;
    return c;
}

function drawRoundedRect(c, x, y, w, h, radius, fill, stroke, lineWidth) {
    const d = c.getContext("2d");

    d.beginPath();
    d.roundRect(
        scale(x),
        scale(y),
        scale(w),
        scale(h),
        scale(radius)
    );

    if (fill) {
        d.fillStyle = fill;
        d.fill();
    }

    if (stroke) {
        d.strokeStyle = stroke;
        d.lineWidth = scale(lineWidth);
        d.stroke();
    }
}

function lerp(a, b, t) {
    return Math.round(a + (b - a) * t);
}

/*
 * همان منطق گرادیان پایتون:
 *
 * 0 تا 0.52 : top -> middle
 * 0.52 تا 1  : middle -> bottom
 *
 * عمداً از createLinearGradient استفاده نشده است.
 */
function buildGradient(p) {
    const c = createOffscreen(1, RH);
    const d = c.getContext("2d");
    const image = d.createImageData(1, RH);

    for (let y = 0; y < RH; y++) {
        const ratio = y / (RH - 1);

        let col;

        if (ratio < 0.52) {
            const t = ratio / 0.52;

            col = [
                lerp(p.top[0], p.middle[0], t),
                lerp(p.top[1], p.middle[1], t),
                lerp(p.top[2], p.middle[2], t)
            ];
        } else {
            const t = (ratio - 0.52) / 0.48;

            col = [
                lerp(p.middle[0], p.bottom[0], t),
                lerp(p.middle[1], p.bottom[1], t),
                lerp(p.middle[2], p.bottom[2], t)
            ];
        }

        const i = y * 4;

        image.data[i] = col[0];
        image.data[i + 1] = col[1];
        image.data[i + 2] = col[2];
        image.data[i + 3] = 255;
    }

    d.putImageData(image, 0, 0);

    const result = createOffscreen();

    const rd = result.getContext("2d");
    rd.imageSmoothingEnabled = false;

    rd.drawImage(
        c,
        0,
        0,
        1,
        RH,
        0,
        0,
        RW,
        RH
    );

    return result;
}

async function loadBackground() {
    if (backgroundImage) {
        return backgroundImage;
    }

    return new Promise((resolve) => {
        const img = new Image();

        img.crossOrigin = "anonymous";

        img.onload = () => {
            backgroundImage = img;
            resolve(img);
        };

        img.onerror = () => {
            backgroundImage = null;
            resolve(null);
        };

        img.src = BG_URL;
    });
}

/*
 * معادل تقریبی مرحله:
 *
 * svg2png(output_width=4320)
 * crop به مربع
 * brightness(.48)
 * blur(8px)
 * alpha=42
 */
async function prepareTazhib() {
    const img = await loadBackground();

    if (!img) {
        return null;
    }

    const sourceSize = 4320;

    const source = createOffscreen(sourceSize, sourceSize);
    const sd = source.getContext("2d");

    sd.clearRect(0, 0, sourceSize, sourceSize);

    const scaleFit = Math.max(
        sourceSize / img.width,
        sourceSize / img.height
    );

    const drawW = img.width * scaleFit;
    const drawH = img.height * scaleFit;

    const sx = (drawW - sourceSize) / 2;
    const sy = (drawH - sourceSize) / 2;

    sd.drawImage(
        img,
        -sx,
        -sy,
        drawW,
        drawH
    );

    const data = sd.getImageData(
        0,
        0,
        sourceSize,
        sourceSize
    );

    for (let i = 0; i < data.data.length; i += 4) {
        data.data[i] = Math.round(data.data[i] * 0.48);
        data.data[i + 1] = Math.round(data.data[i + 1] * 0.48);
        data.data[i + 2] = Math.round(data.data[i + 2] * 0.48);
    }

    sd.putImageData(data, 0, 0);

    const result = createOffscreen();
    const rd = result.getContext("2d");

    rd.filter = "blur(8px)";
    rd.globalAlpha = 42 / 255;

    rd.drawImage(
        source,
        0,
        0,
        RW,
        RH
    );

    rd.filter = "none";
    rd.globalAlpha = 1;

    return result;
}

function buildTexture() {
    if (textureCanvas) {
        return textureCanvas;
    }

    const c = createOffscreen();
    const d = c.getContext("2d");

    const image = d.createImageData(RW, RH);
    const data = image.data;

    /*
     * با توجه به اینکه Python random.Random(8)
     * در JS معادل مستقیم ندارد، برای حفظ همان
     * تراکم و شدت بافت از PRNG قطعی استفاده می‌کنیم.
     */
    let seed = 8;

    function random() {
        seed = (seed * 1664525 + 1013904223) >>> 0;
        return seed / 4294967296;
    }

    const points = 56000;

    for (let i = 0; i < points; i++) {
        const x = Math.floor(random() * RW);
        const y = Math.floor(random() * RH);

        const index = (y * RW + x) * 4;

        if (random() < 0.5) {
            data[index] = 255;
            data[index + 1] = 255;
            data[index + 2] = 255;
            data[index + 3] = 3;
        } else {
            data[index] = 0;
            data[index + 1] = 0;
            data[index + 2] = 0;
            data[index + 3] = 4;
        }
    }

    d.putImageData(image, 0, 0);

    textureCanvas = c;

    return c;
}

function buildPanel() {
    if (panelCanvas) {
        return panelCanvas;
    }

    const c = createOffscreen();
    const d = c.getContext("2d");

    drawRoundedRect(
        c,
        100,
        164,
        880,
        732 - 4,
        45,
        "rgba(0,0,0,45/255)"
    );

    /*
     * پایتون:
     * rounded_rectangle((100,160,980,890), ...)
     */
    drawRoundedRect(
        c,
        100,
        160,
        880,
        730,
        45,
        "rgba(255,255,255,24/255)"
    );

    /*
     * blur(.35*S) = .7px
     */
    const blurred = createOffscreen();
    const bd = blurred.getContext("2d");

    bd.filter = "blur(0.7px)";
    bd.drawImage(c, 0, 0);
    bd.filter = "none";

    const finalPanel = createOffscreen();
    const fd = finalPanel.getContext("2d");

    fd.drawImage(blurred, 0, 0);

    drawRoundedRect(
        finalPanel,
        110,
        170,
        860,
        710,
        37,
        null,
        "rgba(255,255,255,12/255)",
        1
    );

    panelCanvas = finalPanel;

    return panelCanvas;
}

function drawBackground(p) {
    const key = p.name;

    if (backgroundCache.has(key)) {
        return backgroundCache.get(key);
    }

    const c = buildGradient(p);
    const d = c.getContext("2d");

    const tazhibPromise = prepareTazhib();

    const texture = buildTexture();

    /*
     * Python glows:
     *
     * (-260*S,-180*S,650*S,560*S)
     * (690*S,690*S,1250*S,1250*S)
     * (250*S,350*S,850*S,950*S)
     *
     * با مختصات اصلی همان بات.
     */
    const glowLayer = createOffscreen();
    const gd = glowLayer.getContext("2d");

    function ellipseGlow(box, color) {
        gd.save();

        gd.filter = "blur(220px)";
        gd.fillStyle = rgba(color);

        gd.beginPath();

        const x1 = scale(box[0]);
        const y1 = scale(box[1]);
        const x2 = scale(box[2]);
        const y2 = scale(box[3]);

        gd.ellipse(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            Math.abs(x2 - x1) / 2,
            Math.abs(y2 - y1) / 2,
            0,
            0,
            Math.PI * 2
        );

        gd.fill();
        gd.restore();
    }

    ellipseGlow(
        [-260, -180, 650, 560],
        p.glow1
    );

    ellipseGlow(
        [690, 690, 1250, 1250],
        p.glow2
    );

    ellipseGlow(
        [250, 350, 850, 950],
        p.glow3
    );

    d.drawImage(glowLayer, 0, 0);

    /*
     * texture
     */
    d.drawImage(texture, 0, 0);

    backgroundCache.set(key, c);

    /*
     * اگر تذهیب آماده شد، روی بک‌گراند قرار می‌گیرد.
     */
    tazhibPromise.then((tazhib) => {
        if (!tazhib) return;

        const cached = backgroundCache.get(key);

        if (!cached) return;

        const cd = cached.getContext("2d");

        cd.drawImage(tazhib, 0, 0);

        if (poemInput.value.trim()) {
            renderCard();
        }
    });

    return c;
}

function drawFrame(p) {
    drawRoundedRect(
        canvas,
        40,
        40,
        1000,
        1000,
        42,
        null,
        rgb(p.frame),
        3
    );

    drawRoundedRect(
        canvas,
        49,
        49,
        982,
        982,
        35,
        null,
        rgb(p.frame_inner),
        2
    );
}

function drawOrnament(d, p, y) {
    const center = W / 2;
    const width = 150;

    d.strokeStyle = rgb(p.ornament);
    d.lineWidth = scale(2);

    d.beginPath();

    d.moveTo(
        scale(center - width),
        scale(y)
    );

    d.lineTo(
        scale(center - 12),
        scale(y)
    );

    d.moveTo(
        scale(center + 12),
        scale(y)
    );

    d.lineTo(
        scale(center + width),
        scale(y)
    );

    d.stroke();

    d.fillStyle = rgb(p.accent);

    d.beginPath();

    d.moveTo(
        scale(center),
        scale(y - 5)
    );

    d.lineTo(
        scale(center + 5),
        scale(y)
    );

    d.lineTo(
        scale(center),
        scale(y + 5)
    );

    d.lineTo(
        scale(center - 5),
        scale(y)
    );

    d.closePath();
    d.fill();
}

function fontString(size, family, weight = "") {
    return `${weight ? weight + " " : ""}${scale(size)}px "${family}"`;
}

function textMetrics(text, font) {
    ctx.font = font;

    const m = ctx.measureText(text);

    const left =
        m.actualBoundingBoxLeft !== undefined
            ? m.actualBoundingBoxLeft
            : 0;

    const right =
        m.actualBoundingBoxRight !== undefined
            ? m.actualBoundingBoxRight
            : m.width;

    const ascent =
        m.actualBoundingBoxAscent !== undefined
            ? m.actualBoundingBoxAscent
            : scale(50);

    const descent =
        m.actualBoundingBoxDescent !== undefined
            ? m.actualBoundingBoxDescent
            : scale(12);

    return {
        width: right + left,
        height: ascent + descent,
        ascent,
        descent,
        left,
        right
    };
}

function drawTextTop(
    d,
    text,
    x,
    y,
    font,
    color,
    shadow = null
) {
    d.font = font;
    d.textAlign = "left";
    d.textBaseline = "alphabetic";

    const m = d.measureText(text);

    const ascent =
        m.actualBoundingBoxAscent !== undefined
            ? m.actualBoundingBoxAscent
            : scale(50);

    if (shadow) {
        d.fillStyle = shadow;
        d.fillText(
            text,
            scale(x + 2),
            scale(y + 3 + ascent / S)
        );
    }

    d.fillStyle = color;

    d.fillText(
        text,
        scale(x),
        scale(y) + ascent
    );
}

function drawBranding(p) {
    const d = ctx;

    const TITLE_SIZE = 50;
    const SUB_SIZE = 23;
    const FOOT_SIZE = 23;

    const titleFont =
        fontString(TITLE_SIZE, "BTitrBd", "700");

    const subFont =
        fontString(SUB_SIZE, "Vazirmatn");

    const footFont =
        fontString(FOOT_SIZE, "Vazirmatn");

    /*
     * Python:
     *
     * footer_y = 78
     * title_y = H - 78 - th
     *
     * و جای X کاملاً از عرض bbox محاسبه می‌شود.
     */
    d.font = footFont;

    const footerM = d.measureText("کارت شعر");

    const fw =
        (footerM.actualBoundingBoxRight || footerM.width) +
        (footerM.actualBoundingBoxLeft || 0);

    const fh =
        (footerM.actualBoundingBoxAscent || scale(18)) +
        (footerM.actualBoundingBoxDescent || scale(5));

    const footerY = 78;

    const footerX =
        (W - fw / S) / 2;

    /*
     * footer shadow
     */
    drawTextTop(
        d,
        "کارت شعر",
        footerX,
        footerY,
        footFont,
        rgba([0, 0, 0, 60])
    );

    drawTextTop(
        d,
        "کارت شعر",
        footerX,
        footerY,
        footFont,
        rgb(p.accent)
    );

    /*
     * همان:
     *
     * draw_ornament(d, p, footer_y + fh + 25)
     */
    drawOrnament(
        d,
        p,
        footerY + fh / S + 25
    );

    /*
     * عنوان شعرکده
     */
    d.font = titleFont;

    const titleM = d.measureText("شعرکده");

    const tw =
        (titleM.actualBoundingBoxRight || titleM.width) +
        (titleM.actualBoundingBoxLeft || 0);

    const th =
        (titleM.actualBoundingBoxAscent || scale(40)) +
        (titleM.actualBoundingBoxDescent || scale(10));

    /*
     * دقیقاً بر اساس:
     *
     * title_y = H - 78 - th
     * title_x = center + 10
     */
    const titleY =
        H - 78 - th / S;

    const titleX =
        W / 2 + 10;

    /*
     * subtitle:
     *
     * subtitle_x = title_x - sw - 20
     */
    d.font = subFont;

    const subM = d.measureText("( سروش پلاس )");

    const sw =
        (subM.actualBoundingBoxRight || subM.width) +
        (subM.actualBoundingBoxLeft || 0);

    const sh =
        (subM.actualBoundingBoxAscent || scale(18)) +
        (subM.actualBoundingBoxDescent || scale(5));

    const subtitleX =
        titleX - sw / S - 20;

    const subtitleY =
        titleY + (th / S - sh / S) / 2 - 3;

    /*
     * همان جایگاه عنوان بات
     */
    drawTextTop(
        d,
        "شعرکده",
        titleX,
        titleY,
        titleFont,
        rgb(p.accent),
        rgba([0, 0, 0, 80])
    );

    drawTextTop(
        d,
        "( سروش پلاس )",
        subtitleX,
        subtitleY,
        subFont,
        rgb(p.subtitle)
    );

    /*
     * همان:
     *
     * draw_ornament(d, p, title_y - 25)
     */
    drawOrnament(
        d,
        p,
        titleY - 25
    );
}

function prepareLines(text, font, maxWidth) {
    const rawLines = text
        .replaceAll("…", "...")
        .split(/\r?\n/);

    const lines = [];

    for (const raw of rawLines) {
        if (!raw.trim()) {
            lines.push(null);
            continue;
        }

        const words = raw.trim().split(/\s+/);
        let current = "";

        for (const word of words) {
            const test =
                current.length === 0
                    ? word
                    : current + " " + word;

            ctx.font = font;

            const m = ctx.measureText(test);

            if (m.width <= scale(maxWidth)) {
                current = test;
            } else {
                if (current) {
                    lines.push(current);
                }

                current = word;
            }
        }

        if (current) {
            lines.push(current);
        }
    }

    return lines;
}

function calculateLineInfo(lines, font) {
    const items = [];

    for (const line of lines) {
        if (line === null) {
            items.push({
                line: null,
                height: 48,
                width: 0,
                top: 0
            });

            continue;
        }

        ctx.font = font;

        const m = ctx.measureText(line);

        const width =
            (m.actualBoundingBoxLeft || 0) +
            (m.actualBoundingBoxRight || m.width);

        const height =
            (m.actualBoundingBoxAscent || scale(40)) +
            (m.actualBoundingBoxDescent || scale(10));

        const top =
            -(m.actualBoundingBoxAscent || scale(40));

        items.push({
            line,
            width: width / S,
            height: height / S,
            top: top / S
        });
    }

    return items;
}

function calculateHeight(items) {
    if (!items.length) {
        return 0;
    }

    let total = 0;

    for (const item of items) {
        if (item.line === null) {
            total += 48;
        } else {
            total += item.height + 32;
        }
    }

    /*
     * Python:
     *
     * subtract one LINE_SPACING if last line nonblank
     */
    const last = items[items.length - 1];

    if (last.line !== null) {
        total -= 32;
    }

    return total;
}

function fitPoem(text) {
    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;

    const maxWidth = 790;
    const availableHeight = 640;

    let fontSize = 66;

    while (fontSize >= 28) {
        const font =
            fontString(fontSize, "Parastoo");

        const lines =
            prepareLines(
                text,
                font,
                maxWidth
            );

        const items =
            calculateLineInfo(
                lines,
                font
            );

        const totalHeight =
            calculateHeight(items);

        const fitsWidth =
            items.every(
                item =>
                    item.line === null ||
                    item.width <= maxWidth
            );

        if (
            totalHeight <= availableHeight &&
            fitsWidth
        ) {
            return {
                fontSize,
                font,
                items,
                totalHeight,
                left,
                right,
                top,
                bottom,
                maxWidth,
                availableHeight
            };
        }

        fontSize -= 2;
    }

    const font =
        fontString(28, "Parastoo");

    const lines =
        prepareLines(
            text,
            font,
            maxWidth
        );

    const items =
        calculateLineInfo(
            lines,
            font
        );

    return {
        fontSize: 28,
        font,
        items,
        totalHeight: calculateHeight(items),
        left,
        right,
        top,
        bottom,
        maxWidth,
        availableHeight
    };
}

function drawPoem(p) {
    const text = poemInput.value;

    if (!text.trim()) {
        return;
    }

    const result = fitPoem(text);

    const {
        font,
        items,
        totalHeight,
        left,
        top,
        bottom,
        maxWidth,
        availableHeight
    } = result;

    /*
     * Python:
     *
     * y = top + (available_height-total_height)/2
     * max(top, y)
     * if overflow:
     *     y = bottom-total_height
     */
    let y =
        top +
        (availableHeight - totalHeight) / 2;

    y = Math.max(top, y);

    if (y + totalHeight > bottom) {
        y = bottom - totalHeight;
    }

    ctx.font = font;
    ctx.textBaseline = "alphabetic";
    ctx.textAlign = "left";

    for (const item of items) {
        if (item.line === null) {
            y += 48;
            continue;
        }

        const x =
            left +
            (maxWidth - item.width) / 2;

        /*
         * Python:
         *
         * d.text(
         *   (x, y-bbox[1]),
         *   line,
         *   ...
         * )
         *
         * Canvas equivalent:
         * baseline = y + ascent
         */
        const metrics =
            ctx.measureText(item.line);

        const ascent =
            metrics.actualBoundingBoxAscent ||
            scale(40);

        ctx.fillStyle = rgb(p.text);

        /*
         * Python:
         * stroke_width=1
         * stroke_fill=text
         */
        ctx.lineWidth = scale(1);
        ctx.strokeStyle = rgb(p.text);

        const baseline =
            scale(y) + ascent;

        ctx.strokeText(
            item.line,
            scale(x),
            baseline
        );

        ctx.fillText(
            item.line,
            scale(x),
            baseline
        );

        y += item.height + 32;
    }

    /*
     * خطوط کناری دقیقاً طبق بات:
     *
     * x = 65
     * x = 1015
     *
     * center_y =
     * top + available_height // 2
     *
     * ±30
     */
    const centerY =
        top + Math.floor(availableHeight / 2);

    ctx.strokeStyle = rgba(p.side_line);
    ctx.lineWidth = scale(2);

    ctx.beginPath();

    ctx.moveTo(
        scale(65),
        scale(centerY - 30)
    );

    ctx.lineTo(
        scale(65),
        scale(centerY + 30)
    );

    ctx.moveTo(
        scale(1015),
        scale(centerY - 30)
    );

    ctx.lineTo(
        scale(1015),
        scale(centerY + 30)
    );

    ctx.stroke();

    /*
     * نقطه‌های دقیقاً در انتهای خطوط
     */
    ctx.fillStyle = rgba(p.side_dot);

    ctx.beginPath();

    ctx.arc(
        scale(65),
        scale(centerY - 30),
        scale(3),
        0,
        Math.PI * 2
    );

    ctx.arc(
        scale(65),
        scale(centerY + 30),
        scale(3),
        0,
        Math.PI * 2
    );

    ctx.arc(
        scale(1015),
        scale(centerY - 30),
        scale(3),
        0,
        Math.PI * 2
    );

    ctx.arc(
        scale(1015),
        scale(centerY + 30),
        scale(3),
        0,
        Math.PI * 2
    );

    ctx.fill();
}

async function renderCard() {
    const text = poemInput.value.trim();

    if (!text) {
        ctx.clearRect(0, 0, RW, RH);

        canvas.style.display = "none";
        previewEmpty.style.display = "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        return;
    }

    canvas.style.display = "block";
    previewEmpty.style.display = "none";

    const p = selectedPalette;

    const bg = drawBackground(p);

    ctx.clearRect(0, 0, RW, RH);

    ctx.drawImage(bg, 0, 0);

    /*
     * ترتیب create_card پایتون:
     *
     * background
     * frame
     * branding
     * panel
     * panel outline
     * poem
     */
    drawFrame(p);

    drawBranding(p);

    const panel = buildPanel();

    ctx.drawImage(
        panel,
        0,
        0
    );

    /*
     * palette panel outline:
     * (100,160,980,890)
     */
    drawRoundedRect(
        canvas,
        100,
        160,
        880,
        730,
        45,
        null,
        rgba(p.panel_outline),
        2
    );

    drawPoem(p);

    downloadBtn.disabled = false;
    shareBtn.disabled = false;
}

function createPaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach((p, index) => {
        const button =
            document.createElement("button");

        button.type = "button";
        button.className = "palette-btn";

        if (index === 0) {
            button.classList.add("active");
        }

        button.textContent = p.name;

        button.style.background =
            `linear-gradient(135deg,
                ${rgb(p.top)},
                ${rgb(p.bottom)})`;

        button.style.color =
            rgb(p.text);

        button.style.borderColor =
            rgba(p.frame);

        button.addEventListener(
            "click",
            () => {
                selectedPalette = p;

                document
                    .querySelectorAll(".palette-btn")
                    .forEach(btn =>
                        btn.classList.remove("active")
                    );

                button.classList.add("active");

                renderCard();
            }
        );

        paletteButtons.appendChild(button);
    });
}

document
    .querySelectorAll(".option-btn")
    .forEach(button => {
        button.addEventListener(
            "click",
            () => {
                branded =
                    button.dataset.branded === "true";

                document
                    .querySelectorAll(".option-btn")
                    .forEach(btn =>
                        btn.classList.remove("active")
                    );

                button.classList.add("active");

                renderCard();
            }
        );
    });

poemInput.addEventListener(
    "input",
    () => {
        renderCard();
    }
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
            "kart-shere.png";

        link.href =
            canvas.toDataURL("image/png");

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
                await new Promise(resolve =>
                    canvas.toBlob(
                        resolve,
                        "image/png"
                    )
                );

            if (
                navigator.share &&
                navigator.canShare
            ) {
                const file =
                    new File(
                        [blob],
                        "kart-shere.png",
                        {
                            type: "image/png"
                        }
                    );

                if (
                    navigator.canShare({
                        files: [file]
                    })
                ) {
                    await navigator.share({
                        files: [file],
                        title: "کارت شعر"
                    });

                    return;
                }
            }

            const link =
                document.createElement("a");

            link.href =
                URL.createObjectURL(blob);

            link.download =
                "kart-shere.png";

            link.click();

            setTimeout(
                () =>
                    URL.revokeObjectURL(
                        link.href
                    ),
                1000
            );
        } catch (error) {
            console.error(error);
        }
    }
);

createPaletteButtons();

renderCard();
