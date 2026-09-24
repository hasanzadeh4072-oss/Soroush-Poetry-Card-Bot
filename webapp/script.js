"use strict";

/*
    طراحی کارت مستقیماً بر اساس کد اصلی بات کارت شعر
*/

const W = 1080;
const H = 1080;

const S = 2;

const LINE_SPACING = 32;
const BLANK_LINE_SPACING = 48;

const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";


const FONT_URLS = {
    poem:
        "https://raw.githubusercontent.com/" +
        "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/Parastoo%5Bwght%5D.ttf",

    title:
        "https://raw.githubusercontent.com/" +
        "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/BTitrBd.ttf",

    regular:
        "https://raw.githubusercontent.com/" +
        "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/main/Vazirmatn-Regular.ttf"
};


/* -------------------- پالت‌ها -------------------- */

const PALETTES = [
    {
        name: "بنفش سلطنتی",
        top: [76,43,105],
        middle: [50,34,73],
        bottom: [25,18,40],
        glow1: [175,120,215,42],
        glow2: [120,85,175,25],
        glow3: [115,80,160,12],
        frame: [173,137,82],
        frame_inner: [205,172,105],
        text: [255,255,255],
        accent: [244,210,137],
        subtitle: [215,201,184],
        ornament: [155,120,75],
        panel_outline: [205,172,105,42],
        side_line: [205,172,105,82],
        side_dot: [205,172,105,105]
    },

    {
        name: "آبی شبانه",
        top: [30,58,100],
        middle: [25,43,76],
        bottom: [12,20,38],
        glow1: [85,130,205,40],
        glow2: [60,100,175,25],
        glow3: [65,105,165,12],
        frame: [165,140,83],
        frame_inner: [200,170,103],
        text: [255,255,255],
        accent: [239,210,139],
        subtitle: [205,213,220],
        ornament: [145,130,88],
        panel_outline: [190,170,110,42],
        side_line: [200,175,110,82],
        side_dot: [215,185,115,105]
    },

    {
        name: "شرابی",
        top: [103,31,52],
        middle: [65,21,36],
        bottom: [31,10,19],
        glow1: [195,82,105,42],
        glow2: [155,55,78,25],
        glow3: [145,55,70,12],
        frame: [174,133,72],
        frame_inner: [205,169,98],
        text: [255,255,255],
        accent: [241,210,139],
        subtitle: [220,201,190],
        ornament: [155,112,70],
        panel_outline: [195,155,95,42],
        side_line: [200,160,100,82],
        side_dot: [215,175,105,105]
    },

    {
        name: "فیروزه‌ای تیره",
        top: [16,80,88],
        middle: [13,53,61],
        bottom: [6,24,29],
        glow1: [65,170,180,42],
        glow2: [45,125,140,25],
        glow3: [45,135,145,12],
        frame: [172,145,91],
        frame_inner: [205,177,112],
        text: [255,255,255],
        accent: [224,199,132],
        subtitle: [201,218,217],
        ornament: [140,147,98],
        panel_outline: [185,170,110,42],
        side_line: [185,175,110,82],
        side_dot: [210,190,120,105]
    },

    {
        name: "سبز زمردی",
        top: [18,76,64],
        middle: [17,51,46],
        bottom: [7,24,22],
        glow1: [75,160,130,42],
        glow2: [55,125,105,25],
        glow3: [50,115,95,12],
        frame: [168,139,78],
        frame_inner: [200,169,99],
        text: [255,255,255],
        accent: [239,211,137],
        subtitle: [205,218,207],
        ornament: [150,128,77],
        panel_outline: [190,165,100,42],
        side_line: [190,170,105,82],
        side_dot: [210,180,110,105]
    },

    {
        name: "رزگلد",
        top: [94,48,62],
        middle: [60,31,43],
        bottom: [27,13,20],
        glow1: [205,120,135,40],
        glow2: [165,85,105,25],
        glow3: [150,80,95,12],
        frame: [181,125,119],
        frame_inner: [218,165,154],
        text: [255,255,255],
        accent: [235,181,163],
        subtitle: [224,204,197],
        ornament: [174,120,114],
        panel_outline: [215,160,150,42],
        side_line: [210,155,145,82],
        side_dot: [225,170,158,105]
    },

    {
        name: "کرم",
        top: [250,239,210],
        middle: [242,226,190],
        bottom: [226,205,163],
        glow1: [255,252,230,55],
        glow2: [255,240,185,28],
        glow3: [255,255,255,22],
        frame: [91,67,39],
        frame_inner: [126,96,58],
        text: [49,40,31],
        accent: [104,73,38],
        subtitle: [77,61,43],
        ornament: [113,80,42],
        panel_outline: [105,78,43,55],
        side_line: [105,78,43,85],
        side_dot: [94,67,35,125]
    },

    {
        name: "آبی روشن",
        top: [205,235,248],
        middle: [180,220,238],
        bottom: [153,201,225],
        glow1: [235,249,255,58],
        glow2: [145,205,235,28],
        glow3: [255,255,255,24],
        frame: [43,73,91],
        frame_inner: [72,105,124],
        text: [31,51,63],
        accent: [48,82,101],
        subtitle: [54,77,91],
        ornament: [59,91,108],
        panel_outline: [58,91,110,55],
        side_line: [58,91,110,85],
        side_dot: [46,79,99,125]
    },

    {
        name: "مریم‌گلی",
        top: [218,231,205],
        middle: [201,219,184],
        bottom: [179,201,159],
        glow1: [242,249,230,58],
        glow2: [175,205,145,28],
        glow3: [255,255,255,24],
        frame: [60,76,52],
        frame_inner: [91,108,78],
        text: [39,54,35],
        accent: [67,88,55],
        subtitle: [67,82,59],
        ornament: [75,96,62],
        panel_outline: [73,96,62,55],
        side_line: [73,96,62,85],
        side_dot: [62,84,52,125]
    }
];


