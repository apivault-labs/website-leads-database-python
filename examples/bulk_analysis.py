from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
payload = {'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'maxItems': 100}
# Add more targets or queries to the list fields supported by this Actor.
rows = client.run(payload)
print(f"Received {len(rows)} rows")
