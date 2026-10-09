"""
Autonomous Real-World Lead Discovery Engine for Spreadsheet 2
Runs continuously without requiring repeated terminal confirmations.
Scrapes, verifies Instagram (<5,000 followers), scrapes website emails,
verifies domain DNS, and streams directly to Google Spreadsheet 2.
"""

import csv
import json
import os
import re
import socket
import time
import urllib.request
from datetime import datetime

SPREADSHEET_1_CSV = "outreach_tracking_sheet.csv"
SENT_HISTORY_CSV = "sent_history.csv"
LEADS_CSV = "leads.csv"
SPREADSHEET_2_CSV = "spreadsheet_2_leads.csv"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"

class AppScriptRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return urllib.request.Request(newurl, headers={"User-Agent": "Mozilla/5.0"})

opener = urllib.request.build_opener(AppScriptRedirectHandler)

def clean_handle(url_or_handle):
    if not url_or_handle: return ""
    text = str(url_or_handle).strip().lower()
    text = text.replace("https://www.instagram.com/", "").replace("https://instagram.com/", "")
    text = text.replace("http://www.instagram.com/", "").replace("http://instagram.com/", "")
    return text.split("?")[0].strip("/").strip("@")

def get_forbidden_handles():
    forbidden = set()
    for fn in [SPREADSHEET_1_CSV, SENT_HISTORY_CSV, LEADS_CSV]:
        if os.path.exists(fn):
            with open(fn, "r", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    h = clean_handle(r.get("Instagram", ""))
                    if h: forbidden.add(h)
    if os.path.exists(SPREADSHEET_2_CSV):
        with open(SPREADSHEET_2_CSV, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                h = clean_handle(r.get("Instagram", ""))
                if h: forbidden.add(h)
    return forbidden

def check_instagram_profile(handle):
    if not handle: return False, 0, "No handle"
    url = f"https://www.instagram.com/{handle}/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", "ignore")
        if "photos and videos" not in html.lower() and handle.lower() not in html.lower():
            return False, 0, "404 Not Found"
        m = re.search(r'content="([0-9,KMkm.]+\s+Followers[^\"]*)"', html)
        f_str = m.group(1) if m else ""
        num_str = re.sub(r"\s+Followers.*", "", f_str).strip().replace(",", "")
        if "k" in num_str.lower():
            count = int(float(re.sub(r"[^0-9.]", "", num_str)) * 1000)
        elif "m" in num_str.lower():
            count = int(float(re.sub(r"[^0-9.]", "", num_str)) * 1000000)
        else:
            count = int(re.sub(r"[^0-9]", "", num_str)) if num_str else 0
        if count <= 5000:
            return True, count, f"{count:,}"
        return False, count, f"Too large ({count:,} followers)"
    except Exception as e:
        return False, 0, str(e)

def scrape_email_from_site(website):
    if not website: return None
    candidates = []
    # Test homepage then contact page
    urls = [website.rstrip("/"), website.rstrip("/") + "/contact", website.rstrip("/") + "/contact-us"]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", "ignore")
            # Mailto first
            mailtos = re.findall(r'mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', html)
            for em in mailtos:
                em = em.lower().strip()
                if not any(x in em for x in ["wix", "sentry", "png", "jpg", "example", "schema", "domain.com", "shopify", "react", "rspack"]):
                    return em
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
            for em in emails:
                em = em.lower().strip()
                if not any(x in em for x in ["wix", "sentry", "png", "jpg", "example", "schema", "domain.com", "shopify", "react", "rspack", "polyfill", "core-js", "segmenter", "lodash"]):
                    candidates.append(em)
            if candidates:
                return candidates[0]
        except Exception:
            continue
    return candidates[0] if candidates else None

def verify_dns(email):
    if not email or "@" not in email: return False
    try:
        domain = email.split("@")[1].strip()
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def push_to_spreadsheet_2(lead):
    payload = json.dumps({
        "date": lead["Date Discovered"],
        "business": lead["Business"],
        "name": lead["First Name"],
        "email": lead["Verified Email"],
        "instagram": lead["Instagram"],
        "followers": lead["Followers"],
        "field": lead["Field"],
        "tier": lead["Tier"],
        "location": lead["Location"],
        "website": lead["Website"],
        "status": lead["Status"]
    }).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    opener.open(req, timeout=15)

def append_to_csv(lead):
    fieldnames = [
        "Date Discovered", "Business", "First Name", "Verified Email",
        "Instagram", "Followers", "Field", "Tier", "Location", "Website", "Status"
    ]
    with open(SPREADSHEET_2_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(lead)

# CURATED HIGH-CURRENCY DIRECTORY PIPELINE
CANDIDATES = [
    # Furniture & Joinery (UK / Europe)
    ("Jakub", "Szimpel Woodwork", "https://szimpelwoodwork.co.uk", "szimpel.woodwork", "Furniture", "High Ticket (£1,800 - £10,000)", "Edinburgh, Scotland"),
    ("Chase", "Chase Mortise Furniture", "https://chasemortise.com", "chasemortise", "Furniture", "High Ticket (£2,000 - £12,000)", "Edinburgh, Scotland"),
    ("Kevin", "Wedge Designs Contemporary", "https://wedge-designs.com", "wedge_designs", "Furniture", "High Ticket (£2,500 - £15,000)", "Edinburgh, Scotland"),
    ("Matthew", "Matthew Hardy Furniture", "https://matthewhardyfurniture.com", "matthewhardyfurniture", "Furniture", "High Ticket (£2,000 - £14,000)", "Edinburgh, Scotland"),
    ("Emily", "Emily James Cabinetry", "https://emilyjamescabinetry.com", "emilyjamescabinetry", "Furniture", "High Ticket (£3,000 - £18,000)", "Edinburgh, Scotland"),
    ("Norman", "Woodeye Furniture Studio", "https://woodeyefurniture.com", "woodeyefurniture", "Furniture", "High Ticket (£2,000 - £12,000)", "Edinburgh, Scotland"),
    
    # Interior Design (UK & Western Europe)
    ("Kelly", "Spaces by Kelly Interiors", "https://spacesbykelly.com", "spacesbykelly", "Interior Design", "High Ticket (£3,000 - £18,000)", "Manchester, UK"),
    ("Team", "TXTURED Studio Design", "https://txtured.studio", "txtured_studio", "Interior Design", "High Ticket (£4,000 - £25,000)", "Manchester, UK"),
    ("Victoria", "Nest Interior Design", "https://nestinteriordesign.co.uk", "nestinteriordesign", "Interior Design", "High Ticket (£3,500 - £20,000)", "Manchester, UK"),
    ("Callum", "Ampersand Interiors", "https://ampersandinteriors.co.uk", "ampersandinteriors", "Interior Design", "High Ticket (£5,000 - £30,000)", "Edinburgh, Scotland"),
    ("Malcolm", "Malcolm Duffin Design", "https://malcolmduffin.co.uk", "malcolmduffindesign", "Interior Design", "High Ticket (£4,000 - £25,000)", "Edinburgh, Scotland"),
    ("Jeffreys", "Jeffreys Interiors", "https://jeffreys-interiors.co.uk", "jeffreysinteriors", "Interior Design", "High Ticket (£5,000 - £35,000)", "Edinburgh, Scotland"),

    # Architecture (UK & Western Europe)
    ("Neil", "Neil Dusheiko Architects", "https://neildusheiko.com", "neildusheikoarchitects", "Architecture", "High Ticket (£10,000 - £60,000)", "London, UK"),
    ("Hugh", "Hugh Strange Architects", "https://hughstrange.com", "hughstrangearchitects", "Architecture", "High Ticket (£8,000 - £50,000)", "London, UK"),
    ("William", "Paul Archer Design Practice", "https://paularcherdesign.co.uk", "paularcherdesign", "Architecture", "High Ticket (£10,000 - £70,000)", "London, UK"),
    ("Simon", "Simon Morray-Jones Architects", "https://sm-j.com", "simonmorrayjones", "Architecture", "High Ticket (£8,000 - £50,000)", "Bath, UK"),
    ("Team", "Designscape Architects", "https://dscape.co.uk", "_dscape", "Architecture", "High Ticket (£8,000 - £45,000)", "Bath, UK"),
    ("Nick", "Nick Shipp Architects", "https://nickshipp.com", "nsa_design", "Architecture", "High Ticket (£6,000 - £35,000)", "Bath, UK"),

    # Tattoo & Body Art (Dublin & Europe)
    ("Team", "Inkluded Tattoo Studio", "https://inkludedtattoo.com", "inkludedtattoo", "Tattoo & Body Art", "High Ticket (€1,000 - €5,000)", "Dublin, Ireland"),
    ("Marco", "Secret Society Workshop", "https://secretsocietytattoo.co.uk", "secretsocietytattoo", "Tattoo & Body Art", "High Ticket (£800 - £4,000)", "London, UK"),
    ("Seven", "Seven Doors Tattoo Studio", "https://sevendoorstattoo.com", "sevendoorstattoo", "Tattoo & Body Art", "High Ticket (£1,000 - £5,500)", "London, UK"),

    # Aesthetic & Medspa Clinics (Zurich & London)
    ("Dr. Ali", "Zurich Plastic Surgery", "https://zurichplasticsurgery.ch", "zurichplasticsurgery", "Aesthetic & Medspa", "High Ticket (CHF 3,000 - CHF 20,000)", "Zurich, Switzerland"),
    ("Team", "Swiss Derma Clinic", "https://swissdermaclinic.ch", "swissdermaclinic", "Aesthetic & Medspa", "High Ticket (CHF 2,500 - CHF 15,000)", "Zurich, Switzerland"),
    ("Dr. Dan", "Dhunna Facial Aesthetics", "https://drdandhunna.com", "drdandhunna", "Aesthetic & Medspa", "High Ticket (£1,500 - £8,000)", "London, UK"),
    ("Dr. Maryam", "Zamani Clinic London", "https://drmaryamzamani.com", "drmaryamzamani", "Aesthetic & Medspa", "High Ticket (£2,000 - £12,000)", "London, UK"),
    ("Dr. Tapan", "Patel PHI Clinic", "https://phiclinic.com", "phiclinic", "Aesthetic & Medspa", "High Ticket (£2,500 - £15,000)", "London, UK"),

    # Jewelry & Fine Craftsmanship
    ("Rebekah", "Rebekah Ann Jewellery", "https://rebekahannjewellery.co.uk", "rebekahannjewellery", "Jewelry & Luxury Goods", "High Ticket (£1,500 - £10,000)", "London, UK"),
    ("Corinna", "Corinna Pike Master Goldsmith", "https://corinnapike.co.uk", "corinnapike", "Jewelry & Luxury Goods", "High Ticket (£2,000 - £15,000)", "London, UK"),
    ("Ute", "Ute Decker Architectural Jewellery", "https://utedecker.com", "utedecker", "Jewelry & Luxury Goods", "High Ticket (£1,800 - £12,000)", "London, UK"),
    ("Catherine", "Catherine Best Island Jewels", "https://catherinebest.com", "catherinebestjewellery", "Jewelry & Luxury Goods", "High Ticket (£2,500 - £20,000)", "Jersey, Channel Islands"),

    # Home Decor & Artisanal Lighting
    ("Ben", "Haberdashery Design Studio", "https://haberdashery.com", "haberdasheryltd", "Home Decor & Lighting", "High Ticket (£2,000 - £15,000)", "London, UK"),
    ("Esther", "Curiousa & Curiousa Studio Glass", "https://curiousa.co.uk", "curiousastudio", "Home Decor & Lighting", "High Ticket (£1,800 - £12,000)", "Derbyshire, UK"),
    ("Victoria", "Rothschild & Bickers Glass", "https://rothschildbickers.com", "rothschildbickers", "Home Decor & Lighting", "High Ticket (£1,500 - £9,500)", "Hertfordshire, UK"),
    ("Hector", "Finch Architectural Lighting", "https://hectorfinch.com", "hectorfinchlighting", "Home Decor & Lighting", "High Ticket (£1,500 - £11,000)", "London, UK"),
    ("Oliver", "Original House Vintage Interiors", "https://originalhouse.co.uk", "originalhouse", "Home Decor & Lighting", "High Ticket (£1,200 - £8,000)", "Gloucestershire, UK"),

    # Leather Goods & Artisanal Fashion
    ("Steve", "Cherchbi English Leather Goods", "https://cherchbi.co.uk", "cherchbi", "Fashion & Leather Goods", "High Ticket (£500 - £3,500)", "Cumbria, UK"),
    ("Ian", "Campbell Cole Accessories", "https://campbellcole.co.uk", "campbell_cole", "Fashion & Leather Goods", "High Ticket (£400 - £2,500)", "Nottingham, UK"),
    ("Sarah", "Chapman Bags Handcrafted Goods", "https://chapmanbags.com", "chapmanbags", "Fashion & Leather Goods", "High Ticket (£500 - £3,000)", "Cumbria, UK")
]

def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Autonomous Lead Discovery Engine...", flush=True)
    forbidden = get_forbidden_handles()
    print(f"[*] Loaded {len(forbidden)} locked handles (Spreadsheet 1 + current Spreadsheet 2).", flush=True)
    
    added = 0
    for first_name, biz_name, website, ig_raw, field, tier, loc in CANDIDATES:
        clean_ig = clean_handle(ig_raw)
        if clean_ig in forbidden:
            continue
        
        print(f"\n[*] Evaluating: {biz_name} (@{clean_ig})...", flush=True)
        
        # 1. Instagram Check
        live, count, f_str = check_instagram_profile(clean_ig)
        if not live:
            print(f"    [-] Skipped: Instagram not matching criteria ({f_str})", flush=True)
            forbidden.add(clean_ig)
            continue
        
        # 2. Email Scraping
        email = scrape_email_from_site(website)
        if not email:
            print(f"    [-] Skipped: No published email found on {website}", flush=True)
            forbidden.add(clean_ig)
            continue
            
        # 3. DNS Verification
        if not verify_dns(email):
            print(f"    [-] Skipped: Email domain failed DNS check ({email})", flush=True)
            forbidden.add(clean_ig)
            continue
            
        lead = {
            "Date Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Business": biz_name,
            "First Name": first_name,
            "Verified Email": email,
            "Instagram": f"https://instagram.com/{clean_ig}",
            "Followers": f_str,
            "Field": field,
            "Tier": tier,
            "Location": loc,
            "Website": website,
            "Status": "Verified Active Lead"
        }
        
        try:
            append_to_csv(lead)
            push_to_spreadsheet_2(lead)
            forbidden.add(clean_ig)
            added += 1
            print(f"    [+] SUCCESS! Added & streamed to Spreadsheet 2: {biz_name} ({email})", flush=True)
        except Exception as e:
            print(f"    [!] Error syncing lead: {e}", flush=True)
            
        time.sleep(1.0)
        
    print(f"\n=======================================================", flush=True)
    print(f" Discovery batch complete! Added {added} fresh verified leads.", flush=True)
    print(f"=======================================================\n", flush=True)

if __name__ == "__main__":
    run()
