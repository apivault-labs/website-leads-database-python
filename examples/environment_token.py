import os
from website_leads_database import WebsiteLeadsDatabaseClient

if not os.environ.get("APIFY_API_TOKEN"):
    raise SystemExit("Set APIFY_API_TOKEN before running this example")
client = WebsiteLeadsDatabaseClient()
print(client.run_one({'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'maxItems': 100}))
