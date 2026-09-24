"use strict";

/*
=========================================================
کارت شعر - نسخه Web App

این فایل، منطق رسم کارت را از کد اصلی بات
به Canvas منتقل می‌کند.

ابعاد داخلی Canvas:
2160 × 2160

خروجی نهایی:
1080 × 1080

این همان منطق S = 2 در بات است.
=========================================================
*/


/* =====================================================
   تنظیمات اصلی بات
===================================================== */

const W = 1080;
const H = 1080;

const S = 2;

const RW = W * S;
const RH = H * S;

const LINE_SPACING = 32;
const BLANK_LINE_SPACING = 48;


/* =====================================================
   فایل‌ها و فونت‌های همان پروژه
===================================================== */

const POEM_FONT_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/" +
    "Parastoo%5Bwght%5D.ttf";

const TITLE_FONT_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/" +
    "BTitrBd.ttf";

const SUB_FONT_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/" +
    "Vazirmatn-Regular.ttf";


const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";


/* =====================================================
   پالت‌ها - عین کد بات
===================================================== */

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


/* =====================================================
   Canvas
===================================================== */

const canvas =
    document.getElementById("poetryCanvas");

const ctx =
    canvas.getContext("2d", {
        alpha: true
    });


canvas.width = RW;
canvas.height = RH;


/* =====================================================
   وضعیت
===================================================== */

let currentPalette = 0;
let branded = true;

let backgroundImage = null;
let backgroundReady = false;

let fontsReady = false;


/* =====================================================
   ابزار تبدیل رنگ
===================================================== */

function colorRGB(c) {
    return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
}


