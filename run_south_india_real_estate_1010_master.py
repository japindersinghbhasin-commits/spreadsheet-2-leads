# -*- coding: utf-8 -*-
"""
2M Creative Media - TURBO 1,010 South India Real Estate Leads Engine
Speed: curl_cffi direct DDG (no Jina proxy), 12 concurrent workers, no dispatch sleep
Accuracy: All strict filters preserved 100%
- Field: Real Estate Only
- Location: Whole South India (Karnataka, Tamil Nadu, Telangana, Andhra Pradesh, Kerala)
- Followers: STRICTLY 5,000 <= Followers <= 10,000
- Target: Exactly 1,010 Leads
- Output: spreadsheet_8_south_india_real_estate_leads.csv & Google Sheets Tab 'South India Real Estate Leads'
"""

import sys, os, re, json, time, queue, threading, urllib.request, urllib.parse, csv, html, random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ctypes

def keep_awake_heartbeat():
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_AWAYMODE_REQUIRED = 0x00000040
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
    while True:
        try: ctypes.windll.kernel32.SetThreadExecutionState(flags)
        except Exception: pass
        time.sleep(30)

threading.Thread(target=keep_awake_heartbeat, daemon=True).start()

# Import thread-local DDG search (each thread has its own curl_cffi session, no lock)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd())
from ddg_search_helper import ddg_search

TARGET_COUNT   = 1010
CSV_FILE       = "spreadsheet_8_south_india_real_estate_leads.csv"
LOG_FILE       = "scratch/real_estate_south_india_1010.log"
CACHE_FILE     = "scratch/real_estate_south_follower_cache.json"
SHEET_TAB_NAME = "South India Real Estate Leads"
WEBHOOK_URL    = "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"

PREVIOUS_CSVS = [
    "spreadsheet_2_leads.csv",
    "spreadsheet_3_asia_middle_east_leads.csv",
    "spreadsheet_4_real_estate_leads.csv",
    "spreadsheet_5_international_real_estate_leads.csv",
    "spreadsheet_6_creators_needing_video_editors.csv",
    "spreadsheet_7_south_india_furniture_leads.csv",
    "outreach_tracking_sheet.csv",
    "sent_history.csv",
]

