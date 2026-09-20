import csv

from website_leads_database import WebsiteLeadsDatabaseClient

rows = WebsiteLeadsDatabaseClient().run({
    "platforms": ["shopify_sites"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "contacts",
    "maxItems": 50,
})

fields = ["Root Domain", "Company Name", "Emails", "Telephones", "Country"]
with open("shopify_contacts.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to shopify_contacts.csv")