/* -------------------- عناصر صفحه -------------------- */

const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const paletteButtons = document.getElementById("paletteButtons");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const previewEmpty = document.getElementById("previewEmpty");

let currentPalette = 0;
let branded = true;
let backgroundImage = null;
let backgroundReady = false;


/* -------------------- فونت‌ها -------------------- */

async function loadFonts() {

    try {

        const poemFont = new FontFace(
            "PoemFont",
            `url("${FONT_URLS.poem}")`
        );

        const titleFont = new FontFace(
            "TitleFont",
            `url("${FONT_URLS.title}")`
        );

        const regularFont = new FontFace(
            "RegularFont",
            `url("${FONT_URLS.regular}")`
        );

        await Promise.all([
            poemFont.load(),
            titleFont.load(),
            regularFont.load()
        ]);

        document.fonts.add(poemFont);
        document.fonts.add(titleFont);
        document.fonts.add(regularFont);

    } catch (error) {

        console.warn("Font loading failed:", error);

    }
}


/* -------------------- پس‌زمینه -------------------- */

function loadBackground() {

    backgroundImage = new Image();

    backgroundImage.crossOrigin = "anonymous";

    backgroundImage.onload = function () {
        backgroundReady = true;

        if (poemInput.value.trim()) {
            render();
        }
    };

    backgroundImage.onerror = function () {
        backgroundReady = false;

        if (poemInput.value.trim()) {
            render();
        }
    };

    backgroundImage.src = BG_URL;
}


/* -------------------- ابزار رنگ -------------------- */

function rgba(color) {

    if (color.length === 3) {
        return `rgb(${color[0]},${color[1]},${color[2]})`;
    }

    return `rgba(${color[0]},${color[1]},${color[2]},${color[3] / 255})`;
}


function rgb(color) {
    return `rgb(${color[0]},${color[1]},${color[2]})`;
}


/* -------------------- گرادیان -------------------- */

function drawGradient(p) {

    const gradient = ctx.createLinearGradient(
        0,
        0,
        0,
        H
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

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );
}


/* -------------------- پس‌زمینه اصلی بات -------------------- */

