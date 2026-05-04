import requests
from bs4 import BeautifulSoup

url = "https://www.channelstv.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('article', limit=5)
print(f"Found {len(articles)} articles\n")

for i, article in enumerate(articles, 1):
    print(f"=== Article {i} ===")
    h2 = article.find('h2')
    h3 = article.find('h3')
    print(f"H2: {h2.get_text(strip=True) if h2 else 'None'}")
    print(f"H3: {h3.get_text(strip=True) if h3 else 'None'}")
    
    link = article.find('a', href=True)
    print(f"Link: {link['href'] if link else 'None'}\n")
