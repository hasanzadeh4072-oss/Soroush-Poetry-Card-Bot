const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const paletteButtons = document.getElementById("paletteButtons");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const previewEmpty = document.getElementById("previewEmpty");

const W = 1080;
const H = 1080;

const LINE_SPACING = 32;
const BLANK_LINE_SPACING = 48;

const POEM_FONT = "Parastoo";
const TITLE_FONT = "BTitrBd";
const SUB_FONT = "Vazirmatn";

const BG_URL =
    "https://raw.githubusercontent.com/hasanzadeh4072-oss/" +
    "Soroush-Poetry-Card-Bot/be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
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
        top: [232, 218, 187],
        middle: [218, 202, 168],
        bottom: [198, 180, 142],
        glow1: [255, 252, 230, 48],
        glow2: [245, 225, 180, 24],
        glow3: [255, 255, 255, 18],
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
        top: [188, 218, 234],
        middle: [164, 202, 222],
        bottom: [139, 181, 207],
        glow1: [235, 249, 255, 50],
        glow2: [145, 205, 235, 24],
        glow3: [255, 255, 255, 18],
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
        top: [200, 216, 188],
        middle: [183, 201, 165],
        bottom: [161, 181, 140],
        glow1: [242, 249, 230, 50],
        glow2: [175, 205, 145, 24],
        glow3: [255, 255, 255, 18],
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
let currentPoem = "";

function rgba(color) {
    if (!color) {
        return "transparent";
    }

    if (color.length === 3) {
        return `rgb(${color[0]},${color[1]},${color[2]})`;
    }

    return `rgba(${color[0]},${color[1]},${color[2]},${color[3] / 255})`;
}

function rgba3(color) {
    return `rgb(${color[0]},${color[1]},${color[2]})`;
}

function isLightPalette(p) {
    return (
        p.name === "کرم" ||
        p.name === "آبی روشن" ||
        p.name === "مریم‌گلی"
    );
}

function roundedPath(x, y, w, h, radius) {
    const r = Math.min(
        radius,
        w / 2,
        h / 2
    );

    ctx.beginPath();

    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);

    ctx.quadraticCurveTo(
        x + w,
        y,
        x + w,
        y + r
    );

    ctx.lineTo(
        x + w,
        y + h - r
    );

    ctx.quadraticCurveTo(
        x + w,
        y + h,
        x + w - r,
        y + h
    );

    ctx.lineTo(
        x + r,
        y + h
    );

    ctx.quadraticCurveTo(
        x,
        y + h,
        x,
        y + h - r
    );

    ctx.lineTo(
        x,
        y + r
    );

    ctx.quadraticCurveTo(
        x,
        y,
        x + r,
        y
    );

    ctx.closePath();
}

function drawRoundedRect(
    x,
    y,
    w,
    h,
    radius,
    fillStyle = null,
    strokeStyle = null,
    lineWidth = 1
) {
    roundedPath(
        x,
        y,
        w,
        h,
        radius
    );

    if (fillStyle) {
        ctx.fillStyle = fillStyle;
        ctx.fill();
    }

    if (strokeStyle) {
        ctx.strokeStyle = strokeStyle;
        ctx.lineWidth = lineWidth;
        ctx.stroke();
    }
}

function drawBackground(p) {
    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            H
        );

    gradient.addColorStop(
        0,
        rgba3(p.top)
    );

    gradient.addColorStop(
        0.52,
        rgba3(p.middle)
    );

    gradient.addColorStop(
        1,
        rgba3(p.bottom)
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    drawGlow(
        -130,
        -90,
        455,
        370,
        rgba(p.glow1)
    );

    drawGlow(
        345,
        345,
        280,
        280,
        rgba(p.glow2)
    );

    drawGlow(
        125,
        175,
        300,
        300,
        rgba(p.glow3)
    );

    if (isLightPalette(p)) {
        ctx.fillStyle =
            "rgba(0,0,0,0.055)";

        ctx.fillRect(
            0,
            0,
            W,
            H
        );
    }

    drawTexture();
}

