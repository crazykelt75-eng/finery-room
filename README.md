# Finery Room — Luxury Beauty Experience

Official production marketing website for **Finery Room**, a premier eyelash extensions and nail artistry private studio located in **Tati Siding, New Stands, Botswana**.

---

## 💎 Brand Identity & Visual Language

- **Positioning**: Accessible Botswana Pula pricing with an uncompromising high-fashion, private-appointment editorial aesthetic.
- **Background**: Near-black warm plum base (`#0A090C`) with luminous ambient amethyst silk gradient glows.
- **Accent Purple**: Rich royal amethyst (`#9B59B6`) sampled directly from the "F" monogram and border flourish.
- **Secondary Accent**: Soft glowing lavender (`#C9A7E0`) for section eyebrows, dividers, and iconography.
- **Typography**:
  - Headings & Wordmark: High-contrast fashion-editorial serifs (`Bodoni Moda` & `Playfair Display`).
  - Body & UI: Clean, geometric sans-serif (`Jost` & `Work Sans`).
  - Signatures: Classic script (`Great Vibes`).
- **Signature Motifs**:
  - Thin double hairline rules centered with a delicate fleur-de-lis motif.
  - Rounded-rectangle bordered cards with full-width photography.
  - Floating WhatsApp booking trigger with pulse beacon.

---

## 📋 Verified Price List (Botswana Pula — BWP)

### Lashes
- **Classic Set**: `P70` — Natural, lightweight bespoke full set tailored to client eye curvature.
- **Refill (2 Weeks)**: `P40` — Infill and density restoration (recommended every 14 days).
- **Lash Removal**: `P30` — Gentle, non-damaging professional adhesive removal.

### Nails
- **Full Set**: `P80` — Precision tip sculpt, apex balancing, and radiant gel polish.
- **Toes**: `P50` — Dry pedicure prep, cuticle cleanup, and long-wear gel overlay.
- **Nail Repair (per nail)**: `P10` — Quick rescue for broken, chipped, or split nails.

---

## 📜 Studio Policies (Warm but Firm)
1. **Deposit Requirement**: A deposit may be required to secure a booking slot (credited toward service total).
2. **Arrival Time**: Please arrive on time; sessions cannot be extended into the next client's reservation.
3. **No-Show Policy**: No-shows will not be rebooked. Cancellations require 24 hours notice on WhatsApp.

---

## 📍 Studio Location & Contact
- **Address**: New Stands, Tati Siding, North-East District, Botswana
- **WhatsApp / Calls**: `+267 765 841 00`
- **WhatsApp Booking Link**: `https://wa.me/26776584100`

---

## 🚀 Local Development & Preview

Run a static web server locally:

```bash
# Using Python:
python -m http.server 3000

# Or using Node:
npx http-server -p 3000
```
Open `http://localhost:3000` in any browser.

---

## 🌐 Deployment Options

### 1. GitHub Repository
Initialize and push to your GitHub account:
```bash
git remote add origin https://github.com/YOUR_USERNAME/finery-room.git
git branch -M main
git push -u origin main
```

### 2. Supabase Storage Static Web Hosting
You can deploy these static files to a public Supabase Storage bucket (`site` or `public-web`) using the provided script `deploy-supabase.js`:
```bash
# Install dependency:
npm install @supabase/supabase-js

# Set environment variables:
set SUPABASE_URL=https://your-project.supabase.co
set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Run deployment:
node deploy-supabase.js
```

### 3. GitHub Pages / Vercel / Netlify
Because this site is built with modern vanilla HTML5, CSS3, and JavaScript, it can be deployed with zero build configuration to GitHub Pages, Vercel, or Netlify with 100% instant load speeds on mobile WhatsApp browsers.
