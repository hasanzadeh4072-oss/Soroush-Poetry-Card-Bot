const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const previewEmpty = document.getElementById("previewEmpty");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const paletteButtons = document.getElementById("paletteButtons");
const optionButtons = document.querySelectorAll(".option-btn");

const W = 1080;
const H = 1080;

const S = 2;
const RW = W * S;
const RH = H * S;

canvas.width = RW;
canvas.height = RH;

const FONT_URLS = {
    poem: "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/Parastoo%5Bwght%5D.ttf",
    title: "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/BTitrBd.ttf",
    sub: "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/Vazirmatn-Regular.ttf"
};

const BG_URL =
    "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";


/* =========================================================
   پالت‌های دقیق کد بات
========================================================= */

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


/* =========================================================
   وضعیت
========================================================= */

let selectedPalette = 0;
let branded = true;
let fontsReady = false;
let backgroundImage = null;


/* =========================================================
   ابزار رنگ
========================================================= */

function rgba(c) {
    if (c.length === 3) {
        return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
    }

    return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${c[3] / 255})`;
}


/* =========================================================
   بارگذاری فونت‌ها
========================================================= */

async function loadFonts() {
    try {
        const poemFont = new FontFace(
            "PoetryParastoo",
            `url("${FONT_URLS.poem}")`
        );

        const titleFont = new FontFace(
            "PoetryBTitr",
            `url("${FONT_URLS.title}")`
        );

        const subFont = new FontFace(
            "PoetryVazirmatn",
            `url("${FONT_URLS.sub}")`
        );

        await Promise.all([
            poemFont.load(),
            titleFont.load(),
            subFont.load()
        ]).then(fonts => {
            fonts.forEach(font => document.fonts.add(font));
        });

        fontsReady = true;
    } catch (error) {
        console.error("Font loading failed:", error);
        fontsReady = false;
    }
}


/* =========================================================
   بارگذاری پس‌زمینه تذهیب
========================================================= */

function loadBackground() {
    return new Promise(resolve => {
        const img = new Image();

        img.crossOrigin = "anonymous";

        img.onload = () => {
            backgroundImage = img;
            resolve();
        };

        img.onerror = () => {
            console.warn("Background image could not be loaded.");
            backgroundImage = null;
            resolve();
        };

        img.src = BG_URL;
    });
}


/* =========================================================
   دکمه‌های رنگ
========================================================= */

function makePaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach((palette, index) => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "palette-btn";
        button.textContent = palette.name;

        const gradient =
            `linear-gradient(135deg, ` +
            `${rgba(palette.top)}, ` +
            `${rgba(palette.middle)} 55%, ` +
            `${rgba(palette.bottom)})`;

        button.style.background = gradient;

        if (index < 6) {
            button.style.color = "#ffffff";
        } else {
            button.style.color = "#27313a";
        }

        if (index === selectedPalette) {
            button.classList.add("active");
        }

        button.addEventListener("click", () => {
            selectedPalette = index;

            document
                .querySelectorAll(".palette-btn")
                .forEach(btn => btn.classList.remove("active"));

            button.classList.add("active");

            render();
        });

        paletteButtons.appendChild(button);
    });
}


/* =========================================================
   نوع کارت
========================================================= */

optionButtons.forEach(button => {
    button.addEventListener("click", () => {
        optionButtons.forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");

        branded = button.dataset.branded === "true";

        render();
    });
});


/* =========================================================
   تبدیل متن
========================================================= */

function normalizeText(text) {
    return text
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .replace(/…/g, "...")
        .trim();
}


/* =========================================================
   اندازه‌گیری متن
========================================================= */

function getPoemFont(size) {
    return `${size * S}px "PoetryParastoo", "Parastoo", serif`;
}

function measureTextWidth(text, font) {
    ctx.font = font;
    return ctx.measureText(text).width;
}


/* =========================================================
   شکستن خطوط
========================================================= */

function prepareLines(text, fontSize, maxWidth) {
    const rawLines = normalizeText(text).split("\n");
    const lines = [];

    ctx.font = getPoemFont(fontSize);

    for (const rawLine of rawLines) {
        const line = rawLine.trim();

        if (!line) {
            lines.push(null);
            continue;
        }

        const words = line.split(/\s+/);
        let current = "";

        for (const word of words) {
            const candidate = current
                ? `${current} ${word}`
                : word;

            if (measureTextWidth(candidate, ctx.font) <= maxWidth) {
                current = candidate;
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


/* =========================================================
   اندازه فونت
========================================================= */

function getFontSize(text) {
    const left = 145 * S;
    const right = 935 * S;
    const top = 205 * S;
    const bottom = 845 * S;

    const maxWidth = right - left;
    const availableHeight = bottom - top;

    let fontSize = 66;

    while (fontSize >= 28) {
        const lines = prepareLines(
            text,
            fontSize,
            maxWidth
        );

        let totalHeight = 0;

        for (let i = 0; i < lines.length; i++) {
            if (lines[i] === null) {
                totalHeight += 48 * S;
                continue;
            }

            ctx.font = getPoemFont(fontSize);

            const bbox = ctx.measureText(lines[i]);

            const lineHeight =
                Math.max(
                    bbox.actualBoundingBoxAscent +
                    bbox.actualBoundingBoxDescent,
                    fontSize * S
                );

            totalHeight += lineHeight;

            if (i < lines.length - 1) {
                totalHeight += 32 * S;
            }
        }

        if (totalHeight <= availableHeight) {
            return fontSize;
        }

        fontSize -= 2;
    }

    return 28;
}


/* =========================================================
   پس‌زمینه گرادیانی
========================================================= */

function drawGradientBackground(palette) {
    const gradient = ctx.createLinearGradient(
        0,
        0,
        0,
        RH
    );

    gradient.addColorStop(0, rgba(palette.top));
    gradient.addColorStop(0.52, rgba(palette.middle));
    gradient.addColorStop(1, rgba(palette.bottom));

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, RW, RH);
}


/* =========================================================
   تذهیب پس‌زمینه
========================================================= */

function drawBackgroundImage() {
    if (!backgroundImage) {
        return;
    }

    ctx.save();

    ctx.globalAlpha = 42 / 255;

    /*
     * نزدیک‌ترین معادل مرورگر برای:
     * brightness(.48) + blur(4*S)
     */
    ctx.filter = "brightness(0.48) blur(8px)";

    const size = Math.max(
        RW,
        RH,
        backgroundImage.width,
        backgroundImage.height
    );

    const scale = Math.max(
        RW / backgroundImage.width,
        RH / backgroundImage.height
    );

    const dw = backgroundImage.width * scale;
    const dh = backgroundImage.height * scale;

    const dx = (RW - dw) / 2;
    const dy = (RH - dh) / 2;

    ctx.drawImage(
        backgroundImage,
        dx,
        dy,
        dw,
        dh
    );

    ctx.restore();
}


/* =========================================================
   نورهای پس‌زمینه
========================================================= */

function drawGlows(palette) {
    const glowCanvas = document.createElement("canvas");

    glowCanvas.width = RW;
    glowCanvas.height = RH;

    const glowCtx = glowCanvas.getContext("2d");

    glowCtx.save();

    glowCtx.filter = "blur(220px)";

    /*
     * glow1
     * (-260*S, -180*S, 650*S, 560*S)
     */
    glowCtx.fillStyle = rgba(palette.glow1);

    glowCtx.beginPath();

    glowCtx.ellipse(
        ((-260 + 650) / 2) * S,
        ((-180 + 560) / 2) * S,
        ((650 - (-260)) / 2) * S,
        ((560 - (-180)) / 2) * S,
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();

    /*
     * glow2
     * (690*S, 690*S, 1250*S, 1250*S)
     */
    glowCtx.fillStyle = rgba(palette.glow2);

    glowCtx.beginPath();

    glowCtx.ellipse(
        ((690 + 1250) / 2) * S,
        ((690 + 1250) / 2) * S,
        ((1250 - 690) / 2) * S,
        ((1250 - 690) / 2) * S,
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();

    /*
     * glow3
     * (250*S, 350*S, 850*S, 950*S)
     */
    glowCtx.fillStyle = rgba(palette.glow3);

    glowCtx.beginPath();

    glowCtx.ellipse(
        ((250 + 850) / 2) * S,
        ((350 + 950) / 2) * S,
        ((850 - 250) / 2) * S,
        ((950 - 350) / 2) * S,
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();

    glowCtx.restore();

    ctx.drawImage(
        glowCanvas,
        0,
        0
    );
}


/* =========================================================
   بافت
========================================================= */

function seededRandom(seed) {
    let x = seed >>> 0;

    return function () {
        x ^= x << 13;
        x ^= x >>> 17;
        x ^= x << 5;

        return (x >>> 0) / 4294967296;
    };
}

function drawTexture() {
    const textureCanvas = document.createElement("canvas");

    textureCanvas.width = RW;
    textureCanvas.height = RH;

    const textureCtx = textureCanvas.getContext("2d");

    const random = seededRandom(8);

    for (let i = 0; i < 56000; i++) {
        const x = Math.floor(random() * RW);
        const y = Math.floor(random() * RH);

        const isWhite = random() < 0.5;

        textureCtx.fillStyle = isWhite
            ? "rgba(255,255,255,0.0118)"
            : "rgba(0,0,0,0.0157)";

        textureCtx.fillRect(
            x,
            y,
            1,
            1
        );
    }

    ctx.drawImage(
        textureCanvas,
        0,
        0
    );
}


/* =========================================================
   پنل وسط کارت
========================================================= */

function drawPanel(palette) {
    const panelCanvas = document.createElement("canvas");

    panelCanvas.width = RW;
    panelCanvas.height = RH;

    const panelCtx = panelCanvas.getContext("2d");

    panelCtx.save();

    /*
     * لایه مشکی
     */
    panelCtx.fillStyle = "rgba(0,0,0,0.1765)";

    roundedRect(
        panelCtx,
        100 * S,
        164 * S,
        980 * S,
        896 * S,
        45 * S
    );

    panelCtx.fill();

    /*
     * لایه سفید
     */
    panelCtx.fillStyle = "rgba(255,255,255,0.0941)";

    roundedRect(
        panelCtx,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    panelCtx.fill();

    /*
     * خط داخلی
     */
    panelCtx.strokeStyle = "rgba(255,255,255,0.0471)";
    panelCtx.lineWidth = 1 * S;

    roundedRect(
        panelCtx,
        110 * S,
        170 * S,
        970 * S,
        880 * S,
        37 * S
    );

    panelCtx.stroke();

    panelCtx.restore();

    /*
     * GaussianBlur(0.35*S)
     * نزدیک‌ترین معادل
     */
    ctx.save();

    ctx.filter = "blur(0.7px)";

    ctx.drawImage(
        panelCanvas,
        0,
        0
    );

    ctx.restore();

    /*
     * outline مخصوص پالت
     */
    ctx.save();

    ctx.strokeStyle = rgba(palette.panel_outline);
    ctx.lineWidth = 2 * S;

    roundedRect(
        ctx,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    ctx.stroke();

    ctx.restore();
}


/* =========================================================
   مستطیل گوشه‌گرد
========================================================= */

function roundedRect(context, x1, y1, x2, y2, radius) {
    const width = x2 - x1;
    const height = y2 - y1;

    context.beginPath();

    context.moveTo(x1 + radius, y1);

    context.lineTo(x1 + width - radius, y1);

    context.quadraticCurveTo(
        x1 + width,
        y1,
        x1 + width,
        y1 + radius
    );

    context.lineTo(
        x1 + width,
        y1 + height - radius
    );

    context.quadraticCurveTo(
        x1 + width,
        y1 + height,
        x1 + width - radius,
        y1 + height
    );

    context.lineTo(
        x1 + radius,
        y1 + height
    );

    context.quadraticCurveTo(
        x1,
        y1 + height,
        x1,
        y1 + height - radius
    );

    context.lineTo(
        x1,
        y1 + radius
    );

    context.quadraticCurveTo(
        x1,
        y1,
        x1 + radius,
        y1
    );

    context.closePath();
}


/* =========================================================
   قاب اصلی
========================================================= */

function drawFrame(palette) {
    ctx.save();

    ctx.strokeStyle = rgba(palette.frame);
    ctx.lineWidth = 3 * S;

    roundedRect(
        ctx,
        40 * S,
        40 * S,
        1040 * S,
        1040 * S,
        42 * S
    );

    ctx.stroke();

    ctx.strokeStyle = rgba(palette.frame_inner);
    ctx.lineWidth = 2 * S;

    roundedRect(
        ctx,
        49 * S,
        49 * S,
        1031 * S,
        1031 * S,
        35 * S
    );

    ctx.stroke();

    ctx.restore();
}


/* =========================================================
   تزئین وسط
========================================================= */

function drawOrnament(palette, y) {
    const center = (W / 2) * S;
    const width = 150 * S;

    ctx.save();

    ctx.strokeStyle = rgba(palette.ornament);
    ctx.lineWidth = 2 * S;

    ctx.beginPath();

    ctx.moveTo(
        center - width,
        y * S
    );

    ctx.lineTo(
        center - 12 * S,
        y * S
    );

    ctx.moveTo(
        center + 12 * S,
        y * S
    );

    ctx.lineTo(
        center + width,
        y * S
    );

    ctx.stroke();

    ctx.fillStyle = rgba(palette.accent);

    ctx.beginPath();

    ctx.moveTo(
        center,
        (y - 5) * S
    );

    ctx.lineTo(
        center + 5 * S,
        y * S
    );

    ctx.lineTo(
        center,
        (y + 5) * S
    );

    ctx.lineTo(
        center - 5 * S,
        y * S
    );

    ctx.closePath();

    ctx.fill();

    ctx.restore();
}


/* =========================================================
   متن بالای کارت
========================================================= */

function drawHeader(palette) {
    const footerText = "کارت شعر";

    ctx.save();

    ctx.font =
        `${23 * S}px "PoetryVazirmatn", "Vazirmatn", sans-serif`;

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    const metrics = ctx.measureText(footerText);

    const footerY = 78;

    ctx.fillStyle = "rgba(0,0,0,0.2353)";

    ctx.fillText(
        footerText,
        (W / 2) * S + 1 * S,
        footerY * S + 2 * S
    );

    ctx.fillStyle = rgba(palette.accent);

    ctx.fillText(
        footerText,
        (W / 2) * S,
        footerY * S
    );

    const textHeight =
        (metrics.actualBoundingBoxAscent ||
            23 * S);

    drawOrnament(
        palette,
        footerY +
        textHeight / S +
        25
    );

    ctx.restore();
}


/* =========================================================
   برند شعرکده
========================================================= */

function drawBrand(palette) {
    if (!branded) {
        drawOrnament(
            palette,
            H - 112
        );

        return;
    }

    ctx.save();

    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";

    const titleSize = 50;
    const subtitleSize = 23;

    ctx.font =
        `${titleSize * S}px "PoetryBTitr", "BTitrBd", sans-serif`;

    const titleMetrics = ctx.measureText(title);

    const titleWidth = titleMetrics.width;

    const titleHeight =
        titleMetrics.actualBoundingBoxAscent +
        titleMetrics.actualBoundingBoxDescent;

    const titleY =
        H -
        78 -
        titleHeight / S;

    const titleX =
        W / 2 + 10;

    /*
     * عنوان
     */
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";

    ctx.fillStyle = "rgba(0,0,0,0.3137)";

    ctx.fillText(
        title,
        (titleX + 1) * S,
        titleY * S + 2 * S
    );

    ctx.fillStyle = rgba(palette.accent);

    ctx.fillText(
        title,
        titleX * S,
        titleY * S
    );

    /*
     * زیرعنوان
     */
    ctx.font =
        `${subtitleSize * S}px "PoetryVazirmatn", "Vazirmatn", sans-serif`;

    const subMetrics = ctx.measureText(subtitle);
    const subtitleWidth = subMetrics.width;

    const subtitleY =
        titleY +
        (
            titleHeight / S -
            subtitleSize
        ) / 2 -
        3;

    const subtitleX =
        titleX -
        subtitleWidth / S -
        20;

    ctx.fillStyle = rgba(palette.subtitle);

    ctx.fillText(
        subtitle,
        subtitleX * S,
        subtitleY * S
    );

    /*
     * تزئین بالای عنوان
     */
    drawOrnament(
        palette,
        titleY - 25
    );

    ctx.restore();
}


/* =========================================================
   شعر
========================================================= */

function drawPoem(palette, text) {
    const left = 145 * S;
    const right = 935 * S;

    const top = 205 * S;
    const bottom = 845 * S;

    const maxWidth = right - left;
    const availableHeight = bottom - top;

    const fontSize = getFontSize(text);

    const lines = prepareLines(
        text,
        fontSize,
        maxWidth
    );

    ctx.save();

    ctx.font = getPoemFont(fontSize);
    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    let totalHeight = 0;

    const measurements = [];

    for (const line of lines) {
        if (line === null) {
            totalHeight += 48 * S;

            measurements.push({
                line: null,
                height: 48 * S,
                bbox: null
            });

            continue;
        }

        const bbox = ctx.measureText(line);

        const height =
            Math.max(
                bbox.actualBoundingBoxAscent +
                bbox.actualBoundingBoxDescent,
                fontSize * S
            );

        measurements.push({
            line,
            height,
            bbox
        });

        totalHeight += height;
    }

    /*
     * فاصله بین خطوط
     */
    if (lines.length > 1) {
        totalHeight +=
            (lines.length - 1) *
            32 *
            S;
    }

    /*
     * مرکز عمودی
     */
    let y =
        top +
        (availableHeight - totalHeight) / 2;

    for (const item of measurements) {
        if (item.line === null) {
            y += 48 * S;
            continue;
        }

        const bbox = item.bbox;

        const centerX =
            ((left + right) / 2);

        const drawY =
            y +
            item.height / 2 +
            (
                bbox.actualBoundingBoxAscent -
                bbox.actualBoundingBoxDescent
            ) / 2;

        ctx.fillStyle = rgba(palette.text);
        ctx.strokeStyle = rgba(palette.text);

        ctx.lineWidth = 1 * S;

        ctx.fillText(
            item.line,
            centerX,
            drawY
        );

        ctx.strokeText(
            item.line,
            centerX,
            drawY
        );

        y += item.height;
        y += 32 * S;
    }

    ctx.restore();
}


/* =========================================================
   خطوط کناری
========================================================= */

function drawSideDetails(palette) {
    const top = 205;
    const availableHeight = 640;

    const centerY =
        top +
        availableHeight / 2;

    ctx.save();

    ctx.strokeStyle = rgba(palette.side_line);
    ctx.lineWidth = 2 * S;

    /*
     * سمت راست
     */
    ctx.beginPath();

    ctx.moveTo(
        65 * S,
        (centerY - 30) * S
    );

    ctx.lineTo(
        65 * S,
        (centerY + 30) * S
    );

    ctx.stroke();

    /*
     * سمت چپ
     */
    ctx.beginPath();

    ctx.moveTo(
        1015 * S,
        (centerY - 30) * S
    );

    ctx.lineTo(
        1015 * S,
        (centerY + 30) * S
    );

    ctx.stroke();

    /*
     * نقطه‌ها
     */
    ctx.fillStyle = rgba(palette.side_dot);

    ctx.beginPath();

    ctx.ellipse(
        65 * S,
        centerY * S,
        3 * S,
        3 * S,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.ellipse(
        1015 * S,
        centerY * S,
        3 * S,
        3 * S,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();
}


/* =========================================================
   رندر اصلی
========================================================= */

function render() {
    const text = normalizeText(poemInput.value);

    if (!text) {
        canvas.style.display = "none";
        previewEmpty.style.display = "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        return;
    }

    canvas.style.display = "block";
    previewEmpty.style.display = "none";

    downloadBtn.disabled = false;
    shareBtn.disabled = false;

    const palette = PALETTES[selectedPalette];

    /*
     * پاک‌سازی کامل
     */
    ctx.clearRect(
        0,
        0,
        RW,
        RH
    );

    /*
     * 1. گرادیان
     */
    drawGradientBackground(palette);

    /*
     * 2. تذهیب
     */
    drawBackgroundImage();

    /*
     * 3. نورها
     */
    drawGlows(palette);

    /*
     * 4. بافت
     */
    drawTexture();

    /*
     * 5. پنل
     */
    drawPanel(palette);

    /*
     * 6. قاب
     */
    drawFrame(palette);

    /*
     * 7. عنوان بالایی
     */
    drawHeader(palette);

    /*
     * 8. شعر
     */
    drawPoem(
        palette,
        text
    );

    /*
     * 9. جزئیات کناری
     */
    drawSideDetails(palette);

    /*
     * 10. برند
     */
    drawBrand(palette);
}


/* =========================================================
   دانلود
========================================================= */

function createDownloadCanvas() {
    const output = document.createElement("canvas");

    output.width = 1080;
    output.height = 1080;

    const outputCtx = output.getContext("2d");

    outputCtx.imageSmoothingEnabled = true;
    outputCtx.imageSmoothingQuality = "high";

    outputCtx.drawImage(
        canvas,
        0,
        0,
        RW,
        RH,
        0,
        0,
        1080,
        1080
    );

    return output;
}

downloadBtn.addEventListener("click", () => {
    if (!poemInput.value.trim()) {
        return;
    }

    const output = createDownloadCanvas();

    output.toBlob(blob => {
        if (!blob) {
            return;
        }

        const url =
            URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;
        a.download = "kart-sh-er.png";

        document.body.appendChild(a);
        a.click();
        a.remove();

        setTimeout(() => {
            URL.revokeObjectURL(url);
        }, 1000);
    }, "image/png");
});


/* =========================================================
   اشتراک‌گذاری
========================================================= */

shareBtn.addEventListener("click", async () => {
    if (!poemInput.value.trim()) {
        return;
    }

    const output = createDownloadCanvas();

    output.toBlob(async blob => {
        if (!blob) {
            return;
        }

        const file =
            new File(
                [blob],
                "kart-sh-er.png",
                {
                    type: "image/png"
                }
            );

        try {
            if (
                navigator.share &&
                navigator.canShare &&
                navigator.canShare({
                    files: [file]
                })
            ) {
                await navigator.share({
                    title: "کارت شعر",
                    files: [file]
                });

                return;
            }

            if (navigator.share) {
                await navigator.share({
                    title: "کارت شعر"
                });

                return;
            }

            alert(
                "اشتراک‌گذاری در این مرورگر پشتیبانی نمی‌شود."
            );

        } catch (error) {
            if (error.name !== "AbortError") {
                console.error(
                    "Share failed:",
                    error
                );
            }
        }
    }, "image/png");
});


/* =========================================================
   تغییر متن
========================================================= */

poemInput.addEventListener(
    "input",
    render
);


/* =========================================================
   شروع
========================================================= */

async function init() {
    makePaletteButtons();

    await Promise.all([
        loadFonts(),
        loadBackground()
    ]);

    await document.fonts.ready;

    render();
}

init();
