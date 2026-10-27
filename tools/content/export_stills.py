"""Export composites to the repo: WebP for the site, JPG for social posting.

Usage: python -I export_stills.py <composites_dir> <repo_dir> <upload_dir>
"""
import sys
from pathlib import Path
from PIL import Image

C = Path(sys.argv[1])
REPO = Path(sys.argv[2])
UP = Path(sys.argv[3])
IMG = REPO / "assets" / "img"
SOCIAL = IMG / "social"
for d in (IMG, SOCIAL, UP):
    d.mkdir(parents=True, exist_ok=True)

SITE_SIZES = {
    "4x5": [480, 960],      # gallery cards
    "16x9": [960, 1600],    # desktop hero poster
    "9x16": [540, 720],     # mobile hero poster
}

for hand in ("nails-1", "nails-2", "nails-3"):
    for fmt in ("9x16", "4x5", "1x1", "16x9"):
        im = Image.open(C / f"{hand}-{fmt}.png").convert("RGB")
        im.save(SOCIAL / f"{hand}-{fmt}.jpg", quality=86, optimize=True, progressive=True)
        for w in SITE_SIZES.get(fmt, []):
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(IMG / f"{hand}-{fmt}-{w}.webp", quality=80, method=6)
        if fmt in ("9x16", "16x9"):
            im.save(UP / f"{hand}-{fmt}.jpg", quality=94)

for p in sorted(IMG.rglob("*")):
    if p.is_file():
        print(f"{p.relative_to(REPO)}\t{p.stat().st_size // 1024} KB")
