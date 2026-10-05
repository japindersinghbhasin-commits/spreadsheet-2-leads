# 2M Creative Media - Cold Outreach Automation

This automation delivers cold emails using your exact template, strictly adheres to field-based bracket personalization, limits daily volume, and guarantees **no person is ever emailed twice**.

---

## Key Rules Built In

1. **One-Time Only (Strict De-duplication):**
   - Every email sent is permanently recorded in `sent_history.csv` with a timestamp and status.
   - When the script runs tomorrow or any day after, it automatically cross-references `sent_history.csv` and skips anyone who was previously contacted.
2. **Zero Automated Replies:**
   - The script is purely outbound. When a client replies, it lands directly in your standard Gmail inbox so you can personally handle the conversation and close the client.
3. **Daily Quota (200 Emails/Day):**
   - The script picks up to 200 unsent leads per run.
   - It balances across different fields (Furniture, Interior Design, Home Decor, Architecture, etc.) and across your target tiers (**International**, **Premium Local**, and **Local**).
4. **Safe Deliverability Spacing:**
   - Emails are spaced with randomized 40–80 second delays to avoid spam filters and protect your Gmail account.

---

## File Structure

- `send_emails.py` — The core outreach script.
- `leads.csv` — Your lead list (`First Name`, `Business`, `Email`, `Field`, `Tier`, `Location`).
- `niches.json` — Dictionary of field-specific brackets.
- `sent_history.csv` — Automatically created log of every sent email (prevents duplicate sending forever).
- `.env` — Your Gmail credentials (`GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD`).

---

## How to Run Every Day

### 1. Preview Today's Batch (No emails sent)
```bash
python send_emails.py --limit 200
```

### 2. Send Today's 200 Emails
```bash
python send_emails.py --send --limit 200
```
On the next day, simply run the same command: it will skip everyone from yesterday and pick the next 200 fresh leads!