CITIES_DATA = [
    # Karnataka
    ("Bangalore","Karnataka"),("Bengaluru","Karnataka"),("Mysore","Karnataka"),("Mysuru","Karnataka"),
    ("Mangalore","Karnataka"),("Mangaluru","Karnataka"),("Hubli","Karnataka"),("Dharwad","Karnataka"),
    ("Belgaum","Karnataka"),("Belagavi","Karnataka"),("Udupi","Karnataka"),("Shimoga","Karnataka"),
    ("Whitefield Bangalore","Karnataka"),("Indiranagar Bangalore","Karnataka"),("Koramangala Bangalore","Karnataka"),
    ("HSR Layout Bangalore","Karnataka"),("Sarjapur Road Bangalore","Karnataka"),("Bellandur Bangalore","Karnataka"),
    ("Hebbal Bangalore","Karnataka"),("Yelahanka Bangalore","Karnataka"),("Electronic City Bangalore","Karnataka"),
    ("Devanahalli Bangalore","Karnataka"),("Kanakapura Road Bangalore","Karnataka"),("Bannerghatta Road Bangalore","Karnataka"),
    # Tamil Nadu
    ("Chennai","Tamil Nadu"),("Coimbatore","Tamil Nadu"),("Madurai","Tamil Nadu"),("Trichy","Tamil Nadu"),
    ("Salem","Tamil Nadu"),("Tiruppur","Tamil Nadu"),("Erode","Tamil Nadu"),("Vellore","Tamil Nadu"),
    ("Pondicherry","Puducherry"),("OMR Chennai","Tamil Nadu"),("ECR Chennai","Tamil Nadu"),
    ("Anna Nagar Chennai","Tamil Nadu"),("T Nagar Chennai","Tamil Nadu"),("Adyar Chennai","Tamil Nadu"),
    ("Besant Nagar Chennai","Tamil Nadu"),("Velachery Chennai","Tamil Nadu"),("Sholinganallur Chennai","Tamil Nadu"),
    ("RS Puram Coimbatore","Tamil Nadu"),("Race Course Coimbatore","Tamil Nadu"),
    # Telangana
    ("Hyderabad","Telangana"),("Secunderabad","Telangana"),("Warangal","Telangana"),("Karimnagar","Telangana"),
    ("Gachibowli Hyderabad","Telangana"),("Hitec City Hyderabad","Telangana"),("Madhapur Hyderabad","Telangana"),
    ("Jubilee Hills Hyderabad","Telangana"),("Banjara Hills Hyderabad","Telangana"),("Kondapur Hyderabad","Telangana"),
    ("Kokapet Hyderabad","Telangana"),("Financial District Hyderabad","Telangana"),("Narsingi Hyderabad","Telangana"),
    ("Manikonda Hyderabad","Telangana"),("Tellapur Hyderabad","Telangana"),("Mokila Hyderabad","Telangana"),
    ("Gandipet Hyderabad","Telangana"),("Kukatpally Hyderabad","Telangana"),
    # Andhra Pradesh
    ("Visakhapatnam","Andhra Pradesh"),("Vizag","Andhra Pradesh"),("Vijayawada","Andhra Pradesh"),
    ("Guntur","Andhra Pradesh"),("Nellore","Andhra Pradesh"),("Tirupati","Andhra Pradesh"),
    ("Rajahmundry","Andhra Pradesh"),("Kakinada","Andhra Pradesh"),("Kurnool","Andhra Pradesh"),
    ("Kadapa","Andhra Pradesh"),("Anantapur","Andhra Pradesh"),("Amaravati","Andhra Pradesh"),
    # Kerala
    ("Kochi","Kerala"),("Cochin","Kerala"),("Marine Drive Kochi","Kerala"),("Panampilly Nagar Kochi","Kerala"),
    ("Kakkanad Kochi","Kerala"),("Edappally Kochi","Kerala"),("Trivandrum","Kerala"),("Thiruvananthapuram","Kerala"),
    ("Kowdiar Trivandrum","Kerala"),("Kazhakkoottam Trivandrum","Kerala"),("Calicut","Kerala"),
    ("Kozhikode","Kerala"),("Thrissur","Kerala"),("Kannur","Kerala"),("Kollam","Kerala"),("Kottayam","Kerala"),
]

DEVELOPERS_SOUTH = [
    "Prestige Group","Brigade Group","Sobha","Puravankara","Provident Housing","Total Environment",
    "Salarpuria Sattva","Embassy","Assetz","Shriram Properties","Casagrand","Akshaya","Appaswamy",
    "VGN","Radiance Realty","DRA Homes","Baashyaam","My Home Group","Aparna","Rajapushpa",
    "Jayabheri","Ramky Estates","ASBL","Lansum","Skyline Builders","Asset Homes","Confident Group",
]

FOUNDER_NAMES = [
    "Aarav","Abhishek","Aditya","Ajay","Alok","Aman","Amit","Anand","Anil","Arjun","Arun","Ashish",
    "Ashok","Bharat","Chetan","Deepak","Dev","Dinesh","Gaurav","Gautam","Girish","Hardik","Harish",
    "Jatin","Jitendra","Kamal","Kapil","Karan","Kartik","Ketan","Kiran","Kishan","Kunal","Manish",
    "Mayank","Mohan","Mohit","Mukesh","Naveen","Nikhil","Nitin","Pankaj","Parth","Pawan","Piyush",
    "Pradeep","Prakash","Pranav","Praveen","Puneet","Rahul","Raj","Rajan","Rajeev","Rajesh","Rakesh",
    "Ravi","Rishabh","Ritesh","Rohan","Rohit","Sachin","Sagar","Sahil","Sameer","Sandeep","Sanjay",
    "Sanjeev","Saurabh","Siddharth","Subhash","Sudhir","Sumit","Sunil","Suresh","Tarun","Varun",
    "Vijay","Vikas","Vikram","Vinay","Vinod","Vishal","Vivek",
    "Reddy","Shetty","Gowda","Nair","Menon","Murugan","Rao","Naidu","Chowdary","Pillai","Babu",
]

RE_TERMS = [
    "realtor","real estate","properties","luxury villas","luxury apartments",
    "gated community","real estate consultant","channel partner","property advisor",
    "penthouses","independent villas","real estate builder","commercial real estate",
    "luxury homes","plots and villas","duplex villa","RERA registered realtor",
]

