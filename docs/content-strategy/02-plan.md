# Phase 2 — Plan (waiting for approval)

Nothing below has been generated, edited or spent yet. Reply **"approved"**, or say what to change, and answer the open questions at the end.

## Starting point

| Item | Status |
|---|---|
| Higgsfield | Connected. **100 credits**, Plus plan. |
| `raw-photos/` | **Doesn't exist.** The only real work photos are the 6 already in `assets/`. |
| Nail photos (`work-nails-1/2/3.jpg`) | Usable now: real work, hands only, 768–816 × 1024 px, sharp enough. `work-nails-3` is the darkest (mean brightness 86/255), so it needs the most relighting. |
| Lash photos (`work-lashes-1/2/3.jpg`) | **On hold.** All 3 show identifiable client faces, and there's no written consent on file. |
| Studio photos | **None.** The studio set and walkthrough are blocked until 3–5 are supplied. |
| Before/after pairs | **None.** The before/after ad is blocked. |
| Reviews | **None real.** The page will show a "Leave us a review" link instead. |
| Local media tools | Pillow (WebP, crops, layouts) and Chrome (PDF export) are installed. **ffmpeg is not installed**; it's needed for video compression and the video ads. |

## 1. New page structure (Phase 4 order)

The same **Book on WhatsApp** button closes every block, and the sticky WhatsApp button stays on mobile. Every service gets its own prefilled message, and every button gets a `data-src` tag so taps can be counted.

1. **Hero.** One of the headline options below, then "Lashes from P70 · Nails from P80" and Book on WhatsApp. A muted, looping nail clip plays behind it, with a poster image. It isn't loaded on Save-Data or reduced-motion.
   - A: *Nails & lashes in Tati Siding, booked in one WhatsApp message.*
   - B: *Fresh nails. Full lashes. Right here in Tati Siding.*
   - C: *Your nail and lash studio in New Stands, Tati Siding.*
2. **Proof.** A real-work gallery with Nails / Lashes filters, then studio photos once supplied, then real reviews or a "Leave us a review" link.
3. **Services & prices.** The exact six prices. The refill is explained: *refill within 2 weeks for P40 instead of a new Classic Set at P70*.
4. **How booking works.** Message on WhatsApp → pick a time → pay a deposit if asked → arrive on time. "No-shows will not be rebooked", said kindly.
5. **Why Finery Room.** Only benefits the owner approves. The draft is below.
6. **Care Guide.** 5 short aftercare tips, a PDF download and links to the tip videos.
7. **Offers & gift vouchers.** Only offers the owner has approved.
8. **FAQ.** How long a set lasts (no unverified week counts), when to refill, deposits, lateness, removal, how to prepare.
9. **Find us.** Map, hours (7am–5pm), phone, Facebook.

**Removed or merged:**
- The 3 fake testimonials are removed.
- About becomes Why Finery Room.
- Policies becomes How booking works, using only the three real policies.
- The VIP list is dropped. It promises discounts that haven't been approved.
- The unverified claims are removed: hospital-grade, medical adhesives, climate-tested, 4–6 weeks, 24-hour notice, deposit rollover.

**Draft "Why Finery Room" points** [PROPOSED — needs owner approval]: nails and lashes in one studio · clear prices in Pula · book in one WhatsApp message · a refill reminder so lashes stay full.

## 2. Asset list

Prices come from live `get_cost` checks on 27 Oct 2026. Crops, layouts, ad text and PDFs are made locally for free, so prices and the phone number are typed exactly and never drawn by AI.

**How the "truthful portfolio" rule is kept:** the real hand and nail pixels are cut out (background remover) and placed on a brand backdrop. The nails themselves are never regenerated. Only light tone and white-balance fixes are made locally. If a composite looks pasted on, the fallback is a masked edit that changes the background only, never the hand (`nano_banana_2` inpaint, 2 cr each). Every result gets a side-by-side check against the original.

### Batch 1: can run as soon as this is approved

| # | Asset | Source photo | Higgsfield model | Ratio | Length | Credits |
|---|---|---|---|---|---|---|
| 1 | Upscale ×3 | work-nails-1, 2, 3 | `bytedance_image_upscale` (2k) | original | — | 6.0 |
| 2 | Background removal ×3 (real hands kept) | outputs of #1 | `image_background_remover` | original | — | 3.0 |
| 3 | Brand backdrops ×3 (decorative only, no hands) | text prompt | `gpt_image_2_5` (high, 2k) | 16:9, 9:16, 1:1 | — | 8.25 |
| 4 | Cleaned stills ×3 → 1:1, 4:5, 9:16, 16:9 and a 1200×630 share image | #2 on #3 | local (Pillow) | all | — | 0 |
| 5 | Motion clips ×3: slow push-in, light sweeping the gloss, no text | 9:16 stills from #4 | `seedance_2_0_mini` (720p, silent) | 9:16 (1:1 cropped locally) | 5 s | 15.0 |
| 6 | Hero loop ×1 | strongest 16:9 still | `seedance_2_0_mini` (720p, silent) | 16:9 | 8 s | 8.0 |
| 7 | Ads ×3 (premium, problem-focused, refill reminder) in 9:16 and 1:1 | #4, #5, logo | local layout + ffmpeg | 9:16, 1:1 | 6–10 s | 0 |
| | Retry buffer (about 25%, for rejected artefacts) | | | | | 10.0 |
| | **Batch 1 total** | | | | | **≈ 50** |

