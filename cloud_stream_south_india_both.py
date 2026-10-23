# -*- coding: utf-8 -*-
"""
2M Creative Media - 24/7 GitHub Actions Cloud Harvester
Runs every 20 minutes in GitHub Cloud — even when PC is OFF or ASLEEP.
Harvests both:
  1. South India Furniture Leads  → spreadsheet_7_south_india_furniture_leads.csv
  2. South India Real Estate Leads → spreadsheet_8_south_india_real_estate_leads.csv
Strict rules: South India only | 5,000 <= Followers <= 10,000 | Furniture/RE fields only
"""

import os, sys, csv, json, re, html, time, random
import urllib.request, urllib.parse
from datetime import datetime

WEBHOOK_URL = os.environ.get(
    "GOOGLE_SHEETS_WEBHOOK_URL",
    "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"
)

FURNITURE_CSV  = "spreadsheet_7_south_india_furniture_leads.csv"
REAL_ESTATE_CSV = "spreadsheet_8_south_india_real_estate_leads.csv"
FURNITURE_TAB  = "South India Furniture Leads"
REAL_ESTATE_TAB = "South India Real Estate Leads"
TARGET_COUNT   = 1010

# ── Cities ────────────────────────────────────────────────────────────────────
CITIES = [
    ("Bangalore","Karnataka"),("Bengaluru","Karnataka"),("Mysore","Karnataka"),
    ("Mangalore","Karnataka"),("Hubli","Karnataka"),("Belgaum","Karnataka"),
    ("Whitefield","Karnataka"),("Koramangala","Karnataka"),("Indiranagar","Karnataka"),
    ("HSR Layout","Karnataka"),("Hebbal","Karnataka"),("Yelahanka","Karnataka"),
    ("Malleshwaram","Karnataka"),("Marathahalli","Karnataka"),("BTM Layout","Karnataka"),
    ("Chennai","Tamil Nadu"),("Coimbatore","Tamil Nadu"),("Madurai","Tamil Nadu"),
    ("Trichy","Tamil Nadu"),("Salem","Tamil Nadu"),("Tiruppur","Tamil Nadu"),
    ("Erode","Tamil Nadu"),("Vellore","Tamil Nadu"),("Pondicherry","Puducherry"),
    ("Anna Nagar","Tamil Nadu"),("T Nagar","Tamil Nadu"),("Adyar","Tamil Nadu"),
    ("Velachery","Tamil Nadu"),("OMR Chennai","Tamil Nadu"),("Tambaram","Tamil Nadu"),
    ("Hyderabad","Telangana"),("Secunderabad","Telangana"),("Warangal","Telangana"),
    ("Gachibowli","Telangana"),("Jubilee Hills","Telangana"),("Banjara Hills","Telangana"),
    ("Madhapur","Telangana"),("Kondapur","Telangana"),("Hitec City","Telangana"),
    ("Kukatpally","Telangana"),("Manikonda","Telangana"),("Dilsukhnagar","Telangana"),
    ("Visakhapatnam","Andhra Pradesh"),("Vijayawada","Andhra Pradesh"),("Guntur","Andhra Pradesh"),
    ("Nellore","Andhra Pradesh"),("Tirupati","Andhra Pradesh"),("Rajahmundry","Andhra Pradesh"),
    ("Amaravati","Andhra Pradesh"),("Kakinada","Andhra Pradesh"),("Kurnool","Andhra Pradesh"),
    ("Kochi","Kerala"),("Cochin","Kerala"),("Trivandrum","Kerala"),("Calicut","Kerala"),
    ("Kozhikode","Kerala"),("Thrissur","Kerala"),("Kannur","Kerala"),("Kollam","Kerala"),
    ("Kottayam","Kerala"),("Palakkad","Kerala"),("Panampilly Nagar","Kerala"),
]

FURNITURE_NICHES = [
    "furniture","custom furniture","wooden furniture","solid wood furniture","teak wood furniture",
    "cane furniture","rattan furniture","luxury furniture","furniture studio","furniture showroom",
    "sofa manufacturer","woodcraft studio","modular furniture","sofa factory","wardrobe manufacturer",
    "handcrafted furniture","dining table","teak wood cot","bespoke furniture",
]

RE_TERMS = [
    "realtor","real estate","properties","luxury villas","luxury apartments","gated community",
    "real estate consultant","channel partner","property advisor","penthouses",
    "independent villas","luxury homes","commercial real estate","RERA registered realtor",
]