function drawGlow(
    x,
    y,
    w,
    h,
    color
) {
    const temp =
        document.createElement(
            "canvas"
        );

    temp.width = W;
    temp.height = H;

    const tctx =
        temp.getContext("2d");

    const match =
        color.match(
            /rgba?\((\d+),(\d+),(\d+),([\d.]+)\)/
        );

    if (!match) {
        return;
    }

    const r = match[1];
    const g = match[2];
    const b = match[3];
    const a = parseFloat(match[4]);

    const cx =
        x + w / 2;

    const cy =
        y + h / 2;

    const radius =
        Math.max(w, h) / 2;

    const gradient =
        tctx.createRadialGradient(
            cx,
            cy,
            0,
            cx,
            cy,
            radius
        );

    gradient.addColorStop(
        0,
        `rgba(${r},${g},${b},${a})`
    );

    gradient.addColorStop(
        1,
        `rgba(${r},${g},${b},0)`
    );

    tctx.fillStyle =
        gradient;

    tctx.fillRect(
        0,
        0,
        W,
        H
    );

    ctx.save();

    ctx.filter =
        "blur(55px)";

    ctx.globalCompositeOperation =
        "screen";

    ctx.drawImage(
        temp,
        0,
        0
    );

    ctx.restore();
}

function drawTexture() {
    const random =
        mulberry32(8);

    ctx.save();

    for (
        let i = 0;
        i < 18000;
        i++
    ) {
        const x =
            random() * W;

        const y =
            random() * H;

        const white =
            random() > 0.5;

        ctx.fillStyle =
            white
                ? "rgba(255,255,255,0.012)"
                : "rgba(0,0,0,0.016)";

        ctx.fillRect(
            x,
            y,
            1,
            1
        );
    }

    ctx.restore();
}

function mulberry32(seed) {
    return function () {
        let t =
            seed +=
            0x6D2B79F5;

        t = Math.imul(
            t ^ (t >>> 15),
            t | 1
        );

        t ^=
            t +
            Math.imul(
                t ^ (t >>> 7),
                t | 61
            );

        return (
            ((t ^ (t >>> 14)) >>> 0) /
            4294967296
        );
    };
}

function drawGlassPanel(p) {
    const light =
        isLightPalette(p);

    ctx.save();

    if (light) {

        /*
         * لایه سایه زیر شیشه
         * باعث می‌شود پنل از زمینه جدا دیده شود.
         */
        ctx.save();

        ctx.shadowColor =
            "rgba(0,0,0,0.22)";

        ctx.shadowBlur = 26;
        ctx.shadowOffsetY = 6;

        drawRoundedRect(
            100,
            160,
            880,
            730,
            45,
            "rgba(25,30,25,0.085)"
        );

        ctx.restore();

        /*
         * شیشه اصلی
         * عمداً کمی تیره‌تر از نسخه قبل
         * تا تفاوت آن با زمینه کاملاً مشخص باشد.
         */
        roundedPath(
            100,
            160,
            880,
            730,
            45
        );

        const glassGradient =
            ctx.createLinearGradient(
                0,
                160,
                0,
                890
            );

        glassGradient.addColorStop(
            0,
            "rgba(255,255,255,0.16)"
        );

        glassGradient.addColorStop(
            0.18,
            "rgba(255,255,255,0.10)"
        );

        glassGradient.addColorStop(
            0.50,
            "rgba(245,245,245,0.065)"
        );

        glassGradient.addColorStop(
            0.78,
            "rgba(30,35,30,0.075)"
        );

        glassGradient.addColorStop(
            1,
            "rgba(20,25,20,0.12)"
        );

        ctx.fillStyle =
            glassGradient;

        ctx.fill();

        /*
         * لایه شفاف تیره
         * برای ایجاد تفاوت محسوس با زمینه.
         */
        drawRoundedRect(
            100,
            164,
            880,
            732,
            45,
            "rgba(30,35,30,0.065)"
        );

        /*
         * کادر اصلی شیشه
         * عمداً واضح‌تر شده.
         */
        drawRoundedRect(
            100,
            160,
            880,
            730,
            45,
            null,
            rgba(p.panel_outline),
            3
        );

        /*
         * خط روشن داخلی
         */
        drawRoundedRect(
            108,
            168,
            864,
            714,
            39,
            null,
            "rgba(255,255,255,0.24)",
            1.5
        );

        /*
         * خط داخلی دوم
         */
        drawRoundedRect(
            116,
            176,
            848,
            698,
            33,
            null,
            "rgba(255,255,255,0.075)",
            1
        );

        /*
         * انعکاس نور در قسمت بالایی
         */
        ctx.save();

        roundedPath(
            118,
            178,
            844,
            300,
            32
        );

        const highlight =
            ctx.createLinearGradient(
                0,
                178,
                0,
                478
            );

        highlight.addColorStop(
            0,
            "rgba(255,255,255,0.105)"
        );

        highlight.addColorStop(
            0.40,
            "rgba(255,255,255,0.035)"
        );

        highlight.addColorStop(
            1,
            "rgba(255,255,255,0)"
        );

        ctx.fillStyle =
            highlight;

        ctx.fill();

        ctx.restore();

    } else {

        /*
         * پنل رنگ‌های تیره
         */
        drawRoundedRect(
            100,
            164,
            880,
            732,
            45,
            "rgba(0,0,0,0.176)"
        );

        drawRoundedRect(
            100,
            160,
            880,
            730,
            45,
            "rgba(255,255,255,0.094)"
        );

        drawRoundedRect(
            110,
            170,
            860,
            710,
            37,
            null,
            "rgba(255,255,255,0.047)",
            1
        );
    }

    ctx.restore();

    /*
     * کادر نهایی پنل
     * برای هر دو گروه رنگ.
     */
    drawRoundedRect(
        100,
        160,
        880,
        730,
        45,
        null,
        rgba(p.panel_outline),
        light ? 2.5 : 2
    );
}

