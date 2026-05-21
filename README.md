# News Scraper System

A modular Python-based news aggregation system that automatically scrapes daily news from Nigerian and international tech sources, then delivers a beautifully formatted digest via email.

## 📰 What It Does

This system collects news from three sources:

- **Channels TV Nigeria** - Latest Nigerian news
- **TechCrunch** - Business-focused tech news (filters out gadget reviews)
- **Hacker News** - Top 2 trending stories of the day

The collected news is:

- Compiled into an HTML email digest
- Saved locally as JSON
- Sent automatically to configured recipients
- Can run on a daily schedule

---

## 🏗️ Project Architecture

The project follows a modular design pattern where each component has a specific responsibility:

```
News-Scrapper/
├── scrapers/           # Individual news source scrapers
│   ├── __init__.py
│   ├── channels.py
│   ├── techcrunch.py
│   └── hackernews.py
├── aggregator.py       # Coordinates all scrapers
├── email_service.py    # Handles email delivery
├── config.py           # Configuration management
├── scheduler.py        # Automated daily execution
├── main.py             # Entry point
├── .env                # Environment variables (credentials)
├── daily_news.json     # Output: collected news data
└── requirements.txt    # Python dependencies
```

---

## 📁 File Structure & Functionality

### **The `scrapers`** Directory

Contains individual scraper modules for each news source. Each scraper is independent and follows a consistent interface.

#### **`scrapers/channels.py`** - Channels TV Nigeria Scraper

- **Purpose**: Scrapes the latest Nigerian news from Channels TV
- **How it works**:
  - Fetches the Channels TV homepage
  - Parses HTML to find article elements
  - Extracts title, link, and excerpt from each article
  - Returns up to 5 Nigerian news articles
- **Key feature**: Uses a dual-strategy link extraction (checks both parent anchor tags and article-level links for robustness)

#### **`scrapers/techcrunch.py`** - TechCrunch Business News Scraper

- **Purpose**: Scrapes business-focused tech news, filtering out gadget reviews
- **How it works**:
  - Fetches TechCrunch RSS feed
  - Applies intelligent filtering to identify business-related articles
  - Excludes reviews, comparisons, and how-to guides
  - Prioritizes funding announcements, acquisitions, partnerships, and startup news
- **Key feature**: Smart content filtering based on keywords to focus on business activity

#### **`scrapers/hackernews.py`** - Hacker News Top Stories Scraper

- **Purpose**: Retrieves the top 2 trending stories from Hacker News
- **How it works**:
  - Uses the official Hacker News Firebase API
  - Fetches the top stories list
  - Retrieves detailed information for the top 2 stories
  - Includes points and comment counts
- **Key feature**: API-based scraping (more reliable than HTML parsing)

---

### **The Core System Files**

#### **`aggregator.py`** - News Aggregation Engine

- **Purpose**: Orchestrates all scrapers and formats the collected news
- **How it works**:
  - Initializes all scraper instances
  - Calls each scraper's `scrape()` method
  - Collects and organizes results by source
  - Generates both HTML and plain text digests
  - Exports data to JSON format
- **Key feature**: Provides two output formats (HTML for email, text for console/logs)

#### **`email_service.py`** - Email Delivery System

- **Purpose**: Handles SMTP email delivery
- **How it works**:
  - Connects to SMTP server (Gmail by default)
  - Creates multi-part emails (HTML + plain text fallback)
  - Sends digest to configured recipients
  - Includes error handling and logging
- **Key feature**: Supports multiple recipients and uses secure SMTP with TLS

#### **`config.py`** - Configuration Management

- **Purpose**: Centralizes all configuration settings
- **How it works**:
  - Loads environment variables from `.env` file
  - Provides default values for optional settings
  - Validates that required credentials are present
  - Makes configuration accessible throughout the system
- **Key feature**: Uses environment variables to keep credentials secure (never hardcoded)

#### **`scheduler.py`** - Automated Task Scheduler

