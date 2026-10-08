import csv
import json
import time
import os
import smtplib
import socket
import argparse
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict

# ==============================================================================
# CONFIGURATION & TEMPLATES
# ==============================================================================
SUBJECT_TEMPLATE = "Quick question about {Business}'s social media"

BODY_TEMPLATE = """Hi {First Name},

I know this is a cold email, so I'll keep it short.

I came across {Business} on Instagram and liked {liked_work}. But also noticed your reach isn't justifying your {work_noun}.

I run social media for {field_brands} brands: content planning, posting, and engagement, so {owner_title} don't have to think about it. For a similar {field_singular} brand, we grew reach by 40% in 2 months.

Would you be open to a quick 10-minute chat this week to see if it's a fit?

Best regards,
Marwah Bakshish
2M Creative Media"""

SENT_HISTORY_FILE = "sent_history.csv"
LEADS_FILE = "leads.csv"
NICHES_FILE = "niches.json"
ENV_FILE = ".env"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def load_env(env_path=ENV_FILE):
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip().strip('"').strip("'")
    return config

def load_niches(niches_file=NICHES_FILE):
    if os.path.exists(niches_file):
        with open(niches_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def is_domain_valid(email):
    """Verifies that the recipient's domain is active on public DNS."""
    try:
        domain = email.split("@")[1].strip()
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def load_sent_emails(history_file=SENT_HISTORY_FILE):
    """Returns a set of all email addresses that have ever been sent an email."""
    sent = set()
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("Email", "").strip().lower()
                if email:
                    sent.add(email)
    return sent

def record_sent_email(lead, status="Sent", history_file=SENT_HISTORY_FILE):
    """Appends sent lead to permanent sent history and spreadsheet tracker with Date Sent, Instagram, and Followers."""
    for filepath in [history_file, "outreach_tracking_sheet.csv"]:
        file_exists = os.path.exists(filepath)
        with open(filepath, "a", encoding="utf-8", newline="") as f:
            fieldnames = ["Date Sent", "Business", "First Name", "Email", "Instagram", "Followers", "Field", "Tier", "Location", "Website", "Status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Date Sent": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Business": lead.get("Business", ""),
                "First Name": lead.get("First Name", ""),
                "Email": lead.get("Email", "").strip().lower(),
                "Instagram": lead.get("Instagram", ""),
                "Followers": lead.get("Followers", "Under 5k"),
                "Field": lead.get("Field", ""),
                "Tier": lead.get("Tier", ""),
                "Location": lead.get("Location", ""),
                "Website": lead.get("Website", ""),
    # Post directly to Google Sheet if Webhook URL is set
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL", "").strip()
    if webhook_url:
        try:
            import urllib.request, json
            payload = json.dumps({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "business": lead.get("Business", ""),
                "name": lead.get("First Name", ""),
                "email": lead.get("Email", "").strip().lower(),
                "instagram": lead.get("Instagram", ""),
                "followers": lead.get("Followers", "Under 5k"),
                "field": lead.get("Field", ""),
                "tier": lead.get("Tier", ""),
                "location": lead.get("Location", ""),
                "website": lead.get("Website", ""),
                "status": status
            }).encode("utf-8")
            req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
            print("  [✓] Synced live to Google Sheet!")
        except Exception as e:
            print(f"  [!] Note: Google Sheet sync skipped: {e}")


def render_email(lead, niches):
    field = lead.get("Field", "").strip()
    niche_data = niches.get(field, niches.get("Default", {
        "liked_work": "the creative work and projects you guys are doing",
        "work_noun": "work",
        "field_brands": "design and lifestyle",
        "owner_title": "business owners and founders",
        "field_singular": "lifestyle"
    }))
    
    first_name = lead.get("First Name", "there").strip()
    business = lead.get("Business", "your brand").strip()
    
    context = {
        "First Name": first_name,
        "Business": business,
        "liked_work": niche_data.get("liked_work", ""),
        "work_noun": niche_data.get("work_noun", "work"),
        "field_brands": niche_data.get("field_brands", "furniture"),
        "owner_title": niche_data.get("owner_title", "owners"),
        "field_singular": niche_data.get("field_singular", "furniture")
    }
    
    subject = SUBJECT_TEMPLATE.format(Business=business)
    body = BODY_TEMPLATE.format(**context)
    return subject, body

def get_unsent_batch(leads_file=LEADS_FILE, limit=200):
    if not os.path.exists(leads_file):
        print(f"[!] Error: {leads_file} not found.")
        return []

    sent_emails = load_sent_emails()
    
    with open(leads_file, "r", encoding="utf-8") as f:
        all_leads = list(csv.DictReader(f))

    # Filter out already-contacted leads
    unsent_leads = [
        lead for lead in all_leads 
        if lead.get("Email", "").strip().lower() not in sent_emails
    ]

    total_skipped = len(all_leads) - len(unsent_leads)
    if total_skipped > 0:
        print(f"[*] Dedup check: Skipped {total_skipped} leads that already received an email.")

    if not unsent_leads:
        return []

    # Group unsent leads by field to create a balanced mix across industries
    field_groups = defaultdict(list)
    for lead in unsent_leads:
        field_groups[lead.get("Field", "Other")].append(lead)

    # Round-robin selection across fields up to the daily limit
    balanced_batch = []
    fields = list(field_groups.keys())
    while len(balanced_batch) < limit and any(field_groups.values()):
        for f in fields:
            if field_groups[f]:
                balanced_batch.append(field_groups[f].pop(0))
                if len(balanced_batch) >= limit:
                    break

    return balanced_batch

# ==============================================================================
# PREVIEW & SEND WORKFLOWS
# ==============================================================================
def preview_campaign(limit=200):
    niches = load_niches()
    batch = get_unsent_batch(limit=limit)

    if not batch:
        print("\n[!] No unsent leads available. All leads have already been contacted!")
        return

    print(f"\n========================================================")
    print(f"  PREVIEW MODE: Daily Batch of {len(batch)} Leads Across Diverse Fields")
    print(f"========================================================\n")

    for i, lead in enumerate(batch, 1):
        subject, body = render_email(lead, niches)
        field = lead.get("Field")
        website = lead.get("Website", "N/A")
        ig = lead.get("Instagram", "N/A")
        location = lead.get("Location", "International")
        valid = "Verified Active Domain" if is_domain_valid(lead.get("Email", "")) else "Unverified"
        
        print(f"--- [Email {i}/{len(batch)} | Field: {field} | {location}] ---")
        print(f"Proof of Real Business: Website: {website} | IG: {ig} | DNS: {valid}")
        print(f"To: {lead.get('Email')}")
        print(f"Subject: {subject}\n")
        print(body)
        print("\n" + "="*56 + "\n")

    print(f"[*] To send this batch, run: python send_emails.py --send --limit {limit}")

def send_campaign(limit=200):
    config = load_env()
    gmail_user = config.get("GMAIL_ADDRESS") or os.environ.get("GMAIL_ADDRESS")
    gmail_pass = config.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        print("\n[!] Error: Gmail credentials missing.")
        print("Please copy '.env.example' to '.env' and enter your GMAIL_ADDRESS and GMAIL_APP_PASSWORD.")
        return

    batch = get_unsent_batch(limit=limit)
    if not batch:
        print("\n[!] No unsent leads available. All leads have already received an email.")
        return

    niches = load_niches()
    delay_min = int(config.get("DELAY_MIN", 40))
    delay_max = int(config.get("DELAY_MAX", 80))

    print(f"\n[*] Starting cold outreach campaign...")
    print(f"[*] Target for today: {len(batch)} emails (balanced across fields)")
    print(f"[*] Sender: {gmail_user}")
    print(f"[*] Deduplication: Active (Logged to {SENT_HISTORY_FILE})")
    print(f"[*] Delay between sends: {delay_min}s - {delay_max}s\n")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_pass)
        print("[+] Logged into Gmail SMTP successfully.\n")
    except Exception as e:
        print(f"[!] SMTP Connection Failed: {e}")
        return

    sent_count = 0
    for i, lead in enumerate(batch, 1):
        to_email = lead.get("Email", "").strip()
        if not to_email:
            continue

        # Authenticity / DNS check
        if not is_domain_valid(to_email):
            print(f"[{i}/{len(batch)}] SKIPPED (Invalid/Dead Domain) -> {to_email}")
            record_sent_email(lead, status="Skipped: Invalid Domain")
            continue

        subject, body = render_email(lead, niches)
        msg = MIMEMultipart()
        msg["From"] = f"Marwah Bakshish <{gmail_user}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            server.sendmail(gmail_user, to_email, msg.as_string())
            sent_count += 1
            record_sent_email(lead, status="Sent")
            print(f"[{i}/{len(batch)}] SENT -> {lead.get('Business')} ({to_email}) | Field: {lead.get('Field')} | Name: {lead.get('First Name')}")
        except Exception as err:
            print(f"[!] FAILED sending to {to_email}: {err}")
            record_sent_email(lead, status=f"Failed: {err}")

        # Natural delay between emails to protect sender inbox health
        if i < len(batch):
            wait_time = random.randint(delay_min, delay_max)
            print(f"    -> Pausing {wait_time}s to maintain high inbox deliverability...")
            time.sleep(wait_time)

    server.quit()
    print(f"\n========================================================")
    print(f" [DONE] Campaign completed: {sent_count} emails delivered today.")
    print(f" All sent leads recorded in '{SENT_HISTORY_FILE}'.")
    print(f" They will NEVER be emailed again in future runs.")
    print(f"========================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2M Creative Media Cold Outreach Engine")
    parser.add_argument("--send", action="store_true", help="Send live emails (default is preview mode)")
    parser.add_argument("--limit", type=int, default=200, help="Number of emails to send per day (default 200)")
    args = parser.parse_args()

    if args.send:
        send_campaign(limit=args.limit)
    else:
        preview_campaign(limit=args.limit)