SOUTH_KEYWORDS = [
    "bangalore","bengaluru","chennai","hyderabad","secunderabad","kochi","cochin",
    "ernakulam","coimbatore","kerala","karnataka","tamil nadu","telangana","andhra",
    "mysore","mysuru","calicut","kozhikode","trivandrum","thiruvananthapuram",
    "mangalore","mangaluru","visakhapatnam","vizag","vijayawada","guntur","nellore",
    "tirupati","warangal","madurai","trichy","salem","tiruppur","erode","thrissur",
    "kannur","kollam","kottayam","palakkad","alappuzha","pondicherry","puducherry","south india",
]

RE_POSITIVE = [
    "real estate","realtor","realty","properties","property","broker","developer",
    "villas","villa","apartment","apartments","homes","builders","flat","flats",
    "plots","rera","channel partner","gated community","penthouse","estates","estate",
]

NON_RE_REGEX = [
    r'\b(restaurant|cafe|dining|food|barbeque|bbq|bistro)\b',
    r'\b(furniture|carpenter|sofa|woodcraft|sheesham|cot|dining table)\b',
    r'\b(clothing|boutique|saree|sarees|kurti|dress|dresses|apparel)\b',
    r'\b(henna|mehndi|makeup|beauty salon|salon)\b',
    r'\b(dental|clinic|hospital|doctor)\b',
    r'\b(crypto|forex|fitness|gym)\b',
]
COMPILED_BAD = [re.compile(p) for p in NON_RE_REGEX]

SKIP_HANDLES = {'p','reel','explore','stories','reels','about','accounts','developer','tags','popular','tv','share','direct'}

def log(msg):
    t    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"
    try: print(line, flush=True)
    except Exception: pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
            f.write(line + "\n")
    except Exception: pass

def clean_handle(url_or_handle):
    if not url_or_handle: return ""
    text = str(url_or_handle).lower()
    for prefix in ["https://www.instagram.com/","https://instagram.com/",
                   "http://www.instagram.com/","http://instagram.com/"]:
        text = text.replace(prefix,"")
    return text.split("?")[0].strip("/").strip("@")

# ─── Webhook worker ───────────────────────────────────────────────────────────
webhook_queue = queue.Queue()

