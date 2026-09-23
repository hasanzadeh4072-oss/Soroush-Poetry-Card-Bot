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

const FONT_URLS = {
    poem:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
        "085a674b15bd74787ca00701a8ce9780342e3fd9/" +
        "Parastoo%5Bwght%5D.ttf",

    title:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
        "085a674b15bd74787ca00701a8ce9780342e3fd9/" +
        "BTitrBd.ttf",

    sub:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
        "085a674b15bd74787ca00701a8ce9780342e3fd9/" +
        "Vazirmatn-Regular.ttf"
};

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

let selectedPalette = 0;
let branded = true;
let hasContent = false;

let backgroundImage = null;
let fontsReady = false;

function rgba(c) {
    if (c.length === 3) {
        return `rgb(${c[0]},${c[1]},${c[2]})`;
    }

    return `rgba(${c[0]},${c[1]},${c[2]},${c[3] / 255})`;
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

async function loadResources() {
    try {
        backgroundImage = await loadImage(BG_URL);
    } catch (error) {
        backgroundImage = null;
    }

    try {
        await Promise.all([
            document.fonts.load('50px "BTitrBd"'),
            document.fonts.load('23px "Vazirmatn"'),
            document.fonts.load('66px "Parastoo"')
        ]);

        fontsReady = true;
    } catch (error) {
        fontsReady = false;
    }

    drawPreview();
}

function createPaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach((palette, index) => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "palette-btn";
        button.textContent = palette.name;

        button.style.background =
            `linear-gradient(135deg, ${rgba(palette.top)}, ${rgba(palette.bottom)})`;

        button.style.color =
            palette.text[0] + palette.text[1] + palette.text[2] > 600
                ? "#fff"
                : "#1f2933";

        if (index === selectedPalette) {
            button.classList.add("active");
        }

        button.addEventListener("click", () => {
            selectedPalette = index;

            document
                .querySelectorAll(".palette-btn")
                .forEach(btn => btn.classList.remove("active"));

            button.classList.add("active");

            drawPreview();
        });

        paletteButtons.appendChild(button);
    });
}

function colorBetween(a, b, t) {
    return [
        Math.round(a[0] + (b[0] - a[0]) * t),
        Math.round(a[1] + (b[1] - a[1]) * t),
        Math.round(a[2] + (b[2] - a[2]) * t)
    ];
}

function drawGradient(targetCtx, p) {
    const gradient = targetCtx.createLinearGradient(0, 0, 0, RH);

    gradient.addColorStop(
        0,
        `rgb(${p.top[0]},${p.top[1]},${p.top[2]})`
    );

    gradient.addColorStop(
        0.52,
        `rgb(${p.middle[0]},${p.middle[1]},${p.middle[2]})`
    );

    gradient.addColorStop(
        1,
        `rgb(${p.bottom[0]},${p.bottom[1]},${p.bottom[2]})`
    );

    targetCtx.fillStyle = gradient;
    targetCtx.fillRect(0, 0, RW, RH);
}

function drawBackground(targetCtx) {
    if (!backgroundImage) {
        return;
    }

    targetCtx.save();

    targetCtx.globalAlpha = 42 / 255;
    targetCtx.filter = "brightness(48%) blur(8px)";

    const sourceSize =
        Math.min(backgroundImage.width, backgroundImage.height);

    const sx =
        (backgroundImage.width - sourceSize) / 2;

    const sy =
        (backgroundImage.height - sourceSize) / 2;

    targetCtx.drawImage(
        backgroundImage,
        sx,
        sy,
        sourceSize,
        sourceSize,
        0,
        0,
        RW,
        RH
    );

    targetCtx.restore();
}

