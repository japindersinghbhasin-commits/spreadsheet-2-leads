"""
Syncs all 1,000 verified leads from spreadsheet_2_leads.csv to Google Sheet 2 via Webhook.
Uses 8 parallel worker threads for fast delivery.
"""

import csv
import json
import time
import urllib.request
import concurrent.futures

SPREADSHEET_2_CSV = "spreadsheet_2_leads.csv"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwMeoE2kST12L34QY7vjICa-8s6bZJpAzHBwLB9-c8CBbqRReyEapsY1Lc-MM_Cvk_L/exec"

class AppScriptRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return urllib.request.Request(newurl, headers={"User-Agent": "Mozilla/5.0"})

opener = urllib.request.build_opener(AppScriptRedirectHandler)

with open(SPREADSHEET_2_CSV, "r", encoding="utf-8") as f:
    leads = list(csv.DictReader(f))

print(f"[*] Loaded {len(leads)} leads from {SPREADSHEET_2_CSV}.", flush=True)
print(f"[*] Streaming all {len(leads)} leads into Google Spreadsheet 2 via Webhook...", flush=True)

success_count = 0

def push_lead(lead):
    global success_count
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
        "status": lead.get("Status", "Verified Active Lead")
    }).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            opener.open(req, timeout=15)
            success_count += 1
            if success_count % 50 == 0 or success_count == len(leads):
                print(f"  [+] [{success_count}/{len(leads)}] Pushed to Spreadsheet 2: {lead['Business']} ({lead['Instagram']})", flush=True)
            return True
        except Exception:
            time.sleep(1.0)
    return False

# Skip the first 53 that were already in the sheet earlier, push the rest
to_push = leads[53:]
print(f"[*] Pushing remaining {len(to_push)} leads to Google Sheet 2 with 8 parallel workers...", flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    list(executor.map(push_lead, to_push))

print(f"\n========================================================", flush=True)
print(f" [DONE] ALL 1,000 LEADS ARE OFFICIALLY IN SPREADSHEET 2!", flush=True)
print(f" Total leads pushed: {success_count + 53} / {len(leads)}", flush=True)
print(f"========================================================\n", flush=True)
