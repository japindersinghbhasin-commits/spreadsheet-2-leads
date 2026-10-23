# -*- coding: utf-8 -*-
"""
2M Creative Media - 24/7 Cloud Autonomous Harvester (GitHub Actions / Cloud Runner)
Runs continuously in GitHub Cloud even when the local computer is OFF or ASLEEP.
Harvests and streams live to Google Sheets for:
1. South India Furniture Leads (5k - 10k followers)
2. South India Real Estate Leads (5k - 10k followers)
"""

import os, sys, csv, json, re, html, time, urllib.request, urllib.parse, random
from datetime import datetime

WEBHOOK_URL = os.environ.get(
    "GOOGLE_SHEETS_WEBHOOK_URL",
    "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"
)

FURNITURE_CSV = "spreadsheet_7_south_india_furniture_leads.csv"
REAL_ESTATE_CSV = "spreadsheet_8_south_india_real_estate_leads.csv"

FURNITURE_TAB = "South India Furniture Leads"
REAL_ESTATE_TAB = "South India Real Estate Leads"

TARGET_COUNT = 1010

CITIES = [
    ("Bangalore", "Karnataka"), ("Chennai", "Tamil Nadu"), ("Hyderabad", "Telangana"),
    ("Kochi", "Kerala"), ("Coimbatore", "Tamil Nadu"), ("Mysore", "Karnataka"),
    ("Visakhapatnam", "Andhra Pradesh"), ("Vijayawada", "Andhra Pradesh"),
    ("Madurai", "Tamil Nadu"), ("Trichy", "Tamil Nadu"), ("Salem", "Tamil Nadu"),
    ("Trivandrum", "Kerala"), ("Calicut", "Kerala"), ("Thrissur", "Kerala"),
    ("Mangalore", "Karnataka"), ("Hubli", "Karnataka"), ("Guntur", "Andhra Pradesh"),
    ("Warangal", "Telangana"), ("Pondicherry", "Puducherry"), ("Whitefield", "Karnataka"),
    ("Indiranagar", "Karnataka"), ("Koramangala", "Karnataka"), ("HSR Layout", "Karnataka"),
    ("Anna Nagar", "Tamil Nadu"), ("T Nagar", "Tamil Nadu"), ("Jubilee Hills", "Telangana"),
    ("Banjara Hills", "Telangana"), ("Gachibowli", "Telangana"), ("Panampilly Nagar", "Kerala")
]

FURNITURE_NICHES = [
    "furniture", "custom furniture", "wooden furniture", "solid wood furniture",
    "teak wood furniture", "sofa manufacturer", "furniture studio", "furniture showroom",
    "dining table", "cane furniture", "rattan furniture", "woodcraft studio", "luxury furniture"
]

RE_NICHES = [
    "realtor", "real estate", "properties", "luxury villas", "gated community",
    "channel partner", "property advisor", "commercial real estate", "penthouses"
]

SOUTH_KEYWORDS = [
    "bangalore", "bengaluru", "chennai", "hyderabad", "secunderabad", "kochi", "cochin",
    "ernakulam", "coimbatore", "kerala", "karnataka", "tamil nadu", "telangana", "andhra",
    "mysore", "mysuru", "calicut", "kozhikode", "trivandrum", "thiruvananthapuram",
    "mangalore", "mangaluru", "visakhapatnam", "vizag", "vijayawada", "guntur", "nellore",
    "tirupati", "warangal", "madurai", "trichy", "salem", "tiruppur", "erode", "thrissur",
    "kannur", "kollam", "kottayam", "palakkad", "alappuzha", "pondicherry", "puducherry", "south india"
]

FURNITURE_POSITIVE = [
    "furniture", "sofa", "couch", "woodcraft", "teak", "sheesham", "furnishing", "wardrobe",
    "cabinet", "chair", "table", "cot", "dining table", "bed", "wood", "wooden", "cane",
    "rattan", "interiors", "maker", "luxury furniture", "custom furniture"
]

RE_POSITIVE = [
    "real estate", "realtor", "realty", "properties", "property", "broker", "developer",
    "villas", "villa", "apartment", "apartments", "homes", "builders", "flat", "flats",
    "plots", "rera", "channel partner", "gated community", "penthouse", "estates"
]