### Batch 2: blocked until material or approval arrives

| # | Asset | Needs | Model | Credits |
|---|---|---|---|---|
| 8 | Studio set: 3–5 enhanced photos, plus an optional 10 s walkthrough | 3–5 studio photos | `bytedance_image_upscale` + `seedance_2_0_mini` | ≈ 20 |
| 9 | Lash stills and 2 clips | Written consent, or eye-only crops you approve | upscale + `seedance_2_0_mini` | ≈ 14 |
| 10 | Real before/after ad | A real before/after photo pair | local layout (+ optional clip) | 0–5 |
| 11 | Gift voucher ad and voucher designs | Voucher values chosen | local layout | 0 |
| | **Batch 2 total** | | | **≈ 35–40** |

I recommend running Batch 1 now, holding the rest of the 100 credits for Batch 2 and the first weekly refresh, and showing the exact count before every batch.

### Ad scripts (prices exactly as in Part 1)

| Style | Hook (first 3 s) | Middle | End |
|---|---|---|---|
| Premium | "Nails that feel like a treat." | Full Set P80 · Toes P50 · Tati Siding | Book on WhatsApp +267 765 841 00 |
| Problem-focused | "Chipped nails before the weekend?" | Nail Repair P10 per nail · Full Set P80 | Book on WhatsApp +267 765 841 00 |
| Refill reminder | "Day 12? Your lashes are due." | Refill within 2 weeks P40, instead of a new set at P70 | Book on WhatsApp +267 765 841 00 |
| Before/after | *(blocked: needs a real pair)* | | |
| Gift voucher | *(blocked: needs voucher values)* | | |

## 3. Brand style lock

This is added to every Higgsfield prompt.

- **Palette, sampled from the logo:**
  - Ink `#050507` (site background `#0A090C`)
  - Amethyst `#885C99` (the "F"; site accent `#9B59B6`)
  - Lavender `#C9A7E0`
  - Ivory `#F5F4F2` (the "R")
- **Lighting:** soft, diffused key light from the upper left. One gentle highlight runs along the gel gloss. No harsh hotspots. Shadows are deep plum, not crushed black.
- **Background:** a smooth amethyst-to-ink gradient or out-of-focus satin drape. Plain, with no props competing with the hands.
- **Mood words:** polished · intimate · glowing.

**Prompt pattern:**

> *[subject from the real photo]* + change only: *[light / background / camera move]* + keep exactly: nail shape, colour, length, design, finish and hand anatomy, 5 fingers + brand style lock + *[ratio, length]* + no text, no logos.

## 4. Offers [PROPOSED — needs owner approval]

**A. Refill Club** (uses existing prices, no discount)
- **Result:** lashes that stay full.
- **Problem:** a set thins out, and a new one costs P70.
- **Risk removed:** the owner sends a WhatsApp reminder on day 12, so the 2-week window isn't missed.
- **Speed:** a short refill visit instead of a full new set. [confirm]
- **Entry price:** P40.
- **Bonus:** the day-12 reminder.
- **Call to action:** *Book my P40 refill.*

**B. First-visit welcome**
- **Result:** try Finery Room with nothing to lose.
- **Problem:** worry about a new nail or lash tech.
- **Risk removed:** [PROPOSED] a free repair of one nail within 7 days if it chips (P10 value).
- **Entry price:** Classic Set P70 or Full Set P80.
- **Bonus:** the free repair above.
- **Call to action:** *Book my first visit.*

**C. Nails + lashes in one visit**
- **Result:** hands and eyes done in one trip.
- **Problem:** two bookings, two trips.
- **Speed:** both done back to back. [confirm this is possible]
- **Price:** P150 at list prices. [PROPOSED] a bundle price of P140.
- **Call to action:** *Book nails + lashes.*

**Gift vouchers** [PROPOSED]: values that match the services (P40 / P70 / P80 / P150), sold and confirmed by the owner on WhatsApp.

## Open questions (needed before Phase 3)

1. **[CREDIT BUDGET]**: how many of the 100 credits may this round use? I recommend 50 for Batch 1.
2. **Hours:** "7am to 5pm" on which days? Is the studio closed on Sundays?
3. **Francistown:** is it part of the service area, so it can stay in the copy and SEO?
4. **Lash photos:** is there written consent from the 3 clients whose faces show? If not, lash content waits.
5. **More material:** please add a `raw-photos/` folder with 3–5 studio photos, more hands-only nail shots, close-up lash shots, and any real before/after pairs.
6. **Reviews:** are there any real ones with permission? Which link should "Leave us a review" use: the exact Facebook page URL, or a Google Business Profile?
7. **FAQ assistant:** the uncommitted n8n form uses a webhook that's still inactive. Should it be included in this branch, committed separately first, or left out?
8. **Live site address and hosting:** `fineryroom.bw` doesn't resolve, and the deploy scripts point to Supabase. This is needed for `og:url`, the share image and Phase 8.
9. **ffmpeg:** OK to install it (`winget install Gyan.FFmpeg`)? Without it there's no hero video and no video ads, only stills.
10. **Deposit payment methods:** the site says Orange Money and eWallet. Confirm them, or remove them.

Note: Batch 1 uploads the 3 hands-only nail photos to Higgsfield. No face photos are uploaded without consent.
