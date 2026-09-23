const canvas =
    document.getElementById("poetryCanvas");

const ctx =
    canvas.getContext("2d");

const poemInput =
    document.getElementById("poemInput");

const paletteButtons =
    document.getElementById("paletteButtons");

const downloadBtn =
    document.getElementById("downloadBtn");

const shareBtn =
    document.getElementById("shareBtn");

const previewEmpty =
    document.getElementById("previewEmpty");


const W = 1080;
const H = 1080;

const LINE_SPACING = 32;
const BLANK_LINE_SPACING = 48;

const POEM_FONT = "Parastoo";
const TITLE_FONT = "BTitrBd";
const SUB_FONT = "Vazirmatn";


const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";


const backgroundImage =
    new Image();

backgroundImage.crossOrigin =
    "anonymous";


let backgroundLoaded = false;


backgroundImage.onload = () => {

    backgroundLoaded = true;

    updateCard();

};


backgroundImage.onerror = () => {

    backgroundLoaded = false;

    updateCard();

};


backgroundImage.src = BG_URL;


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


let selectedPalette = 0;
let branded = true;
let currentPoem = "";


function rgba(c) {

    if (c.length === 3) {

        return `rgb(
            ${c[0]},
            ${c[1]},
            ${c[2]}
        )`;

    }

    return `rgba(
        ${c[0]},
        ${c[1]},
        ${c[2]},
        ${c[3] / 255}
    )`;
}


function gradientBackground(p) {

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            H
        );


    gradient.addColorStop(
        0,
        `rgb(${p.top.join(",")})`
    );


    gradient.addColorStop(
        0.52,
        `rgb(${p.middle.join(",")})`
    );


    gradient.addColorStop(
        1,
        `rgb(${p.bottom.join(",")})`
    );


    ctx.fillStyle =
        gradient;

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

}


function drawGlow(
    x,
    y,
    w,
    h,
    color
) {

    ctx.save();

    ctx.translate(
        x + w / 2,
        y + h / 2
    );

    ctx.scale(
        w / 2,
        h / 2
    );


    const gradient =
        ctx.createRadialGradient(
            0,
            0,
            0,
            0,
            0,
            1
        );


    gradient.addColorStop(
        0,
        color
    );


    gradient.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );


    ctx.fillStyle =
        gradient;


    ctx.beginPath();

    ctx.arc(
        0,
        0,
        1,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();

}


function drawTexture() {

    const random =
        mulberry32(73421);


    ctx.save();


    for (
        let i = 0;
        i < 1500;
        i++
    ) {

        const x =
            random() * W;

        const y =
            random() * H;

        const alpha =
            .012 +
            random() * .018;


        ctx.fillStyle =
            `rgba(
                255,
                255,
                255,
                ${alpha}
            )`;


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


        t =
            Math.imul(
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
            (t ^ (t >>> 14))
            >>> 0
        ) / 4294967296;

    };

}


function drawBackground(p) {

    gradientBackground(p);


    /*
     * تصویر اصلی تذهیب بات
     * با همان حالت محو
     */

    if (
        backgroundLoaded &&
        backgroundImage.naturalWidth > 0
    ) {

        ctx.save();

        ctx.globalAlpha = 0.165;

        ctx.filter =
            "blur(4px)";

        ctx.drawImage(
            backgroundImage,
            0,
            0,
            W,
            H
        );

        ctx.restore();

    }


    drawTexture();

}


