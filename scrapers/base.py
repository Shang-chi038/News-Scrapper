from abc import ABC, abstractmethod
from typing import List, Dict

class NewsScraper(ABC):
    """Base class for all news scrapers"""
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape news and return list of articles"""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the news source"""
        pass
