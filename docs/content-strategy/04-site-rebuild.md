# Phase 4 — Site rebuilt as a selling page

Mobile screenshots at 390 px: [before](screenshots/before-home-390.jpg) · [after](screenshots/after-home-390.jpg)

## Page order

Every block ends with a **Book on WhatsApp** button. A sticky WhatsApp button stays on screen on phones.

1. **Hero.** "Nails & lashes in Tati Siding", then "Lashes from P70 · Nails from P80", the hours and the service area. Behind it is a real nail photo. A slow CSS push-in and light sweep animate it; there's no AI video, so the nails can't change. The motion switches off for reduced-motion and Save-Data visitors.
2. **Our Work.** 6 real photos (3 nails, 3 lashes) with All / Nails / Lashes filters.
3. **Services & prices.** The exact six prices. Every row opens WhatsApp with its own message, for example "I'd like to book a Classic Lash Set". Refill timing is explained: P40 within 2 weeks instead of P70.
4. **How booking works.** Message → pick a time → deposit if asked → arrive on time, with the no-show rule.
5. **Why Finery Room.** Four factual points only.
6. **Care Guide.** Five lash tips and four nail tips.
7. **FAQ,** plus the "Ask Finery Room" assistant (already on `main`).
8. **Find us.** Address, "serving Tati Siding and Francistown", the map, hours (every day 7:00–17:00), phone, Facebook.

**Hero headline alternatives** for a later A/B test:
- "Fresh nails. Full lashes. Right here in Tati Siding."
- "Your nail and lash studio in New Stands, Tati Siding."

## Removed

- The three placeholder testimonials. They were made up.
- These invented details: the 24-hour notice rule, the deposit rollover and deduction, the "Orange Money / eWallet" payment methods, "hospital-grade", "medical adhesives", "climate-tested", the "4–6 weeks" claim, and the wrong hours.
- The VIP list, which promised discounts that haven't been approved.
- The Instagram and Facebook placeholder links. Facebook now shows as plain text until the real link is supplied.

## Speed (Lighthouse 12.2.1, mobile, simulated slow 4G, local)

| | Before | After |
|---|---|---|
| Performance | 70 | **94** |
| Accessibility | 98 | **100** |
| Best Practices | 100 | 100 |
| SEO | 100 | 100 |
| Page weight | 696 KiB | **369 KiB** |
| LCP | 2.8 s | **2.4 s** |
| Total blocking time | 700 ms | **0 ms** |

**What changed:**
- WebP images with phone-sized variants, plus width and height on every image.
- 2 font families instead of 4, loaded without blocking the first paint.
- Icons are written once and reused.
- The 89 KB header logo became a 2 KB WebP.
- `server.js` now gzips text like the live host, so local scores are comparable. Its `no-store` header is the remaining bf-cache warning; that's dev-only.

## Waiting on the owner

- **Deposit payment number:** the number supplied has 7 digits after `+267`. Botswana mobile numbers have 8, so it isn't published until it's confirmed. The site says the details are sent on WhatsApp.
- **Facebook page link:** to make "Katlego Thale" clickable.
- **Care Guide wording:** the owner should check it matches the advice she gives clients.
- **Offers and gift vouchers:** no offer section yet. The plan's three offers are still marked [PROPOSED — needs owner approval].
