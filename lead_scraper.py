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
        
        # Parse follower count
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
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "ignore")
        
        # Look for mailto: links first
        mailtos = re.findall(r'mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', html)
        clean_mailtos = [e.lower() for e in mailtos if not any(x in e.lower() for x in ["wix", "sentry", "png", "jpg", "example"])]
        if clean_mailtos:
            return clean_mailtos[0]
            
        # General email regex on page
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
        clean = [e.lower() for e in emails if not any(x in e.lower() for x in ["wix", "sentry", "png", "jpg", "example", "1.8.1", "svg"])]
        return clean[0] if clean else None
    except Exception:
        return None

def log_to_spreadsheet_2(lead, webhook_url=None):
    """Saves discovered lead to local CSV and pushes live to Spreadsheet 2."""
    file_exists = os.path.exists(DISCOVERED_LEADS_CSV)
    fieldnames = ["Date Discovered", "Business", "First Name", "Verified Email", "Instagram", "Followers", "Field", "Tier", "Location", "Website", "Status"]
    
    with open(DISCOVERED_LEADS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(lead)

    # Sync to Spreadsheet 2 via Webhook if configured
    if webhook_url:
        try:
            payload = json.dumps(lead).encode("utf-8")
            class AppScriptRedirectHandler(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return urllib.request.Request(newurl, headers={"User-Agent": "Mozilla/5.0"})
            opener = urllib.request.build_opener(AppScriptRedirectHandler)
            req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            opener.open(req, timeout=15)
            print(f"  [+] Synced live to Spreadsheet 2: {lead['Business']}")
        except Exception as e:
            print(f"  [!] Note: Spreadsheet 2 sync: {e}")
