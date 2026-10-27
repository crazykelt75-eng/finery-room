# Content tools

These are the local scripts used for Batch 1. They need Python 3 with Pillow, Google Chrome, and ffmpeg (`winget install Gyan.FFmpeg`). Run every Python script with `python -I`.

| Script | What it does | Usage |
|---|---|---|
| `compose.py` | Puts real hand cutouts (pixels unchanged) on the brand backdrops in 9:16, 4:5, 1:1 and 16:9. | `python -I compose.py <masters_dir> <out_dir>` |
| `export_stills.py` | Writes site WebP sizes and social JPGs into `assets/img/`. | `python -I export_stills.py <composites_dir> <repo_dir> <upload_dir>` |
| `ads.py` | Renders the static ads and the 1200×630 share image. Prices and phone are typed in the script. | `python -I ads.py <composites_dir> <repo_dir> <work_dir>` |
| `video_ads.py` | Builds 10-second video ads: hook from 0 s, prices from 2.5 s, call to action from 5 s. | `python -I video_ads.py <scratch_dir> <repo_dir> <ffmpeg.exe> [name-format ...]` |

**What goes in `<masters_dir>`** (downloaded from Higgsfield, kept outside the repo):
- `nails-N-cutout.png` from `image_background_remover`
- `backdrop-amethyst-16x9.png`, `backdrop-amethyst-9x16.png` and `backdrop-ivory-1x1.png`

Edit the `HANDS`, `ADS` and `SOURCES` tables at the top of each script for new photos.

Before anything is published, compare every output with its original (see `WEEKLY_REFRESH.md`).
