from website_leads_database import WebsiteLeadsDatabaseClient

client = WebsiteLeadsDatabaseClient()
query = {
    "platforms": ["shopify_sites"],
    "hasEmail": True,
    "dedupeByDomain": True,
    "outputPreset": "contacts",
    "maxItems": 50,
}

first_page = client.run_page(query)
print(f"First page: {len(first_page['rows'])} rows")

continuation = first_page["continuation"] or {}
resume_input = continuation.get("resumeInput")
if resume_input and continuation.get("hasMore"):
    second_page = client.run_page(resume_input)
    print(f"Second page: {len(second_page['rows'])} rows")
else:
    print("No next page is available")
