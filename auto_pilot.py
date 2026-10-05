import re
import os
import time
import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httpx

# ==============================================================================
# CONFIGURATION
# ==============================================================================
GMAIL_USER = "aloneviber0102@gmail.com"
SENT_HISTORY_FILE = "sent_history.csv"
ENV_FILE = ".env"

NICHES = {
  "Furniture": {
    "liked_work": "the custom dining tables and handcrafted furniture you guys are making",
    "work_noun": "craftsmanship",
    "field_brands": "furniture",
    "owner_title": "furniture makers and founders",
    "field_singular": "furniture"
  },
  "Luxury Furniture": {
    "liked_work": "the modern furniture designs and workshop finishes you guys are creating",
    "work_noun": "designs",
    "field_brands": "custom and luxury furniture",
    "owner_title": "furniture designers and studio owners",
    "field_singular": "furniture"
  },
  "Interior Design": {
    "liked_work": "the residential interior projects and transformations you guys are designing",
    "work_noun": "designs",
    "field_brands": "interior design",
    "owner_title": "designers and studio founders",
    "field_singular": "interior design"
  },
  "Home Decor & Lighting": {
    "liked_work": "the aesthetic home decor pieces and curated lighting you guys are showcasing",
    "work_noun": "products",
    "field_brands": "home decor and lighting",
    "owner_title": "brand owners and creative directors",
    "field_singular": "home decor"
  }
}

BODY_TEMPLATE = """Hi {First Name},

I know this is a cold email, so I'll keep it short.

I came across {Business} on Instagram and liked {liked_work}. But also noticed your reach isn't justifying your {work_noun}.

I run social media for {field_brands} brands: content planning, posting, and engagement, so {owner_title} don't have to think about it. For a similar {field_singular} brand, we grew reach by 40% in 2 months.

Would you be open to a quick 10-minute chat this week to see if it's a fit?

Best regards,
Marwah Bakshish
2M Creative Media"""

def load_env():
    config = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config

def get_already_sent():
    sent = set()
    if os.path.exists(SENT_HISTORY_FILE):
        with open(SENT_HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts:
                    sent.add(parts[0].lower().strip())
    return sent

def log_sent(email, business, first_name, field, tier, location, status):
    exists = os.path.exists(SENT_HISTORY_FILE)
    with open(SENT_HISTORY_FILE, "a", encoding="utf-8") as f:
        if not exists:
            f.write("Email,Business,First Name,Field,Tier,Location,Date Sent,Status\n")
        f.write(f'"{email}","{business}","{first_name}","{field}","{tier}","{location}","{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}","{status}"\n')

def extract_emails_from_text(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found = re.findall(pattern, text)
    valid = []
    # Filter out common junk image/font extensions masquerading as emails
    for e in found:
        e_lower = e.lower()
        if not any(e_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"]):
            valid.append(e_lower)
    return list(set(valid))

def render_email(first_name, business, field):
    niche = NICHES.get(field, NICHES["Furniture"])
    subject = f"Quick question about {business}'s social media"
    body = BODY_TEMPLATE.format(
        **{
            "First Name": first_name or "there",
            "Business": business,
            "liked_work": niche["liked_work"],
            "work_noun": niche["work_noun"],
            "field_brands": niche["field_brands"],
            "owner_title": niche["owner_title"],
            "field_singular": niche["field_singular"]
        }
    )
    return subject, body

def send_one_email(server, from_email, to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = f"Marwah Bakshish <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    server.sendmail(from_email, to_email, msg.as_string())

if __name__ == "__main__":
    print("=== Auto-Pilot Outreach Engine ===")
    config = load_env()
    app_pass = config.get("GMAIL_APP_PASSWORD", "")

    if not app_pass or "xxxx" in app_pass or "your_" in app_pass:
        print("\n[!] ACTION REQUIRED: Add your Google App Password to .env")
        print("    1. Go to: https://myaccount.google.com/apppasswords")
        print("    2. Generate an app password for 'Mail'")
        print("    3. Paste the 16 letters into .env next to GMAIL_APP_PASSWORD")
    else:
        print(f"[+] Gmail App Password detected for {GMAIL_USER}")
