import csv
from website_leads_database import WebsiteLeadsDatabaseClient

rows = WebsiteLeadsDatabaseClient().run({'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'maxItems': 100})
if rows:
    scalar_keys = [k for k, v in rows[0].items() if not isinstance(v, (dict, list))]
    with open("results.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=scalar_keys)
        writer.writeheader()
        writer.writerows({k: row.get(k) for k in scalar_keys} for row in rows)