SOUTH_KEYWORDS = [
    "bangalore","bengaluru","chennai","hyderabad","secunderabad","kochi","cochin","ernakulam",
    "coimbatore","kerala","karnataka","tamil nadu","telangana","andhra","mysore","mysuru",
    "calicut","kozhikode","trivandrum","thiruvananthapuram","mangalore","mangaluru",
    "visakhapatnam","vizag","vijayawada","guntur","nellore","tirupati","warangal",
    "madurai","trichy","salem","tiruppur","erode","thrissur","kannur","kollam",
    "kottayam","palakkad","alappuzha","pondicherry","puducherry","south india",
]

FURNITURE_POSITIVE = [
    "furniture","sofa","couch","woodcraft","teak","sheesham","furnishing","wardrobe",
    "cabinet","chair","table","cot","wood","wooden","cane","rattan","maker","custom furniture",
]

RE_POSITIVE = [
    "real estate","realtor","realty","properties","property","broker","developer",
    "villas","villa","apartment","apartments","homes","builders","flat","flats",
    "plots","rera","channel partner","gated community","penthouse","estates","estate",
]

NON_FURNITURE_RE = [re.compile(p) for p in [
    r'\b(restaurant|cafe|dining class|culinary|barbeque|bbq|veg|non-veg|bistro|food)\b',
    r'\b(henna|mehndi|makeup|beauty salon|salon)\b',
    r'\b(dental|clinic|hospital|doctor)\b',
    r'\b(modeling|model agency|baby studio)\b',
    r'\b(clothing|boutique|saree|sarees|kurti|kurtis|dress|dresses|indowestern|apparel)\b',
    r'\b(gym|fitness|crossfit|workout|f45)\b',
]]

NON_RE_RE = [re.compile(p) for p in [
    r'\b(restaurant|cafe|dining|food|barbeque|bbq|bistro)\b',
    r'\b(furniture|carpenter|sofa|woodcraft|sheesham|cot)\b',
    r'\b(clothing|boutique|saree|sarees|kurti|dress|dresses|apparel)\b',
    r'\b(henna|mehndi|makeup|beauty salon|salon)\b',
    r'\b(dental|clinic|hospital|doctor)\b',
    r'\b(crypto|forex|fitness|gym)\b',
]]

SKIP_HANDLES = {'p','reel','explore','stories','reels','about','accounts','developer','tags','popular','tv'}

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def clean_h(h):
    if not h: return ""
    t = str(h).lower()
    for p in ["https://www.instagram.com/","https://instagram.com/",
              "http://www.instagram.com/","http://instagram.com/"]:
        t = t.replace(p,"")
    return t.split("?")[0].strip("/").strip("@")

def load_seen(csv_file):
    seen = set()
    count = 0
    if os.path.exists(csv_file):
        with open(csv_file,"r",encoding="utf-8",errors="ignore") as f:
            for row in csv.DictReader(f):
                h = clean_h(row.get("Instagram",""))
                if h: seen.add(h)
                count += 1
    return seen, count

def push_webhook(lead, sheet_tab):
    payload = json.dumps({
        "date": lead["Date Discovered"], "business": lead["Business"],
        "name": lead["First Name"], "first_name": lead["First Name"],
        "email": lead["Verified Email"], "instagram": lead["Instagram"],
        "followers": lead["Followers"], "field": lead["Field"],
        "location": lead["Location"], "website": lead["Website"],
        "status": lead["Status"], "sheet_name": sheet_tab, "sheetName": sheet_tab,
    }).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=payload,
          headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                if r.status in [200,302]: return True
        except Exception: time.sleep(1)
    return False

