from scrapers.channels import ChannelsNewsScraper

scraper = ChannelsNewsScraper()
print(f"Attempting to scrape: {scraper.base_url}")
articles = scraper.scrape()

print(f"\nFound {len(articles)} articles")
for i, article in enumerate(articles, 1):
    print(f"\n{i}. {article['title']}")
    print(f"   Link: {article['link']}")