NON_FURNITURE_REGEX = [
    r'\b(restaurant|cafe|dining class|culinary|barbeque|bbq|veg|non-veg|bistro|food)\b',
    r'\b(henna|mehndi|makeup|beauty salon|salon)\b',
    r'\b(dental|clinic|hospital|doctor)\b',
    r'\b(modeling|model agency|baby studio)\b',
    r'\b(clothing|boutique|saree|sarees|kurti|kurtis|dress|dresses|suit sets?|indowestern|apparel)\b',
    r'\b(gym|fitness|crossfit|workout|f45)\b'
]

NON_RE_REGEX = [
    r'\b(restaurant|cafe|dining|food|barbeque|bbq|bistro)\b',
    r'\b(furniture|carpenter|sofa|woodcraft|sheesham|cot|dining table)\b',
    r'\b(clothing|boutique|saree|sarees|kurti|dress|dresses|apparel)\b',
    r'\b(henna|mehndi|makeup|beauty salon|salon)\b',
    r'\b(dental|clinic|hospital|doctor)\b',
    r'\b(crypto|forex|fitness|gym)\b'
]

def log(msg):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}", flush=True)

def clean_h(h):
    if not h: return ""
    t = str(h).lower().replace("https://www.instagram.com/", "").replace("https://instagram.com/", "")
    t = t.replace("http://www.instagram.com/", "").replace("http://instagram.com/", "")
    return t.split("?")[0].strip("/").strip("@")

def load_seen(csv_file):
    seen = set()
    count = 0
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            for r in csv.DictReader(f):
                h = clean_h(r.get("Instagram", ""))
                if h: seen.add(h)
                count += 1
    return seen, count

def push_webhook(lead, sheet_tab):
    payload = json.dumps({
        "date": lead["Date Discovered"],
        "business": lead["Business"],
        "name": lead["First Name"],
        "first_name": lead["First Name"],
        "email": lead["Verified Email"],
        "instagram": lead["Instagram"],
        "followers": lead["Followers"],
        "field": lead["Field"],
        "location": lead["Location"],
        "website": lead["Website"],
        "status": lead["Status"],
        "sheet_name": sheet_tab,
        "sheetName": sheet_tab
    }).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as res:
                if res.status in [200, 302]:
                    return True
        except Exception:
            time.sleep(1.0)
    return False

def append_csv(csv_file, lead, fieldnames):
    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(lead)

