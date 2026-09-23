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
   پالت‌ها
   ۶ رنگ تیره برای نمایش وب کمی روشن‌تر شده‌اند.
   ۳ رنگ روشن بدون تغییر هستند.
========================================================= */

const PALETTES = [
    {
        name: "بنفش سلطنتی",
        top: [92, 55, 123],
        middle: [63, 45, 88],
        bottom: [34, 25, 52],
        glow1: [185, 135, 225, 48],
        glow2: [135, 100, 190, 30],
        glow3: [125, 90, 175, 16],
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
        top: [42, 75, 120],
        middle: [34, 58, 94],
        bottom: [20, 32, 55],
        glow1: [100, 150, 220, 48],
        glow2: [75, 120, 190, 30],
        glow3: [75, 120, 180, 16],
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
        top: [120, 42, 63],
        middle: [79, 29, 45],
        bottom: [40, 15, 25],
        glow1: [210, 95, 120, 48],
        glow2: [170, 65, 90, 30],
        glow3: [155, 65, 80, 16],
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
        top: [24, 98, 106],
        middle: [19, 68, 77],
        bottom: [10, 34, 40],
        glow1: [75, 185, 195, 48],
        glow2: [55, 140, 155, 30],
        glow3: [55, 145, 155, 16],
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
        top: [28, 92, 77],
        middle: [25, 64, 57],
        bottom: [12, 32, 30],
        glow1: [85, 175, 145, 48],
        glow2: [65, 140, 115, 30],
        glow3: [60, 130, 105, 16],
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
        top: [110, 62, 77],
        middle: [72, 42, 55],
        bottom: [36, 20, 30],
        glow1: [215, 135, 150, 46],
        glow2: [175, 100, 120, 30],
        glow3: [160, 90, 105, 16],
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
let backgroundImage = null;


/* =========================================================
   رنگ
========================================================= */

function rgba(c) {
    if (c.length === 3) {
        return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
    }

    return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${c[3] / 255})`;
}


/* =========================================================
   فونت‌ها
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

        const fonts = await Promise.all([
            poemFont.load(),
            titleFont.load(),
            subFont.load()
        ]);

        fonts.forEach(font => {
            document.fonts.add(font);
        });

    } catch (error) {
        console.error("Font loading failed:", error);
    }
}


/* =========================================================
   پس‌زمینه
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

        button.style.background =
            `linear-gradient(135deg,
                ${rgba(palette.top)},
                ${rgba(palette.middle)} 52%,
                ${rgba(palette.bottom)}
            )`;

        button.style.color =
            index < 6 ? "#ffffff" : "#27313a";

        if (index === selectedPalette) {
            button.classList.add("active");
        }

        button.addEventListener("click", () => {
            selectedPalette = index;

            document
                .querySelectorAll(".palette-btn")
                .forEach(btn =>
                    btn.classList.remove("active")
                );

            button.classList.add("active");

            render();
        });

        paletteButtons.appendChild(button);
    });
}


/* =========================================================
   انتخاب نوع کارت
========================================================= */

optionButtons.forEach(button => {
    button.addEventListener("click", () => {
        optionButtons.forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");

        branded =
            button.dataset.branded === "true";

        render();
    });
});


/* =========================================================
   متن
========================================================= */

function normalizeText(text) {
    return text
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .replace(/…/g, "...")
        .trim();
}


/* =========================================================
   فونت شعر
========================================================= */

function getPoemFont(size) {
    return `${size * S}px "PoetryParastoo", "Parastoo", serif`;
}


/* =========================================================
   اندازه متن
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
            const candidate =
                current
                    ? `${current} ${word}`
                    : word;

            if (
                ctx.measureText(candidate).width <=
                maxWidth
            ) {
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


function getFontSize(text) {
    const maxWidth = 790 * S;
    const availableHeight = 640 * S;

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

            ctx.font =
                getPoemFont(fontSize);

            const metrics =
                ctx.measureText(lines[i]);

            const lineHeight =
                Math.max(
                    metrics.actualBoundingBoxAscent +
                    metrics.actualBoundingBoxDescent,
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
   گرادیان
========================================================= */

function drawGradientBackground(palette) {
    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            RH
        );

    gradient.addColorStop(
        0,
        rgba(palette.top)
    );

    gradient.addColorStop(
        0.52,
        rgba(palette.middle)
    );

    gradient.addColorStop(
        1,
        rgba(palette.bottom)
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        RW,
        RH
    );
}


/* =========================================================
   تذهیب
   در نسخه وب، brightness بسیار کمتر شده تا کارت تیره نشود.
========================================================= */

function drawBackgroundImage() {
    if (!backgroundImage) {
        return;
    }

    ctx.save();

    /*
     * در بات brightness=.48 بود،
     * اما روی Canvas باعث تیرگی شدید می‌شد.
     * مقدار جدید عمداً ملایم‌تر است.
     */
    ctx.globalAlpha = 0.15;

    ctx.filter =
        "brightness(0.82) blur(5px)";

    const scale =
        Math.max(
            RW / backgroundImage.width,
            RH / backgroundImage.height
        );

    const dw =
        backgroundImage.width * scale;

    const dh =
        backgroundImage.height * scale;

    const dx =
        (RW - dw) / 2;

    const dy =
        (RH - dh) / 2;

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
   نورها
========================================================= */

function drawGlows(palette) {
    const glowCanvas =
        document.createElement("canvas");

    glowCanvas.width = RW;
    glowCanvas.height = RH;

    const glowCtx =
        glowCanvas.getContext("2d");

    glowCtx.save();

    glowCtx.filter = "blur(150px)";

    function ellipse(
        x1,
        y1,
        x2,
        y2,
        color
    ) {
        glowCtx.fillStyle =
            rgba(color);

        glowCtx.beginPath();

        glowCtx.ellipse(
            ((x1 + x2) / 2) * S,
            ((y1 + y2) / 2) * S,
            ((x2 - x1) / 2) * S,
            ((y2 - y1) / 2) * S,
            0,
            0,
            Math.PI * 2
        );

        glowCtx.fill();
    }

    ellipse(
        -260,
        -180,
        650,
        560,
        palette.glow1
    );

    ellipse(
        690,
        690,
        1250,
        1250,
        palette.glow2
    );

    ellipse(
        250,
        350,
        850,
        950,
        palette.glow3
    );

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

        return (
            (x >>> 0) /
            4294967296
        );
    };
}


function drawTexture() {
    const texture =
        document.createElement("canvas");

    texture.width = RW;
    texture.height = RH;

    const textureCtx =
        texture.getContext("2d");

    const random =
        seededRandom(8);

    for (let i = 0; i < 56000; i++) {
        const x =
            Math.floor(random() * RW);

        const y =
            Math.floor(random() * RH);

        if (random() < 0.5) {
            textureCtx.fillStyle =
                "rgba(255,255,255,0.012)";
        } else {
            textureCtx.fillStyle =
                "rgba(0,0,0,0.016)";
        }

        textureCtx.fillRect(
            x,
            y,
            1,
            1
        );
    }

    ctx.drawImage(
        texture,
        0,
        0
    );
}


/* =========================================================
   مستطیل گوشه‌گرد
========================================================= */

function roundedRect(
    context,
    x,
    y,
    width,
    height,
    radius
) {
    context.beginPath();

    context.moveTo(
        x + radius,
        y
    );

    context.lineTo(
        x + width - radius,
        y
    );

    context.quadraticCurveTo(
        x + width,
        y,
        x + width,
        y + radius
    );

    context.lineTo(
        x + width,
        y + height - radius
    );

    context.quadraticCurveTo(
        x + width,
        y + height,
        x + width - radius,
        y + height
    );

    context.lineTo(
        x + radius,
        y + height
    );

    context.quadraticCurveTo(
        x,
        y + height,
        x,
        y + height - radius
    );

    context.lineTo(
        x,
        y + radius
    );

    context.quadraticCurveTo(
        x,
        y,
        x + radius,
        y
    );

    context.closePath();
}


/* =========================================================
   پنل
========================================================= */

function drawPanel(palette) {
    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.10)";

    roundedRect(
        ctx,
        100 * S,
        164 * S,
        880 * S,
        732 * S,
        45 * S
    );

    ctx.fill();

    ctx.fillStyle =
        "rgba(255,255,255,0.065)";

    roundedRect(
        ctx,
        100 * S,
        160 * S,
        880 * S,
        730 * S,
        45 * S
    );

    ctx.fill();

    ctx.strokeStyle =
        "rgba(255,255,255,0.045)";

    ctx.lineWidth = S;

    roundedRect(
        ctx,
        110 * S,
        170 * S,
        860 * S,
        710 * S,
        37 * S
    );

    ctx.stroke();

    ctx.strokeStyle =
        rgba(palette.panel_outline);

    ctx.lineWidth = 2 * S;

    roundedRect(
        ctx,
        100 * S,
        160 * S,
        880 * S,
        730 * S,
        45 * S
    );

    ctx.stroke();

    ctx.restore();
}


/* =========================================================
   قاب
========================================================= */

function drawFrame(palette) {
    ctx.save();

    ctx.strokeStyle =
        rgba(palette.frame);

    ctx.lineWidth =
        3 * S;

    roundedRect(
        ctx,
        40 * S,
        40 * S,
        1000 * S,
        1000 * S,
        42 * S
    );

    ctx.stroke();

    ctx.strokeStyle =
        rgba(palette.frame_inner);

    ctx.lineWidth =
        2 * S;

    roundedRect(
        ctx,
        49 * S,
        49 * S,
        982 * S,
        982 * S,
        35 * S
    );

    ctx.stroke();

    ctx.restore();
}


/* =========================================================
   تزئین
========================================================= */

function drawOrnament(palette, y) {
    const center =
        (W / 2) * S;

    const width =
        150 * S;

    ctx.save();

    ctx.strokeStyle =
        rgba(palette.ornament);

    ctx.lineWidth =
        2 * S;

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

    ctx.fillStyle =
        rgba(palette.accent);

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
   عنوان بالای کارت
========================================================= */

function drawHeader(palette) {
    const text = "کارت شعر";

    ctx.save();

    ctx.font =
        `${23 * S}px "PoetryVazirmatn", "Vazirmatn", sans-serif`;

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    const y = 78;

    ctx.fillStyle =
        "rgba(0,0,0,0.20)";

    ctx.fillText(
        text,
        (W / 2 + 1) * S,
        y * S + 2 * S
    );

    ctx.fillStyle =
        rgba(palette.accent);

    ctx.fillText(
        text,
        (W / 2) * S,
        y * S
    );

    drawOrnament(
        palette,
        126
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

    ctx.font =
        `${50 * S}px "PoetryBTitr", "BTitrBd", sans-serif`;

    const titleMetrics =
        ctx.measureText(title);

    const titleWidth =
        titleMetrics.width;

    const titleHeight =
        titleMetrics.actualBoundingBoxAscent +
        titleMetrics.actualBoundingBoxDescent;

    const titleY =
        H -
        78 -
        titleHeight / S;

    const titleX =
        W / 2 + 10;

    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";

    ctx.fillStyle =
        "rgba(0,0,0,0.24)";

    ctx.fillText(
        title,
        (titleX + 1) * S,
        titleY * S + 2 * S
    );

    ctx.fillStyle =
        rgba(palette.accent);

    ctx.fillText(
        title,
        titleX * S,
        titleY * S
    );

    ctx.font =
        `${23 * S}px "PoetryVazirmatn", "Vazirmatn", sans-serif`;

    const subWidth =
        ctx.measureText(subtitle).width;

    const subtitleX =
        titleX -
        subWidth / S -
        20;

    const subtitleY =
        titleY +
        (titleHeight / S - 23) / 2 -
        3;

    ctx.fillStyle =
        rgba(palette.subtitle);

    ctx.fillText(
        subtitle,
        subtitleX * S,
        subtitleY * S
    );

    drawOrnament(
        palette,
        titleY - 25
    );

    ctx.restore();
}


/* =========================================================
   شعر
========================================================= */

function drawPoem(
    palette,
    text
) {
    const left = 145 * S;
    const right = 935 * S;

    const top = 205 * S;
    const bottom = 845 * S;

    const maxWidth =
        right - left;

    const availableHeight =
        bottom - top;

    const fontSize =
        getFontSize(text);

    const lines =
        prepareLines(
            text,
            fontSize,
            maxWidth
        );

    ctx.save();

    ctx.font =
        getPoemFont(fontSize);

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    const items = [];
    let totalHeight = 0;

    for (const line of lines) {
        if (line === null) {
            items.push({
                line: null,
                height: 48 * S
            });

            totalHeight +=
                48 * S;

            continue;
        }

        const metrics =
            ctx.measureText(line);

        const height =
            Math.max(
                metrics.actualBoundingBoxAscent +
                metrics.actualBoundingBoxDescent,
                fontSize * S
            );

        items.push({
            line,
            height,
            metrics
        });

        totalHeight += height;
    }

    if (lines.length > 1) {
        totalHeight +=
            (lines.length - 1) *
            32 *
            S;
    }

    let y =
        top +
        (availableHeight - totalHeight) / 2;

    for (const item of items) {
        if (item.line === null) {
            y += 48 * S;
            continue;
        }

        const ascent =
            item.metrics.actualBoundingBoxAscent;

        const descent =
            item.metrics.actualBoundingBoxDescent;

        const drawY =
            y +
            item.height / 2 +
            (ascent - descent) / 2;

        ctx.fillStyle =
            rgba(palette.text);

        ctx.strokeStyle =
            rgba(palette.text);

        ctx.lineWidth =
            S;

        ctx.fillText(
            item.line,
            (left + right) / 2,
            drawY
        );

        ctx.strokeText(
            item.line,
            (left + right) / 2,
            drawY
        );

        y += item.height;
        y += 32 * S;
    }

    ctx.restore();
}


/* =========================================================
   جزئیات کناری
========================================================= */

function drawSideDetails(palette) {
    const centerY =
        205 + 640 / 2;

    ctx.save();

    ctx.strokeStyle =
        rgba(palette.side_line);

    ctx.lineWidth =
        2 * S;

    [65, 1015].forEach(x => {
        ctx.beginPath();

        ctx.moveTo(
            x * S,
            (centerY - 30) * S
        );

        ctx.lineTo(
            x * S,
            (centerY + 30) * S
        );

        ctx.stroke();
    });

    ctx.fillStyle =
        rgba(palette.side_dot);

    [65, 1015].forEach(x => {
        ctx.beginPath();

        ctx.arc(
            x * S,
            centerY * S,
            3 * S,
            0,
            Math.PI * 2
        );

        ctx.fill();
    });

    ctx.restore();
}


/* =========================================================
   رندر
========================================================= */

function render() {
    const text =
        normalizeText(
            poemInput.value
        );

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

    const palette =
        PALETTES[selectedPalette];

    ctx.clearRect(
        0,
        0,
        RW,
        RH
    );

    drawGradientBackground(
        palette
    );

    drawBackgroundImage();

    drawGlows(
        palette
    );

    drawTexture();

    drawPanel(
        palette
    );

    drawFrame(
        palette
    );

    drawHeader(
        palette
    );

    drawPoem(
        palette,
        text
    );

    drawSideDetails(
        palette
    );

    drawBrand(
        palette
    );
}


/* =========================================================
   خروجی 1080×1080
========================================================= */

function createDownloadCanvas() {
    const output =
        document.createElement("canvas");

    output.width = 1080;
    output.height = 1080;

    const outputCtx =
        output.getContext("2d");

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


/* =========================================================
   دانلود
========================================================= */

downloadBtn.addEventListener(
    "click",
    () => {
        if (!poemInput.value.trim()) {
            return;
        }

        const output =
            createDownloadCanvas();

        output.toBlob(blob => {
            if (!blob) {
                return;
            }

            const url =
                URL.createObjectURL(blob);

            const a =
                document.createElement("a");

            a.href = url;
            a.download =
                "kart-sh-er.png";

            document.body.appendChild(a);

            a.click();

            a.remove();

            setTimeout(() => {
                URL.revokeObjectURL(url);
            }, 1000);

        }, "image/png");
    }
);


/* =========================================================
   اشتراک‌گذاری
========================================================= */

shareBtn.addEventListener(
    "click",
    async () => {
        if (!poemInput.value.trim()) {
            return;
        }

        const output =
            createDownloadCanvas();

        output.toBlob(
            async blob => {
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
                    if (
                        error.name !==
                        "AbortError"
                    ) {
                        console.error(
                            "Share failed:",
                            error
                        );
                    }
                }
            },
            "image/png"
        );
    }
);


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