function getTextSize(
    text,
    font
) {
    ctx.save();

    ctx.font = font;

    const metrics =
        ctx.measureText(text);

    const width =
        metrics.width;

    const ascent =
        metrics.actualBoundingBoxAscent ||
        0;

    const descent =
        metrics.actualBoundingBoxDescent ||
        0;

    const height =
        ascent + descent;

    ctx.restore();

    return {
        width,
        height,
        ascent,
        descent
    };
}

function loadFont(
    fontFamily,
    size
) {
    return `${size}px "${fontFamily}"`;
}

function drawFrame(p) {
    drawRoundedRect(
        40,
        40,
        1000,
        1000,
        42,
        null,
        rgba3(p.frame),
        3
    );

    drawRoundedRect(
        49,
        49,
        982,
        982,
        35,
        null,
        rgba3(p.frame_inner),
        2
    );
}

function drawBranding(p) {
    const titleFont =
        loadFont(
            TITLE_FONT,
            50
        );

    const subFont =
        loadFont(
            SUB_FONT,
            23
        );

    const footFont =
        loadFont(
            SUB_FONT,
            23
        );

    const title =
        "شعرکده";

    const subtitle =
        "( سروش پلاس )";

    const footer =
        "کارت شعر";

    const titleSize =
        getTextSize(
            title,
            titleFont
        );

    const subtitleSize =
        getTextSize(
            subtitle,
            subFont
        );

    const footerSize =
        getTextSize(
            footer,
            footFont
        );

    const footerY = 78;

    const footerX =
        (W - footerSize.width) / 2;

    ctx.save();

    ctx.font =
        footFont;

    ctx.fillStyle =
        "rgba(0,0,0,0.24)";

    ctx.fillText(
        footer,
        footerX + 1,
        footerY +
            footerSize.ascent +
            2
    );

    ctx.fillStyle =
        rgba3(p.accent);

    ctx.fillText(
        footer,
        footerX,
        footerY +
            footerSize.ascent
    );

    drawOrnament(
        footerY +
            footerSize.height +
            25,
        p
    );

    if (branded) {
        const titleY =
            H -
            78 -
            titleSize.height;

        const titleX =
            W / 2 + 10;

        const subtitleX =
            titleX -
            subtitleSize.width -
            20;

        const subtitleY =
            titleY +
            (
                titleSize.height -
                subtitleSize.height
            ) / 2 -
            3;

        ctx.font =
            titleFont;

        ctx.fillStyle =
            "rgba(0,0,0,0.31)";

        ctx.fillText(
            title,
            titleX + 2,
            titleY +
                titleSize.ascent +
                3
        );

        ctx.fillStyle =
            rgba3(p.accent);

        ctx.fillText(
            title,
            titleX,
            titleY +
                titleSize.ascent
        );

        ctx.font =
            subFont;

        ctx.fillStyle =
            rgba3(p.subtitle);

        ctx.fillText(
            subtitle,
            subtitleX,
            subtitleY +
                subtitleSize.ascent
        );

        drawOrnament(
            titleY - 25,
            p
        );
    } else {
        drawOrnament(
            H - 112,
            p
        );
    }

    ctx.restore();
}

