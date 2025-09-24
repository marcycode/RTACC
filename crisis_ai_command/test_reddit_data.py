# Test reddit connection
import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='CrisisAI:v1.0 (by /u/YourUsername)'
)

print(f"✅ Reddit connected: {reddit.read_only}")