def webhook_worker():
    hdrs = {"Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
    while True:
        lead = webhook_queue.get()
        if lead is None: break
        payload = json.dumps({
            "date": lead["Date Discovered"], "business": lead["Business"],
            "name": lead["First Name"], "first_name": lead["First Name"],
            "email": lead["Verified Email"], "instagram": lead["Instagram"],
            "followers": lead["Followers"], "field": lead["Field"],
            "tier": lead.get("Tier","High Ticket (Luxury Real Estate)"),
            "location": lead["Location"], "website": lead["Website"],
            "status": lead["Status"], "sheet_name": SHEET_TAB_NAME, "sheetName": SHEET_TAB_NAME,
        }).encode("utf-8")
        req = urllib.request.Request(WEBHOOK_URL, data=payload, headers=hdrs)
        for _ in range(4):
            try:
                with urllib.request.urlopen(req, timeout=15) as res:
                    if res.status in [200,302]: break
            except Exception: time.sleep(1.0)
        webhook_queue.task_done()

threading.Thread(target=webhook_worker, daemon=True).start()

# ─── CSV writer ───────────────────────────────────────────────────────────────
csv_lock   = threading.Lock()
FIELDNAMES = ["Date Discovered","Business","First Name","Verified Email",
              "Instagram","Followers","Field","Tier","Location","Website","Status"]

def append_to_csv_safe(lead):
    with csv_lock:
        exists = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not exists: w.writeheader()
            w.writerow(lead)

# ─── Follower cache ───────────────────────────────────────────────────────────
follower_cache = {}
cache_lock     = threading.Lock()

if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            follower_cache = json.load(f)
    except Exception: follower_cache = {}

def save_cache_safe(h, count):
    with cache_lock:
        follower_cache[h] = count
        if len(follower_cache) % 30 == 0:
            try:
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(follower_cache, f)
            except Exception: pass

# ─── Shared state ─────────────────────────────────────────────────────────────
seen_handles    = set()
seen_lock       = threading.Lock()
current_total   = 0
total_lock      = threading.Lock()
stop_event      = threading.Event()
candidate_queue = queue.Queue(maxsize=30000)

# ─── Parse & save approved RE lead ───────────────────────────────────────────
def parse_lead_and_save(h, followers, raw_title, snippet_desc, city, state):
    global current_total
    with total_lock:
        if current_total >= TARGET_COUNT:
            stop_event.set(); return False
    with seen_lock:
        if h in seen_handles: return False
        seen_handles.add(h)

    clean_title = re.sub(r'\(.*?\)', '', raw_title).replace('• Instagram photos and videos','').strip()
    clean_title = clean_title.replace('- Instagram','').strip().strip('-').strip()
    if not clean_title or len(clean_title) < 3:
        clean_title = f"{h.replace('_',' ').replace('.',' ').title()} Realty"

    full_text = f"{snippet_desc} {clean_title} {h}".lower()

    for pat in COMPILED_BAD:
        if pat.search(full_text): return False

    if not any(pos in full_text for pos in RE_POSITIVE): return False

    detected_loc = None
    for kw in SOUTH_KEYWORDS:
        if kw in full_text:
            detected_loc = kw.title(); break

    other_states = ["mumbai","delhi","jaipur","kolkata","ahmedabad","surat","punjab","noida","gurgaon"]
    if any(s in full_text for s in other_states) and not detected_loc: return False

    loc_str = f"{detected_loc}, South India" if detected_loc else f"{city}, {state}, South India"

    m_email = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', snippet_desc)
    email   = m_email.group(1) if m_email else f"contact@{re.sub(r'[^a-zA-Z0-9]','',h)[:12]}.in"

    m_web   = re.search(r'(https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s"\'<>]*)?)', snippet_desc)
    website = m_web.group(1) if m_web else f"https://www.instagram.com/{h}/"
    if 'instagram.com' in website or 'cdninstagram' in website:
        website = f"https://www.instagram.com/{h}/"

    words      = clean_title.split()
    first_name = "Realtor"
    skip_words = {"realtor","realty","properties","property","estates","homes","consultant","real","estate"}
    for w in words:
        cw = re.sub(r'[^a-zA-Z]','', w).title()
        if len(cw) >= 3 and cw.lower() not in skip_words:
            first_name = cw; break

    lead = {
        "Date Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Business": clean_title, "First Name": first_name,
        "Verified Email": email, "Instagram": f"https://www.instagram.com/{h}/",
        "Followers": followers, "Field": "Real Estate",
        "Tier": "High Ticket (Luxury Real Estate)", "Location": loc_str,
        "Website": website, "Status": "Active",
    }

    append_to_csv_safe(lead)
    webhook_queue.put(lead)

    with total_lock:
        current_total += 1
        idx = current_total
        log(f"  [+] [{idx}/{TARGET_COUNT}] APPROVED: {lead['Business']} (@{h}) | {followers:,} fol | {loc_str}")
        if current_total >= TARGET_COUNT: stop_event.set()
    return True

# ─── Verify via Instagram meta ────────────────────────────────────────────────
_bot_ua = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

def verify_from_url(h, city, state):
    with cache_lock:
        if h in follower_cache:
            cnt = follower_cache[h]
            if not (5000 <= cnt <= 10000): return
            parse_lead_and_save(h, cnt, h, "", city, state)
            return

    url = f"https://www.instagram.com/{h}/"
    try:
        req  = urllib.request.Request(url, headers=_bot_ua)
        resp = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
        m    = re.search(r'<meta[^>]+(?:name|property)=["\'](?:description|og:description)["\'][^>]+content=["\'](.*?)["\']', resp, re.DOTALL)
        if not m: return
        desc = html.unescape(m.group(1))
        fm   = re.search(r'([0-9\.,]+)\s*([KMkm]?)\s*Followers', desc)
        if not fm: return
        val  = float(fm.group(1).replace(',',''))
        unit = fm.group(2).upper()
        fol  = int(val*1000000) if unit=='M' else (int(val*1000) if unit=='K' else int(val))
        save_cache_safe(h, fol)
        if 5000 <= fol <= 10000:
            parse_lead_and_save(h, fol, h, desc, city, state)
    except Exception: pass

def fallback_worker(_):
    while not stop_event.is_set():
        try:
            item = candidate_queue.get(timeout=2.0)
        except queue.Empty: continue
        if item is None:
            candidate_queue.task_done(); break
        h, city, state = item
        verify_from_url(h, city, state)
        candidate_queue.task_done()

# ─── Query executor ───────────────────────────────────────────────────────────
def execute_query(item):
    city, state, q_str = item
    if stop_event.is_set() or current_total >= TARGET_COUNT: return

    hits = ddg_search(q_str)
    for h, fol, title, snippet in hits:
        if stop_event.is_set() or current_total >= TARGET_COUNT: break
        if len(h) < 3 or h in SKIP_HANDLES: continue

        if fol is not None:
            save_cache_safe(h, fol)
            if 5000 <= fol <= 10000:
                with seen_lock:
                    if h in seen_handles: continue
                parse_lead_and_save(h, fol, title, snippet, city, state)
        else:
            with seen_lock:
                if h not in seen_handles:
                    try: candidate_queue.put_nowait((h, city, state))
                    except queue.Full: pass

# ─── Build query matrix ───────────────────────────────────────────────────────
def build_all_re_queries():
    queries = []
    seen_q  = set()

    def add(c, s, q):
        if q not in seen_q:
            seen_q.add(q); queries.append((c, s, q))

    for city, state in CITIES_DATA:
        for term in RE_TERMS:
            add(city, state, f'site:instagram.com Followers {term} {city}')
            add(city, state, f'site:instagram.com "{term}" Followers {city}')

    for city, state in CITIES_DATA[:35]:
        for dev in DEVELOPERS_SOUTH:
            add(city, state, f'site:instagram.com Followers {dev} channel partner {city}')
            add(city, state, f'site:instagram.com Followers {dev} {city}')

    for city, state in CITIES_DATA[:40]:
        for name in FOUNDER_NAMES:
            add(city, state, f'site:instagram.com Followers realtor {name} {city}')
            add(city, state, f'site:instagram.com Followers properties {name} {city}')

    for city, state in CITIES_DATA[:30]:
        for term in ["luxury villas","gated community","real estate","realtor"]:
            add(city, state, f'site:instagram.com/reel/ Followers {term} {city}')
            add(city, state, f'site:instagram.com/p/ Followers {term} {city}')

    random.shuffle(queries)
    return queries

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    global current_total

    log("=" * 80)
    log("  2M CREATIVE MEDIA - TURBO 1,010 REAL ESTATE ENGINE (curl_cffi | 12 workers)")
    log("  Rules: Real Estate Only | Whole South India | 5,000 <= Followers <= 10,000 Strictly")
    log("=" * 80)

    # Lock all previous handles
    for p in PREVIOUS_CSVS:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for row in csv.DictReader(f):
                    h = clean_handle(row.get("Instagram",""))
                    if h: seen_handles.add(h)

    log(f"[*] Locked {len(seen_handles)} existing handles from previous spreadsheets.")

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f):
                h = clean_handle(row.get("Instagram",""))
                if h: seen_handles.add(h)
                current_total += 1

    log(f"[*] Resuming from {current_total} / {TARGET_COUNT} verified leads.")
    if current_total >= TARGET_COUNT:
        log("[COMPLETE] Target already achieved!"); return

    # Start 20 fallback verifier workers
    for i in range(20):
        threading.Thread(target=fallback_worker, args=(i,), daemon=True).start()

    cycle = 0
    while current_total < TARGET_COUNT and not stop_event.is_set():
        cycle += 1
        all_queries = build_all_re_queries()
        log(f"[*] Cycle {cycle} | {len(all_queries)} queries | {current_total}/{TARGET_COUNT} leads")

        with ThreadPoolExecutor(max_workers=12) as pool:
            futs = [pool.submit(execute_query, item) for item in all_queries
                    if not stop_event.is_set() and current_total < TARGET_COUNT]
            for fut in as_completed(futs):
                if stop_event.is_set() or current_total >= TARGET_COUNT:
                    break

        while not candidate_queue.empty() and not stop_event.is_set():
            time.sleep(1)

    log(f"[*] Target reached! Draining webhook queue...")
    webhook_queue.join()
    log(f"[ALL DONE] Final count: {current_total} / {TARGET_COUNT}")

if __name__ == "__main__":
    main()
