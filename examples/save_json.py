import json
from website_leads_database import WebsiteLeadsDatabaseClient

rows = WebsiteLeadsDatabaseClient().run({'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'maxItems': 100})
with open("results.json", "w", encoding="utf-8") as handle:
    json.dump(rows, handle, ensure_ascii=False, indent=2)
