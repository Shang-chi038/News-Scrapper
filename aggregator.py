from datetime import datetime
from typing import Dict, List
import json

class NewsAggregator:
    """Main aggregator that coordinates all scrapers"""
    
    def __init__(self, scrapers: List):
        self.scrapers = scrapers
    
    def collect_all_news(self) -> Dict[str, List[Dict]]:
        """Collect news from all sources"""
        all_news = {}
        
        for scraper in self.scrapers:
            source_name = scraper.get_source_name()
            print(f"Scraping {source_name}...")
            articles = scraper.scrape()
            all_news[source_name] = articles
            print(f"Found {len(articles)} articles from {source_name}")
        
        return all_news
    
    def generate_text_digest(self) -> str:
        """Generate a plain text formatted digest"""
        all_news = self.collect_all_news()
        
        digest = f"Daily News Digest - {datetime.now().strftime('%B %d, %Y')}\n"
        digest += "=" * 60 + "\n\n"
        
        for source, articles in all_news.items():
            digest += f"\n📰 {source.upper()}\n"
            digest += "-" * 60 + "\n"
            
            if not articles:
                digest += "No articles found.\n"
            else:
                for i, article in enumerate(articles, 1):
                    digest += f"\n{i}. {article['title']}\n"
                    if article.get('excerpt'):
                        digest += f"   {article['excerpt']}\n"
                    digest += f"   🔗 {article['link']}\n"
            
            digest += "\n"
        
        return digest
    
    def generate_html_digest(self) -> str:
        """Generate an HTML formatted digest for email"""
        all_news = self.collect_all_news()
        
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                    border-left: 4px solid #3498db;
                    padding-left: 10px;
                }}
                .article {{
                    margin: 20px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                .article-title {{
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 8px;
                }}
                .article-excerpt {{
                    color: #555;
                    margin-bottom: 8px;
                    font-size: 14px;
                }}
                .article-link {{
                    color: #3498db;
                    text-decoration: none;
                }}
                .article-link:hover {{
                    text-decoration: underline;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #777;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <h1>📰 Daily News Digest</h1>
            <p style="color: #777;">{datetime.now().strftime('%B %d, %Y')}</p>
        """
        
        for source, articles in all_news.items():
            html += f"<h2>{source}</h2>"
            
            if not articles:
                html += "<p>No articles found.</p>"
            else:
                for article in articles:
                    html += f"""
                    <div class="article">
                        <div class="article-title">{article['title']}</div>
                        <div class="article-excerpt">{article.get('excerpt', '')}</div>
                        <a href="{article['link']}" class="article-link">Read more →</a>
                    </div>
                    """
        
        html += """
            <div class="footer">
                <p>This is your automated daily news digest.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def save_to_json(self, filename: str = 'daily_news.json'):
        """Save collected news to JSON file"""
        news_data = self.collect_all_news()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        print(f"News saved to {filename}")

