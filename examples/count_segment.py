from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
summary = client.count({
    "platforms": ["shopify_sites", "woocommerce_sites"],
    "country": ["US"],
    "hasEmail": True,
})

print(summary)