- **Purpose**: Runs the news scraper automatically on a daily schedule
- **How it works**:
  - Uses the `schedule` library for time-based execution
  - Runs `main.py` at a specified time each day (default: 8:00 AM)
  - Logs all activities to both console and `scraper.log`
  - Keeps running continuously in the background
  - Handles errors gracefully without stopping
- **Key feature**: Supports custom scheduling times via command-line argument

#### **`main.py`** - Application Entry Point

- **Purpose**: Orchestrates the entire scraping workflow
- **How it works**:
  1. Initializes all scraper instances
  2. Creates the aggregator with all scrapers
  3. Generates text and HTML digests
  4. Saves collected news to `daily_news.json`
  5. Sends email digest if configured
  6. Prints summary to console
- **Key feature**: Can be run manually or via the scheduler

---

### **The Data Files**

#### **`daily_news.json`** - Collected News Archive

- **Purpose**: Stores scraped news articles in structured JSON format
- **Structure**: Organized by source with article metadata (title, link, summary)
- **Use cases**:
  - Historical record of collected news
  - Data analysis and trend tracking
  - Backup in case email delivery fails
  - Can be imported into other applications

#### **`.env`** - Environment Variables (Not in repo)

- **Purpose**: Stores sensitive configuration (email credentials)
- **Required variables**:
  - `EMAIL_SENDER` - Your Gmail address
  - `EMAIL_PASSWORD` - Gmail App Password (not regular password)
  - `EMAIL_RECIPIENTS` - Comma-separated list of recipient emails
  - `SMTP_SERVER` - SMTP server address (default: smtp.gmail.com)
  - `SMTP_PORT` - SMTP port (default: 587)
- **Security**: This file is never committed to Git (listed in `.gitignore`)

#### **`scraper.log`** - Execution Log (Generated at runtime)

- **Purpose**: Records all scheduler activities and errors
- **Contents**: Timestamps, success/failure messages, error details
- **Use cases**: Debugging, monitoring system health, tracking execution history

---

## 🔄 How Everything Works Together

### Workflow Diagram:

```
 ┌─────────────┐
│ scheduler.py│  (Optional: Runs daily at specified time)
└──────┬──────┘
       │ Triggers
       ▼
┌─────────────┐
│   main.py   │  (Entry point)
└──────┬──────┘
       │ Initializes
       ▼
┌──────────────────┐
│  aggregator.py   │  (Coordinates scraping)
└────────┬─────────┘
         │ Calls
         ▼
┌────────────────────────────────┐
│       scrapers/ modules        │
│  ┌──────────┬──────────────┐   │
│  │channels  │ techcrunch   │   │
│  │  .py     │    .py       │   │
│  └────┬─────┴──────┬───────┘   │
│       │            │           │
│       │  hackernews.py         │
│       │      │                 │
└───────┼──────┼─────────────────┘
        │      │
        │ Returns articles
        ▼
┌──────────────────┐
│  aggregator.py   │  (Formats digests)
└────────┬─────────┘
         │
         ├─── Saves ──→ daily_news.json
         │
         └─── Sends ──→ email_service.py
                              │
                              ▼ Uses config from
                         ┌──────────┐
                         │ config.py│
                         └──────────┘
                              │ Loads
                              ▼
                          .env file
```

### Execution Flow:

1. **Initialization**:

   - `scheduler.py` (optional) triggers `main.py` at scheduled time
   - OR run `main.py` directly for manual execution
2. **Configuration Loading**:

   - `config.py` loads credentials and settings from `.env` file
   - Validates that required variables are present
3. **Scraping Phase**:

   - `main.py` initializes all scraper classes
   - `aggregator.py` calls each scraper's `scrape()` method
   - Each scraper independently fetches and parses its news source
   - Articles are collected and organized by source
4. **Formatting Phase**:

   - `aggregator.py` generates HTML digest (styled email format)
   - `aggregator.py` generates plain text digest (fallback format)
   - Both digests include all collected articles organized by source
