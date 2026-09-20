from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
rows = client.run({
    "platforms": ["shopify_sites", "woocommerce_sites"],
    "country": ["US"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "contacts",
    "maxItems": 50,
})

print(f"Received {len(rows)} sample rows")