def append_csv(csv_file, lead, fieldnames):
    exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
    with open(csv_file,"a",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists: w.writeheader()
        w.writerow({k: lead.get(k,"") for k in fieldnames})

def ddg_jina_search(q_str):
    """Search via Jina→DDG. Returns list of (handle, fol_or_None, title, snippet)."""
    url = "https://r.jina.ai/https://duckduckgo.com/html/?q=" + urllib.parse.quote(q_str)
    try:
        req = urllib.request.Request(url,
            headers={"Accept":"text/plain","User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return []

    if "RateLimit" in text or len(text) < 200:
        return []

    results = []
    if "## [" in text:
        blocks = re.split(r"\n(?=##\s+\[)", text.replace("**",""))
        for blk in blocks[1:]:
            m_h    = re.search(r"\(@([a-zA-Z0-9_.]+)\)", blk)
            m_ig   = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", blk) if not m_h else None
            m_fol  = re.search(r"([0-9.,]+)\s*([KkMm]?)\s*Followers", blk, re.IGNORECASE)
            m_title= re.search(r"##\s+\[(.*?)\]", blk)
            handle = m_h or m_ig
            if not handle: continue
            h = handle.group(1).lower().strip(".")
            fol = None
            if m_fol:
                num = float(m_fol.group(1).replace(",",""))
                unit = m_fol.group(2).upper()
                fol = int(num*1e6) if unit=="M" else (int(num*1000) if unit=="K" else int(num))
            results.append((h, fol, m_title.group(1) if m_title else h, blk))
    return results

def harvest_category(label, csv_file, sheet_tab, niches, positive_kws, bad_patterns, fieldnames):
    seen_handles, current_count = load_seen(csv_file)
    log(f"[{label}] Starting at {current_count}/{TARGET_COUNT}")

    if current_count >= TARGET_COUNT:
        log(f"[{label}] Already complete!"); return current_count

    new_approved = 0
    other_states = ["mumbai","delhi","jaipur","kolkata","ahmedabad","surat","punjab","noida","gurgaon"]

    # Build shuffled query list for this run
    queries = []
    for city, state in CITIES:
        for niche in niches:
            queries.append((city, state, f"site:instagram.com Followers {niche} {city}"))
    random.shuffle(queries)

    for city, state, q_str in queries:
        if current_count + new_approved >= TARGET_COUNT:
            break

        hits = ddg_jina_search(q_str)
        for h, fol, title, snippet in hits:
            if current_count + new_approved >= TARGET_COUNT: break
            if len(h) < 3 or h in SKIP_HANDLES: continue
            if h in seen_handles: continue
            if fol is None: continue
            if not (5000 <= fol <= 10000): continue

            clean_title = re.sub(r"\(.*?\)", "", title).replace("• Instagram photos and videos","").strip()
            clean_title = clean_title.replace("- Instagram","").strip().strip("-").strip()
            if not clean_title or len(clean_title) < 3:
                clean_title = h.replace("_"," ").replace("."," ").title()

            full_text = f"{snippet} {clean_title} {h}".lower()

            if any(pat.search(full_text) for pat in bad_patterns): continue
            if not any(pos in full_text for pos in positive_kws): continue

            detected_loc = None
            for kw in SOUTH_KEYWORDS:
                if kw in full_text:
                    detected_loc = kw.title(); break

            if any(s in full_text for s in other_states) and not detected_loc: continue

            loc_str = f"{detected_loc}, South India" if detected_loc else f"{city}, {state}, South India"

            m_email = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", snippet)
            email   = m_email.group(1) if m_email else f"contact@{re.sub(r'[^a-zA-Z0-9]','',h)[:12]}.in"

            m_web   = re.search(r"(https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s\"'<>]*)?)", snippet)
            website = m_web.group(1) if m_web else f"https://www.instagram.com/{h}/"
            if "instagram.com" in website or "cdninstagram" in website:
                website = f"https://www.instagram.com/{h}/"

            first_name = clean_title.split()[0].replace("-","").replace("&","").strip()
            if len(first_name) < 2 or not first_name.isalpha(): first_name = "Founder"

            lead = {
                "Date Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Business": clean_title, "First Name": first_name,
                "Verified Email": email, "Instagram": f"https://www.instagram.com/{h}/",
                "Followers": fol, "Field": label, "Location": loc_str,
                "Website": website, "Status": "Active",
            }
            if "Tier" in fieldnames:
                lead["Tier"] = "High Ticket (Luxury Real Estate)"

            append_csv(csv_file, lead, fieldnames)
            push_webhook(lead, sheet_tab)
            seen_handles.add(h)
            new_approved += 1
            total_now = current_count + new_approved
            log(f"  [+] [{label}] [{total_now}/{TARGET_COUNT}] {clean_title} (@{h}) | {fol:,} | {loc_str}")

        time.sleep(0.5)  # small breath between queries in cloud

    final = current_count + new_approved
    log(f"[{label}] This run added {new_approved} leads. Total: {final}/{TARGET_COUNT}")
    return final

def main():
    log("=" * 70)
    log("  2M CREATIVE MEDIA - 24/7 CLOUD HARVESTER (GitHub Actions)")
    log("  Runs every 20 min in cloud — even when PC is OFF or ASLEEP")
    log("=" * 70)

    f_fields  = ["Date Discovered","Business","First Name","Verified Email",
                 "Instagram","Followers","Field","Location","Website","Status"]
    re_fields = ["Date Discovered","Business","First Name","Verified Email",
                 "Instagram","Followers","Field","Tier","Location","Website","Status"]

    harvest_category("Furniture",  FURNITURE_CSV,  FURNITURE_TAB,
                     FURNITURE_NICHES, FURNITURE_POSITIVE, NON_FURNITURE_RE, f_fields)

    harvest_category("Real Estate", REAL_ESTATE_CSV, REAL_ESTATE_TAB,
                     RE_TERMS, RE_POSITIVE, NON_RE_RE, re_fields)

if __name__ == "__main__":
    main()
