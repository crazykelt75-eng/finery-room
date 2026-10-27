# Phase 1 — Site audit (before any changes)

Audited 27 Oct 2026 on `main` at commit `1a7e894`, plus the uncommitted FAQ-assistant changes in the working tree. Checked at 390 px wide in the browser and with Lighthouse 12.2.1 (mobile, simulated slow 4G).

Screenshot: [before-home-390.jpg](screenshots/before-home-390.jpg)

## Audit table

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Hero answers what / where / what you get / how to book in 5 seconds | **FAIL** | The H1 is just "Finery Room" and the tagline. "Nails and lashes" only appears in a paragraph further down, there are no prices in the hero, and there's no photo. The location badge and the Book on WhatsApp button do pass. |
| 2 | Prices visible without hunting | PASS | The price list is the second section, and the hero has a "View Prices" button. All six prices match Part 1. |
| 3 | One-tap WhatsApp booking with a prefilled message | PASS | Header, hero, both service cards, the refill callout and the floating button all open `wa.me/26776584100` with a prefilled message. The messages are per category ("Lashes appointment"), not per service, and none are tagged for counting. |
| 4 | Real work photos high on the page | **FAIL** | The first photo starts about 1,250 px down, which is 1.5 phone screens. All 6 photos are real work, but all 3 lash photos show identifiable client faces, and consent isn't on file. |
| 5 | "How booking works" steps, with the deposit and on-time policies | **FAIL** | There are no steps. The Policies block adds terms that aren't in the business facts: 24-hour notice, the deposit being deducted from the bill, deposits rolling over, and "cannot be refunded". |
| 6 | Benefits, FAQ, map, hours, phone | **FAIL** | The FAQ, map (general Tati Siding area) and phone are there. The **hours are wrong**: the site says Mon–Fri 08:30–17:30 and Sat 08:00–18:00, the facts say 7am–5pm, and a visible "[Studio Hours — Placeholder]" tag is showing. The benefits list makes unverified claims: "hospital-grade sanitation", "climate-tested retention" and "premium medical adhesives". |
| 7 | A booking button after every block | **FAIL** | No booking button follows the Gallery (it ends with an Instagram link), Reviews, Policies or FAQ blocks. |
| 8 | Real reviews section | **FAIL — hard rule** | Three made-up testimonials with names (Tshepiso M., Amantle K., Lorato S.) and 5 stars are live on the page. Each carries only a small "[Verified Review · Placeholder]" tag. One claims a set "lasted over 3 weeks". |
| 9 | Mobile speed | **FAIL** | Lighthouse mobile scores: Performance **70**, Accessibility 98, Best Practices 100, SEO 100. FCP/LCP 2.8 s, TBT 700 ms, Speed Index 5.0 s, 696 KiB in total. Images are JPEG only, with no `srcset` and no width/height (about 410 KiB could be saved). 6 Google font files add about 207 KiB across 4 families. Most main-thread time (about 4 s) goes to style and layout on the document, not to `script.js`. |
| 10 | Local SEO: title, description, structured data, share image | **FAIL** | The title and meta description are good. The BeautySalon JSON-LD exists but has the wrong hours, invented payment methods ("Orange Money, eWallet…") and a relative image URL. `og:image` is the square logo, not a 1200×630 share image. `og:url` points to `fineryroom.bw`, which doesn't resolve. The keywords mention Francistown, which isn't confirmed. |
| 11 | Retention | **FAIL** | There's a refill callout (P40) and a VIP WhatsApp list, which is good. There's no care guide or refill reminder. The Instagram (`@fineryroom_bw`) and Facebook (`facebook.com/fineryroom`) links are placeholders; the facts list Facebook as "katlego thale". The VIP block promises "seasonal discounts" that haven't been approved. |

### Other fact problems found

- FAQ: "A full classic set can last anywhere from 4 to 6 weeks". This is an unverified longevity claim.
- Gallery subtitle: "photographed directly in our Tati Siding studio under clean ring light, with zero misleading filters". At least two lash photos were clearly taken on a sofa, not under a ring light.
- Refill callout: "Natural lashes cycle out over 14 days". This is an unverified claim.
- Hero pillar: "Location: Tatisiding Newstance", copied from the ad card. Everywhere else says "New Stands, Tati Siding".
- `README.md` repeats the invented 24-hour cancellation rule and the deposit-credit rule.

## Top 5 fixes, ranked by likely effect on bookings

1. **Rebuild the hero.** "Nails & lashes in Tati Siding", "Lashes from P70 · Nails from P80" and Book on WhatsApp, over a real nail photo or motion loop. Right now a visitor sees a brand name, not an offer.
2. **Remove what breaks trust.** Take out the fake reviews and replace them with a "Leave us a review" link. Correct the hours to 7am–5pm. Remove the invented policies, claims and payment methods. Fix the social links.
3. **Put real work in the first screen.** Use the hands-only nail photos now, add a Nails / Lashes filter, and hold back lash face photos until consent is in writing.
4. **Make booking effortless after every block.** Add a 4-step "How booking works" block, put a booking button after every section, and give each service its own prefilled, tagged WhatsApp message (`?src=`).
5. **Speed and retention together.** Switch to WebP with responsive sizes, cut down to 2 font families, and add a 1200×630 share image. Add the Care Guide and an explanation of refill timing, so clients come back every 2 weeks.