function drawOrnament(
    y,
    p
) {
    const center =
        W / 2;

    const width = 150;

    ctx.save();

    ctx.strokeStyle =
        rgba3(p.ornament);

    ctx.lineWidth = 2;

    ctx.beginPath();

    ctx.moveTo(
        center - width,
        y
    );

    ctx.lineTo(
        center - 12,
        y
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(
        center + 12,
        y
    );

    ctx.lineTo(
        center + width,
        y
    );

    ctx.stroke();

    ctx.fillStyle =
        rgba3(p.accent);

    ctx.beginPath();

    ctx.moveTo(
        center,
        y - 5
    );

    ctx.lineTo(
        center + 5,
        y
    );

    ctx.lineTo(
        center,
        y + 5
    );

    ctx.lineTo(
        center - 5,
        y
    );

    ctx.closePath();

    ctx.fill();

    ctx.restore();
}

function prepareLines(
    text,
    font
) {
    const rawLines =
        text
            .replace(/…/g, "...")
            .split(/\r?\n/);

    const result = [];

    for (
        const raw of rawLines
    ) {
        if (!raw.trim()) {
            result.push(null);
            continue;
        }

        const words =
            raw
                .trim()
                .split(/\s+/);

        let current = "";

        for (
            const word of words
        ) {
            const candidate =
                current.length
                    ? `${current} ${word}`
                    : word;

            const size =
                getTextSize(
                    candidate,
                    font
                );

            if (
                size.width <= 790 ||
                !current
            ) {
                current =
                    candidate;
            } else {
                result.push(
                    current
                );

                current =
                    word;
            }
        }

        if (current) {
            result.push(
                current
            );
        }
    }

    return result;
}

function calculateTextHeight(
    lines,
    font
) {
    let total = 0;
    let lastWasNonBlank = false;

    for (
        const line of lines
    ) {
        if (line === null) {
            total +=
                BLANK_LINE_SPACING;

            lastWasNonBlank =
                false;

            continue;
        }

        const size =
            getTextSize(
                line,
                font
            );

        total +=
            size.height +
            LINE_SPACING;

        lastWasNonBlank =
            true;
    }

    if (lastWasNonBlank) {
        total -=
            LINE_SPACING;
    }

    return total;
}

function drawPoem(p) {
    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;

    const maxWidth =
        right - left;

    const availableHeight =
        bottom - top;

    let fontSize = 66;
    let lines = [];
    let font = "";

    while (
        fontSize >= 28
    ) {
        font =
            loadFont(
                POEM_FONT,
                fontSize
            );

        lines =
            prepareLines(
                currentPoem,
                font
            );

        const height =
            calculateTextHeight(
                lines,
                font
            );

        if (
            height <=
            availableHeight
        ) {
            break;
        }

        fontSize -= 2;
    }

    if (!lines.length) {
        fontSize = 46;

        font =
            loadFont(
                POEM_FONT,
                fontSize
            );

        lines = [
            "متن خالی است"
        ];
    }

    const totalHeight =
        calculateTextHeight(
            lines,
            font
        );

    let y =
        top +
        (
            availableHeight -
            totalHeight
        ) / 2;

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

    ctx.save();

    ctx.font = font;

    ctx.textAlign =
        "left";

    ctx.textBaseline =
        "alphabetic";

    for (
        const line of lines
    ) {
        if (line === null) {
            y +=
                BLANK_LINE_SPACING;

            continue;
        }

        const size =
            getTextSize(
                line,
                font
            );

        const x =
            left +
            (
                maxWidth -
                size.width
            ) / 2;

        ctx.fillStyle =
            rgba3(p.text);

        ctx.strokeStyle =
            rgba3(p.text);

        ctx.lineWidth = 1;

        ctx.strokeText(
            line,
            x,
            y + size.ascent
        );

        ctx.fillText(
            line,
            x,
            y + size.ascent
        );

        y +=
            size.height +
            LINE_SPACING;
    }

    ctx.restore();

    ctx.save();

    ctx.strokeStyle =
        rgba(p.side_line);

    ctx.lineWidth = 2;

    const centerY =
        top +
        Math.floor(
            availableHeight / 2
        );

    ctx.beginPath();

    ctx.moveTo(
        65,
        centerY - 30
    );

    ctx.lineTo(
        65,
        centerY + 30
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(
        1015,
        centerY - 30
    );

    ctx.lineTo(
        1015,
        centerY + 30
    );

    ctx.stroke();

    ctx.fillStyle =
        rgba(p.side_dot);

    ctx.beginPath();

    ctx.arc(
        65,
        centerY,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.arc(
        1015,
        centerY,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();
}

function drawCard() {
    const p =
        PALETTES[
            selectedPalette
        ];

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    drawBackground(p);

    drawGlassPanel(p);

    drawPoem(p);

    drawFrame(p);

    drawBranding(p);

    canvas.style.display =
        "block";

    previewEmpty.style.display =
        "none";

    downloadBtn.disabled =
        false;

    shareBtn.disabled =
        false;
}

function updateCard() {
    currentPoem =
        poemInput.value.trim();

    if (!currentPoem) {
        canvas.style.display =
            "none";

        previewEmpty.style.display =
            "flex";

        downloadBtn.disabled =
            true;

        shareBtn.disabled =
            true;

        return;
    }

    drawCard();
}

function createPaletteButtons() {
    paletteButtons.innerHTML =
        "";

    PALETTES.forEach(
        (palette, index) => {
            const button =
                document.createElement(
                    "button"
                );

            button.type = "button";

            button.className =
                "palette-btn";

            if (
                index ===
                selectedPalette
            ) {
                button.classList.add(
                    "active"
                );
            }

            button.style.background =
                `linear-gradient(
                    135deg,
                    rgb(
                        ${palette.top[0]},
                        ${palette.top[1]},
                        ${palette.top[2]}
                    ),
                    rgb(
                        ${palette.bottom[0]},
                        ${palette.bottom[1]},
                        ${palette.bottom[2]}
                    )
                )`;

            button.style.color =
                isLightPalette(
                    palette
                )
                    ? "#26352c"
                    : "#fff";

            button.textContent =
                palette.name;

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

                    updateCard();
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

                updateCard();
            }
        );
    });

poemInput.addEventListener(
    "input",
    updateCard
);

downloadBtn.addEventListener(
    "click",
    () => {
        if (!currentPoem) {
            return;
        }

        const link =
            document.createElement(
                "a"
            );

        link.download =
            "kart-shere.png";

        link.href =
            canvas.toDataURL(
                "image/png",
                1
            );

        link.click();
    }
);

shareBtn.addEventListener(
    "click",
    async () => {
        if (!currentPoem) {
            return;
        }

        if (
            !navigator.share ||
            !navigator.canShare
        ) {
            alert(
                "اشتراک‌گذاری در این مرورگر پشتیبانی نمی‌شود."
            );

            return;
        }

        canvas.toBlob(
            async blob => {
                if (!blob) {
                    return;
                }

                const file =
                    new File(
                        [blob],
                        "kart-shere.png",
                        {
                            type: "image/png"
                        }
                    );

                if (
                    !navigator.canShare({
                        files: [file]
                    })
                ) {
                    alert(
                        "اشتراک‌گذاری تصویر در این دستگاه پشتیبانی نمی‌شود."
                    );

                    return;
                }

                try {
                    await navigator.share({
                        files: [file],
                        title: "کارت شعر",
                        text: "کارت شعر"
                    });
                } catch (error) {
                    if (
                        error &&
                        error.name ===
                            "AbortError"
                    ) {
                        return;
                    }

                    console.error(
                        "Share error:",
                        error
                    );
                }
            },
            "image/png",
            1
        );
    }
);

createPaletteButtons();