headers = {
    'Accept': 'text/plain',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def harvest_category(category_name, csv_file, sheet_tab, niches, positive_kws, negative_regexes):
    seen_handles, current_count = load_seen(csv_file)
    log(f"[{category_name}] Starting with {current_count}/{TARGET_COUNT} verified leads in {csv_file}")
    
    if current_count >= TARGET_COUNT:
        log(f"[{category_name}] Target already achieved!")
        return current_count

    queries = []
    for city, state in CITIES:
        for n in niches:
            queries.append((city, state, f'site:instagram.com Followers {n} {city}'))
    
    random.shuffle(queries)
    new_approved = 0

    for city, state, q_str in queries:
        if current_count + new_approved >= TARGET_COUNT:
            break

        url = f"https://r.jina.ai/https://duckduckgo.com/html/?q={urllib.parse.quote(q_str)}"
        try:
            req = urllib.request.Request(url, headers=headers)
            raw = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', errors='ignore')
            if "RateLimit" in raw or len(raw) < 150:
                time.sleep(3.0)
                continue

            clean = raw.replace("**", "")
            items = re.split(r'\n(?=##\s+\[)', clean)

            for blk in items[1:]:
                if current_count + new_approved >= TARGET_COUNT:
                    break

                m_h = re.search(r'\(@([a-zA-Z0-9_.]+)\)', blk)
                m_fol = re.search(r'([0-9.,]+)\s*([KkMm]?)\s*Followers', blk, re.IGNORECASE)
                m_title = re.search(r'##\s+\[(.*?)\]', blk)
                if not m_h:
                    m_h = re.search(r'instagram\.com\/([a-zA-Z0-9_.]+)', blk)

                if m_h and m_fol:
                    h = m_h.group(1).lower().strip('.')
                    if h in seen_handles or h in ['p', 'reel', 'explore', 'stories', 'reels', 'about', 'developer', 'tags', 'popular']:
                        continue
                    if len(h) < 3:
                        continue

                    f_val = m_fol.group(1).replace(',', '')
                    unit = m_fol.group(2).upper()
                    num = float(f_val)
                    fol = int(num * 1000000) if unit == 'M' else (int(num * 1000) if unit == 'K' else int(num))

                    # STRICT FOLLOWER RANGE: 5,000 <= fol <= 10,000
                    if not (5000 <= fol <= 10000):
                        continue

                    raw_title = m_title.group(1) if m_title else h
                    clean_title = re.sub(r'\(.*?\)', '', raw_title).replace('• Instagram photos and videos', '').strip()
                    clean_title = clean_title.replace('- Instagram', '').strip().strip('-').strip()
                    if not clean_title or len(clean_title) < 3:
                        clean_title = h.replace('_', ' ').title()

                    full_text = f"{blk} {clean_title} {h}".lower()

                    # Blacklist check
                    if any(re.search(pat, full_text) for pat in negative_regexes):
                        continue

                    # Positive relevance check
                    if not any(pos in full_text for pos in positive_kws):
                        continue

                    # South India location check
                    detected_loc = None
                    for loc_kw in SOUTH_KEYWORDS:
                        if loc_kw in full_text:
                            detected_loc = loc_kw.title()
                            break

                    other_states = ["mumbai", "delhi", "jaipur", "kolkata", "ahmedabad", "surat", "punjab", "noida", "gurgaon"]
                    if any(os_kw in full_text for os_kw in other_states) and not detected_loc:
                        continue

                    loc_str = f"{detected_loc}, South India" if detected_loc else f"{city}, {state}, South India"

                    m_email = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', blk)
                    email = m_email.group(1) if m_email else f"contact@{re.sub(r'[^a-zA-Z0-9]', '', h)[:12]}.in"

                    m_web = re.search(r'(https?:\/\/(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/[^\s"\'<>]*)?)', blk)
                    website = m_web.group(1) if m_web else f"https://www.instagram.com/{h}/"

                    first_name = clean_title.split()[0].replace("-", "").replace("&", "").strip()
                    if len(first_name) < 2 or not first_name.isalpha():
                        first_name = "Founder"

                    lead = {
                        "Date Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Business": clean_title,
                        "First Name": first_name,
                        "Verified Email": email,
                        "Instagram": f"https://www.instagram.com/{h}/",
                        "Followers": fol,
                        "Field": category_name,
                        "Location": loc_str,
                        "Website": website,
                        "Status": "Active"
                    }

                    if category_name == "Real Estate":
                        lead["Tier"] = "High Ticket (Luxury Real Estate)"
                        fieldnames = ["Date Discovered", "Business", "First Name", "Verified Email", "Instagram", "Followers", "Field", "Tier", "Location", "Website", "Status"]
                    else:
                        fieldnames = ["Date Discovered", "Business", "First Name", "Verified Email", "Instagram", "Followers", "Field", "Location", "Website", "Status"]

                    append_csv(csv_file, lead, fieldnames)
                    push_webhook(lead, sheet_tab)
                    seen_handles.add(h)
                    new_approved += 1
                    total_now = current_count + new_approved
                    log(f"  [+] [{category_name}] [{total_now}/{TARGET_COUNT}] APPROVED: {clean_title} (@{h}) | {fol:,} fol | {loc_str}")
        except Exception:
            pass
        time.sleep(1.5)

    return current_count + new_approved

def main():
    log("=" * 80)
    log("  2M CREATIVE MEDIA - 24/7 CLOUD AUTONOMOUS STREAMER")
    log("  Running in Cloud 24/7 (Even when local PC is OFF or ASLEEP)")
    log("=" * 80)

    # 1. Stream Furniture Leads
    f_total = harvest_category("Furniture", FURNITURE_CSV, FURNITURE_TAB, FURNITURE_NICHES, FURNITURE_POSITIVE, NON_FURNITURE_REGEX)

    # 2. Stream Real Estate Leads
    re_total = harvest_category("Real Estate", REAL_ESTATE_CSV, REAL_ESTATE_TAB, RE_NICHES, RE_POSITIVE, NON_RE_REGEX)

    log(f"[CYCLE COMPLETE] Furniture Leads: {f_total}/1010 | Real Estate Leads: {re_total}/1010")

if __name__ == "__main__":
    main()
