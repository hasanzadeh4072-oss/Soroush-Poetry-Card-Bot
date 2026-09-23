const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const previewEmpty = document.getElementById("previewEmpty");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");
const paletteButtons = document.getElementById("paletteButtons");

const W = 1080;
const H = 1080;

canvas.width = W;
canvas.height = H;

const POEM_FONT = "Parastoo";
const TITLE_FONT = "BTitrBd";
const SUB_FONT = "Vazirmatn";
const FOOT_FONT = "Vazirmatn";

const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";

const PALETTES = [
    {
        name:"بنفش سلطنتی",
        top:[55,25,82],
        middle:[32,21,53],
        bottom:[13,10,25],
        glow1:[160,105,200,38],
        glow2:[105,70,160,22],
        glow3:[100,65,145,10],
        frame:[173,137,82],
        frame_inner:[205,172,105],
        text:[255,255,255],
        accent:[244,210,137],
        subtitle:[205,191,168],
        ornament:[145,112,68],
        panel_outline:[205,172,105,38],
        side_line:[205,172,105,75],
        side_dot:[205,172,105,100]
    },
    {
        name:"آبی شبانه",
        top:[18,39,76],
        middle:[16,27,53],
        bottom:[7,11,23],
        glow1:[75,115,185,32],
        glow2:[50,80,150,22],
        glow3:[55,85,140,10],
        frame:[165,140,83],
        frame_inner:[200,170,103],
        text:[255,255,255],
        accent:[239,210,139],
        subtitle:[195,204,211],
        ornament:[140,125,82],
        panel_outline:[190,170,110,38],
        side_line:[200,175,110,75],
        side_dot:[215,185,115,100]
    },
    {
        name:"شرابی",
        top:[76,19,37],
        middle:[45,14,26],
        bottom:[20,6,13],
        glow1:[175,70,90,35],
        glow2:[135,45,65,20],
        glow3:[130,45,60,10],
        frame:[174,133,72],
        frame_inner:[205,169,98],
        text:[255,255,255],
        accent:[241,210,139],
        subtitle:[211,193,181],
        ornament:[145,105,65],
        panel_outline:[195,155,95,38],
        side_line:[200,160,100,75],
        side_dot:[215,175,105,100]
    },
    {
        name:"فیروزه‌ای تیره",
        top:[10,61,67],
        middle:[9,39,45],
        bottom:[4,17,21],
        glow1:[55,155,165,34],
        glow2:[35,110,125,20],
        glow3:[40,120,130,10],
        frame:[172,145,91],
        frame_inner:[205,177,112],
        text:[255,255,255],
        accent:[224,199,132],
        subtitle:[188,209,208],
        ornament:[130,137,91],
        panel_outline:[185,170,110,38],
        side_line:[185,175,110,75],
        side_dot:[210,190,120,100]
    },
    {
        name:"سبز زمردی",
        top:[12,59,51],
        middle:[13,38,35],
        bottom:[5,18,17],
        glow1:[65,145,120,35],
        glow2:[45,110,95,20],
        glow3:[40,100,85,10],
        frame:[168,139,78],
        frame_inner:[200,169,99],
        text:[255,255,255],
        accent:[239,211,137],
        subtitle:[194,207,197],
        ornament:[140,118,70],
        panel_outline:[190,165,100,38],
        side_line:[190,170,105,75],
        side_dot:[210,180,110,100]
    },
    {
        name:"رزگلد",
        top:[72,35,48],
        middle:[45,23,32],
        bottom:[19,9,14],
        glow1:[190,105,120,32],
        glow2:[150,75,95,20],
        glow3:[135,70,85,10],
        frame:[181,125,119],
        frame_inner:[218,165,154],
        text:[255,255,255],
        accent:[235,181,163],
        subtitle:[216,194,187],
        ornament:[164,112,106],
        panel_outline:[215,160,150,38],
        side_line:[210,155,145,75],
        side_dot:[225,170,158,100]
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

let selectedPalette = PALETTES[0];
let branded = true;
let currentImage = null;

const backgroundImage = new Image();
backgroundImage.crossOrigin = "anonymous";
backgroundImage.src = BG_URL;

function rgba(c) {
    return `rgba(${c[0]},${c[1]},${c[2]},${(c[3] ?? 255) / 255})`;
}

function rgb(c) {
    return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function lerp(a,b,t) {
    return a * (1-t) + b * t;
}

function gradientBackground(p) {
    const gradient = ctx.createLinearGradient(0,0,0,H);

    gradient.addColorStop(0, rgb(p.top));
    gradient.addColorStop(.52, rgb(p.middle));
    gradient.addColorStop(1, rgb(p.bottom));

    ctx.fillStyle = gradient;
    ctx.fillRect(0,0,W,H);
}

function drawGlow(p) {
    ctx.save();

    let g = ctx.createRadialGradient(
        190,190,0,
        190,190,470
    );

    g.addColorStop(0, rgba(p.glow1));
    g.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = g;
    ctx.fillRect(0,0,W,H);

    g = ctx.createRadialGradient(
        980,980,0,
        980,980,300
    );

    g.addColorStop(0, rgba(p.glow2));
    g.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = g;
    ctx.fillRect(0,0,W,H);

    g = ctx.createRadialGradient(
        550,650,0,
        550,650,320
    );

    g.addColorStop(0, rgba(p.glow3));
    g.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = g;
    ctx.fillRect(0,0,W,H);

    ctx.restore();
}

function drawTexture() {
    ctx.save();

    let rng = 8;

    for (let i = 0; i < 35000; i++) {
        rng = (rng * 9301 + 49297) % 233280;

        const x = rng / 233280 * W;

        rng = (rng * 9301 + 49297) % 233280;

        const y = rng / 233280 * H;

        ctx.fillStyle =
            i % 2 === 0
                ? "rgba(255,255,255,.012)"
                : "rgba(0,0,0,.016)";

        ctx.fillRect(x,y,1,1);
    }

    ctx.restore();
}

function drawBackground(p) {
    gradientBackground(p);
    drawGlow(p);
    drawTexture();

    if (backgroundImage.complete && backgroundImage.naturalWidth) {
        ctx.save();

        ctx.globalAlpha = .165;

        const ratio =
            backgroundImage.naturalWidth /
            backgroundImage.naturalHeight;

        const target = W / H;

        let dw;
        let dh;

        if (ratio > target) {
            dh = H;
            dw = backgroundImage.naturalWidth * H /
                backgroundImage.naturalHeight;
        } else {
            dw = W;
            dh = backgroundImage.naturalHeight * W /
                backgroundImage.naturalWidth;
        }

        const x = (W - dw) / 2;
        const y = (H - dh) / 2;

        ctx.filter = "brightness(.48) blur(4px)";
        ctx.drawImage(
            backgroundImage,
            x,y,dw,dh
        );

        ctx.restore();
    }
}

function roundedRect(x,y,w,h,r) {
    ctx.beginPath();
    ctx.roundRect(x,y,w,h,r);
}

function drawOrnament(p,y) {
    const center = W / 2;
    const width = 150;

    ctx.save();

    ctx.strokeStyle = rgb(p.ornament);
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(center-width,y);
    ctx.lineTo(center-12,y);
    ctx.moveTo(center+12,y);
    ctx.lineTo(center+width,y);
    ctx.stroke();

    ctx.fillStyle = rgb(p.accent);

    ctx.beginPath();
    ctx.moveTo(center,y-5);
    ctx.lineTo(center+5,y);
    ctx.lineTo(center,y+5);
    ctx.lineTo(center-5,y);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
}

function drawPanel(p) {
    ctx.save();

    roundedRect(100,160,880,730,45);
    ctx.fillStyle = "rgba(255,255,255,.024)";
    ctx.fill();

    roundedRect(100,160,880,730,45);
    ctx.strokeStyle = rgba(p.panel_outline);
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.restore();
}

function fontFamily(name) {
    if (name === POEM_FONT) return `"Parastoo", serif`;
    if (name === TITLE_FONT) return `"BTitrBd", sans-serif`;
    return `"Vazirmatn", sans-serif`;
}

function setFont(name,size) {
    ctx.font = `${size}px ${fontFamily(name)}`;
}

function measure(text) {
    return ctx.measureText(text).width;
}

function wrapLine(text,maxWidth) {
    const words = text.trim().split(/\s+/);

    if (!words.length) return [];

    const lines = [];
    let current = words[0];

    for (let i=1; i<words.length; i++) {
        const candidate = current + " " + words[i];

        if (measure(candidate) <= maxWidth) {
            current = candidate;
        } else {
            lines.push(current);
            current = words[i];
        }
    }

    lines.push(current);

    return lines;
}

function prepareLines(text,size,maxWidth) {
    setFont(POEM_FONT,size);

    const result = [];

    text.replace(/…/g,"...").split("\n").forEach(raw => {
        if (!raw.trim()) {
            result.push(null);
            return;
        }

        result.push(
            ...wrapLine(
                raw.trim(),
                maxWidth
            )
        );
    });

    return result;
}

function textHeight(size,lineSpacing,blankSpacing) {
    setFont(POEM_FONT,size);

    const lines = prepareLines(
        poemInput.value,
        size,
        790
    );

    let total = 0;

    lines.forEach(line => {
        if (line === null) {
            total += blankSpacing;
        } else {
            total += size + lineSpacing;
        }
    });

    if (lines.length && lines[lines.length-1] !== null) {
        total -= lineSpacing;
    }

    return {
        lines,
        total
    };
}

function drawTextCentered(
    text,
    y,
    size,
    color
) {
    setFont(POEM_FONT,size);

    ctx.fillStyle = rgb(color);
    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    ctx.fillText(
        text,
        W/2,
        y
    );
}

function createCard() {
    const text = poemInput.value.trim();

    if (!text) {
        currentImage = null;
        canvas.style.display = "none";
        previewEmpty.style.display = "flex";
        downloadBtn.disabled = true;
        shareBtn.disabled = true;
        return;
    }

    canvas.style.display = "block";
    previewEmpty.style.display = "none";

    drawBackground(selectedPalette);

    ctx.save();

    roundedRect(40,40,1000,1000,42);
    ctx.strokeStyle = rgb(selectedPalette.frame);
    ctx.lineWidth = 3;
    ctx.stroke();

    roundedRect(49,49,982,982,35);
    ctx.strokeStyle = rgb(selectedPalette.frame_inner);
    ctx.lineWidth = 2;
    ctx.stroke();

    setFont(FOOT_FONT,23);

    const footer = "کارت شعر";
    const footerWidth = measure(footer);

    ctx.textAlign = "center";
    ctx.textBaseline = "top";

    ctx.fillStyle = "rgba(0,0,0,.24)";
    ctx.fillText(
        footer,
        W/2+1,
        80+2
    );

    ctx.fillStyle = rgb(selectedPalette.accent);
    ctx.fillText(
        footer,
        W/2,
        80
    );

    drawOrnament(
        selectedPalette,
        80 + 23 + 25
    );

    if (branded) {
        setFont(TITLE_FONT,50);

        const title = "شعرکده";
        const subtitle = "( سروش پلاس )";

        const tw = measure(title);

        setFont(SUB_FONT,23);

        const sw = measure(subtitle);

        const titleX = W/2 + 10;
        const titleY = H - 78 - 50;

        setFont(TITLE_FONT,50);

        ctx.textAlign = "left";
        ctx.textBaseline = "top";

        ctx.fillStyle = "rgba(0,0,0,.30)";
        ctx.fillText(
            title,
            titleX+2,
            titleY+3
        );

        ctx.fillStyle = rgb(selectedPalette.accent);
        ctx.fillText(
            title,
            titleX,
            titleY
        );

        setFont(SUB_FONT,23);

        ctx.fillStyle = rgb(selectedPalette.subtitle);
        ctx.fillText(
            subtitle,
            titleX - sw - 20,
            titleY + 15
        );

        drawOrnament(
            selectedPalette,
            titleY - 25
        );
    } else {
        drawOrnament(
            selectedPalette,
            H - 112
        );
    }

    ctx.restore();

    drawPanel(selectedPalette);

    const left = 145;
    const right = 935;
    const top = 205;
    const bottom = 845;

    const maxWidth = right - left;
    const availableHeight = bottom - top;

    let fontSize = 66;
    let lineSpacing = 32;
    let blankSpacing = 48;
    let result;

    while (fontSize >= 28) {
        let spacing;

        result = textHeight(
            fontSize,
            20,
            32
        );

        const lineCount =
            result.lines.filter(
                x => x !== null
            ).length;

        if (lineCount <= 2) {
            spacing = 32;
            blankSpacing = 48;
        } else if (lineCount === 3) {
            spacing = 26;
            blankSpacing = 40;
        } else if (lineCount === 4) {
            spacing = 20;
            blankSpacing = 32;
        } else if (lineCount === 5) {
            spacing = 17;
            blankSpacing = 28;
        } else {
            spacing = 14;
            blankSpacing = 24;
        }

        result = textHeight(
            fontSize,
            spacing,
            blankSpacing
        );

        if (result.total <= availableHeight) {
            lineSpacing = spacing;
            break;
        }

        fontSize -= 2;
    }

    result = textHeight(
        fontSize,
        lineSpacing,
        blankSpacing
    );

    const lines = result.lines;

    let y =
        top +
        (availableHeight - result.total) / 2;

    y = Math.max(top,y);

    if (y + result.total > bottom) {
        y = bottom - result.total;
    }

    setFont(POEM_FONT,fontSize);

    ctx.fillStyle = rgb(
        selectedPalette.text
    );

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    lines.forEach((line,index) => {

        if (line === null) {
            y += blankSpacing;
            return;
        }

        ctx.fillText(
            line,
            W/2,
            y + fontSize
        );

        y += fontSize;

        if (index !== lines.length-1) {
            y += lineSpacing;
        }
    });

    const centerY =
        top + availableHeight / 2;

    ctx.strokeStyle =
        rgba(selectedPalette.side_line);

    ctx.fillStyle =
        rgba(selectedPalette.side_dot);

    ctx.lineWidth = 2;

    [65,1015].forEach(x => {

        ctx.beginPath();
        ctx.moveTo(x,centerY-30);
        ctx.lineTo(x,centerY+30);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(
            x,
            centerY,
            3,
            0,
            Math.PI*2
        );
        ctx.fill();
    });

    currentImage = canvas.toDataURL(
        "image/png"
    );

    downloadBtn.disabled = false;
    shareBtn.disabled = false;
}

function makePaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach((palette,index) => {
        const button = document.createElement("button");

        button.type = "button";
        button.className =
            "palette-btn" +
            (index === 0 ? " active" : "");

        button.textContent = palette.name;

        button.style.background =
            `linear-gradient(135deg,
                ${rgb(palette.top)},
                ${rgb(palette.bottom)})`;

        button.style.color =
            rgb(palette.text);

        button.addEventListener(
            "click",
            () => {
                selectedPalette = palette;

                document
                    .querySelectorAll(".palette-btn")
                    .forEach(
                        b => b.classList.remove("active")
                    );

                button.classList.add("active");

                createCard();
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
                    .forEach(
                        b => b.classList.remove("active")
                    );

                button.classList.add("active");

                createCard();
            }
        );
    });

poemInput.addEventListener(
    "input",
    createCard
);

downloadBtn.addEventListener(
    "click",
    () => {

        if (!currentImage) return;

        const link =
            document.createElement("a");

        link.download =
            "kart-shere.png";

        link.href =
            currentImage;

        link.click();
    }
);

shareBtn.addEventListener(
    "click",
    async () => {

        if (!currentImage) return;

        try {

            const response =
                await fetch(currentImage);

            const blob =
                await response.blob();

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
                navigator.canShare({files:[file]})
            ) {
                await navigator.share({
                    title: "کارت شعر",
                    text: "کارت شعر",
                    files: [file]
                });

                return;
            }

            if (navigator.share) {
                await navigator.share({
                    title: "کارت شعر",
                    text: "کارت شعر"
                });

                return;
            }

            alert(
                "اشتراک‌گذاری در این دستگاه در دسترس نیست."
            );

        } catch (error) {

            if (error.name !== "AbortError") {
                alert(
                    "اشتراک‌گذاری انجام نشد."
                );
            }
        }
    }
);

backgroundImage.onload = createCard;

makePaletteButtons();
createCard();



