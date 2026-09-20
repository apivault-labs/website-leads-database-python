# Shopify & Ecommerce Store Finder — Python SDK

Python client for the [Shopify & Ecommerce Store Finder Apify Actor](https://apify.com/apivault_labs/website-leads-database). Send public Actor inputs, wait for the hosted run, and receive clean Dataset rows without maintaining scraping infrastructure.

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue)](https://apify.com/apivault_labs/website-leads-database)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Results

- Platform and country targeting
- Public emails, phones and social profiles
- Firmographic and technology fields
- Sorting, pagination and count-only queries

The repository exposes only the Actor's public input and output contract. Dataset selection and processing remain inside the hosted Actor.

## Install

```bash
pip install git+https://github.com/apivault-labs/website-leads-database-python.git
```

Create an Apify token at [Console → Integrations](https://console.apify.com/account/integrations), then:

```python
from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient(api_token="apify_api_xxxxxx")
rows = client.run({'platforms': ['shopify_sites', 'woocommerce_sites'],
 'country': ['US'],
 'hasEmail': True,
 'dedupeByDomain': True,
 'outputPreset': 'contacts',
 'maxItems': 50})
print(rows[0] if rows else "No results")
```

You can set `APIFY_API_TOKEN` instead of passing the token in code.

## Public input options

| Field | Type | Default | Description |
|---|---|---|---|
| `workflow` | `string` | `auto` | Choose `count` for audience size or `export` for rows. The SDK helpers set this automatically. |
| `outputPreset` | `string` | `custom` | Use `compact`, `contacts`, `sales`, `traffic`, `full` or exact custom columns. |
| `platforms` | `array` | `["all"]` | Platform datasets to search, such as Shopify, WooCommerce, WordPress, Wix, Magento or all platforms. |
| `columns` | `array` | `[]` | Exact public output-column names. Leave empty to return all available columns. |
| `sortBy` | `string` | `` | Optional public column used to order rows before applying the limit. |
| `country` | `array` | `[]` | ISO-2 country codes such as US, GB or DE. |
| `keyword` | `string` | `` | Substring matched against the domain or company name. |
| `phoneCode` | `string` | `` | Keep sites with at least one public phone beginning with this country code. |
| `filters` | `array` | `[]` | Additional public column conditions using column, operator and value fields. |
| `hasEmail` | `boolean` | `False` | Return only records with a public email. |
| `hasPhone` | `boolean` | `False` | Return only records with a public phone. |
| `sortDesc` | `boolean` | `True` | Return highest sort values first. |
| `dedupeByDomain` | `boolean` | `False` | Remove repeated root domains within the selected window. |
| `countOnly` | `boolean` | `False` | Return match counts instead of exporting website rows. |
| `onlyWithTrafficData` | `boolean` | `False` | Keep only rows with traffic data. |
| `minMonthlyVisits` | `integer` |  | Optional minimum monthly visits for traffic-qualified exports. |
| `maxMonthlyVisits` | `integer` |  | Optional maximum monthly visits for traffic-qualified exports. |
| `maxItems` | `integer` | `1000` | Maximum returned rows across selected platforms. |
| `offset` | `integer` | `0` | Rows to skip for stable pagination across runs. |

The complete, versioned schema is also available on the [Actor page](https://apify.com/apivault_labs/website-leads-database).

## Pricing

Pay per delivered result through Apify, starting around **$8/1,000 results** on paid tiers. Free-plan pricing and platform usage can differ; check the Actor page before large runs.

## Examples

- [`guides/shopify-leads-to-crm.md`](guides/shopify-leads-to-crm.md) — count, sample, qualify and continue a Shopify lead segment

- `examples/count_segment.py` — inspect audience size before export
- `examples/sample_50.py` — review a safe 50-row sample
- `examples/export_contacts.py` — save Shopify contacts to CSV
- `examples/traffic_qualified_export.py` — prioritize stores by audience size
- `examples/resume_next_page.py` — continue with the Actor-provided next-page input
- `examples/quickstart.py` — minimal first run
- `examples/export_csv.py` — save flat result fields
- `examples/save_json.py` — preserve nested output
- `examples/cost_estimate.py` — estimate result-event charges
- `examples/environment_token.py` — keep credentials out of code

Use `client.count(...)` before a large request. Use `client.run_page(...)` when you
need the copy-ready continuation returned by the hosted Actor.

## Architecture and privacy

This repository is intentionally a thin API client. Collection, retries, analysis and billing run inside the hosted Apify Actor. No private implementation, credentials, scoring weights or infrastructure configuration are included.

## License

MIT. The hosted Actor is a separate paid service governed by Apify terms.
