import os
import requests
from dotenv import load_dotenv
from supabase import create_client
from src.schemas import FinanceSignal
from src.preflight import run_preflight_checks
from src.brain import SentimentBrain

load_dotenv()  # Loads .env keys

def _get_runtime_config():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    av_key = os.getenv("ALPHA_VANTAGE_KEY")

    if not supabase_url or not supabase_key or not av_key:
        raise ValueError(
            "Missing required environment variables: SUPABASE_URL, SUPABASE_KEY, ALPHA_VANTAGE_KEY"
        )

    return create_client(supabase_url, supabase_key), av_key

def ingest_news(ticker="NVDA"):
    #initializing the Brain
    brain= SentimentBrain()
    print(f"--- 🛰️ Fetching {ticker} Signals ---")
    supabase, av_key = _get_runtime_config()
    
    # 1. Get Raw Data
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={av_key}"
    response = requests.get(url)
    feed = response.json().get("feed", [])[:5] # Fetch top 5 for the test

    for item in feed:
        try:
            # 3. ASK THE BRAIN (The "Intelligence" Step)
            analysis = brain.get_sentiment(item['title'])
            
            # 4. Map to Schema
            signal = FinanceSignal(
                ticker=ticker,
                headline=item['title'],
                url=item['url'],
                published_at=item['time_published'],
                sentiment_score=analysis['score'], # <--- AI Score
                sentiment_label=analysis['label']   # <--- AI Label
            )

            # 5. Push to Supabase
            supabase.table("financial_signals").upsert(
                signal.model_dump(mode="json"), 
                on_conflict="url"
            ).execute()
            
            print(f"✅ {signal.sentiment_label}: {signal.headline[:50]}...")

        except Exception as e:
            print(f"⚠️ Skipped: {e}")

if __name__ == "__main__":
    run_preflight_checks()
    ingest_news()