import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class TechCrunchScraper:
    """Scraper for TechCrunch - focusing on business news, filtering out gadget reviews"""
    
    def __init__(self):
        self.rss_url = "https://techcrunch.com/feed/"
    
    def get_source_name(self) -> str:
        return "TechCrunch"
    
    def _is_business_focused(self, title: str, description: str) -> bool:
        """Filter out gadget reviews and keep business-focused articles"""
        combined_text = (title + " " + description).lower()
        
        exclude_keywords = [
            'review', 'hands-on', 'unboxing', 'vs', 'comparison',
            'best', 'top 10', 'how to', 'guide', 'tutorial'
        ]
        
        include_keywords = [
            'funding', 'raises', 'acquisition', 'merger', 'ipo',
            'launch', 'partnership', 'deal', 'investment', 'startup',
            'revenue', 'valuation', 'series', 'venture', 'acquires'
        ]
        
        if any(keyword in combined_text for keyword in exclude_keywords):
            return False
        
        if any(keyword in combined_text for keyword in include_keywords):
            return True
        
        return 'review' not in combined_text
    
    def scrape(self) -> List[Dict]:
        """Scrape top business-focused headlines from TechCrunch"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.rss_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=15)
            
            articles = []
            for item in items:
                try:
                    title = item.find('title').get_text(strip=True)
                    link = item.find('link').get_text(strip=True)
                    description_elem = item.find('description')
                    description = description_elem.get_text(strip=True) if description_elem else ""
                    
                    if self._is_business_focused(title, description):
                        articles.append({
                            'title': title,
                            'link': link,
                            'excerpt': description[:200] + "..." if len(description) > 200 else description,
                            'source': self.get_source_name()
                        })
                    
                    if len(articles) >= 5:
                        break
                        
                except Exception as e:
                    print(f"Error parsing TechCrunch item: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            print(f"Error scraping TechCrunch: {e}")
            return []

