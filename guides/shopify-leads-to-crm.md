# From 69M websites to 50 qualified Shopify leads

This playbook turns a broad website audience into a small, review-ready CRM list using the hosted [Shopify & Ecommerce Store Finder](https://apify.com/apivault_labs/website-leads-database).

The goal is not to export the largest possible file on the first run. Start with a count, inspect 50 results, confirm the segment, and only then continue to larger pages.

## 1. Count the audience before exporting

Use the same public filters you plan to export, but choose the count workflow:

```python
from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
summary = client.count({
    "platforms": ["shopify_sites"],
    "country": ["US"],
    "hasEmail": True,
})
print(summary)
```

The count does not create paid lead rows. Apify platform usage may still apply. Use it to decide whether to narrow the country, platform or contact requirements before exporting results.

## 2. Review a 50-row sample

```python
rows = client.run({
    "platforms": ["shopify_sites"],
    "country": ["US"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "contacts",
    "maxItems": 50,
})
```

Check the domain, company, country, available email and phone fields. A missing optional field does not prove that the business has no such contact; it only means the field was not available in that result.

## 3. Add traffic qualification when it helps

For an established-store campaign, request traffic data and set a minimum audience threshold:

```python
rows = client.run({
    "platforms": ["shopify_sites"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "traffic",
    "onlyWithTrafficData": True,
    "minMonthlyVisits": 10_000,
    "maxItems": 50,
})
```

Traffic figures are estimates and coverage varies by domain. Use them as prioritization signals, not guaranteed measurements.

## 4. Prepare a review-first CRM row

Useful CRM fields include:

- Root Domain;
- Company and Country;
- Emails and Telephones;
- eCommerce Platform and CMS Platform;
- Monthly Visits when traffic enrichment is enabled;
- an internal review status and campaign owner.

Review relevance and personalize outreach before contacting a business. Do not treat a public contact as automatic consent for every marketing channel.

## 5. Continue without repeating the first page

Use `run_page` when you need the copy-ready continuation returned by the Actor:

```python
page = client.run_page({
    "platforms": ["shopify_sites"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "contacts",
    "maxItems": 50,
})

continuation = page["continuation"] or {}
resume_input = continuation.get("resumeInput")
if continuation.get("hasMore") and resume_input:
    next_page = client.run_page(resume_input)
```

Keep the Actor-provided continuation unchanged so the next request preserves the selected segment and offset.

## No-code option

Import the maintained [n8n quickstart workflow](https://github.com/apivault-labs/n8n-nodes-apivault-shopify-finder/blob/main/examples/quickstart-workflow.json). It starts with a 50-row traffic-qualified sample and prepares each result for a CRM or manual review queue.

## Expected outcome

You finish with a small list of relevant ecommerce websites, available business contacts and optional traffic signals. Once the sample is useful, repeat the same segment through continuation pages or schedule a reviewed workflow.

The public SDK and n8n node are thin clients to the hosted Actor. They contain no data collection implementation, private sources, credentials or infrastructure configuration.
