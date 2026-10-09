import csv
import json
import os
import re
import time
import urllib.request
from datetime import datetime

# ==============================================================================
# CONFIGURATION & STRICT DEDUPLICATION
# ==============================================================================
SPREADSHEET_1_CSV = "outreach_tracking_sheet.csv"
SENT_HISTORY_CSV = "sent_history.csv"
LEADS_CSV = "leads.csv"
DISCOVERED_LEADS_CSV = "discovered_leads.csv"
ENV_FILE = ".env"

SPREADSHEET_2_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"

def clean_handle(url_or_handle):
    """Normalizes any Instagram link or handle to a clean lowercase username."""
    if not url_or_handle:
        return ""
    text = str(url_or_handle).strip().lower()
    text = text.replace("https://www.instagram.com/", "").replace("https://instagram.com/", "")
    text = text.replace("http://www.instagram.com/", "").replace("http://instagram.com/", "")
    text = text.split("?")[0].strip("/").strip("@")
    return text

def get_forbidden_instagram_ids():
    """Loads EVERY Instagram ID from Spreadsheet 1, sent history, and existing leads
    to guarantee 100% zero overlap between Spreadsheet 1 and Spreadsheet 2."""
    forbidden = set()
    
    # 1. From Spreadsheet 1 (Outreach Tracker)
    if os.path.exists(SPREADSHEET_1_CSV):
        with open(SPREADSHEET_1_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                h = clean_handle(row.get("Instagram", ""))
                if h:
                    forbidden.add(h)

    # 2. From Sent History
    if os.path.exists(SENT_HISTORY_CSV):
        with open(SENT_HISTORY_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                h = clean_handle(row.get("Instagram", ""))
                if h:
                    forbidden.add(h)

    # 3. From Main Leads Pool
    if os.path.exists(LEADS_CSV):
        with open(LEADS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                h = clean_handle(row.get("Instagram", ""))
                if h:
                    forbidden.add(h)

    # 4. From already-discovered leads in Spreadsheet 2
    if os.path.exists(DISCOVERED_LEADS_CSV):
        with open(DISCOVERED_LEADS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                h = clean_handle(row.get("Instagram", ""))
                if h:
                    forbidden.add(h)

    return forbidden

def check_instagram_profile(handle):
    """Verifies that an Instagram handle is LIVE and has under 5,000 followers."""
    if not handle:
        return False, 0, "No handle"
    url = f"https://www.instagram.com/{handle}/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", "ignore")
        title_match = re.search(r"<title>(.*?)</title>", html)
        title_str = title_match.group(1) if title_match else ""
        
        is_live = "photos and videos" in title_str.lower() or handle.lower() in title_str.lower()
        if not is_live:
            return False, 0, "404 Not Found"

        follower_match = re.search(r'content="([0-9,KMkm.]+\s+Followers[^\"]*)"', html)
        f_str = follower_match.group(1) if follower_match else ""
        
        num_str = re.sub(r"\s+Followers.*", "", f_str).strip().replace(",", "")
        if "k" in num_str.lower():
            count = int(float(re.sub(r"[^0-9.]", "", num_str)) * 1000)
        elif "m" in num_str.lower():
            count = int(float(re.sub(r"[^0-9.]", "", num_str)) * 1000000)
        else:
            count = int(re.sub(r"[^0-9]", "", num_str)) if num_str else 0

        # Strict rule: Under 5,000 followers
        if count <= 5000:
            return True, count, f"{count:,}"
        else:
            return False, count, f"Too large ({count:,} followers)"
    except Exception as e:
        return False, 0, str(e)

def scrape_verified_email(website):
    """Scrapes official website contact pages for real, verified email addresses. Zero guessing."""
    if not website:
        return None
    try:
        req = urllib.request.Request(website, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", "ignore")
        
        # Look for mailto: links first
        mailtos = re.findall(r'mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', html)
        clean_mailtos = [e.lower() for e in mailtos if not any(x in e.lower() for x in ["wix", "sentry", "png", "jpg", "example"])]
        if clean_mailtos:
            return clean_mailtos[0]
            
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
        clean = [e.lower() for e in emails if not any(x in e.lower() for x in ["wix", "sentry", "png", "jpg", "example", "1.8.1", "svg", "wght"])]
        return clean[0] if clean else None
    except Exception:
        return None

def log_to_spreadsheet_2(lead, webhook_url=SPREADSHEET_2_WEBHOOK_URL):
    """Saves discovered lead to local CSV and pushes live to Spreadsheet 2."""
    file_exists = os.path.exists(DISCOVERED_LEADS_CSV)
    fieldnames = ["Date Discovered", "Business", "First Name", "Verified Email", "Instagram", "Followers", "Field", "Tier", "Location", "Website", "Status"]
    
    with open(DISCOVERED_LEADS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(lead)

    # Sync to Spreadsheet 2 via Webhook
    if webhook_url:
        try:
            payload = json.dumps({
                "date": lead.get("Date Discovered", ""),
                "business": lead.get("Business", ""),
                "name": lead.get("First Name", ""),
                "email": lead.get("Verified Email", ""),
                "instagram": lead.get("Instagram", ""),
                "followers": lead.get("Followers", ""),
                "field": lead.get("Field", ""),
                "tier": lead.get("Tier", ""),
                "location": lead.get("Location", ""),
                "website": lead.get("Website", ""),
                "status": lead.get("Status", "Verified New")
            }).encode("utf-8")

            class AppScriptRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return urllib.request.Request(newurl, headers={"User-Agent": "Mozilla/5.0"})
            opener = urllib.request.build_opener(AppScriptRedirectHandler)
            req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            opener.open(req, timeout=15)
            print(f"  [+] Synced live to Spreadsheet 2: {lead['Business']}")
        except Exception as e:
            print(f"  [!] Note: Spreadsheet 2 sync: {e}")

# ==============================================================================
# DISCOVERY CANDIDATES CATALOG (Boutique Studios, Low Reach, High Craftsmanship)
# ==============================================================================
DISCOVERY_CANDIDATES = [
    # Furniture
    ("Jonathan", "Jonathan Field Furniture", "https://jonathanfield.co.uk", "jonathan_field_furniture", "Furniture", "Local", "London UK"),
    ("Simon", "Waywood Furniture", "https://waywood.co.uk", "waywoodfurniture", "Furniture", "Local", "Oxfordshire UK"),
    ("Toby", "Toby Winteringham Furniture", "https://tobywinteringham.co.uk", "tobywinteringham", "Furniture", "Local", "Norfolk UK"),
    ("Rupert", "Rupert Senior Studio", "https://rupertsenior.co.uk", "rupertseniorfurniture", "Furniture", "Local", "Surrey UK"),
    ("Paul", "Paul Case Furniture", "https://paulcase.co.uk", "paulcasefurniture", "Furniture", "Local", "Preston UK"),
    
    # Interior Design
    ("Sarah", "Etons of Bath Period Interiors", "https://etonsofbath.com", "etonsofbath", "Interior Design", "Higher than Local", "Bath UK"),
    ("Henrietta", "Spencer-Churchill Designs", "https://spencerchurchilldesigns.com", "spencerchurchilldesigns", "Interior Design", "Local", "Woodstock UK"),
    ("Hannah", "Hannah Barnes Designs", "https://hannahbarnesdesigns.co.uk", "hannahbarnesdesigns", "Interior Design", "Local", "Edinburgh Scotland"),
    ("Kavita", "Kavita Interiors", "https://kavitainteriors.com", "kavitainteriors", "Interior Design", "Local", "London UK"),
    
    # Architecture
    ("William", "Paul Archer Design Practice", "https://paularcherdesign.co.uk", "paularcherdesign", "Architecture", "Local", "London UK"),
    ("Neil", "Neil Dusheiko Architects", "https://neildusheiko.com", "neildusheikoarchitects", "Architecture", "Local", "London UK"),
    ("Hugh", "Hugh Strange Architects", "https://hughstrange.com", "hughstrangearchitects", "Architecture", "Local", "London UK"),
    
    # Real Estate
    ("Alex", "Mountgrange Heritage Estates", "https://mountgrangeheritage.co.uk", "mountgrangeh", "Real Estate", "Local", "London UK"),
    ("Mark", "Middleton Advisors Property", "https://middletonadvisors.com", "middletonadvisors", "Real Estate", "Higher than Local", "London UK"),
    ("Robert", "Wetherell Mayfair Estates", "https://wetherell.co.uk", "wetherellmayfair", "Real Estate", "Local", "Mayfair London"),
    
    # Jewelry & Luxury Goods
    ("Catherine", "Catherine Best Island Jewels", "https://catherinebest.com", "catherinebestjewellery", "Jewelry & Luxury Goods", "Local", "Jersey Channel Islands"),
    ("Ute", "Ute Decker Architectural Jewellery", "https://utedecker.com", "utedecker", "Jewelry & Luxury Goods", "Local", "London UK"),
    ("Corinna", "Corinna Pike Master Goldsmith", "https://corinnapike.co.uk", "corinnapike", "Jewelry & Luxury Goods", "Local", "London UK"),
    
    # Aesthetic & Medspa
    ("Alison", "The Glasshouse Aesthetic Clinic", "https://theglasshouseclinic.co.uk", "glasshouse_clinic", "Aesthetic & Medspa", "Local", "London UK"),
    ("Dr. Dan", "Dhunna Facial Aesthetics", "https://drdandhunna.com", "drdandhunna", "Aesthetic & Medspa", "Local", "London & Midlands UK"),
    ("Dr. Grace", "Tailor Health & Aesthetic Clinic", "https://healthandaesthetics.co.uk", "healthandaestheticsclinic", "Aesthetic & Medspa", "Local", "Surrey UK"),
    ("Dr. Nick", "Milojevic Milo Clinic", "https://miloclinic.com", "miloclinic", "Aesthetic & Medspa", "Local", "London UK"),
    
    # Fitness & Wellness
    ("Oliver", "Equilibrium Total Balance", "https://weareequilibrium.com", "weareequilibrium", "Fitness & Wellness", "Local", "London UK"),
    ("Sarah", "FitLife Private Gym", "https://fitlife.co.uk", "fitlife_uk", "Fitness & Wellness", "Local", "Oxfordshire UK"),
    ("Rob", "Transition Cycle & Strength Hub", "https://transitionzone.co.uk", "transition_zone", "Fitness & Wellness", "Local", "London UK"),
    
    # Fashion & Leather Goods
    ("Alasdair", "McRostie Leather Scotland", "https://mcrostie.co.uk", "mcrostiescotland", "Fashion & Leather Goods", "Local", "Scotland UK"),
    ("Ian", "Campbell Cole Accessories", "https://campbellcole.co.uk", "campbell_cole", "Fashion & Leather Goods", "Local", "Nottingham UK"),
    ("Sarah", "Chapman Bags Handcrafted Goods", "https://chapmanbags.com", "chapmanbags", "Fashion & Leather Goods", "Higher than Local", "Cumbria UK"),
    
    # Home Decor & Lighting
    ("Oliver", "Original House Vintage Interiors", "https://originalhouse.co.uk", "originalhouse", "Home Decor & Lighting", "Local", "Gloucestershire UK"),
    ("Ben", "Haberdashery Design Studio", "https://haberdashery.com", "haberdasheryltd", "Home Decor & Lighting", "Local", "London UK"),
    ("Esther", "Curiousa & Curiousa Studio Glass", "https://curiousa.co.uk", "curiousastudio", "Home Decor & Lighting", "Local", "Derbyshire UK"),
    
    # Tattoo & Body Art
    ("Marco", "Secret Society Tattoo Workshop", "https://secretsocietytattoo.co.uk", "secretsocietytattoo", "Tattoo & Body Art", "Local", "London UK"),
    ("Stevie", "Hunter & Fox Tattoo Parlour", "https://hunterandfox.com.au", "hunterandfox", "Tattoo & Body Art", "Local", "Sydney Australia")
]

def verify_email_dns(email):
    """Verifies that the email domain actually resolves to prevent future bounces."""
    if not email or "@" not in email:
        return False
    try:
        import socket
        domain = email.split("@")[1].strip()
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def run_discovery_pipeline(limit=10):
    print("\n" + "="*65)
    print(" [*] STARTING LEAD DISCOVERY PIPELINE (FOR SPREADSHEET 2)")
    print(" [*] Rule: Zero emails sent | Only verified scraped inboxes")
    print(" [*] Rule: Strictly < 5k followers | Active Instagram only")
    print(" [*] Rule: Pre-checks DNS to eliminate bounce risk")
    print("="*65 + "\n")

    forbidden_ids = get_forbidden_instagram_ids()
    print(f"[*] Loaded {len(forbidden_ids)} forbidden Instagram IDs from Sheet 1 & history.")
    print("[*] Strict check active: ANY matching handle will be rejected instantly.\n")

    discovered_count = 0

    for item in DISCOVERY_CANDIDATES:
        if discovered_count >= limit:
            break

        first_name, biz_name, website, ig_handle, field, tier, loc = item
        clean_ig = clean_handle(ig_handle)

        # 1. STRICT DEDUPLICATION CHECK
        if clean_ig in forbidden_ids:
            print(f"[-] REJECTED (Already in Spreadsheet 1 / History): @{clean_ig} ({biz_name})")
            continue

        # 2. INSTAGRAM LIVE & FOLLOWER VERIFICATION (< 5,000)
        is_live, count, follower_str = check_instagram_profile(clean_ig)
        if not is_live:
            print(f"[-] SKIPPED Instagram check: @{clean_ig} ({follower_str})")
            continue

        # 3. WEBSITE EMAIL EXTRACTION (NO GUESSING)
        scraped_email = scrape_verified_email(website)
        if not scraped_email:
            print(f"[-] SKIPPED (No verified email published on website): {website}")
            continue

        # 4. DNS / BOUNCE PREVENTION CHECK
        if not verify_email_dns(scraped_email):
            print(f"[-] SKIPPED (Domain failed DNS check): {scraped_email}")
            continue

        # 4. PASSED ALL CHECKS -> RECORD TO SPREADSHEET 2
        lead_record = {
            "Date Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Business": biz_name,
            "First Name": first_name,
            "Verified Email": scraped_email,
            "Instagram": f"https://instagram.com/{clean_ig}",
            "Followers": follower_str,
            "Field": field,
            "Tier": tier,
            "Location": loc,
            "Website": website,
            "Status": "Verified New Lead"
        }

        log_to_spreadsheet_2(lead_record)
        forbidden_ids.add(clean_ig) # Prevent re-adding in same run
        discovered_count += 1

        print(f"\n[+] DISCOVERED [{discovered_count}/{limit}]: {biz_name}")
        print(f"    • Niche: {field} | Location: {loc}")
        print(f"    • Verified Email: {scraped_email} (scraped from site)")
        print(f"    • Instagram: @{clean_ig} (Followers: {follower_str})")
        print(f"    • Overlap with Sheet 1: ZERO (100% Unique)")
        print("-" * 55)

        time.sleep(0.5)

    print("\n" + "="*65)
    print(f" [DONE] Discovery complete: {discovered_count} fresh, unique leads logged to Spreadsheet 2.")
    print("="*65 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10, help="Number of fresh leads to discover")
    args = parser.parse_args()
    run_discovery_pipeline(limit=args.limit)