function drawBackground(p) {

    drawGradient(p);

    /*
        در بات:
        BG با Brightness(.48)
        Blur = 8
        Alpha = 42 / 255
    */

    if (backgroundReady && backgroundImage) {

        const bgCanvas = document.createElement("canvas");

        bgCanvas.width = W;
        bgCanvas.height = H;

        const bgCtx = bgCanvas.getContext("2d");

        bgCtx.clearRect(
            0,
            0,
            W,
            H
        );

        const iw = backgroundImage.naturalWidth || W;
        const ih = backgroundImage.naturalHeight || H;

        const scale = Math.max(
            W / iw,
            H / ih
        );

        const dw = iw * scale;
        const dh = ih * scale;

        const dx = (W - dw) / 2;
        const dy = (H - dh) / 2;

        bgCtx.filter = "brightness(48%) blur(8px)";

        bgCtx.drawImage(
            backgroundImage,
            dx,
            dy,
            dw,
            dh
        );

        ctx.save();

        ctx.globalAlpha = 42 / 255;

        ctx.drawImage(
            bgCanvas,
            0,
            0,
            W,
            H
        );

        ctx.restore();
    }


    /*
        glow های دقیق پالت بات
    */

    ctx.save();

    ctx.filter = "blur(55px)";

    ctx.fillStyle = rgba(p.glow1);

    ctx.beginPath();

    ctx.ellipse(
        260,
        230,
        270,
        210,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = rgba(p.glow2);

    ctx.beginPath();

    ctx.ellipse(
        850,
        390,
        250,
        280,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle = rgba(p.glow3);

    ctx.beginPath();

    ctx.ellipse(
        500,
        900,
        360,
        180,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();
}


/* -------------------- پنل دقیق بات -------------------- */

function drawPanel(p) {

    const panel = document.createElement("canvas");

    panel.width = W;
    panel.height = H;

    const d = panel.getContext("2d");

    /*
        d.rr((100,164,980,896), radius=45, fill=(0,0,0,45))
    */

    d.fillStyle = "rgba(0,0,0,45/255)";

    roundedRect(
        d,
        100,
        164,
        880,
        732,
        45
    );

    d.fill();


    /*
        d.rr((100,160,980,890), radius=45, fill=(255,255,255,24))
    */

    d.fillStyle = "rgba(255,255,255,24/255)";

    roundedRect(
        d,
        100,
        160,
        880,
        730,
        45
    );

    d.fill();


    /*
        d.rr((110,170,970,880), radius=37,
             outline=(255,255,255,12), width=1)
    */

    roundedRectStroke(
        d,
        110,
        170,
        860,
        710,
        37,
        "rgba(255,255,255,12/255)",
        1
    );


    ctx.save();

    ctx.globalAlpha = 1;

    ctx.drawImage(
        panel,
        0,
        0
    );

    ctx.restore();
}


function roundedRect(
    context,
    x,
    y,
    width,
    height,
    radius
) {

    context.beginPath();

    context.moveTo(x + radius, y);

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


function roundedRectStroke(
    context,
    x,
    y,
    width,
    height,
    radius,
    color,
    lineWidth
) {

    context.beginPath();

    context.moveTo(x + radius, y);

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

    context.strokeStyle = color;
    context.lineWidth = lineWidth;

    context.stroke();
}


/* -------------------- قاب دقیق بات -------------------- */

function drawFrame(p) {

    roundedRectStroke(
        ctx,
        40,
        40,
        1000,
        1000,
        42,
        rgb(p.frame),
        3
    );

    roundedRectStroke(
        ctx,
        49,
        49,
        982,
        982,
        35,
        rgb(p.frame_inner),
        2
    );
}


/* -------------------- تزئین وسط -------------------- */

function drawOrnament(p, y) {

    const center = W / 2;

    const width = 150;


    ctx.strokeStyle = rgb(p.ornament);
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


    ctx.fillStyle = rgb(p.accent);

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
}


/* -------------------- نوشته‌های بات -------------------- */

function drawBranding(p) {

    const title = "شعرکده";
    const subtitle = "( سروش پلاس )";
    const footer = "کارت شعر";

    const titleFontSize = 42;
    const subtitleFontSize = 22;
    const footerFontSize = 23;

    const footerY = 78;


    /*
        footer = کارت شعر
        بالای کارت
    */

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    ctx.font =
        `${footerFontSize}px RegularFont, Vazirmatn, sans-serif`;

    ctx.fillStyle = rgb(p.accent);

    ctx.fillText(
        footer,
        W / 2,
        footerY
    );


    /*
        ornament بعد از footer
    */

    drawOrnament(
        p,
        footerY + 23 + 25
    );


    /*
        پایین کارت:
        شعرکده + ( سروش پلاس )
    */

    ctx.font =
        `bold ${titleFontSize}px TitleFont, Vazirmatn, sans-serif`;

    const titleWidth =
        ctx.measureText(title).width;

    const titleHeight = titleFontSize;


    ctx.font =
        `${subtitleFontSize}px RegularFont, Vazirmatn, sans-serif`;

    const subtitleWidth =
        ctx.measureText(subtitle).width;

    const subtitleHeight = subtitleFontSize;


    const titleY =
        H - 78 - titleHeight;

    const titleX =
        W / 2 + 10;


    ctx.font =
        `bold ${titleFontSize}px TitleFont, Vazirmatn, sans-serif`;

    ctx.textAlign = "left";

    ctx.fillStyle = rgb(p.accent);

    ctx.fillText(
        title,
        titleX,
        titleY
    );


    ctx.font =
        `${subtitleFontSize}px RegularFont, Vazirmatn, sans-serif`;

    ctx.fillStyle = rgb(p.subtitle);

    ctx.fillText(
        subtitle,
        titleX - titleWidth - 20,
        titleY + (titleHeight - subtitleHeight) / 2 - 3
    );


    /*
        ornament بالای نوشته پایین
    */

    drawOrnament(
        p,
        titleY - 25
    );
}


/* -------------------- متن شعر -------------------- */

function wrapText(
    text,
    fontSize,
    maxWidth
) {

    ctx.font =
        `${fontSize}px PoemFont, Parastoo, serif`;

    const result = [];

    const paragraphs = text.split("\n");

    for (const paragraph of paragraphs) {

        if (paragraph.trim() === "") {

            result.push("");

            continue;
        }

        const words = paragraph.trim().split(/\s+/);

        let line = "";

        for (const word of words) {

            const test =
                line
                    ? line + " " + word
                    : word;

            const width =
                ctx.measureText(test).width;

            if (
                width <= maxWidth ||
                !line
            ) {

                line = test;

            } else {

                result.push(line);

                line = word;
            }
        }

        if (line) {
            result.push(line);
        }
    }

    return result;
}


/* -------------------- ارتفاع شعر -------------------- */

function calculateTextHeight(
    lines,
    lineSpacing,
    blankSpacing
) {

    let height = 0;

    for (let i = 0; i < lines.length; i++) {

        if (lines[i] === "") {
            height += blankSpacing;
        } else {
            height += lineSpacing;
        }
    }

    return height;
}


/* -------------------- رسم شعر -------------------- */

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

        lines = wrapText(
            text,
            fontSize,
            maxWidth
        );

        const height =
            calculateTextHeight(
                lines,
                LINE_SPACING,
                BLANK_LINE_SPACING
            );

        if (height <= availableHeight) {
            break;
        }

        fontSize -= 2;
    }


    const totalHeight =
        calculateTextHeight(
            lines,
            LINE_SPACING,
            BLANK_LINE_SPACING
        );


    let y =
        top +
        (availableHeight - totalHeight) / 2;


    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    ctx.font =
        `${fontSize}px PoemFont, Parastoo, serif`;

    ctx.fillStyle = rgb(p.text);

    ctx.strokeStyle = rgb(p.text);

    ctx.lineWidth = 1;


    for (const line of lines) {

        if (line === "") {

            y += BLANK_LINE_SPACING;

            continue;
        }


        /*
            در کد بات:
            fill=p["text"]
            stroke_width=1
            stroke_fill=p["text"]
        */

        ctx.strokeText(
            line,
            (left + right) / 2,
            y + fontSize
        );

        ctx.fillText(
            line,
            (left + right) / 2,
            y + fontSize
        );


        y += LINE_SPACING;
    }
}


/* -------------------- المان‌های کناری دقیق بات -------------------- */

function drawSideDecoration(p) {

    const xs = [65, 1015];

    for (const x of xs) {

        ctx.strokeStyle = rgba([
            p.side_line[0],
            p.side_line[1],
            p.side_line[2],
            p.side_line[3]
        ]);

        ctx.lineWidth = 2;

        ctx.beginPath();

        ctx.moveTo(
            x,
            495
        );

        ctx.lineTo(
            x,
            555
        );

        ctx.stroke();


        ctx.fillStyle = rgba([
            p.side_dot[0],
            p.side_dot[1],
            p.side_dot[2],
            p.side_dot[3]
        ]);

        ctx.beginPath();

        ctx.arc(
            x,
            525,
            3,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}


/* -------------------- ساخت کارت -------------------- */

function createCard(text) {

    const p = PALETTES[currentPalette];

    ctx.clearRect(
        0,
        0,
        W,
        H
    );


    /*
        ترتیب دقیق create_card بات:

        1. background
        2. frame
        3. branding/footer/ornament
        4. panel
        5. poem
        6. side decoration
    */

    drawBackground(p);

    drawFrame(p);

    drawBranding(p);

    drawPanel(p);

    drawPoem(p, text);

    drawSideDecoration(p);
}


/* -------------------- رندر -------------------- */

function render() {

    const text = poemInput.value.trim();

    if (!text) {

        canvas.classList.remove("visible");

        previewEmpty.style.display = "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        return;
    }


    createCard(text);

    canvas.classList.add("visible");

    previewEmpty.style.display = "none";

    downloadBtn.disabled = false;
    shareBtn.disabled = false;
}


/* -------------------- پالت‌ها -------------------- */

function createPaletteButtons() {

    paletteButtons.innerHTML = "";

    PALETTES.forEach((palette, index) => {

        const button =
            document.createElement("button");

        button.type = "button";

        button.className = "palette-btn";

        if (index === currentPalette) {
            button.classList.add("active");
        }


        const gradient =
            `linear-gradient(180deg,
            rgb(${palette.top.join(",")}) 0%,
            rgb(${palette.middle.join(",")}) 52%,
            rgb(${palette.bottom.join(",")}) 100%)`;

        button.style.background = gradient;

        button.title = palette.name;

        button.setAttribute(
            "aria-label",
            palette.name
        );


        button.addEventListener(
            "click",
            () => {

                currentPalette = index;

                document
                    .querySelectorAll(".palette-btn")
                    .forEach(
                        item =>
                            item.classList.remove("active")
                    );

                button.classList.add("active");

                render();
            }
        );


        paletteButtons.appendChild(button);
    });
}


/* -------------------- نوع کارت -------------------- */

document
    .querySelectorAll(".option-btn")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(".option-btn")
                    .forEach(
                        item =>
                            item.classList.remove("active")
                    );

                button.classList.add("active");

                branded =
                    button.dataset.branded === "true";

                /*
                    متغیر branded برای حفظ منطق
                    انتخاب امضا نگه داشته شده است.
                */

                render();
            }
        );
    });


