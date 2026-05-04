import schedule
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

def run_scraper():
    """Run the news scraper job"""
    try:
        logging.info("Starting scheduled news scraping job...")
        from main import main
        main()
        logging.info("Scheduled job completed successfully")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def start_scheduler(run_time: str = "08:00"):
    """
    Start the scheduler to run daily at specified time
    
    Args:
        run_time: Time to run in 24-hour format (HH:MM), default is 08:00 AM
    """
    logging.info(f"Scheduler started. Will run daily at {run_time}")
    logging.info(f"Next run scheduled for: {run_time}")
    
    # Schedule the job
    schedule.every().day.at(run_time).do(run_scraper)
    
    # Optional: Run immediately on startup
    run_scraper()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")

if __name__ == "__main__":
    import sys
    
    # Allow custom time from command line argument
    if len(sys.argv) > 1:
        custom_time = sys.argv[1]
        start_scheduler(custom_time)
    else:
        # Default: run at 8:00 AM daily
        start_scheduler("08:00")

