import os
from dotenv import load_dotenv

load_dotenv()

print("EMAIL_SENDER:", os.getenv('EMAIL_SENDER'))
print("EMAIL_PASSWORD:", os.getenv('EMAIL_PASSWORD')[:4] + "****")  # Only show first 4 chars
print("EMAIL_RECIPIENTS:", os.getenv('EMAIL_RECIPIENTS'))
