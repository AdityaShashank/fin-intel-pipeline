
import pytest
from src.schemas import FinanceSignal  # Your Pydantic model
from src.brain import SentimentBrain

# Test 1: Validate the Data Contract
def test_pydantic_schema():
    raw_data = {
        "ticker": "NVDA",
        "headline": "NVIDIA beats earnings",
        "url": "https://example.com",
        # Change this to match your %Y%m%dT%H%M%S validator
        "published_at": "20260426T120000" 
    }
    signal = FinanceSignal(**raw_data)
    assert signal.ticker == "NVDA"

# Test 2: Validate the Brain
def test_finbert_output():
    text = "Stocks are soaring today!"
    brain = SentimentBrain()
    result = brain.get_sentiment(text)
    assert -1 <= result["score"] <= 1
    assert result["label"] in ["Bullish", "Bearish", "Neutral"]

# Test 3: API Safety (MOCKING)
def test_env_variables_exist():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    assert os.getenv("SUPABASE_URL") is not None