import os
import requests
from dotenv import load_dotenv
from supabase import create_client
from src.schemas import FinanceSignal
from src.preflight import run_preflight_checks
from src.brain import SentimentBrain

load_dotenv()

def _get_runtime_config():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    av_key = os.getenv("ALPHA_VANTAGE_KEY")
    if not supabase_url or not supabase_key or not av_key:
        raise ValueError("Missing environment variables: SUPABASE_URL, SUPABASE_KEY, ALPHA_VANTAGE_KEY")
    return create_client(supabase_url, supabase_key), av_key

def ingest_news(ticker, brain, supabase, av_key):
    print(f"--- 🛰️ Fetching {ticker} Signals ---")
    
    # 1. API Request
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={av_key}"
    response = requests.get(url)
    data = response.json()
    feed = data.get("feed", [])[:5] # Top 5 stories to stay efficient

    for item in feed:
        try:
            # 2. AI Scoring
            analysis = brain.get_sentiment(item['title'])
            
            # 3. Schema Mapping
            signal = FinanceSignal(
                ticker=ticker,
                headline=item['title'],
                url=item['url'],
                published_at=item['time_published'],
                sentiment_score=analysis['score'],
                sentiment_label=analysis['label']
            )

            # 4. Database Upsert (Prevents duplicates via URL)
            supabase.table("financial_signals").upsert(
                signal.model_dump(mode="json"), 
                on_conflict="url"
            ).execute()
            
            print(f"✅ {signal.sentiment_label}: {signal.headline[:50]}...")

        except Exception as e:
            print(f"⚠️ Skipped item: {e}")

if __name__ == "__main__":
    run_preflight_checks()
    
    # Configuration for the American Stock Exchange leaders
    WATCHLIST = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"]
    supabase_client, api_key = _get_runtime_config()
    brain_instance = SentimentBrain() # Loaded once to save resources

    for ticker in WATCHLIST:
        ingest_news(ticker, brain_instance, supabase_client, api_key)