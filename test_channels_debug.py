import requests
from bs4 import BeautifulSoup

url = "https://www.channelstv.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"Fetching: {url}\n")
response = requests.get(url, headers=headers, timeout=10)
print(f"Status Code: {response.status_code}\n")

soup = BeautifulSoup(response.content, 'html.parser')

# Test different selectors
print("=== Testing h3 selector ===")
h3_elements = soup.select('a h3')
print(f"Found {len(h3_elements)} h3 elements inside links")
for i, h3 in enumerate(h3_elements[:5], 1):
    print(f"{i}. {h3.get_text(strip=True)}")

print("\n=== Testing article tags ===")
articles = soup.find_all('article')
print(f"Found {len(articles)} article tags")

print("\n=== Testing div with h3 ===")
divs_with_h3 = soup.find_all('div', class_=lambda x: x and 'article' in x.lower() if x else False)
print(f"Found {len(divs_with_h3)} divs with 'article' in class name")

print("\n=== Looking at Top Stories section ===")
top_stories = soup.find('h3', string=lambda x: 'Top Stories' in x if x else False)
if top_stories:
    print("Found 'Top Stories' section")
    parent = top_stories.find_parent()
    if parent:
        links = parent.find_all('a', href=True)[:5]
        print(f"Found {len(links)} links in Top Stories")
        for i, link in enumerate(links, 1):
            h3 = link.find('h3')
            if h3:
                print(f"{i}. {h3.get_text(strip=True)}")
                print(f"   URL: {link['href']}")
