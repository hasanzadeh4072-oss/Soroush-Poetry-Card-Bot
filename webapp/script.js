const canvas = document.getElementById("poetryCanvas");
const ctx = canvas.getContext("2d");

const poemInput = document.getElementById("poemInput");
const previewEmpty = document.getElementById("previewEmpty");
const paletteButtons = document.getElementById("paletteButtons");
const downloadBtn = document.getElementById("downloadBtn");
const shareBtn = document.getElementById("shareBtn");

const W = 1080;
const H = 1080;
const S = 2;

const FONT_URLS = {
    Parastoo:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/Parastoo%5Bwght%5D.ttf",

    BTitrBd:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/BTitrBd.ttf",

    Vazirmatn:
        "https://raw.githubusercontent.com/hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/085a674b15bd74787ca00701a8ce9780342e3fd9/Vazirmatn-Regular.ttf"
};

const BG_URL =
    "https://raw.githubusercontent.com/" +
    "hasanzadeh4072-oss/Soroush-Poetry-Card-Bot/" +
    "be5859ec92836a14ef0ef28d82ca6c161959cb26/" +
    "tazhib-21-v1-t1-pub1-inkscape-plain.svg";

const PALETTES = [
    {
        name: "بنفش سلطنتی",
        top: [55,25,82],
        middle: [32,21,53],
        bottom: [13,10,25],
        glow1: [160,105,200,38],
        glow2: [105,70,160,22],
        glow3: [100,65,145,10],
        frame: [173,137,82],
        frame_inner: [205,172,105],
        text: [255,255,255],
        accent: [244,210,137],
        subtitle: [205,191,168],
        ornament: [145,112,68],
        panel_outline: [205,172,105,38],
        side_line: [205,172,105,75],
        side_dot: [205,172,105,100]
    },
    {
        name: "آبی شبانه",
        top: [18,39,76],
        middle: [16,27,53],
        bottom: [7,11,23],
        glow1: [75,115,185,32],
        glow2: [50,80,150,22],
        glow3: [55,85,140,10],
        frame: [165,140,83],
        frame_inner: [200,170,103],
        text: [255,255,255],
        accent: [239,210,139],
        subtitle: [195,204,211],
        ornament: [140,125,82],
        panel_outline: [190,170,110,38],
        side_line: [200,175,110,75],
        side_dot: [215,185,115,100]
    },
    {
        name: "شرابی",
        top: [76,19,37],
        middle: [45,14,26],
        bottom: [20,6,13],
        glow1: [175,70,90,35],
        glow2: [135,45,65,20],
        glow3: [130,45,60,10],
        frame: [174,133,72],
        frame_inner: [205,169,98],
        text: [255,255,255],
        accent: [241,210,139],
        subtitle: [211,193,181],
        ornament: [145,105,65],
        panel_outline: [195,155,95,38],
        side_line: [200,160,100,75],
        side_dot: [215,175,105,100]
    },
    {
        name: "فیروزه‌ای تیره",
        top: [10,61,67],
        middle: [9,39,45],
        bottom: [4,17,21],
        glow1: [55,155,165,34],
        glow2: [35,110,125,20],
        glow3: [40,120,130,10],
        frame: [172,145,91],
        frame_inner: [205,177,112],
        text: [255,255,255],
        accent: [224,199,132],
        subtitle: [188,209,208],
        ornament: [130,137,91],
        panel_outline: [185,170,110,38],
        side_line: [185,175,110,75],
        side_dot: [210,190,120,100]
    },
    {
        name: "سبز زمردی",
        top: [12,59,51],
        middle: [13,38,35],
        bottom: [5,18,17],
        glow1: [65,145,120,35],
        glow2: [45,110,95,20],
        glow3: [40,100,85,10],
        frame: [168,139,78],
        frame_inner: [200,169,99],
        text: [255,255,255],
        accent: [239,211,137],
        subtitle: [194,207,197],
        ornament: [140,118,70],
        panel_outline: [190,165,100,38],
        side_line: [190,170,105,75],
        side_dot: [210,180,110,100]
    },
    {
        name: "رزگلد",
        top: [72,35,48],
        middle: [45,23,32],
        bottom: [19,9,14],
        glow1: [190,105,120,32],
        glow2: [150,75,95,20],
        glow3: [135,70,85,10],
        frame: [181,125,119],
        frame_inner: [218,165,154],
        text: [255,255,255],
        accent: [235,181,163],
        subtitle: [216,194,187],
        ornament: [164,112,106],
        panel_outline: [215,160,150,38],
        side_line: [210,155,145,75],
        side_dot: [225,170,158,100]
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
let backgroundImage = new Image();
let fontsReady = false;
let hasCard = false;

backgroundImage.crossOrigin = "anonymous";
backgroundImage.src = BG_URL;

function rgba(c) {
    if (c.length === 3) {
        return `rgb(${c[0]},${c[1]},${c[2]})`;
    }

    return `rgba(${c[0]},${c[1]},${c[2]},${c[3] / 255})`;
}

function color(c) {
    return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
}

async function loadFonts() {
    try {
        const fonts = [
            ["Parastoo", FONT_URLS.Parastoo],
            ["BTitrBd", FONT_URLS.BTitrBd],
            ["Vazirmatn", FONT_URLS.Vazirmatn]
        ];

        await Promise.all(
            fonts.map(async ([name, url]) => {
                const font = new FontFace(name, `url("${url}")`);
                await font.load();
                document.fonts.add(font);
            })
        );

        await Promise.all([
            document.fonts.load('66px "Parastoo"'),
            document.fonts.load('30px "BTitrBd"'),
            document.fonts.load('20px "Vazirmatn"')
        ]);

        fontsReady = true;
    } catch (error) {
        console.error("Font loading error:", error);
        fontsReady = true;
    }
}

function makePaletteButtons() {
    paletteButtons.innerHTML = "";

    PALETTES.forEach((palette, index) => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "palette-btn";
        button.textContent = palette.name;

        const gradient = `linear-gradient(135deg,
            ${color(palette.top)},
            ${color(palette.middle)},
            ${color(palette.bottom)}
        )`;

        button.style.background = gradient;
        button.style.color =
            index >= 6 ? color(palette.text) : "#fff";

        if (index === selectedPalette) {
            button.classList.add("active");
        }

        button.addEventListener("click", () => {
            selectedPalette = index;

            document
                .querySelectorAll(".palette-btn")
                .forEach((btn, i) => {
                    btn.classList.toggle("active", i === selectedPalette);
                });

            if (poemInput.value.trim()) {
                createCard();
            }
        });

        paletteButtons.appendChild(button);
    });
}

function normalizePoem(text) {
    return text
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .replace(/\u200c/g, "\u200c")
        .trim();
}

function getLines(text) {
    return normalizePoem(text).split("\n");
}

function getSpacing(lines) {
    const nonBlank = lines.filter(line => line.trim()).length;

    if (nonBlank <= 2) {
        return {
            line: 32,
            blank: 48
        };
    }

    if (nonBlank === 3) {
        return {
            line: 26,
            blank: 40
        };
    }

    if (nonBlank === 4) {
        return {
            line: 20,
            blank: 32
        };
    }

    if (nonBlank === 5) {
        return {
            line: 17,
            blank: 28
        };
    }

    return {
        line: 14,
        blank: 24
    };
}

function getFontSize(lines) {
    const maxWidth = 790;
    const maxHeight = 640;

    const spacing = getSpacing(lines);

    for (let size = 66; size >= 28; size -= 2) {

        ctx.font = `${size}px "Parastoo"`;

        let totalHeight = 0;
        let fits = true;

        for (const line of lines) {

            if (!line.trim()) {
                totalHeight += spacing.blank;
                continue;
            }

            const metrics = ctx.measureText(line);
            const width = metrics.width;

            if (width > maxWidth) {
                fits = false;
                break;
            }

            totalHeight += size + spacing.line;
        }

        if (fits && totalHeight <= maxHeight) {
            return size;
        }
    }

    return 28;
}

function drawBackground(palette) {

    const gradient = ctx.createLinearGradient(0, 0, 0, H);

    gradient.addColorStop(0, color(palette.top));
    gradient.addColorStop(.5, color(palette.middle));
    gradient.addColorStop(1, color(palette.bottom));

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    if (backgroundImage.complete && backgroundImage.naturalWidth) {

        ctx.save();

        ctx.globalAlpha = .165;

        ctx.filter = "brightness(.48) blur(4px)";

        const scale = Math.max(
            W / backgroundImage.naturalWidth,
            H / backgroundImage.naturalHeight
        );

        const bw = backgroundImage.naturalWidth * scale;
        const bh = backgroundImage.naturalHeight * scale;

        ctx.drawImage(
            backgroundImage,
            (W - bw) / 2,
            (H - bh) / 2,
            bw,
            bh
        );

        ctx.restore();
    }

    const glow1 = ctx.createRadialGradient(
        540, 350, 10,
        540, 350, 520
    );

    glow1.addColorStop(0, rgba(palette.glow1));
    glow1.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = glow1;
    ctx.fillRect(0, 0, W, H);

    const glow2 = ctx.createRadialGradient(
        540, 700, 10,
        540, 700, 500
    );

    glow2.addColorStop(0, rgba(palette.glow2));
    glow2.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = glow2;
    ctx.fillRect(0, 0, W, H);

    const glow3 = ctx.createRadialGradient(
        540, 540, 10,
        540, 540, 600
    );

    glow3.addColorStop(0, rgba(palette.glow3));
    glow3.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = glow3;
    ctx.fillRect(0, 0, W, H);
}

function drawTexture() {

    ctx.save();

    for (let i = 0; i < 35000; i++) {

        const x = Math.random() * W;
        const y = Math.random() * H;

        const alpha = Math.random() * .045;

        ctx.fillStyle =
            `rgba(255,255,255,${alpha})`;

        ctx.fillRect(x, y, 1, 1);
    }

    ctx.restore();
}

function drawFrame(palette) {

    ctx.save();

    ctx.strokeStyle = color(palette.frame);
    ctx.lineWidth = 3;

    ctx.strokeRect(
        34,
        34,
        W - 68,
        H - 68
    );

    ctx.strokeStyle = color(palette.frame_inner);
    ctx.lineWidth = 1;

    ctx.strokeRect(
        46,
        46,
        W - 92,
        H - 92
    );

    ctx.restore();
}

function drawOrnament(palette) {

    const cx = W / 2;

    ctx.save();

    ctx.strokeStyle = color(palette.ornament);
    ctx.fillStyle = color(palette.ornament);
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(cx - 75, 125);
    ctx.quadraticCurveTo(cx, 85, cx + 75, 125);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(cx - 55, 125);
    ctx.quadraticCurveTo(cx, 105, cx + 55, 125);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(cx, 116, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

function drawBrand(palette) {

    if (!branded) {
        return;
    }

    ctx.save();

    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.font = `34px "BTitrBd"`;
    ctx.fillStyle = color(palette.accent);

    ctx.fillText(
        "شعرکده",
        W / 2,
        122
    );

    ctx.font = `18px "Vazirmatn"`;
    ctx.fillStyle = color(palette.subtitle);

    ctx.fillText(
        "( سروش پلاس )",
        W / 2,
        154
    );

    ctx.restore();
}

function drawPoem(palette, lines) {

    const spacing = getSpacing(lines);
    const fontSize = getFontSize(lines);

    ctx.font = `${fontSize}px "Parastoo"`;

    const textMetrics = lines.map(line => ({
        line,
        width: ctx.measureText(line).width
    }));

    let totalHeight = 0;

    textMetrics.forEach(item => {
        if (!item.line.trim()) {
            totalHeight += spacing.blank;
        } else {
            totalHeight += fontSize + spacing.line;
        }
    });

    totalHeight = Math.max(
        totalHeight - spacing.line,
        0
    );

    const centerY = 525;

    let y = centerY - totalHeight / 2 + fontSize * .8;

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = color(palette.text);

    for (const item of textMetrics) {

        if (!item.line.trim()) {
            y += spacing.blank;
            continue;
        }

        ctx.fillText(
            item.line,
            W / 2,
            y
        );

        y += fontSize + spacing.line;
    }
}

function drawFooter(palette) {

    ctx.save();

    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.font = `18px "Vazirmatn"`;
    ctx.fillStyle = color(palette.subtitle);

    ctx.fillText(
        "کارت شعر",
        W / 2,
        960
    );

    ctx.restore();
}

function createCard() {

    const text = normalizePoem(poemInput.value);

    if (!text) {
        canvas.style.display = "none";
        previewEmpty.style.display = "flex";

        downloadBtn.disabled = true;
        shareBtn.disabled = true;

        hasCard = false;

        return;
    }

    if (!fontsReady) {
        return;
    }

    const palette = PALETTES[selectedPalette];
    const lines = getLines(text);

    ctx.clearRect(0, 0, W, H);

    drawBackground(palette);
    drawTexture();
    drawFrame(palette);
    drawOrnament(palette);
    drawBrand(palette);
    drawPoem(palette, lines);
    drawFooter(palette);

    canvas.style.display = "block";
    previewEmpty.style.display = "none";

    downloadBtn.disabled = false;
    shareBtn.disabled = false;

    hasCard = true;
}

document.querySelectorAll(".option-btn").forEach(button => {

    button.addEventListener("click", () => {

        document
            .querySelectorAll(".option-btn")
            .forEach(btn => {
                btn.classList.remove("active");
            });

        button.classList.add("active");

        branded = button.dataset.branded === "true";

        if (poemInput.value.trim()) {
            createCard();
        }
    });

});

poemInput.addEventListener("input", () => {
    createCard();
});

downloadBtn.addEventListener("click", () => {

    if (!hasCard) {
        return;
    }

    const link = document.createElement("a");

    link.download = "kart-shere.png";
    link.href = canvas.toDataURL("image/png");

    link.click();
});

shareBtn.addEventListener("click", async () => {

    if (!hasCard) {
        return;
    }

    try {

        const blob = await new Promise(resolve => {
            canvas.toBlob(resolve, "image/png");
        });

        if (!blob) {
            return;
        }

        const file = new File(
            [blob],
            "kart-shere.png",
            { type: "image/png" }
        );

        if (
            navigator.share &&
            navigator.canShare &&
            navigator.canShare({ files: [file] })
        ) {

            await navigator.share({
                title: "کارت شعر",
                files: [file]
            });

            return;
        }

        if (navigator.share) {

            await navigator.share({
                title: "کارت شعر",
                text: "کارت شعر من"
            });

            return;
        }

        alert("اشتراک‌گذاری در این مرورگر پشتیبانی نمی‌شود.");

    } catch (error) {

        if (error.name !== "AbortError") {
            console.error("Share error:", error);
        }
    }
});

async function initialize() {

    makePaletteButtons();

    await loadFonts();

    if (
        backgroundImage.complete &&
        backgroundImage.naturalWidth
    ) {
        createCard();
    }
}

backgroundImage.onload = () => {

    if (fontsReady) {
        createCard();
    }
};

initialize();
