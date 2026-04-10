import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"

# Stock Analysis Configuration
ANALYSIS_CONFIG = {
    "lookback_days": 252,  # 1 year of trading days
    "short_term_days": 20,
    "medium_term_days": 50,
    "long_term_days": 200,
    "rsi_threshold": (30, 70),  # Oversold, Overbought
    "volatility_threshold": 0.02,
    "volume_threshold": 1.2,  # 20% above average
}

# Recommendation Thresholds
RECOMMENDATION_CONFIG = {
    "strong_buy_score": 0.8,
    "buy_score": 0.6,
    "hold_score": 0.4,
    "sell_score": 0.2,
    "strong_sell_score": 0.0,
}

# Default stocks to analyze
DEFAULT_STOCKS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

# Data Configuration
DATA_CONFIG = {
    "interval": "1d",  # Daily data
    "auto_adjust": True,
    "cache_period": 3600,  # Cache for 1 hour
}

# Agent Configuration
AGENT_CONFIG = {
    "temperature": 0.3,  # Lower temperature for more consistent recommendations
    "max_tokens": 2000,
    "timeout": 30,
}