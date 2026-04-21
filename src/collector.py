import os
import requests
from dotenv import load_dotenv
from supabase import create_client
from src.schemas import FinanceSignal
from src.preflight import run_preflight_checks

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
    print(f"--- 🛰️ Fetching {ticker} Signals ---")
    supabase, av_key = _get_runtime_config()
    
    # 1. Get Raw Data
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={av_key}"
    response = requests.get(url)
    feed = response.json().get("feed", [])[:5] # Fetch top 5 for the test

    for item in feed:
        try:
            # 2. Validate using our Pydantic 'Contract'
            # We map Alpha Vantage fields to our schema fields
            signal = FinanceSignal(
                ticker=ticker,
                headline=item['title'],
                url=item['url'],
                published_at=item['time_published'] 
            )

            # 3. Push to Supabase
            # .dict() converts the Pydantic object back to a format SQL understands
            # mode="json" is the "magic" that converts HttpUrl to a string 
            # and Datetime to an ISO string that Supabase understands.
            supabase.table("financial_signals").insert(signal.model_dump(mode="json")).execute()
            print(f"✅ Saved: {signal.headline[:50]}...")

        except Exception as e:
            # This handles both Validation errors and Database 'Unique' constraint errors
            print(f"⚠️ Skipped article: {e}")

if __name__ == "__main__":
    run_preflight_checks()
    ingest_news()