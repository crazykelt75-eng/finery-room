# Phase 7 — Quality check

Run on 27 Oct 2026 on the `content-strategy` branch. Automated checks: `python -I tools/content/qc.py .`

## What failed

**Nothing in the final automated run.** The checker covers the page, the care guide source, the ad scripts and every file in `marketing/`. It was also tested against planted errors: a wrong price, a wrong phone number, "guaranteed", "100% safe" and "lasts 6 weeks". All were caught.

Items rejected earlier and kept out of the site:

| Item | Reason |
|---|---|
| AI upscale of `work-nails-1` and `work-nails-3` | Changed the bead charm and the daisy petals. The originals are used instead. |
| Motion clips for `nails-1` and `nails-3` | The charm and beads morphed, and the little-finger nail changed shape. |
| 16:9 hero clip | Slight drift in the gold charm. The site uses CSS motion on the real still instead. |

## Checklist

| Check | Result |
|---|---|
| Name, phone, prices, location match the business facts | Pass. Only P10/P30/P40/P50/P70/P80 appear (P150 only on the draft vouchers); only +267 765 841 00; New Stands, Tati Siding. |
| Hours | Pass. "Every day, 7am–5pm" in the copy and 07:00–17:00 Mon–Sun in the structured data. |
| Gallery vs originals | Pass. See [`qa/gallery-vs-original.jpg`](qa/gallery-vs-original.jpg): hand pixels are identical, only the background changed. Lash photos are crops only. |
| No fake reviews, unapproved offers or misleading claims | Pass. The reviews section and VIP discounts are removed, no offers are published, and there are no week-count promises. |
| No AI artefacts | Pass on everything shipped. Each still was compared at full zoom, and the accepted clip was checked frame by frame. |
| Every button opens WhatsApp with the right number and message | Pass. All 19 links go to 26776584100, each with its own `data-src` tag and prefilled text. |
| Lighthouse mobile ≥ 85 / ≥ 90 / ≥ 90 | Pass. **Performance 96, Accessibility 100, Best Practices 100, SEO 100.** LCP 1.6 s, CLS 0, 297 KiB loaded. |
| Page weight under about 1.5 MB | Pass. 297–369 KiB across runs. |
| Works from 360 px wide | Pass. No sideways scroll at 360 or 390 px, and every tap target is at least 40 px tall. |

## Notes for Phase 8

- **`.assetsignore`** keeps `docs/`, `marketing/`, `tools/`, the Markdown files and the dev scripts out of the published site. Cloudflare Workers static assets reads this file. After the first deploy, check that `/docs/` and `/README.md` return 404.
- **The bf-cache warning** in Lighthouse comes from the local dev server's `no-store` header, not from the live host.
- **Not checked on a real phone yet.** That happens after deploy (Phase 8).
