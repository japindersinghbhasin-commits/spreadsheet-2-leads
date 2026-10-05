/**
 * 2M Creative Media - Cloud Outreach Engine (Runs 24/7 in Google Cloud)
 * 
 * Works even when your computer is turned OFF!
 * Daily Quota: 200 emails / day
 * Deduplication: Automatically marks "Sent" in column G and skips contacted leads.
 */

const NICHES = {
  "Furniture": {
    liked_work: "the custom dining tables and handcrafted furniture you guys are making",
    work_noun: "craftsmanship",
    field_brands: "furniture",
    owner_title: "furniture makers and founders",
    field_singular: "furniture"
  },
  "Luxury Furniture": {
    liked_work: "the modern furniture designs and workshop finishes you guys are creating",
    work_noun: "designs",
    field_brands: "custom and luxury furniture",
    owner_title: "furniture designers and studio owners",
    field_singular: "furniture"
  },
  "Interior Design": {
    liked_work: "the residential interior projects and transformations you guys are designing",
    work_noun: "designs",
    field_brands: "interior design",
    owner_title: "designers and studio founders",
    field_singular: "interior design"
  },
  "Home Decor & Lighting": {
    liked_work: "the aesthetic home decor pieces and curated lighting you guys are showcasing",
    work_noun: "products",
    field_brands: "home decor and lighting",
    owner_title: "brand owners and creative directors",
    field_singular: "home decor"
  },
  "Architecture": {
    liked_work: "the contemporary residential architecture and site builds you guys are doing",
    work_noun: "portfolio",
    field_brands: "architecture",
    owner_title: "principal architects and firm owners",
    field_singular: "architecture"
  },
  "Real Estate": {
    liked_work: "the luxury property tours and home showcases you guys are posting",
    work_noun: "listings",
    field_brands: "real estate",
    owner_title: "brokers and agents",
    field_singular: "real estate"
  },
  "Jewelry & Luxury Goods": {
    liked_work: "the handcrafted jewelry collections and details you guys are crafting",
    work_noun: "pieces",
    field_brands: "fine jewelry and luxury",
    owner_title: "designers and brand founders",
    field_singular: "jewelry"
  },
  "Default": {
    liked_work: "the creative work and products you guys are putting out",
    work_noun: "work",
    field_brands: "design and lifestyle",
    owner_title: "founders and business owners",
    field_singular: "lifestyle"
  }
};

function sendDailyBatch() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  
  // Column indices (0-based)
  // Assumes headers: First Name, Business, Email, Field, Tier, Location, Status, Date Sent
  const colFirstName = headers.indexOf("First Name");
  const colBusiness = headers.indexOf("Business");
  const colEmail = headers.indexOf("Email");
  const colField = headers.indexOf("Field");
  const colTier = headers.indexOf("Tier");
  const colStatus = headers.indexOf("Status");
  const colDateSent = headers.indexOf("Date Sent");

  const DAILY_LIMIT = 200;
  let sentToday = 0;

  for (let i = 1; i < data.length; i++) {
    if (sentToday >= DAILY_LIMIT) break;

    const row = data[i];
    const email = String(row[colEmail]).trim();
    const status = String(row[colStatus]).trim();

    // Skip if already sent or missing email
    if (!email || status.toLowerCase() === "sent") {
      continue;
    }

    const firstName = String(row[colFirstName]).trim() || "there";
    const business = String(row[colBusiness]).trim() || "your brand";
    const field = String(row[colField]).trim();
    const niche = NICHES[field] || NICHES["Default"];

    const subject = `Quick question about ${business}'s social media`;
    const body = 
`Hi ${firstName},

I know this is a cold email, so I'll keep it short.

I came across ${business} on Instagram and liked ${niche.liked_work}. But also noticed your reach isn't justifying your ${niche.work_noun}.

I run social media for ${niche.field_brands} brands: content planning, posting, and engagement, so ${niche.owner_title} don't have to think about it. For a similar ${niche.field_singular} brand, we grew reach by 40% in 2 months.

Would you be open to a quick 10-minute chat this week to see if it's a fit?

Best regards,
Marwah Bakshish
2M Creative Media`;

    try {
      GmailApp.sendEmail(email, subject, body, {
        name: "Marwah Bakshish"
      });

      // Update row in Google Sheet immediately
      sheet.getRange(i + 1, colStatus + 1).setValue("Sent");
      sheet.getRange(i + 1, colDateSent + 1).setValue(new Date().toISOString());

      sentToday++;
      Utilities.sleep(1500); // polite pause
    } catch (err) {
      Logger.log(`Error sending to ${email}: ${err}`);
      sheet.getRange(i + 1, colStatus + 1).setValue("Failed: " + err);
    }
  }

  Logger.log(`Finished sending batch. Total sent today: ${sentToday}`);
}
