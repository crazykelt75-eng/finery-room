# Phase 3 — Batch 1 results

Run on 27 Oct 2026 with an approved budget of 50 credits. **40.25 credits were spent**, leaving 59.75 on the account. Every generation, prompt and accept/reject decision is logged in [`assets/manifest.json`](../../assets/manifest.json).

## What shipped

| Asset | Files | Notes |
|---|---|---|
| Cleaned stills, 3 photos × 4 formats | `assets/img/social/nails-{1,2,3}-{1x1,4x5,9x16,16x9}.jpg` | Ready to post as feed 1:1, feed ad 4:5, Reels/Status 9:16, or 16:9. |
| Site-sized WebP | `assets/img/nails-*-{4x5,9x16,16x9}-{width}.webp` | Gallery cards are 15–60 KB each. Hero posters are for desktop (16:9) and mobile (9:16). |
| Share image | `assets/img/share-1200x630.jpg` | For `og:image` and WhatsApp/Facebook link previews. |
| Static ads, 3 styles × 2 formats | `assets/ads/ad-{premium,problem,refill}-{9x16,1x1}.jpg` | Prices and phone number typed from Part 1. Text never sits on the nails. |
| Side-by-side check | [`qa/gallery-vs-original.jpg`](qa/gallery-vs-original.jpg) | Original vs. cleaned still, for all 3 photos. |

**How the truthful-portfolio rule was kept:**
- The background remover returned hand pixels **identical** to the input (0.0 mean difference inside the hand mask).
- The nails are never regenerated. Only the background was replaced and a soft shadow added.
- `nails-3` was shot from above, so it sits on the top-down ivory satin instead of the upright drape.
- The small pink nail at its edge is the client's own thumb, so it stays.

## What was rejected, and why

| Item | Credits | Reason |
|---|---|---|
| AI upscale of `work-nails-1` | 2 | Redrew the bead charm on the index nail. That photo uses the original pixels, resized normally. |
| AI upscale of `work-nails-3` | 2 | Lost the petals of the daisy on the accent nail. That photo uses the original pixels too. |
| Motion clip `nails-1` (9:16) | 5 | The gold charm and beads change shape mid-clip. |
| Motion clip `nails-3` (9:16) | 5 | The little-finger nail becomes longer and lighter. |
| Hero loop (16:9) | 8 | Not rejected outright, but the gold charm drifts slightly. It isn't used on the site. |

The `nails-2` upscale and its motion clip passed. The clip is held back until it can be compressed (ffmpeg is needed).

**Lesson for the weekly refresh:** image-to-video models redraw fine nail art (charms, beads, small flowers). Plain colours and simple French tips hold up much better. For the site hero, a CSS push-in and light sweep over the real still gives the same feel, with zero risk to the nails and almost no extra page weight.

## Not done yet, and what's needed

- **Video ads and the accepted Reels clip** need ffmpeg to compress and to add text. Only the static ads are done.
- **Before/after ad and gift-voucher ad** need a real before/after pair and approved voucher values.
- **Studio set and lash content** need studio photos, plus written consent for the lash photos that show faces.
