"""
Ultra-Fast Continuous Instagram Creator Harvester - Fully Automated
====================================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

import re, time, csv, os, html, requests
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Keep PC awake
try:
    import ctypes
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)
    print("[Power] Sleep prevention ON.")
except Exception:
    pass

TODAY = datetime(2026, 10, 23)
CUTOFF_DATE = TODAY - timedelta(days=16)

CSV_PATH = r"c:\Users\DELL\Downloads\gmail automation\spreadsheet_6_creators_needing_video_editors.csv"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"
SHEET_NAME = "Strict Freelance Creator Gigs"

MONTH_MAP = {
    "january":1,"february":2,"march":3,"april":4,
    "may":5,"june":6,"july":7,"august":8,
    "september":9,"october":10,"november":11,"december":12
}

seen_handles = set()
seen_codes = set()
lock = threading.Lock()

def load_seen():
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                h = row.get("Instagram Handle", "").lstrip("@").strip().lower()
                if h: seen_handles.add(h)
    print(f"[Init] Loaded {len(seen_handles)} verified handles from CSV.")

QUERIES = [
    'site:instagram.com/reel "hiring a video editor" podcast',
    'site:instagram.com/reel "hiring a video editor" youtube',
    'site:instagram.com/reel "hiring a video editor" vlog',
    'site:instagram.com/reel "hiring a video editor" reels',
    'site:instagram.com/reel "hiring a video editor" fitness',
    'site:instagram.com/reel "hiring a video editor" travel',
    'site:instagram.com/reel "hiring a video editor" lifestyle',
    'site:instagram.com/reel "hiring a video editor" comedy',
    'site:instagram.com/reel "hiring a video editor" tech',
    'site:instagram.com/reel "hiring a video editor" entrepreneur',
    'site:instagram.com/reel "need a video editor" podcast',
    'site:instagram.com/reel "need a video editor" youtube',
    'site:instagram.com/reel "need a video editor" reels',
    'site:instagram.com/reel "need a video editor" fitness',
    'site:instagram.com/reel "need a video editor" travel',
    'site:instagram.com/reel "need a video editor" lifestyle',
    'site:instagram.com/reel "need a video editor" business',
    'site:instagram.com/reel "looking for a video editor" podcast',
    'site:instagram.com/reel "looking for a video editor" youtube',
    'site:instagram.com/reel "looking for a video editor" reels',
    'site:instagram.com/reel "looking for a video editor" vlog',
    'site:instagram.com/reel "looking for a video editor" fitness',
    'site:instagram.com/reel "looking for a video editor" lifestyle',
    'site:instagram.com/reel "looking for a video editor" creator',
    'site:instagram.com/reel "video editor needed" podcast',
    'site:instagram.com/reel "video editor needed" youtube',
    'site:instagram.com/reel "video editor needed" reels',
    'site:instagram.com/reel "video editor wanted" creator',
    'site:instagram.com/reel "editor wanted" "dm portfolio"',
    'site:instagram.com/reel "hiring video editor" "dm portfolio"',
    'site:instagram.com/reel "hiring video editor" "send portfolio"',
    'site:instagram.com/reel "hiring video editor" "fill out the form"',
    'site:instagram.com/reel "hiring video editor" "apply link in bio"',
    'site:instagram.com/reel "calling all video editors" creator',
    'site:instagram.com/reel "need someone to edit my podcast"',
    'site:instagram.com/reel "need someone to edit my youtube"',
    'site:instagram.com/reel "need someone to edit my reels"',
    'site:instagram.com/reel "looking for someone to edit my podcast"',
    'site:instagram.com/reel "looking for someone to edit my youtube"',
    'site:instagram.com/reel "looking for someone to edit my reels"'
]

DISQUALIFIED_TERMS = [
    "agency","studio","studios","media","marketing","solutions","technologies",
    "insurance","insure","careers","placement","jobs","consulting","recruitment",
    "academy","institute","pvt","ltd","corp","holdings","advisory","office job",
    "9 to 5","working hours","qualification","full-time office","walk-in","job vacancy",
    "babyorgano","medigita","eduport","sendrang","nilal_arts","oneinsure",
    "without hiring","without needing","no need to hire","instead of hiring",
    "don't hire","stop hiring","before hiring","tutorial","prompt from my broadcast"
]

EDITOR_SELF_AD = [
    "i am a video editor","i'm a video editor","i edit videos for",
    "hire me as","my editing services","dm me for editing",
    "i offer editing","book me","i can edit your","editor available",
    "editing packages","my rates","check out my work",
    "portfolio link in bio","i do video editing for",
    "services starting","per video","per reel","editing service",
    "i provide","i specialize in editing","my client work",
    "open for work","looking for work"
]

CREATOR_HIRING_TERMS = [
    "i need a video editor","i'm looking for","i am looking for a video editor",
    "hiring a video editor","need a video editor","looking for a video editor",
    "video editor needed","editor wanted","need an editor for my",
    "dm your portfolio","dm me your portfolio","send me your work",
    "apply now","join my team","help me with editing","edit my content",
    "edit my reels","edit my videos","for my channel","for my page",
    "for my content","for my instagram","for my youtube",
    "we're hiring","we are hiring","hiring video editor",
    "video editor for my","editor for my","edit for me",
    "need someone to edit","looking for someone to edit",
    "hiring video editors","calling cool video editors",
    "apply today","comment work","comment editor"
]

LOCATIONS = [
    "Mumbai","Delhi","Bangalore","Chennai","Hyderabad","Kolkata",
    "Pune","Ahmedabad","Jaipur","Lucknow","Kochi","Kerala","Noida","Gurgaon",
    "Dubai","Abu Dhabi","UAE","Sharjah","Riyadh","Saudi Arabia",
    "Karachi","Lahore","Islamabad","Pakistan",
    "Dhaka","Bangladesh",
    "New York","Los Angeles","Chicago","Houston","Atlanta","Miami","USA","Scottsdale","Arizona",
    "London","Manchester","Birmingham","UK","England",
    "Toronto","Vancouver","Canada",
    "Sydney","Melbourne","Australia",
    "Lagos","Abuja","Nigeria",
    "Nairobi","Kenya",
    "Accra","Ghana",
    "Johannesburg","Cape Town","South Africa",
    "Manila","Philippines",
    "Jakarta","Indonesia",
    "Kuala Lumpur","Malaysia",
    "Singapore"
]

def clean_html(text):
    return html.unescape(text).replace("\n", " ").strip()

def search_one_query(q):
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    codes = set()
    for offset in [0, 30]:
        url = f"https://r.jina.ai/https://lite.duckduckgo.com/lite/?q={quote_plus(q)}&s={offset}"
        try:
            r = s.get(url, timeout=12)
            if r.status_code == 200:
                found = re.findall(r"instagram\.com/reel/([A-Za-z0-9_\-]+)", r.text)
                codes.update(found)
        except Exception:
            pass
    return codes

def parse_handle(desc, title):
    m = re.search(r'[-–]\s*(@?[\w.]+)\s+on\s+[A-Za-z]+', desc)
    if m: return m.group(1).lstrip("@")
    m = re.search(r'(@?[\w.]+)\s+on\s+[A-Za-z]+\s+\d+', desc)
    if m: return m.group(1).lstrip("@")
    m = re.search(r'@([\w.]+)\s+on\s+Instagram', title)
    if m: return m.group(1)
    return ""

def parse_date(desc):
    m = re.search(
        r'on\s+(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(\d{1,2}),?\s+(\d{4})', desc, re.IGNORECASE
    )
    if m:
        try:
            return datetime(int(m.group(3)), MONTH_MAP[m.group(1).lower()], int(m.group(2)))
        except Exception:
            return None
    return None

def get_caption(desc):
    m = re.search(r'on\s+[A-Za-z]+\s+\d+,?\s+\d+:\s*(.*)', desc, re.DOTALL)
    if m: return clean_html(m.group(1))
    return clean_html(desc)

def is_creator_hiring(caption, handle):
    c = (caption + " " + handle).lower()
    for term in DISQUALIFIED_TERMS:
        if term in c: return False, f"company/agency/brand: '{term}'"
    for term in EDITOR_SELF_AD:
        if term in c: return False, f"editor self-ad: '{term}'"
    for term in CREATOR_HIRING_TERMS:
        if term in c: return True, ""
    return False, "no hiring intent"

def get_followers(session, handle):
    try:
        r = session.get(f"https://www.instagram.com/{handle}/", timeout=12)
        for pat in [r'"edge_followed_by":\{"count":(\d+)\}', r'"followers_count":(\d+)']:
            m = re.search(pat, r.text)
            if m: return int(m.group(1))
        m = re.search(r'([\d,.]+)\s*([KkMm]?)\s*[Ff]ollowers', r.text)
        if m:
            n = float(m.group(1).replace(",",""))
            s = m.group(2).lower()
            return int(n*1000) if s=="k" else int(n*1_000_000) if s=="m" else int(n)
    except Exception:
        pass
    return 0

def get_location(caption, title):
    combined = (caption + " " + title).lower()
    for loc in LOCATIONS:
        if loc.lower() in combined: return loc
    return "India"

def infer_niche(caption):
    c = caption.lower()
    if any(w in c for w in ["podcast","interview"]): return "Podcast Creator"
    if any(w in c for w in ["fitness","gym","workout"]): return "Fitness Creator"
    if any(w in c for w in ["travel","vlog","adventure"]): return "Travel Creator"
    if any(w in c for w in ["fashion","style","ootd"]): return "Fashion Influencer"
    if any(w in c for w in ["food","recipe","cooking"]): return "Food Creator"
    if any(w in c for w in ["entrepreneur","business","startup"]): return "Entrepreneur"
    if any(w in c for w in ["motivat","mindset","coach"]): return "Motivational Creator"
    if any(w in c for w in ["tech","ai","coding"]): return "Tech Creator"
    return "Content Creator"

def infer_role(caption):
    c = caption.lower()
    if "podcast" in c: return "Freelance Podcast Video Editor"
    if "youtube" in c: return "Freelance YouTube Video Editor"
    if "reel" in c or "short" in c: return "Freelance Reels & Short-Form Video Editor"
    if "vlog" in c: return "Freelance Vlog Editor"
    return "Freelance Video Editor"

def push_lead(row):
    with lock:
        exists = os.path.exists(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            cols = ["Date Discovered","Creator Name","Instagram Handle","Instagram Profile",
                    "Followers","Date of Post","Field / Niche","Location","Proof",
                    "Proof Caption Snippet","Role Needed","Status"]
            w = csv.DictWriter(f, fieldnames=cols)
            if not exists: w.writeheader()
            w.writerow(row)
            
    try:
        requests.post(WEBHOOK_URL, json={
            "sheetName": SHEET_NAME,
            "business":  row["Creator Name"],
            "name":      row["Creator Name"],
            "first_name":row["Creator Name"].split()[0],
            "instagram": row["Instagram Profile"],
            "followers": str(row["Followers"]),
            "location":  row["Location"],
            "website":   row["Proof"],
            "proof":     row["Proof"],
            "caption":   row["Proof Caption Snippet"],
            "role_needed":row["Role Needed"],
            "field":     row["Field / Niche"],
            "status":    "Active Gig",
            "tier":      "Standard",
            "email":     "",
        }, timeout=15)
    except Exception:
        pass

def verify_reel(code):
    session = requests.Session()
    session.headers.update({"User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"})
    url = f"https://www.instagram.com/reel/{code}/"
    try:
        r = session.get(url, timeout=12)
        if r.status_code != 200: return None
        t = re.search(r'<meta property="og:title" content="([^"]*)"', r.text)
        d = re.search(r'<meta property="og:description" content="([^"]*)"', r.text)
        if not t: return None
        title = clean_html(t.group(1))
        desc = clean_html(d.group(1)) if d else ""
        
        handle = parse_handle(desc, title)
        if not handle: return None
        h_lower = handle.lower()
        with lock:
            if h_lower in seen_handles: return None
                
        post_date = parse_date(desc)
        if not post_date: return None
        if not (CUTOFF_DATE <= post_date <= TODAY): return None
            
        caption = get_caption(desc)
        ok, reason = is_creator_hiring(caption, handle)
        if not ok: return None
            
        f_count = get_followers(session, handle)
        if f_count < 10000: return None
            
        with lock:
            if h_lower in seen_handles: return None
            seen_handles.add(h_lower)
            
        loc = get_location(caption, title)
        name = handle.replace("."," ").replace("_"," ").title()
        
        row = {
            "Date Discovered":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Creator Name":          name,
            "Instagram Handle":      "@" + handle,
            "Instagram Profile":     f"https://instagram.com/{handle}",
            "Followers":             f_count,
            "Date of Post":          post_date.strftime("%B %d, %Y"),
            "Field / Niche":         infer_niche(caption),
            "Location":              loc,
            "Proof":                 url,
            "Proof Caption Snippet": caption,
            "Role Needed":           infer_role(caption),
            "Status":                "Active Gig"
        }
        push_lead(row)
        print(f"\n >>> [NEW VERIFIED LEAD #{len(seen_handles)}] @{handle} | {f_count:,} followers | {post_date.strftime('%b %d, %Y')} | {loc}")
        print(f"     URL: {url}")
        print(f"     Caption: {caption[:110]}...\n")
        return row
    except Exception:
        return None

def main():
    load_seen()
    print("\n" + "="*70)
    print("  ULTRA-FAST PARALLEL INSTAGRAM CREATOR HARVESTER")
    print(f"  Verified leads: {len(seen_handles)} | Window: {CUTOFF_DATE.strftime('%b %d')} - {TODAY.strftime('%b %d, %Y')}")
    print("="*70 + "\n")
    
    t0 = time.time()
    print(f"[Search Engine] Executing {len(QUERIES)} search queries in parallel with 10 workers...")
    all_codes = set()
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(search_one_query, q) for q in QUERIES]
        for f in as_completed(futs):
            all_codes.update(f.result())
            
    fresh = [c for c in all_codes if c not in seen_codes]
    for c in fresh: seen_codes.add(c)
    print(f"[Search Engine] Discovered {len(fresh)} fresh candidate reels in {time.time()-t0:.2f}s.")
    
    if fresh:
        print(f"[Verifier Engine] Validating {len(fresh)} reels with 15 parallel workers...")
        t1 = time.time()
        new_leads = 0
        with ThreadPoolExecutor(max_workers=15) as ex:
            futs = [ex.submit(verify_reel, c) for c in fresh]
            for f in as_completed(futs):
                if f.result(): new_leads += 1
        print(f"[Verifier Engine] Validation completed in {time.time()-t1:.2f}s. New verified leads: {new_leads}")
    else:
        print("[Verifier Engine] No fresh candidates to verify.")

    print(f"\n[Summary] Total verified leads in database: {len(seen_handles)}")

if __name__ == "__main__":
    main()
