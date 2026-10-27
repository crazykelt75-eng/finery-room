"""Build 10-second video ads (9:16 and 1:1) from real photos and the accepted clip.

Usage: python -I video_ads.py <scratch_dir> <repo_dir> <ffmpeg_exe>
Text layers are HTML rendered by headless Chrome (transparent PNG) and faded in
with ffmpeg: hook from 0 s, prices from 2.5 s, call to action from 5 s to the end.
Photos only get a uniform slow zoom; the accepted AI clip is used as-is.
"""
import subprocess
import sys
from pathlib import Path

S = Path(sys.argv[1]).resolve()
REPO = Path(sys.argv[2]).resolve()
FF = sys.argv[3]
WORK = S / "video_ads_work"
OUT = REPO / "assets" / "ads"
WORK.mkdir(parents=True, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LOGO = (REPO / "assets" / "logo.jpg").as_uri()
PHONE = "+267 765 841 00"
DUR = 10
FPS = 30

ADS = {
    "premium": {
        "hook": "Nails that feel like a treat.",
        "lines": ["Full Set <b>P80</b>", "Toes <b>P50</b>"],
        # Accepted Higgsfield clip (720x1280); crops keep the whole hand in frame.
        "clip": S / "masters" / "video" / "nails-2-9x16.mp4",
        "clip_crop": {"9x16": "crop=720:720:0:430", "1x1": "crop=640:1280:40:0"},
    },
    "problem": {
        "hook": "Chipped nails before the weekend?",
        "lines": ["Nail Repair <b>P10</b> per nail", "Full Set <b>P80</b>"],
        "still": {"9x16": S / "composites" / "nails-3-1x1.png", "1x1": S / "composites" / "nails-3-4x5.png"},
    },
    "refill": {
        "hook": "Day 12? Your lashes are due.",
        "lines": ["Refill within 2 weeks <b>P40</b>", "instead of a new Classic Set at P70"],
        "still": {"9x16": REPO / "assets" / "work-lashes-2.jpg", "1x1": REPO / "assets" / "work-lashes-1.jpg"},
    },
}

# Photo box and text positions per format.
LAYOUT = {
    "9x16": {"w": 1080, "h": 1920, "box": (130, 520, 820, 820)},
    "1x1": {"w": 1080, "h": 1080, "box": (0, 0, 540, 1080)},
}

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,500..700'
         '&family=Jost:wght@400;500;600&display=block" rel="stylesheet">')

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:transparent;font-family:Jost,sans-serif;color:#F5F4F2}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 28%% 18%%,#885C99 0%%,#3a2244 36%%,#0A090C 78%%)}
.logo{width:%(logo)dpx;height:%(logo)dpx;border-radius:50%%;mix-blend-mode:screen}
h1{font-family:'Bodoni Moda',serif;font-weight:500;font-size:%(hook)dpx;line-height:1.08}
.lines{display:flex;flex-direction:column;gap:8px}
.lines span{font-size:%(line)dpx}
.lines b{color:#C9A7E0;font-weight:600}
.sub{font-size:%(sub)dpx;letter-spacing:4px;text-transform:uppercase;color:#C9A7E0}
.cta{display:inline-block;background:#25D366;color:#06210f;font-weight:600;font-size:%(cta)dpx;padding:%(ctap)dpx %(ctapx)dpx;border-radius:999px;line-height:1.2}
.frame{position:absolute;border:2px solid rgba(201,167,224,.6)}
.abs{position:absolute}
"""

SIZE_CSS = {
    "9x16": dict(w=1080, h=1920, logo=120, hook=88, line=44, sub=24, cta=38, ctap=24, ctapx=46),
    "1x1": dict(w=1080, h=1080, logo=90, hook=60, line=32, sub=18, cta=30, ctap=18, ctapx=30),
}


def layer_html(ad, fmt, part):
    s = SIZE_CSS[fmt]
    css = BASE_CSS % s
    x, y, bw, bh = LAYOUT[fmt]["box"]
    lines = "".join(f"<span>{l}</span>" for l in ad["lines"])
    if fmt == "9x16":
        col = 'style="left:80px;right:80px;text-align:center;display:flex;flex-direction:column;align-items:center"'
        parts = {
            "bg": '<div class="bg"></div>',
            "hook": (f'<div class="frame" style="left:{x-2}px;top:{y-2}px;width:{bw+4}px;height:{bh+4}px"></div>'
                     f'<div class="abs" {col[:-1]};top:90px"><img class="logo" src="{LOGO}" alt="">'
                     f'<h1 style="margin-top:22px">{ad["hook"]}</h1></div>'),
            "prices": (f'<div class="abs" {col[:-1]};top:{y+bh+40}px"><div class="lines">{lines}</div>'
                       f'<div class="sub" style="margin-top:20px">Finery Room · Tati Siding</div></div>'),
            "cta": f'<div class="abs" {col[:-1]};top:{y+bh+250}px"><div class="cta">Book on WhatsApp {PHONE}</div></div>',
        }
    else:
        col = 'style="left:584px;right:44px;display:flex;flex-direction:column;gap:22px'
        parts = {
            "bg": '<div class="bg"></div>',
            "hook": (f'<div class="frame" style="left:{bw}px;top:0;width:0;height:1080px;border-width:0 0 0 2px"></div>'
                     f'<div class="abs" {col};top:110px"><img class="logo" src="{LOGO}" alt=""><h1>{ad["hook"]}</h1></div>'),
            "prices": (f'<div class="abs" {col};top:560px"><div class="lines">{lines}</div>'
                       f'<div class="sub">Finery Room · Tati Siding</div></div>'),
            "cta": f'<div class="abs" {col};top:800px"><div><div class="cta">Book on WhatsApp<br>{PHONE}</div></div></div>',
        }
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>{parts[part]}</body></html>'


def render(html, w, h, png, transparent):
    src = WORK / (png.stem + ".html")
    src.write_text(html, encoding="utf-8")
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
            "--virtual-time-budget=8000", f"--window-size={w},{h}", f"--screenshot={png}"]
    if transparent:
        args.append("--default-background-color=00000000")
    subprocess.run(args + [src.as_uri()], check=True, capture_output=True, timeout=90)


def motion_input(ad, fmt):
    """Return ffmpeg input args and a filter producing [m] sized to the photo box."""
    _, _, bw, bh = LAYOUT[fmt]["box"]
    if "clip" in ad:
        crop = ad["clip_crop"][fmt]
        return (["-stream_loop", "1", "-i", str(ad["clip"])],
                f"[1:v]{crop},scale={bw}:{bh},setsar=1,fps={FPS},trim=duration={DUR},setpts=PTS-STARTPTS[m]")
    still = ad["still"][fmt]
    frames = DUR * FPS
    # Fill the box first, then a slow centred zoom from 1.00 to 1.06.
    return (["-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(still)],
            f"[1:v]scale={bw*3}:{bh*3}:force_original_aspect_ratio=increase,crop={bw*3}:{bh*3},"
            f"zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={bw}x{bh}:fps={FPS},"
            f"setsar=1[m]")


def build(name, ad, fmt):
    L = LAYOUT[fmt]
    w, h = L["w"], L["h"]
    x, y, _, _ = L["box"]
    pngs = {}
    for part in ("bg", "hook", "prices", "cta"):
        png = WORK / f"{name}-{fmt}-{part}.png"
        render(layer_html(ad, fmt, part), w, h, png, transparent=(part != "bg"))
        pngs[part] = png
    m_args, m_filter = motion_input(ad, fmt)
    out = OUT / f"ad-{name}-{fmt}.mp4"
    filt = (f"{m_filter};"
            f"[0:v][m]overlay={x}:{y}[v1];"
            f"[2:v]format=rgba[hk];[v1][hk]overlay=0:0[v2];"
            f"[3:v]format=rgba,fade=t=in:st=2.5:d=0.5:alpha=1[pr];[v2][pr]overlay=0:0[v3];"
            f"[4:v]format=rgba,fade=t=in:st=5:d=0.5:alpha=1[ct];[v3][ct]overlay=0:0,format=yuv420p[out]")
    cmd = [FF, "-v", "error", "-y",
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(pngs["bg"]),
           *m_args,
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(pngs["hook"]),
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(pngs["prices"]),
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(pngs["cta"]),
           "-filter_complex", filt, "-map", "[out]", "-t", str(DUR), "-an",
           "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(out.relative_to(REPO), out.stat().st_size // 1024, "KB", flush=True)


if __name__ == "__main__":
    only = sys.argv[4:]
    for name, ad in ADS.items():
        for fmt in LAYOUT:
            if only and f"{name}-{fmt}" not in only:
                continue
            build(name, ad, fmt)
