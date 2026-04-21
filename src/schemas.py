# Its about defining the data models for the application using Pydantic. These models will be used for data validation and serialization when interacting with the database and external APIs.
'''We keep this because "Dirty Data" is the #1 killer of MVP projects. 
If you save a headline without a URL today,
 your deduplication will break tomorrow. 
 Defining the structure first takes 2 minutes but saves 2 hours of debugging.'''
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional

class FinanceSignal(BaseModel):
    ticker: str
    headline: str
    url: HttpUrl
    published_at: datetime
    sentiment_score: Optional[float] = None  # This will be filled in later by the sentiment analysis step

    @field_validator("published_at", mode="before")
    @classmethod
    def parse_alpha_vantage_time(cls, value):
        """Converts '20260420T231301' to a real datetime object."""
        if isinstance(value, str):
            # Alpha Vantage format: YYYYMMDDTHHMMSS
            return datetime.strptime(value, "%Y%m%dT%H%M%S")
        return value