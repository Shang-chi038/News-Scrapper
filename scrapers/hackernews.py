import requests
from typing import List, Dict

class HackerNewsScraper:
    """Scraper for Hacker News - top 2 stories of the day"""
    
    def __init__(self):
        self.api_url = "https://hacker-news.firebaseio.com/v0"
    
    def get_source_name(self) -> str:
        return "Hacker News"
    
    def scrape(self) -> List[Dict]:
        """Scrape top 2 stories from Hacker News"""
        try:
            response = requests.get(f"{self.api_url}/topstories.json", timeout=10)
            response.raise_for_status()
            top_ids = response.json()[:2]
            
            articles = []
            for story_id in top_ids:
                try:
                    story_response = requests.get(
                        f"{self.api_url}/item/{story_id}.json",
                        timeout=10
                    )
                    story_response.raise_for_status()
                    story = story_response.json()
                    
                    if story and story.get('title'):
                        articles.append({
                            'title': story.get('title', ''),
                            'link': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'excerpt': f"Points: {story.get('score', 0)} | Comments: {story.get('descendants', 0)}",
                            'source': self.get_source_name()
                        })
                        
                except Exception as e:
                    print(f"Error fetching HN story {story_id}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            print(f"Error scraping Hacker News: {e}")
            return []

