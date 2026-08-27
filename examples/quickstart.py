from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
rows = client.run({'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'maxItems': 100})
print(rows[0] if rows else "No results")
