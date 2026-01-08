import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class ChannelsNewsScraper:
    """Scraper for Channels TV Nigeria news"""
    
    def __init__(self):
        self.base_url = "https://www.channelstv.com"
        self.news_url = f"{self.base_url}/category/news/"
    
    def get_source_name(self) -> str:
        return "Channels TV Nigeria"
    
    def scrape(self) -> List[Dict]:
        """Scrape latest Nigerian news from Channels TV"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article tags
            article_elements = soup.find_all('article', limit=10)
            
            for article in article_elements:
                try:
                    # Find title in h2 or h3
                    title_elem = article.find('h2') or article.find('h3')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Find link - could be on title or article itself
                    link_elem = title_elem.find_parent('a') or article.find('a', href=True)
                    if not link_elem:
                        continue
                    
                    link = link_elem.get('href', '')
                    
                    # Ensure full URL
                    if link and not link.startswith('http'):
                        link = self.base_url + link if not link.startswith('/') else self.base_url + link
                    
                    # Find excerpt
                    excerpt = ""
                    p_elem = article.find('p')
                    if p_elem:
                        excerpt = p_elem.get_text(strip=True)
                    
                    # Only add if we have both title and link
                    if title and link and len(articles) < 5:
                        articles.append({
                            'title': title,
                            'link': link,
                            'excerpt': excerpt[:200] + "..." if len(excerpt) > 200 else excerpt,
                            'source': self.get_source_name()
                        })
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            print(f"Error scraping Channels TV: {e}")
            return []
