# Weekly refresh

Paste this into Claude Code every Monday, from this repository, with the Higgsfield connector on:

> It's Monday. Take the new real photos in raw-photos/new/, make 3 fresh Higgsfield variations of each within [CREDIT BUDGET], add the best to the gallery, prepare 3 posts and 1 WhatsApp Status, update manifest.json, and run the Phase 7 check.

Replace **[CREDIT BUDGET]** with the week's limit before pasting. The first batch used about 40 credits for 3 photos.

## How to do it safely (lessons from Batch 1)

1. **Real photos only.** Put the week's phone photos in `raw-photos/new/`: daylight, plain background, hands only unless the client agreed in writing (use template `/photo` in `marketing/whatsapp-templates.md`).
2. **Show the plan and cost first.** Before any generation, list how many generations it needs and the estimated credits (use `get_cost`), then wait for the owner's OK.
3. **Never let AI redraw the nails.**
   - *Background:* use `image_background_remover` (1 credit). It returned the hand pixels unchanged in Batch 1. Then place the hand on a brand backdrop locally.
   - *AI upscaling:* don't use it on detailed nail art. It redrew a bead charm and lost daisy petals in Batch 1. Resize the original instead.
   - *Image-to-video:* only on simple designs (plain colour, French tips), and only after a frame-by-frame check. Charms, beads and small flowers morphed in 2 of 3 clips.
4. **Side-by-side check.** Compare every result with the original at full zoom. Reject it if the shape, colour, length, design, finish or finger count changed.
5. **Text is never AI-drawn.** Prices, the phone number and the logo are added from HTML templates by the scripts in `tools/content/` (`ads.py`, `video_ads.py`).
6. **Compress before committing.**
   - Images: WebP for the site, JPG for social.
   - Video: H.264, CRF 24–26, no audio, `+faststart`.
7. **Log everything** in `assets/manifest.json`: file, source photo, model, prompt, date, where it's used, and accepted or rejected (with the reason).

## Phase 7 check (run every week)

- Names, phone (`+267 765 841 00`), prices (P70 / P40 / P30 / P80 / P50 / P10) and location (New Stands, Tati Siding) match exactly.
- Hours read "every day, 7am–5pm".
- Gallery images compared side by side with their originals.
- No made-up reviews, unapproved offers or claims such as "lasts 6 weeks" or "100% safe".
- No AI artefacts: fingers, nails, text, logo.
- Every booking button opens WhatsApp to 26776584100 with the right message.
- Lighthouse mobile: Performance ≥ 85, Accessibility ≥ 90, SEO ≥ 90. The home page stays under about 1.5 MB.
