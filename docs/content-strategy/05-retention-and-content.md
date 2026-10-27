# Phases 5 and 6 — Retention and content engine

## Delivered

| Item | Where |
|---|---|
| Lash & Nail Aftercare Guide (1-page A4 PDF, 210 KB) | `assets/care-guide.pdf`, linked from the site's Care Guide section. Source: `marketing/care-guide/care-guide.html` |
| WhatsApp templates: booking confirmation, day-before reminder, day-12 refill nudge, thank-you, photo permission | `marketing/whatsapp-templates.md` (to be saved as Quick Replies; nothing sends automatically) |
| Gift voucher design (1600×900), drafts at P40, P70, P80 and P150 | `marketing/vouchers/` (not on the site) |
| Video ads, 3 styles in 9:16 and 1:1, 10 s, silent | `assets/ads/ad-{premium,problem,refill}-{9x16,1x1}.mp4` |
| 30-day calendar (13 posts, Mon/Wed/Fri) | `marketing/content-calendar.md` |
| 10 faceless video scripts | `marketing/video-scripts.md` |
| Weekly refresh prompt and safety checklist | `WEEKLY_REFRESH.md` |
| Reusable content scripts | `tools/content/` |

**How the video ads keep the work truthful:**
- *Premium* uses the one AI clip that passed the frame check.
- *Problem* and *Refill* use a slow, uniform zoom on real photos. No AI touches them.
- All text is layered on from HTML.

## Tap tracking (proposal, needs your OK)

Every booking button carries a `data-src` tag: `hero`, `work`, `price-classic-set`, `refill-callout`, `sticky` and so on. That way each WhatsApp tap can be counted by where it came from.

The site has no analytics yet. **Recommendation:** [GoatCounter](https://www.goatcounter.com/). It's free for small sites and uses no cookies, so no consent banner is needed. It can count clicks per button with one script tag and a few lines of code.

A second option is Cloudflare Web Analytics. It's free on the current host, but it only counts page views, not button taps.

**Nothing is added until you approve.**

## Still waiting on the owner

- **Offers:** the three in `02-plan.md` (Refill Club, First-visit welcome, Nails + lashes in one visit) are still [PROPOSED — needs owner approval], so the site has no offers block.
- **Voucher values:** P40, P70, P80 and P150 are suggestions. Also needed: who issues voucher numbers, and how long vouchers are valid.
- **Deposit:** the FNB PayToCell number (to confirm) and the deposit amount. The booking template has blanks for both.
- **Facebook page link:** so the site and templates can link to it.
- **Care-tip wording:** the owner should confirm it matches the advice she gives.
