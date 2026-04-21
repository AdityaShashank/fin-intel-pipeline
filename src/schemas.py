from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional

class FinanceSignal(BaseModel):  # Make sure this name matches what you use in collector.py
    ticker: str
    headline: str
    url: HttpUrl
    published_at: datetime
    
    # ⬇️ ADD THESE TWO LINES ⬇️
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None 

    @field_validator("published_at", mode="before")
    @classmethod
    def parse_alpha_vantage_time(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y%m%dT%H%M%S")
        return value