function drawGlows(targetCtx, p) {
    const glowCanvas = document.createElement("canvas");

    glowCanvas.width = RW;
    glowCanvas.height = RH;

    const glowCtx = glowCanvas.getContext("2d");

    glowCtx.filter = "blur(220px)";

    glowCtx.fillStyle = rgba(p.glow1);

    glowCtx.beginPath();
    glowCtx.ellipse(
        -260 * S,
        -180 * S,
        (650 * S) / 2,
        (560 * S) / 2,
        0,
        0,
        Math.PI * 2
    );
    glowCtx.fill();

    glowCtx.fillStyle = rgba(p.glow2);

    glowCtx.beginPath();
    glowCtx.ellipse(
        970 * S,
        970 * S,
        (560 * S) / 2,
        (560 * S) / 2,
        0,
        0,
        Math.PI * 2
    );
    glowCtx.fill();

    glowCtx.fillStyle = rgba(p.glow3);

    glowCtx.beginPath();
    glowCtx.ellipse(
        550 * S,
        650 * S,
        (600 * S) / 2,
        (600 * S) / 2,
        0,
        0,
        Math.PI * 2
    );
    glowCtx.fill();

    targetCtx.drawImage(glowCanvas, 0, 0);
}

function drawTexture(targetCtx) {
    const textureCanvas = document.createElement("canvas");

    textureCanvas.width = RW;
    textureCanvas.height = RH;

    const textureCtx = textureCanvas.getContext("2d");
    const imageData = textureCtx.createImageData(RW, RH);

    const data = imageData.data;

    let seed = 8;

    function random() {
        seed ^= seed << 13;
        seed ^= seed >>> 17;
        seed ^= seed << 5;

        return ((seed >>> 0) / 4294967296);
    }

    const count = 56000;

    for (let i = 0; i < count; i++) {
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

    textureCtx.putImageData(imageData, 0, 0);

    targetCtx.drawImage(textureCanvas, 0, 0);
}

function roundedRect(targetCtx, x1, y1, x2, y2, radius) {
    targetCtx.beginPath();

    targetCtx.moveTo(x1 + radius, y1);
    targetCtx.lineTo(x2 - radius, y1);

    targetCtx.quadraticCurveTo(
        x2,
        y1,
        x2,
        y1 + radius
    );

    targetCtx.lineTo(x2, y2 - radius);

    targetCtx.quadraticCurveTo(
        x2,
        y2,
        x2 - radius,
        y2
    );

    targetCtx.lineTo(x1 + radius, y2);

    targetCtx.quadraticCurveTo(
        x1,
        y2,
        x1,
        y2 - radius
    );

    targetCtx.lineTo(x1, y1 + radius);

    targetCtx.quadraticCurveTo(
        x1,
        y1,
        x1 + radius,
        y1
    );

    targetCtx.closePath();
}

function drawPanel(targetCtx, p) {
    targetCtx.save();

    roundedRect(
        targetCtx,
        100 * S,
        164 * S,
        980 * S,
        896 * S,
        45 * S
    );

    targetCtx.fillStyle = "rgba(0,0,0,0.1764705882)";
    targetCtx.fill();

    roundedRect(
        targetCtx,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    targetCtx.fillStyle = "rgba(255,255,255,0.0941176471)";
    targetCtx.fill();

    roundedRect(
        targetCtx,
        110 * S,
        170 * S,
        970 * S,
        880 * S,
        37 * S
    );

    targetCtx.strokeStyle =
        "rgba(255,255,255,0.0470588235)";

    targetCtx.lineWidth = 1 * S;
    targetCtx.stroke();

    targetCtx.restore();

    targetCtx.save();

    roundedRect(
        targetCtx,
        100 * S,
        160 * S,
        980 * S,
        890 * S,
        45 * S
    );

    targetCtx.strokeStyle = rgba(p.panel_outline);
    targetCtx.lineWidth = 2 * S;
    targetCtx.stroke();

    targetCtx.restore();
}

function drawFrame(targetCtx, p) {
    targetCtx.save();

    roundedRect(
        targetCtx,
        40 * S,
        40 * S,
        1040 * S,
        1040 * S,
        42 * S
    );

    targetCtx.strokeStyle = rgba(p.frame);
    targetCtx.lineWidth = 3 * S;
    targetCtx.stroke();

    roundedRect(
        targetCtx,
        49 * S,
        49 * S,
        1031 * S,
        1031 * S,
        35 * S
    );

    targetCtx.strokeStyle = rgba(p.frame_inner);
    targetCtx.lineWidth = 2 * S;
    targetCtx.stroke();

    targetCtx.restore();
}

function drawOrnament(targetCtx, p, y) {
    const center = W / 2;
    const width = 150;

    targetCtx.save();

    targetCtx.strokeStyle = rgba(p.ornament);
    targetCtx.lineWidth = 2;

    targetCtx.beginPath();
    targetCtx.moveTo(
        (center - width) * S,
        y * S
    );
    targetCtx.lineTo(
        (center - 12) * S,
        y * S
    );
    targetCtx.stroke();

    targetCtx.beginPath();
    targetCtx.moveTo(
        (center + 12) * S,
        y * S
    );
    targetCtx.lineTo(
        (center + width) * S,
        y * S
    );
    targetCtx.stroke();

    targetCtx.fillStyle = rgba(p.accent);

    targetCtx.beginPath();

    targetCtx.moveTo(center * S, (y - 5) * S);
    targetCtx.lineTo((center + 5) * S, y * S);
    targetCtx.lineTo(center * S, (y + 5) * S);
    targetCtx.lineTo((center - 5) * S, y * S);

    targetCtx.closePath();
    targetCtx.fill();

    targetCtx.restore();
}

function getFont(size, family, weight = "400") {
    return `${weight} ${size * S}px "${family}"`;
}

function normalizeText(text) {
    return text
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .replace(/…/g, "...");
}

function prepareLines(targetCtx, text, fontSize) {
    const left = 145;
    const right = 935;
    const maxWidth = right - left;

    targetCtx.font = getFont(
        fontSize,
        "Parastoo",
        "600"
    );

    const sourceLines = normalizeText(text).split("\n");
    const lines = [];

    for (const sourceLine of sourceLines) {
        const trimmed = sourceLine.trim();

        if (!trimmed) {
            lines.push(null);
            continue;
        }

        const words = trimmed.split(/\s+/);
        let current = "";

        for (const word of words) {
            const test =
                current.length === 0
                    ? word
                    : current + " " + word;

            const width =
                targetCtx.measureText(test).width / S;

            if (
                width <= maxWidth ||
                current.length === 0
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

function getLineMetrics(targetCtx, fontSize) {
    targetCtx.font = getFont(
        fontSize,
        "Parastoo",
        "600"
    );

    const metrics =
        targetCtx.measureText("آ");

    const ascent =
        (metrics.actualBoundingBoxAscent || fontSize * 0.8);

    const descent =
        (metrics.actualBoundingBoxDescent || fontSize * 0.25);

    return {
        ascent: ascent / S,
        descent: descent / S,
        height: (ascent + descent) / S
    };
}

function getPoemLayout(targetCtx, text) {
    const maxWidth = 790;
    const availableHeight = 640;

    let fontSize = 66;
    let lines = [];
    let metrics;
    let totalHeight;

    while (fontSize >= 28) {
        lines = prepareLines(
            targetCtx,
            text,
            fontSize
        );

        metrics = getLineMetrics(
            targetCtx,
            fontSize
        );

        totalHeight = 0;

        for (let i = 0; i < lines.length; i++) {
            if (lines[i] === null) {
                totalHeight += BLANK_LINE_SPACING;
            } else {
                totalHeight += metrics.height;

                if (i < lines.length - 1) {
                    totalHeight += LINE_SPACING;
                }
            }
        }

        if (
            totalHeight <= availableHeight &&
            lines.length > 0
        ) {
            break;
        }

        fontSize -= 2;
    }

    return {
        fontSize,
        lines,
        metrics,
        totalHeight
    };
}

function drawPoem(targetCtx, p, text) {
    const layout = getPoemLayout(
        targetCtx,
        text
    );

    const centerX = W / 2;
    const top = 205;
    const bottom = 845;

    let y =
        top +
        (bottom - top - layout.totalHeight) / 2;

    targetCtx.save();

    targetCtx.font = getFont(
        layout.fontSize,
        "Parastoo",
        "600"
    );

    targetCtx.textAlign = "center";
    targetCtx.textBaseline = "alphabetic";

    for (let i = 0; i < layout.lines.length; i++) {
        const line = layout.lines[i];

        if (line === null) {
            y += BLANK_LINE_SPACING;
            continue;
        }

        const ascent =
            layout.metrics.ascent;

        const baseline =
            y + ascent;

        targetCtx.fillStyle = rgba(p.text);
        targetCtx.strokeStyle = rgba(p.text);
        targetCtx.lineWidth = 1 * S;

        targetCtx.fillText(
            line,
            centerX * S,
            baseline * S
        );

        targetCtx.strokeText(
            line,
            centerX * S,
            baseline * S
        );

        y += layout.metrics.height;

        if (i < layout.lines.length - 1) {
            y += LINE_SPACING;
        }
    }

    targetCtx.restore();

    drawSideDecoration(
        targetCtx,
        p,
        top,
        bottom
    );
}

function drawSideDecoration(
    targetCtx,
    p,
    top,
    bottom
) {
    const centerY =
        (top + bottom) / 2;

    targetCtx.save();

    targetCtx.strokeStyle =
        rgba(p.side_line);

    targetCtx.fillStyle =
        rgba(p.side_dot);

    targetCtx.lineWidth = 2;

    targetCtx.beginPath();

    targetCtx.moveTo(
        65 * S,
        (centerY - 30) * S
    );

    targetCtx.lineTo(
        65 * S,
        (centerY + 30) * S
    );

    targetCtx.stroke();

    targetCtx.beginPath();

    targetCtx.moveTo(
        1015 * S,
        (centerY - 30) * S
    );

    targetCtx.lineTo(
        1015 * S,
        (centerY + 30) * S
    );

    targetCtx.stroke();

    targetCtx.beginPath();
    targetCtx.arc(
        65 * S,
        centerY * S,
        3 * S,
        0,
        Math.PI * 2
    );
    targetCtx.fill();

    targetCtx.beginPath();
    targetCtx.arc(
        1015 * S,
        centerY * S,
        3 * S,
        0,
        Math.PI * 2
    );
    targetCtx.fill();

    targetCtx.restore();
}

function drawBranding(targetCtx, p) {
    const footerText = "کارت شعر";

    targetCtx.save();

    targetCtx.font =
        getFont(23, "Vazirmatn", "400");

    targetCtx.textAlign = "center";
    targetCtx.textBaseline = "alphabetic";

    const footerMetrics =
        targetCtx.measureText(footerText);

    const footerHeight =
        (footerMetrics.actualBoundingBoxAscent || 23) +
        (footerMetrics.actualBoundingBoxDescent || 6);

    const footerY = 78;

    targetCtx.fillStyle =
        rgba(p.accent);

    targetCtx.shadowColor =
        "rgba(0,0,0,0.2352941176)";

    targetCtx.shadowOffsetX = 1;
    targetCtx.shadowOffsetY = 2;
    targetCtx.shadowBlur = 0;

    targetCtx.fillText(
        footerText,
        (W / 2) * S,
        footerY * S
    );

    targetCtx.restore();

    drawOrnament(
        targetCtx,
        p,
        footerY + footerHeight + 25
    );

    if (!branded) {
        drawOrnament(
            targetCtx,
            p,
            H - 112
        );

        return;
    }

    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";

    targetCtx.save();

    targetCtx.font =
        getFont(50, "BTitrBd", "700");

    const titleMetrics =
        targetCtx.measureText(title);

    const th =
        (titleMetrics.actualBoundingBoxAscent || 50) +
        (titleMetrics.actualBoundingBoxDescent || 10);

    targetCtx.font =
        getFont(23, "Vazirmatn", "400");

    const subtitleMetrics =
        targetCtx.measureText(subtitle);

    const sw =
        subtitleMetrics.width / S;

    const sh =
        (subtitleMetrics.actualBoundingBoxAscent || 23) +
        (subtitleMetrics.actualBoundingBoxDescent || 6);

    const titleY =
        H - 78 - th;

    const titleX =
        W / 2 + 10;

    const subtitleX =
        titleX - sw - 20;

    const subtitleY =
        titleY +
        (th - sh) / 2 -
        3;

    targetCtx.textBaseline = "alphabetic";

    targetCtx.font =
        getFont(50, "BTitrBd", "700");

    targetCtx.textAlign = "center";

    targetCtx.fillStyle =
        rgba(p.accent);

    targetCtx.shadowColor =
        "rgba(0,0,0,0.3137254902)";

    targetCtx.shadowOffsetX = 1;
    targetCtx.shadowOffsetY = 2;
    targetCtx.shadowBlur = 0;

    targetCtx.fillText(
        title,
        titleX * S,
        (titleY + th) * S
    );

    targetCtx.shadowColor = "transparent";

    targetCtx.font =
        getFont(23, "Vazirmatn", "400");

    targetCtx.fillStyle =
        rgba(p.subtitle);

    targetCtx.textAlign = "left";

    targetCtx.fillText(
        subtitle,
        subtitleX * S,
        (subtitleY + sh) * S
    );

    targetCtx.restore();

    drawOrnament(
        targetCtx,
        p,
        titleY - 25
    );
}

function renderCard(text) {
    const p = PALETTES[selectedPalette];

    const highCanvas =
        document.createElement("canvas");

    highCanvas.width = RW;
    highCanvas.height = RH;

    const highCtx =
        highCanvas.getContext("2d");

    highCtx.imageSmoothingEnabled = true;
    highCtx.imageSmoothingQuality = "high";

    /*
     * ترتیب همان منطق بات:
     * gradient → background → glows → texture
     * → panel → frame → poem → branding
     */

    drawGradient(highCtx, p);
    drawBackground(highCtx);
    drawGlows(highCtx, p);
    drawTexture(highCtx);

    drawPanel(highCtx, p);
    drawFrame(highCtx, p);

    drawPoem(highCtx, p, text);
    drawBranding(highCtx, p);

    /*
     * خروجی نهایی بات:
     * 2160×2160 → 1080×1080
     */
    canvas.width = W;
    canvas.height = H;

    ctx.clearRect(0, 0, W, H);

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";

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

function drawPreview() {
    const text = poemInput.value.trim();

    if (!text) {
        hasContent = false;

        canvas.style.display = "none";
        previewEmpty.style.display = "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        return;
    }

    hasContent = true;

    previewEmpty.style.display = "none";
    canvas.style.display = "block";

    downloadBtn.disabled = false;
    shareBtn.disabled = false;

    renderCard(text);
}

document
    .querySelectorAll(".option-btn")
    .forEach(button => {
        button.addEventListener("click", () => {
            document
                .querySelectorAll(".option-btn")
                .forEach(btn =>
                    btn.classList.remove("active")
                );

            button.classList.add("active");

            branded =
                button.dataset.branded === "true";

            drawPreview();
        });
    });

poemInput.addEventListener(
    "input",
    drawPreview
);

downloadBtn.addEventListener(
    "click",
    () => {
        if (!hasContent) return;

        const link =
            document.createElement("a");

        link.download = "kart-sh3r.png";
        link.href =
            canvas.toDataURL("image/png");

        link.click();
    }
);

shareBtn.addEventListener(
    "click",
    async () => {
        if (!hasContent) return;

        try {
            const blob =
                await new Promise(resolve =>
                    canvas.toBlob(
                        resolve,
                        "image/png"
                    )
                );

            if (!blob) return;

            const file =
                new File(
                    [blob],
                    "kart-sh3r.png",
                    { type: "image/png" }
                );

            if (
                navigator.share &&
                navigator.canShare &&
                navigator.canShare({ files: [file] })
            ) {
                await navigator.share({
                    files: [file],
                    title: "کارت شعر"
                });
            } else {
                const url =
                    URL.createObjectURL(blob);

                const link =
                    document.createElement("a");

                link.href = url;
                link.download = "kart-sh3r.png";

                link.click();

                setTimeout(
                    () => URL.revokeObjectURL(url),
                    1000
                );
            }
        } catch (error) {
            if (error.name !== "AbortError") {
                console.error(error);
            }
        }
    }
);

createPaletteButtons();
loadResources();
