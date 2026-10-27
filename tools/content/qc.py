"""Phase 7 quality check: facts, links, claims and images. Prints only failures.

Usage: python -I tools/content/qc.py <repo_dir>
Exit code 1 if anything failed.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

REPO = Path(sys.argv[1]).resolve()
PRICES = {"P10", "P30", "P40", "P50", "P70", "P80"}
VOUCHER_ONLY = {"P150"}  # Classic Set + Full Set; only allowed on voucher drafts and planning notes
PHONE_DISPLAY = "+267 765 841 00"
PHONE_LINK = "26776584100"

# Customer-facing text. docs/ is excluded on purpose: it records what was removed.
PUBLIC = [REPO / "index.html", REPO / "marketing" / "care-guide" / "care-guide.html",
          REPO / "tools" / "content" / "ads.py", REPO / "tools" / "content" / "video_ads.py",
          *sorted((REPO / "marketing").glob("*.md"))]
BANNED = [
    r"guarantee", r"100\s*%\s+[a-z]", r"hospital", r"medical", r"clinical", r"\b\d+\s*(?:to|-|–)\s*\d+\s*weeks",
    r"lasts? \d+ weeks", r"orange money", r"ewallet", r"24 hours", r"testimonial", r"★",
    r"08:30", r"17:30", r"18:00", r"advance booking", r"instagram\.com/fineryroom", r"facebook\.com/fineryroom",
    r"\bdiscount(?:ed)? (?:price|of|on)\b", r"% off", r"\bfree (?:set|refill|repair)",
]

failures = []


def fail(where, msg):
    failures.append(f"{where}: {msg}")


# 1. Facts in customer-facing text
for path in PUBLIC:
    if not path.exists():
        fail(path.relative_to(REPO), "file missing")
        continue
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(REPO).as_posix()
    for m in re.finditer(r"(?<![\w#])P(\d{1,4})\b", text):
        tok = "P" + m.group(1)
        if tok not in PRICES and not (tok in VOUCHER_ONLY and "voucher" in text.lower()):
            line = text.count("\n", 0, m.start()) + 1
            fail(f"{rel}:{line}", f"price {tok} is not on the price list")
    for m in re.finditer(r"\+?267[\d\s]{7,12}\d", text):
        digits = re.sub(r"\D", "", m.group(0))
        if digits != PHONE_LINK:
            line = text.count("\n", 0, m.start()) + 1
            fail(f"{rel}:{line}", f"unexpected phone number {m.group(0).strip()}")
    for pat in BANNED:
        for m in re.finditer(pat, text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            fail(f"{rel}:{line}", f"banned or unapproved wording: {m.group(0)!r}")


# 2. Links, images and structured data on the page
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.ld, self._in_ld, self.srcsets = [], [], [], False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a)
        if tag == "img":
            self.imgs.append(a)
        if tag in ("img", "source") and a.get("srcset"):
            self.srcsets.append(a["srcset"])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_ld:
            self.ld[-1] += data


page = Page()
page.feed((REPO / "index.html").read_text(encoding="utf-8"))

wa_messages = []
for a in page.links:
    href = a["href"]
    if "wa.me" in href:
        u = urlparse(href)
        if u.path.strip("/") != PHONE_LINK:
            fail("index.html", f"WhatsApp link to wrong number: {href}")
        text = unquote(parse_qs(u.query).get("text", [""])[0])
        wa_messages.append((a.get("data-src", "-"), text))
        if a.get("data-src") is None and a.get("id") != "faqAssistantWhatsApp":
            fail("index.html", f"booking link without data-src tag: {href[:60]}")
    if href.startswith("tel:") and re.sub(r"\D", "", href) != PHONE_LINK:
        fail("index.html", f"tel link to wrong number: {href}")
    if not href.startswith(("http", "#", "tel:", "mailto:")) and not (REPO / href.split("#")[0]).exists():
        fail("index.html", f"broken local link: {href}")

for img in page.imgs:
    if "alt" not in img:
        fail("index.html", f"image without alt: {img.get('src')}")
    if not img.get("width") or not img.get("height"):
        fail("index.html", f"image without width/height: {img.get('src')}")
    if not (REPO / img["src"]).exists():
        fail("index.html", f"missing image file: {img['src']}")
for srcset in page.srcsets:
    for part in srcset.split(","):
        src = part.strip().split(" ")[0]
        if not (REPO / src).exists():
            fail("index.html", f"missing srcset file: {src}")

for block in page.ld:
    try:
        data = json.loads(block)
        hours = data["openingHoursSpecification"][0]
        if (hours["opens"], hours["closes"], len(hours["dayOfWeek"])) != ("07:00", "17:00", 7):
            fail("index.html", "JSON-LD hours do not match 7am-5pm every day")
        if data["telephone"] != "+" + PHONE_LINK:
            fail("index.html", "JSON-LD phone does not match")
        listed = sorted(int(o["price"]) for o in data["hasOfferCatalog"]["itemListElement"])
        if listed != [10, 30, 40, 50, 70, 80]:
            fail("index.html", f"JSON-LD prices {listed} do not match the price list")
    except (ValueError, KeyError, IndexError) as e:
        fail("index.html", f"JSON-LD problem: {e}")

# 3. Every logged asset exists
manifest = json.loads((REPO / "assets" / "manifest.json").read_text(encoding="utf-8"))
for entry in manifest["files"]:
    if not (REPO / entry["file"]).exists():
        fail("assets/manifest.json", f"logged file is missing: {entry['file']}")

print("WhatsApp buttons checked:", len(wa_messages))
for src, text in wa_messages:
    print(f"  {src:<20} {text}")
if failures:
    print(f"\n{len(failures)} FAILED:")
    print("\n".join("  " + f for f in failures))
    sys.exit(1)
print("\nAll checks passed.")