5. **Output Phase**:

   - Articles saved to `daily_news.json` for archival
   - `email_service.py` sends HTML digest via SMTP
   - Success/failure messages logged to console and `scraper.log`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Gmail account with App Password enabled
- Internet connection

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Shang-chi038/News-Scrapper.git
cd News-Scrapper
```

2. Install dependencies:

These are the required dependencies:

- **requests** - a HTTP library for fetching web pages
- **beautifulsoup4** - for HTML parsing and scraping
- **lxml** - a fast XML/HTML parser
- **python-dotenv** - an environment variable management
- **schedule** - a task scheduling library

Install all at once:

```bash
pip install requests beautifulsoup4 lxml python-dotenv schedule
```

Or through the requirements.txt file:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

Create a `.env` file in the project root:

```
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_RECIPIENTS=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Important**: Use a Gmail App Password, not your regular password. It is a unique 16 digit passcode that gives a less secure app or device permission to access your Google Account. [Learn how to create one](https://support.google.com/accounts/answer/185833).
<!-- [To create and manage one](https://myaccount.google.com/apppasswords) -->

### Usage

#### Manual Execution:

```bash
python main.py
```

#### Scheduled Execution:

Run daily at 8:00 AM:

```bash
python scheduler.py
```

Run at custom time (e.g., 2:30 PM):

```bash
python scheduler.py "14:30"
```

The scheduler will keep running and execute the scraper daily at the specified time.

---


## 🔒 Security Notes

- Never commit your `.env` file (it's in `.gitignore`)
- Use Gmail App Passwords, not your main password
- Keep your `EMAIL_PASSWORD` secure and never share it
- The `.env` file should only be readable by you

---

## 🛠️ Customization

### Adding More News Sources:

1. Create a new scraper in `scrapers/new_source.py`
2. Implement the `scrape()` and `get_source_name()` methods
3. Add your scraper to `main.py`:

```python
from scrapers.new_source import NewSourceScraper
scrapers = [
    ChannelsNewsScraper(),
    TechCrunchScraper(),
    HackerNewsScraper(),
    NewSourceScraper()  # Add here
]
```

### Changing Schedule Time:

Edit the default time in `scheduler.py` or pass it as an argument:

```bash
python scheduler.py "06:00"  # Run at 6:00 AM
```

### Modifying Email Format:

Edit the `generate_html_digest()` method in `aggregator.py` to customize the email styling and layout.

---

## 📊 Output Example

### Email Digest Format:

- **Subject**: Daily News Digest - January 09, 2026
- **Format**: Beautifully styled HTML email
- **Sections**: One section per news source
- **Content**: Article title, summary, and clickable link

### JSON Output Format:

```json
{
  "Channels TV Nigeria": [
    {
      "title": "Article Title",
      "link": "https://...",
      "excerpt": "Article preview...",
      "source": "Channels TV Nigeria"
    }
  ],
  "TechCrunch": [...],
  "Hacker News": [...]
}
```

---

## 🐛 Troubleshooting

### Email not sending:

- Verify your Gmail App Password is correct
- Check that 2-Factor Authentication is enabled on your Google account
- Ensure `.env` file has no quotes around values

### Scraper returning 0 articles:

- Check your internet connection
- The website might be temporarily down
- Website structure may have changed (scrapers may need updating)

### Scheduler not running:

- Keep the terminal window open or run as a background service
- Check that the scheduled time is in 24-hour format (HH:MM)

---

## 📝 License

This project is open source and available for personal and educational use, but I must be acknowledged.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new news sources
- Improve scraping reliability
- Enhance email formatting
- Add new features

---

## 👤 Author

**Shang-chi038**

- GitHub: [@Shang-chi038](https://github.com/Shang-chi038)

---

## ⭐ Acknowledgments

- Built with Python and love for automation
- Uses public APIs and RSS feeds where available
- Respects robots.txt and website terms of service


## 📖 Index
- Excerpt - this means a short preview/summary of the article that was scrapped from Channels news.