function roundedPath(
    x,
    y,
    w,
    h,
    radius
) {

    const r =
        Math.min(
            radius,
            w / 2,
            h / 2
        );


    ctx.beginPath();

    ctx.moveTo(
        x + r,
        y
    );

    ctx.lineTo(
        x + w - r,
        y
    );

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


function drawGlassPanel(p) {

    ctx.save();


    ctx.shadowColor =
        "rgba(0,0,0,0.09)";

    ctx.shadowBlur = 22;

    ctx.shadowOffsetY = 4;


    roundedPath(
        100,
        160,
        880,
        730,
        45
    );


    const glass =
        ctx.createLinearGradient(
            0,
            160,
            0,
            890
        );


    glass.addColorStop(
        0,
        "rgba(255,255,255,0.028)"
    );


    glass.addColorStop(
        .25,
        "rgba(255,255,255,0.008)"
    );


    glass.addColorStop(
        .55,
        "rgba(255,255,255,0.002)"
    );


    glass.addColorStop(
        .80,
        "rgba(255,255,255,0.006)"
    );


    glass.addColorStop(
        1,
        "rgba(255,255,255,0.025)"
    );


    ctx.fillStyle =
        glass;

    ctx.fill();

    ctx.restore();


    roundedPath(
        100,
        160,
        880,
        730,
        45
    );


    ctx.strokeStyle =
        rgba([
            p.panel_outline[0],
            p.panel_outline[1],
            p.panel_outline[2],
            135
        ]);


    ctx.lineWidth = 3;

    ctx.stroke();


    roundedPath(
        108,
        168,
        864,
        714,
        39
    );


    ctx.strokeStyle =
        "rgba(255,255,255,0.22)";

    ctx.lineWidth = 1.5;

    ctx.stroke();


    roundedPath(
        114,
        174,
        852,
        702,
        35
    );


    ctx.strokeStyle =
        "rgba(255,255,255,0.055)";

    ctx.lineWidth = 1;

    ctx.stroke();


    ctx.save();

    roundedPath(
        116,
        176,
        848,
        696,
        34
    );

    ctx.clip();


    const reflection =
        ctx.createLinearGradient(
            0,
            176,
            0,
            290
        );


    reflection.addColorStop(
        0,
        "rgba(255,255,255,0.10)"
    );


    reflection.addColorStop(
        .45,
        "rgba(255,255,255,0.025)"
    );


    reflection.addColorStop(
        1,
        "rgba(255,255,255,0)"
    );


    ctx.fillStyle =
        reflection;


    ctx.fillRect(
        100,
        160,
        880,
        150
    );


    ctx.restore();

}


function drawFrame(p) {

    roundedPath(
        40,
        40,
        1000,
        1000,
        42
    );


    ctx.strokeStyle =
        rgba(p.frame);

    ctx.lineWidth = 3;

    ctx.stroke();


    roundedPath(
        49,
        49,
        982,
        982,
        35
    );


    ctx.strokeStyle =
        rgba(p.frame_inner);

    ctx.lineWidth = 2;

    ctx.stroke();

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
        rgba(p.ornament);

    ctx.fillStyle =
        rgba(p.ornament);

    ctx.lineWidth = 2;


    ctx.beginPath();

    ctx.moveTo(
        center - width / 2,
        y
    );

    ctx.lineTo(
        center - 18,
        y
    );

    ctx.lineTo(
        center,
        y - 10
    );

    ctx.lineTo(
        center + 18,
        y
    );

    ctx.lineTo(
        center + width / 2,
        y
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        center,
        y - 7
    );

    ctx.lineTo(
        center + 7,
        y
    );

    ctx.lineTo(
        center,
        y + 7
    );

    ctx.lineTo(
        center - 7,
        y
    );

    ctx.closePath();

    ctx.fill();


    ctx.restore();

}


function drawBranding(p) {

    if (!branded) {
        return;
    }


    ctx.save();

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


    ctx.font =
        `50px "${TITLE_FONT}"`;


    ctx.fillStyle =
        rgba(p.accent);


    ctx.fillText(
        "شعرکده",
        W / 2,
        100
    );


    ctx.font =
        `23px "${SUB_FONT}"`;


    ctx.fillStyle =
        rgba(p.subtitle);


    ctx.fillText(
        "شعر، برای ماندن",
        W / 2,
        1002
    );


    ctx.restore();

}


function prepareLines(
    text,
    fontSize
) {

    const maxWidth = 790;

    ctx.font =
        `${fontSize}px "${POEM_FONT}"`;


    const lines = [];


    const rawLines =
        text
            .replace(/\r/g, "")
            .split("\n");


    for (
        const rawLine
        of rawLines
    ) {

        if (
            rawLine.trim() === ""
        ) {

            lines.push("");

            continue;
        }


        const words =
            rawLine
                .trim()
                .split(/\s+/);


        let current = "";


        for (
            const word
            of words
        ) {

            const test =
                current
                    ? `${current} ${word}`
                    : word;


            if (
                ctx.measureText(test).width
                <= maxWidth
            ) {

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


function calculateTextHeight(
    lines,
    fontSize
) {

    let height = 0;


    for (
        const line
        of lines
    ) {

        height +=
            line === ""
                ? BLANK_LINE_SPACING
                : fontSize + LINE_SPACING;

    }


    return Math.max(
        0,
        height - LINE_SPACING
    );

}


function drawPoem(p) {

    const text =
        currentPoem.trim();


    if (!text) {
        return;
    }


    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;


    const availableHeight =
        bottom - top;


    const maxWidth =
        right - left;


    let fontSize = 66;
    let lines = [];


    while (
        fontSize >= 28
    ) {

        lines =
            prepareLines(
                text,
                fontSize
            );


        const height =
            calculateTextHeight(
                lines,
                fontSize
            );


        if (
            height <= availableHeight
        ) {
            break;
        }


        fontSize -= 2;

    }


    if (fontSize < 28) {

        fontSize = 28;

        lines =
            prepareLines(
                text,
                fontSize
            );

    }


    const textHeight =
        calculateTextHeight(
            lines,
            fontSize
        );


    let y =
        top +
        (
            availableHeight -
            textHeight
        ) / 2;


    ctx.save();


    ctx.font =
        `${fontSize}px "${POEM_FONT}"`;

    ctx.fillStyle =
        rgba(p.text);

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "top";


    for (
        const line
        of lines
    ) {

        if (line === "") {

            y +=
                BLANK_LINE_SPACING;

            continue;
        }


        ctx.fillText(
            line,
            W / 2,
            y
        );


        y +=
            fontSize +
            LINE_SPACING;

    }


    ctx.restore();

}


function drawSideDecoration(p) {

    const centerY = 525;


    ctx.save();


    ctx.strokeStyle =
        rgba(p.side_line);

    ctx.fillStyle =
        rgba(p.side_dot);

    ctx.lineWidth = 2;


    for (
        const x of [65, 1015]
    ) {

        ctx.beginPath();

        ctx.moveTo(
            x,
            centerY - 30
        );

        ctx.lineTo(
            x,
            centerY + 30
        );

        ctx.stroke();


        ctx.beginPath();

        ctx.arc(
            x,
            centerY,
            3,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }


    ctx.restore();

}


function drawCard() {

    const p =
        PALETTES[selectedPalette];


    ctx.clearRect(
        0,
        0,
        W,
        H
    );


    drawBackground(p);

    drawGlassPanel(p);

    drawFrame(p);

    drawSideDecoration(p);

    drawOrnament(
        185,
        p
    );

    drawPoem(p);

    drawBranding(p);

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


    canvas.style.display =
        "block";

    previewEmpty.style.display =
        "none";


    drawCard();


    downloadBtn.disabled =
        false;

    shareBtn.disabled =
        false;

}


function createPaletteButtons() {

    paletteButtons.innerHTML = "";


    PALETTES.forEach(
        (palette, index) => {

            const button =
                document.createElement(
                    "button"
                );


            button.type =
                "button";


            button.className =
                "palette-btn";


            button.textContent =
                palette.name;


            button.style.background =
                `linear-gradient(
                    135deg,
                    rgb(${palette.top.join(",")}),
                    rgb(${palette.bottom.join(",")})
                )`;


            button.style.color =
                `rgb(${palette.text.join(",")})`;


            button.style.borderColor =
                `rgb(${palette.frame.join(",")})`;


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
                            (btn, i) => {

                                btn.classList.toggle(
                                    "active",
                                    i === index
                                );

                            }
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
    .forEach(
        button => {

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


                    updateCard();

                }
            );

        }
    );


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
            "کارت-شعر.png";


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


        try {

            const blob =
                await new Promise(
                    resolve => {

                        canvas.toBlob(
                            resolve,
                            "image/png",
                            1
                        );

                    }
                );


            const file =
                new File(
                    [blob],
                    "کارت-شعر.png",
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

                return;
            }


            if (
                navigator.share
            ) {

                await navigator.share({
                    title: "کارت شعر",
                    text: currentPoem
                });

                return;
            }


            alert(
                "اشتراک‌گذاری در این مرورگر پشتیبانی نمی‌شود."
            );


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

    }
);


createPaletteButtons();
