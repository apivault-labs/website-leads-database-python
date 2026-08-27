from website_leads_database import WebsiteLeadsDatabaseClient

for count in (10, 100, 1000):
    print(count, WebsiteLeadsDatabaseClient.estimate_cost(count), "USD estimated result charges")