function colorRGBA(c) {

    return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${c[3] / 255})`;
}


/* =====================================================
   تبدیل مختصات 1080 به Canvas 2160
===================================================== */

function X(value) {
    return value * S;
}


/* =====================================================
   Rounded Rectangle
===================================================== */

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


/* =====================================================
   بارگذاری فونت‌ها
===================================================== */

async function loadFonts() {

    try {

        const poemFont = new FontFace(
            "PoemFont",
            `url("${POEM_FONT_URL}")`
        );

        const titleFont = new FontFace(
            "TitleFont",
            `url("${TITLE_FONT_URL}")`
        );

        const subFont = new FontFace(
            "SubFont",
            `url("${SUB_FONT_URL}")`
        );


        await Promise.all([
            poemFont.load(),
            titleFont.load(),
            subFont.load()
        ]);


        document.fonts.add(poemFont);
        document.fonts.add(titleFont);
        document.fonts.add(subFont);


        fontsReady = true;

    } catch (error) {

        console.error(
            "Font loading error:",
            error
        );

        fontsReady = false;
    }
}


/* =====================================================
   بارگذاری Background همان BG_URL بات
===================================================== */

function loadBackground() {

    return new Promise(resolve => {

        backgroundImage = new Image();

        backgroundImage.crossOrigin = "anonymous";

        backgroundImage.onload = () => {

            backgroundReady = true;

            resolve();
        };

        backgroundImage.onerror = error => {

            console.error(
                "Background loading error:",
                error
            );

            backgroundReady = false;

            resolve();
        };

        backgroundImage.src = BG_URL;
    });
}


/* =====================================================
   ساخت Background دقیق
===================================================== */

function createBackground(p) {

    /*
        در بات:

        image = RGB(1, RH)

        gradient:
        top -> middle در 52%
        middle -> bottom در 48%
    */


    const background =
        document.createElement("canvas");

    background.width = RW;
    background.height = RH;

    const bgCtx =
        background.getContext("2d");


    const gradient =
        bgCtx.createLinearGradient(
            0,
            0,
            0,
            RH
        );


    gradient.addColorStop(
        0,
        colorRGB(p.top)
    );

    gradient.addColorStop(
        0.52,
        colorRGB(p.middle)
    );

    gradient.addColorStop(
        1,
        colorRGB(p.bottom)
    );


    bgCtx.fillStyle = gradient;

    bgCtx.fillRect(
        0,
        0,
        RW,
        RH
    );


    /* -----------------------------------------------
       BG همان SVG بات
    ------------------------------------------------ */

    if (backgroundReady) {

        const svgCanvas =
            document.createElement("canvas");

        /*
            CairoSVG در بات:
            output_width = 4320
        */

        const renderWidth = 4320;

        const ratio =
            backgroundImage.naturalHeight /
            backgroundImage.naturalWidth;

        const renderHeight =
            Math.round(
                renderWidth * ratio
            );


        svgCanvas.width = renderWidth;
        svgCanvas.height = renderHeight;


        const svgCtx =
            svgCanvas.getContext("2d");


        svgCtx.drawImage(
            backgroundImage,
            0,
            0,
            renderWidth,
            renderHeight
        );


        /*
            همان Brightness(.48)
            و سپس GaussianBlur(8px)
        */

        const bgEffect =
            document.createElement("canvas");

        bgEffect.width = renderWidth;
        bgEffect.height = renderHeight;

        const effectCtx =
            bgEffect.getContext("2d");


        effectCtx.filter =
            "brightness(48%) blur(8px)";


        effectCtx.drawImage(
            svgCanvas,
            0,
            0
        );


        /*
            crop همان منطق PIL
        */

        const sourceRatio =
            renderWidth / renderHeight;

        const targetRatio =
            RW / RH;


        let sx = 0;
        let sy = 0;
        let sw = renderWidth;
        let sh = renderHeight;


        if (sourceRatio > targetRatio) {

            sh = renderHeight;

            sw = Math.round(
                renderHeight * targetRatio
            );

            sx =
                Math.floor(
                    (renderWidth - sw) / 2
                );

        } else {

            sw = renderWidth;

            sh = Math.round(
                renderWidth / targetRatio
            );

            sy =
                Math.floor(
                    (renderHeight - sh) / 2
                );
        }


        const bgFinal =
            document.createElement("canvas");

        bgFinal.width = RW;
        bgFinal.height = RH;


        const finalCtx =
            bgFinal.getContext("2d");


        finalCtx.drawImage(
            bgEffect,
            sx,
            sy,
            sw,
            sh,
            0,
            0,
            RW,
            RH
        );


        /*
            image.putalpha(42)
        */

        bgCtx.save();

        bgCtx.globalAlpha =
            42 / 255;

        bgCtx.drawImage(
            bgFinal,
            0,
            0,
            RW,
            RH
        );

        bgCtx.restore();
    }


    /* -----------------------------------------------
       Glow ها دقیقاً مطابق بات
    ------------------------------------------------ */

    const glow =
        document.createElement("canvas");

    glow.width = RW;
    glow.height = RH;

    const glowCtx =
        glow.getContext("2d");


    glowCtx.fillStyle =
        colorRGBA(p.glow1);

    glowCtx.beginPath();

    glowCtx.ellipse(
        X(-260),
        X(-180),
        X(455),
        X(370),
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();


    glowCtx.fillStyle =
        colorRGBA(p.glow2);

    glowCtx.beginPath();

    glowCtx.ellipse(
        X(970),
        X(970),
        X(280),
        X(280),
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();


    glowCtx.fillStyle =
        colorRGBA(p.glow3);

    glowCtx.beginPath();

    glowCtx.ellipse(
        X(550),
        X(650),
        X(300),
        X(300),
        0,
        0,
        Math.PI * 2
    );

    glowCtx.fill();


    /*
        GaussianBlur(110 * S)
    */

    const blurredGlow =
        document.createElement("canvas");

    blurredGlow.width = RW;
    blurredGlow.height = RH;

    const blurCtx =
        blurredGlow.getContext("2d");


    blurCtx.filter =
        `blur(${110 * S}px)`;


    blurCtx.drawImage(
        glow,
        0,
        0
    );


    bgCtx.drawImage(
        blurredGlow,
        0,
        0
    );


    /* -----------------------------------------------
       Texture همان منطق بات
    ------------------------------------------------ */

    const texture =
        document.createElement("canvas");

    texture.width = RW;
    texture.height = RH;

    const textureCtx =
        texture.getContext("2d");


    /*
        random seed = 8
        برای رفتار پایدار از یک PRNG ساده استفاده می‌کنیم.
    */

    let seed = 8;

    function random() {

        seed =
            (seed * 1664525 + 1013904223)
            >>> 0;

        return seed / 4294967296;
    }


    for (let i = 0; i < 56000; i++) {

        const px =
            Math.floor(
                random() * RW
            );

        const py =
            Math.floor(
                random() * RH
            );


        if (random() < 0.5) {

            textureCtx.fillStyle =
                "rgba(255,255,255,3/255)";

        } else {

            textureCtx.fillStyle =
                "rgba(0,0,0,4/255)";
        }


        textureCtx.fillRect(
            px,
            py,
            1,
            1
        );
    }


    bgCtx.drawImage(
        texture,
        0,
        0
    );


    return background;
}


/* =====================================================
   پنل دقیق بات
===================================================== */

function drawPanel(p) {

    /*
        PANEL:

        (100,164,980,896)
        black alpha 45

        (100,160,980,890)
        white alpha 24

        (110,170,970,880)
        white outline alpha 12

        GaussianBlur(.35*S)
    */


    const panel =
        document.createElement("canvas");

    panel.width = RW;
    panel.height = RH;


    const panelCtx =
        panel.getContext("2d");


    panelCtx.fillStyle =
        "rgba(0,0,0,45/255)";

    roundedRect(
        panelCtx,
        X(100),
        X(164),
        X(880),
        X(732),
        X(45)
    );

    panelCtx.fill();


    panelCtx.fillStyle =
        "rgba(255,255,255,24/255)";

    roundedRect(
        panelCtx,
        X(100),
        X(160),
        X(880),
        X(730),
        X(45)
    );

    panelCtx.fill();


    panelCtx.strokeStyle =
        "rgba(255,255,255,12/255)";

    panelCtx.lineWidth = X(1);

    roundedRect(
        panelCtx,
        X(110),
        X(170),
        X(860),
        X(710),
        X(37)
    );

    panelCtx.stroke();


    /*
        blur .35*S = .7
    */

    const blurredPanel =
        document.createElement("canvas");

    blurredPanel.width = RW;
    blurredPanel.height = RH;

    const blurCtx =
        blurredPanel.getContext("2d");


    blurCtx.filter = "blur(0.7px)";

    blurCtx.drawImage(
        panel,
        0,
        0
    );


    ctx.drawImage(
        blurredPanel,
        0,
        0
    );
}


/* =====================================================
   قاب دقیق بات
===================================================== */

function drawFrame(p) {

    ctx.strokeStyle =
        colorRGB(p.frame);

    ctx.lineWidth =
        X(3);

    roundedRect(
        ctx,
        X(40),
        X(40),
        X(1000),
        X(1000),
        X(42)
    );

    ctx.stroke();


    ctx.strokeStyle =
        colorRGB(p.frame_inner);

    ctx.lineWidth =
        X(2);

    roundedRect(
        ctx,
        X(49),
        X(49),
        X(982),
        X(982),
        X(35)
    );

    ctx.stroke();
}


/* =====================================================
   draw_ornament عین کد بات
===================================================== */

function drawOrnament(p, y) {

    const center =
        W / 2;

    const width = 150;


    ctx.strokeStyle =
        colorRGB(p.ornament);

    ctx.lineWidth =
        X(2);


    ctx.beginPath();

    ctx.moveTo(
        X(center - width),
        X(y)
    );

    ctx.lineTo(
        X(center - 12),
        X(y)
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        X(center + 12),
        X(y)
    );

    ctx.lineTo(
        X(center + width),
        X(y)
    );

    ctx.stroke();


    ctx.fillStyle =
        colorRGB(p.accent);

    ctx.beginPath();

    ctx.moveTo(
        X(center),
        X(y - 5)
    );

    ctx.lineTo(
        X(center + 5),
        X(y)
    );

    ctx.lineTo(
        X(center),
        X(y + 5)
    );

    ctx.lineTo(
        X(center - 5),
        X(y)
    );

    ctx.closePath();

    ctx.fill();
}


/* =====================================================
   اندازه متن
===================================================== */

function textSize(
    text,
    font
) {

    ctx.font = font;

    const metrics =
        ctx.measureText(text);

    const ascent =
        metrics.actualBoundingBoxAscent || 0;

    const descent =
        metrics.actualBoundingBoxDescent || 0;

    return {
        width: metrics.width,
        height: ascent + descent
    };
}


/* =====================================================
   Branding عین create_card بات
===================================================== */

function drawBranding(p) {

    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";
    const footer = "کارت شعر";


    const titleFont =
        `50px TitleFont`;

    const subtitleFont =
        `23px SubFont`;

    const footerFont =
        `23px SubFont`;


    const titleSize =
        textSize(
            title,
            titleFont
        );


    const subtitleSize =
        textSize(
            subtitle,
            subtitleFont
        );


    const footerSize =
        textSize(
            footer,
            footerFont
        );


    const center =
        W / 2;


    const footer_y = 78;


    const footer_x =
        (W - footerSize.width) / 2;


    /*
        بات:

        title_y = H - 78 - th
        title_x = center + 10
    */

    const title_y =
        H - 78 - titleSize.height;

    const title_x =
        center + 10;


    const subtitle_x =
        title_x
        - subtitleSize.width
        - 20;


    const subtitle_y =
        title_y
        + (titleSize.height - subtitleSize.height) / 2
        - 3;


    /*
        footer shadow
    */

    ctx.font =
        footerFont;

    ctx.textAlign =
        "left";

    ctx.textBaseline =
        "alphabetic";


    ctx.fillStyle =
        "rgba(0,0,0,60/255)";

    ctx.fillText(
        footer,
        X(footer_x + 1),
        X(footer_y + 2)
    );


    ctx.fillStyle =
        colorRGB(p.accent);

    ctx.fillText(
        footer,
        X(footer_x),
        X(footer_y)
    );


    /*
        ornament بعد از footer
    */

    drawOrnament(
        p,
        footer_y
        + footerSize.height
        + 25
    );


    if (branded) {

        /*
            title shadow
        */

        ctx.font =
            titleFont;

        ctx.fillStyle =
            "rgba(0,0,0,80/255)";

        ctx.fillText(
            title,
            X(title_x + 2),
            X(title_y + 3)
        );


        /*
            title
        */

        ctx.fillStyle =
            colorRGB(p.accent);

        ctx.fillText(
            title,
            X(title_x),
            X(title_y)
        );


        /*
            subtitle
        */

        ctx.font =
            subtitleFont;

        ctx.fillStyle =
            colorRGB(p.subtitle);

        ctx.fillText(
            subtitle,
            X(subtitle_x),
            X(subtitle_y)
        );


        /*
            ornament بالای عنوان پایین
        */

        drawOrnament(
            p,
            title_y - 25
        );

    } else {

        /*
            کارت عمومی بدون امضا
        */

        drawOrnament(
            p,
            H - 112
        );
    }
}


/* =====================================================
   اندازه‌گیری متن و wrap
===================================================== */

function measureTextBox(
    text,
    font
) {

    ctx.font = font;

    const m =
        ctx.measureText(text);

    const left =
        m.actualBoundingBoxLeft || 0;

    const right =
        m.actualBoundingBoxRight || m.width;

    const ascent =
        m.actualBoundingBoxAscent || 0;

    const descent =
        m.actualBoundingBoxDescent || 0;


    return {
        width: right + left,
        height: ascent + descent,
        left,
        right,
        ascent,
        descent
    };
}


function wrapText(
    text,
    font,
    maxWidth
) {

    const words =
        text.split(/\s+/);

    if (!words.length) {
        return [];
    }


    const lines = [];

    let current =
        words[0];


    for (
        let i = 1;
        i < words.length;
        i++
    ) {

        const candidate =
            current
            + " "
            + words[i];


        const box =
            measureTextBox(
                candidate,
                font
            );


        if (box.width <= maxWidth) {

            current =
                candidate;

        } else {

            lines.push(
                current
            );

            current =
                words[i];
        }
    }


    lines.push(current);

    return lines;
}


/* =====================================================
   prepare_lines عین منطق بات
===================================================== */

function prepareLines(
    text,
    font,
    maxWidth
) {

    const result = [];


    const normalized =
        text.replace(
            /…/g,
            "..."
        );


    const rawLines =
        normalized.split(/\r?\n/);


    for (const raw of rawLines) {

        if (!raw.trim()) {

            result.push(null);

            continue;
        }


        const wrapped =
            wrapText(
                raw.trim(),
                font,
                maxWidth
            );


        result.push(
            ...wrapped
        );
    }


    return result;
}


/* =====================================================
   calculate_height عین منطق بات
===================================================== */

function calculateHeight(
    lines,
    font
) {

    let total = 0;


    for (
        let i = 0;
        i < lines.length;
        i++
    ) {

        const line =
            lines[i];


        if (line === null) {

            total +=
                X(BLANK_LINE_SPACING);

            continue;
        }


        const box =
            measureTextBox(
                line,
                font
            );


        total +=
            box.height
            + X(LINE_SPACING);
    }


    if (
        lines.length &&
        lines[lines.length - 1] !== null
    ) {

        total -=
            X(LINE_SPACING);
    }


    return total;
}


/* =====================================================
   شعر - منطق همان create_card بات
===================================================== */

function drawPoem(
    p,
    text
) {

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

    let poemFont;


    while (fontSize >= 28) {

        poemFont =
            `${fontSize * S}px PoemFont`;


        lines =
            prepareLines(
                text,
                poemFont,
                maxWidth * S
            );


        const height =
            calculateHeight(
                lines,
                poemFont
            );


        if (
            height <=
            availableHeight * S
        ) {

            break;
        }


        fontSize -= 2;
    }


    if (!lines.length) {

        poemFont =
            `46px PoemFont`;

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

        const line =
            lines[index];


        if (line === null) {

            items.push({
                line: null,
                height:
                    BLANK_LINE_SPACING * S
            });

            totalHeight +=
                BLANK_LINE_SPACING * S;

            continue;
        }


        const box =
            measureTextBox(
                line,
                poemFont
            );


        items.push({
            line,
            box,
            height: box.height
        });


        totalHeight +=
            box.height;


        if (
            index !==
            lines.length - 1
        ) {

            totalHeight +=
                LINE_SPACING * S;
        }
    }


    let y =
        top * S
        + (
            availableHeight * S
            - totalHeight
        ) / 2;


    y =
        Math.max(
            top * S,
            y
        );


    if (
        y + totalHeight >
        bottom * S
    ) {

        y =
            bottom * S
            - totalHeight;
    }


    ctx.textAlign =
        "left";

    ctx.textBaseline =
        "alphabetic";

    ctx.font =
        poemFont;

    ctx.fillStyle =
        colorRGB(p.text);

    ctx.strokeStyle =
        colorRGB(p.text);

    ctx.lineWidth =
        X(1);


    for (const item of items) {

        if (item.line === null) {

            y +=
                BLANK_LINE_SPACING * S;

            continue;
        }


        const line =
            item.line;

        const box =
            item.box;


        /*
            در PIL:

            x = left + (
                max_width - width
            ) / 2

            d.text(
                (x, y - bbox[1]),
                ...
            )
        */

        const x =
            left * S
            + (
                maxWidth * S
                - box.width
            ) / 2;


        /*
            Canvas از baseline استفاده می‌کند.
            برای نزدیک‌ترین معادل PIL:
            baseline = y + ascent
        */

        const baseline =
            y + box.ascent;


        ctx.strokeText(
            line,
            x,
            baseline
        );


        ctx.fillText(
            line,
            x,
            baseline
        );


        y +=
            item.height
            + LINE_SPACING * S;
    }
}


/* =====================================================
   المان‌های کناری عین بات
===================================================== */

function drawSideElements(p) {

    const centerY =
        H / 2;


    for (
        const x of [65, 1015]
    ) {

        ctx.strokeStyle =
            colorRGBA(
                p.side_line
            );

        ctx.lineWidth =
            X(2);


        ctx.beginPath();

        ctx.moveTo(
            X(x),
            X(centerY - 30)
        );

        ctx.lineTo(
            X(x),
            X(centerY + 30)
        );

        ctx.stroke();


        ctx.fillStyle =
            colorRGBA(
                p.side_dot
            );


        ctx.beginPath();

        ctx.arc(
            X(x),
            X(centerY),
            X(3),
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}


/* =====================================================
   ساخت کارت
   ترتیب دقیق create_card بات
===================================================== */

function createCard(
    text
) {

    const p =
        PALETTES[
            currentPalette
        ];


    /*
        Background
    */

    const background =
        createBackground(p);


    ctx.clearRect(
        0,
        0,
        RW,
        RH
    );


    ctx.drawImage(
        background,
        0,
        0
    );


    /*
        Frame
    */

    drawFrame(p);


    /*
        Branding / footer / ornament
    */

    drawBranding(p);


    /*
        Panel
    */

    drawPanel(p);


    /*
        Poem
    */

    drawPoem(
        p,
        text
    );


    /*
        Side decoration
    */

    drawSideElements(p);
}


/* =====================================================
   خروجی 1080×1080
===================================================== */

function exportCanvas() {

    const output =
        document.createElement("canvas");

    output.width = W;
    output.height = H;


    const outputCtx =
        output.getContext("2d");


    outputCtx.imageSmoothingEnabled =
        true;

    outputCtx.imageSmoothingQuality =
        "high";


    outputCtx.drawImage(
        canvas,
        0,
        0,
        RW,
        RH,
        0,
        0,
        W,
        H
    );


    return output;
}


/* =====================================================
   Render
===================================================== */

function render() {

    const text =
        document
            .getElementById("poemInput")
            .value
            .trim();


    const previewEmpty =
        document.getElementById(
            "previewEmpty"
        );


    const downloadBtn =
        document.getElementById(
            "downloadBtn"
        );


    const shareBtn =
        document.getElementById(
            "shareBtn"
        );


    if (!text) {

        canvas.classList.remove(
            "visible"
        );

        previewEmpty.style.display =
            "flex";

        downloadBtn.disabled =
            true;

        shareBtn.disabled =
            true;

        return;
    }


    createCard(text);


    canvas.classList.add(
        "visible"
    );


    previewEmpty.style.display =
        "none";


    downloadBtn.disabled =
        false;

    shareBtn.disabled =
        false;
}


/* =====================================================
   پالت‌ها
===================================================== */

function buildPaletteButtons() {

    const container =
        document.getElementById(
            "paletteButtons"
        );


    container.innerHTML = "";


    PALETTES.forEach(
        (palette, index) => {

            const button =
                document.createElement(
                    "button"
                );


            button.type =
                "button";


            button.className =
                "palette-button";


            if (
                index ===
                currentPalette
            ) {

                button.classList.add(
                    "active"
                );
            }


            button.title =
                palette.name;


            button.setAttribute(
                "aria-label",
                palette.name
            );


            button.style.background =
                `linear-gradient(
                    180deg,
                    ${colorRGB(palette.top)} 0%,
                    ${colorRGB(palette.middle)} 52%,
                    ${colorRGB(palette.bottom)} 100%
                )`;


            button.addEventListener(
                "click",
                () => {

                    currentPalette =
                        index;


                    document
                        .querySelectorAll(
                            ".palette-button"
                        )
                        .forEach(
                            item =>
                                item.classList.remove(
                                    "active"
                                )
                        );


                    button.classList.add(
                        "active"
                    );


                    render();
                }
            );


            container.appendChild(
                button
            );
        }
    );
}


/* =====================================================
   انتخاب نوع کارت
===================================================== */

document
    .querySelectorAll(
        ".type-button"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(
                        ".type-button"
                    )
                    .forEach(
                        item =>
                            item.classList.remove(
                                "active"
                            )
                    );


                button.classList.add(
                    "active"
                );


                branded =
                    button.dataset.branded
                    === "true";


                render();
            }
        );
    });


/* =====================================================
   متن شعر
===================================================== */

document
    .getElementById(
        "poemInput"
    )
    .addEventListener(
        "input",
        render
    );


/* =====================================================
   ذخیره
===================================================== */

document
    .getElementById(
        "downloadBtn"
    )
    .addEventListener(
        "click",
        () => {

            const text =
                document
                    .getElementById(
                        "poemInput"
                    )
                    .value
                    .trim();


            if (!text) {
                return;
            }


            const output =
                exportCanvas();


            output.toBlob(
                blob => {

                    if (!blob) {
                        return;
                    }


                    const url =
                        URL.createObjectURL(
                            blob
                        );


                    const link =
                        document.createElement(
                            "a"
                        );


                    link.href =
                        url;


                    link.download =
                        "kart-sh-er.png";


                    document.body.appendChild(
                        link
                    );


                    link.click();


                    link.remove();


                    setTimeout(
                        () =>
                            URL.revokeObjectURL(
                                url
                            ),
                        1000
                    );
                },
                "image/png"
            );
        }
    );


/* =====================================================
   اشتراک‌گذاری
===================================================== */

document
    .getElementById(
        "shareBtn"
    )
    .addEventListener(
        "click",
        async () => {

            const text =
                document
                    .getElementById(
                        "poemInput"
                    )
                    .value
                    .trim();


            if (!text) {
                return;
            }


            const output =
                exportCanvas();


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
                                type:
                                    "image/png"
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
                                title:
                                    "کارت شعر",
                                files: [file]
                            });

                            return;
                        }


                        if (
                            navigator.share
                        ) {

                            await navigator.share({
                                title:
                                    "کارت شعر",
                                text:
                                    "کارت شعر"
                            });

                            return;
                        }


                        alert(
                            "اشتراک‌گذاری مستقیم در این دستگاه در دسترس نیست. ابتدا کارت را ذخیره کنید."
                        );

                    } catch (error) {

                        if (
                            error.name !==
                            "AbortError"
                        ) {

                            console.error(
                                "Share error:",
                                error
                            );
                        }
                    }

                },
                "image/png"
            );
        }
    );


/* =====================================================
   شروع
===================================================== */

async function init() {

    buildPaletteButtons();

    /*
        هر دو منبع قبل از اولین Render آماده می‌شوند.
    */

    await Promise.all([
        loadFonts(),
        loadBackground()
    ]);


    render();
}


init();
