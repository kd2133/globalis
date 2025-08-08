import praw
import pandas as pd
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from globalis_pipeline import GlobalisPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_reddit_posts(subreddit, count=10):
    try:
        load_dotenv()
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        posts = reddit.subreddit(subreddit).hot(limit=count)
        data = [
            {
                "text": post.title,
                "created_at": datetime.fromtimestamp(post.created_utc),
                "lang": "en",
                "score": post.score
            }
            for post in posts if post.score >= 100  # Pre-Pipeline-Threshold
        ]
        logger.info(f"{len(data)} Posts von r/{subreddit} abgerufen (nach Filter: score >= 100).")
        return data
    except Exception as e:
        logger.error(f"Fehler beim Abrufen von Reddit-Posts: {e}")
        return []

def process_reddit_posts():
    queries = [
        {"subreddit": "healthcare", "topic": "Healthcare", "country": "US", "lang": "en"},
        {"subreddit": "economy", "topic": "Inflation", "country": "DE", "lang": "en"},
        {"subreddit": "worldnews", "topic": "Freedom", "country": "UK", "lang": "en"}
    ]
    all_posts = []
    for q in queries:
        logger.info(f"Verarbeite Subreddit: r/{q['subreddit']} (Land: {q['country']}, Sprache: {q['lang']})")
        posts = fetch_reddit_posts(q["subreddit"], count=10)
        for post in posts:
            post["country"] = q["country"]
            all_posts.append(post["text"])  # Nur Text für Pipeline

    # Führe Pipeline aus
    pipeline = GlobalisPipeline()
    df, gsi_weighted, total_analyzed_posts = pipeline.run(all_posts)

    # Füge Länderinformationen hinzu
    if not df.empty:
        post_countries = {post["text"]: post["country"] for post in all_posts}
        df["country"] = df["text"].map(post_countries)
        df.to_csv("data/gsi_data.csv", index=False)
        logger.info(f"Daten in data/gsi_data.csv gespeichert! GSI: {gsi_weighted}, Posts: {total_analyzed_posts}")
    else:
        logger.warning("Keine Daten nach Pipeline-Verarbeitung.")
    
    return df, gsi_weighted

if __name__ == "__main__":
    process_reddit_posts()