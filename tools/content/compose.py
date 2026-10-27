"""Place real hand cutouts (pixels untouched) on the AI brand backdrops.

Usage: python -I compose.py <masters_dir> <out_dir>
Only the backdrop and a soft contact shadow are added; the hand layer is
scaled uniformly and never recoloured.
"""
import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops

M = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

BACKDROPS = {
    "wide": M / "backdrop-amethyst-16x9.png",
    "tall": M / "backdrop-amethyst-9x16.png",
    "topdown": M / "backdrop-ivory-1x1.png",
}

# Which canvas edges each hand's arm exits through in the source photo.
# nails-3 was shot from above, so it sits on the top-down satin backdrop.
HANDS = {
    # Shot against a white light, so its edge needs a 2px trim to lose the white rim.
    "nails-1": {"file": "nails-1-cutout.png", "anchor": {"bottom"}, "erode": 5},
    "nails-2": {"file": "nails-2-cutout.png", "anchor": {"left"}},
    "nails-3": {"file": "nails-3-cutout.png", "anchor": {"top", "right"}, "backdrop": "topdown"},
}

FORMATS = {
    # name: (W, H, backdrop, max hand height frac, max width frac, x centre frac, y centre frac)
    "9x16": (1080, 1920, "tall", 0.62, 0.92, 0.50, 0.66),
    "4x5": (1080, 1350, "tall", 0.80, 0.88, 0.50, 0.58),
    "1x1": (1080, 1080, "tall", 0.84, 0.84, 0.50, 0.55),
    "16x9": (1920, 1080, "wide", 0.88, 0.52, 0.70, 0.55),
}


def cover(img, w, h, valign=1.0):
    """Resize to cover w×h and crop; valign 1.0 keeps the bottom (the surface)."""
    s = max(w / img.width, h / img.height)
    r = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (r.width - w) // 2
    y = round((r.height - h) * valign)
    return r.crop((x, y, x + w, y + h))


def largest_component(alpha):
    """Mask of the largest opaque region, so stray objects at the photo edge drop out."""
    sw = 240
    sh = round(alpha.height * sw / alpha.width)
    small = alpha.resize((sw, sh)).point(lambda v: 255 if v > 64 else 0)
    px = small.load()
    seen = set()
    best = []
    for sy in range(sh):
        for sx in range(sw):
            if px[sx, sy] and (sx, sy) not in seen:
                comp, stack = [], [(sx, sy)]
                seen.add((sx, sy))
                while stack:
                    cx, cy = stack.pop()
                    comp.append((cx, cy))
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < sw and 0 <= ny < sh and px[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                if len(comp) > len(best):
                    best = comp
    keep = Image.new("L", (sw, sh), 0)
    kp = keep.load()
    for cx, cy in best:
        kp[cx, cy] = 255
    keep = keep.filter(ImageFilter.MaxFilter(5)).resize(alpha.size, Image.BILINEAR)
    return keep.point(lambda v: 255 if v > 0 else 0)


def clean_alpha(cut, erode=3):
    a = cut.getchannel("A")
    a = ImageChops.multiply(a, largest_component(a))
    a = a.filter(ImageFilter.MinFilter(erode)).filter(ImageFilter.GaussianBlur(0.7))
    out = cut.copy()
    out.putalpha(a)
    return out


def compose(hand, fmt):
    W, H, bd, fh, fw, cx, cy = FORMATS[fmt]
    spec = HANDS[hand]
    cut = clean_alpha(Image.open(M / spec["file"]).convert("RGBA"), spec.get("erode", 3))
    l, t, r, b = cut.getchannel("A").getbbox()
    bw, bh = r - l, b - t
    s = min(fh * H / bh, fw * W / bw)
    cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
    l, t, r, b = (round(v * s) for v in (l, t, r, b))
    bw, bh = r - l, b - t
    anchor = spec["anchor"]

    x = round(cx * W - bw / 2) - l
    y = round(cy * H - bh / 2) - t
    if "left" in anchor:
        x = -l
    if "right" in anchor:
        x = W - r
    if "top" in anchor:
        y = -t
    if "bottom" in anchor:
        y = H - b

    bd = spec.get("backdrop", bd)
    valign = 0.5 if bd == "topdown" else 1.0
    canvas = cover(Image.open(BACKDROPS[bd]).convert("RGB"), W, H, valign).convert("RGBA")

    # Soft contact shadow from the hand's own silhouette.
    shadow_a = Image.new("L", (W, H), 0)
    shadow_a.paste(cut.getchannel("A"), (x + round(W * 0.012), y + round(H * 0.016)))
    shadow_a = shadow_a.filter(ImageFilter.GaussianBlur(W * 0.018)).point(lambda v: v * 0.42)
    shadow = Image.new("RGBA", (W, H), (26, 15, 34, 0))
    shadow.putalpha(shadow_a)
    canvas = Image.alpha_composite(canvas, shadow)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(cut, (x, y), cut)
    canvas = Image.alpha_composite(canvas, layer)
    return canvas.convert("RGB")


if __name__ == "__main__":
    for hand in HANDS:
        for fmt in FORMATS:
            img = compose(hand, fmt)
            img.save(OUT / f"{hand}-{fmt}.png")
            print(hand, fmt, img.size)
