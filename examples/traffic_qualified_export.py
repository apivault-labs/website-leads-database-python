from website_leads_database import WebsiteLeadsDatabaseClient

rows = WebsiteLeadsDatabaseClient().run({
    "platforms": ["shopify_sites", "woocommerce_sites"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "traffic",
    "onlyWithTrafficData": True,
    "minMonthlyVisits": 10_000,
    "maxItems": 50,
})

for row in rows:
    print(row.get("Root Domain"), row.get("Monthly Visits"), row.get("Emails"))