/* -------------------- ورود شعر -------------------- */

poemInput.addEventListener(
    "input",
    () => {
        render();
    }
);


/* -------------------- ذخیره -------------------- */

downloadBtn.addEventListener(
    "click",
    () => {

        if (!poemInput.value.trim()) {
            return;
        }

        const link =
            document.createElement("a");

        link.download = "kart-sh-er.png";

        link.href =
            canvas.toDataURL(
                "image/png",
                1
            );

        document.body.appendChild(link);

        link.click();

        link.remove();
    }
);


/* -------------------- اشتراک‌گذاری -------------------- */

shareBtn.addEventListener(
    "click",
    async () => {

        if (!poemInput.value.trim()) {
            return;
        }


        if (!navigator.share) {

            alert(
                "اشتراک‌گذاری مستقیم در این دستگاه در دسترس نیست. ابتدا کارت را ذخیره کنید."
            );

            return;
        }


        try {

            const blob =
                await new Promise(
                    resolve =>
                        canvas.toBlob(
                            resolve,
                            "image/png",
                            1
                        )
                );


            const file =
                new File(
                    [blob],
                    "kart-sh-er.png",
                    {
                        type: "image/png"
                    }
                );


            if (
                navigator.canShare &&
                !navigator.canShare({ files: [file] })
            ) {

                await navigator.share({
                    title: "کارت شعر"
                });

                return;
            }


            await navigator.share({
                title: "کارت شعر",
                text: "کارت شعر"
            });


        } catch (error) {

            if (error.name !== "AbortError") {

                console.error(
                    "Share error:",
                    error
                );
            }
        }
    }
);


/* -------------------- شروع -------------------- */

async function init() {

    createPaletteButtons();

    await loadFonts();

    loadBackground();

    render();
}


init();
