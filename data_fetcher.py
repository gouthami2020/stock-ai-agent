import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StockDataFetcher:
    """Fetches real-time and historical stock data"""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache = {} if cache_enabled else None
        self.cache_timestamp = {}
    
    def fetch_stock_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch stock data for a given symbol
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Check cache
            cache_key = f"{symbol}_{period}_{interval}"
            if self.cache is not None and cache_key in self.cache:
                if datetime.now() - self.cache_timestamp.get(cache_key, datetime.now()) < timedelta(hours=1):
                    logger.info(f"Using cached data for {symbol}")
                    return self.cache[cache_key]
            
            logger.info(f"Fetching data for {symbol}...")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            # Cache the data
            if self.cache is not None:
                self.cache[cache_key] = df
                self.cache_timestamp[cache_key] = datetime.now()
            
            return df
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def fetch_multiple_stocks(
        self,
        symbols: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks
        
        Args:
            symbols: List of stock ticker symbols
            period: Time period
            interval: Data interval
        
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_stock_data(symbol, period, interval)
        return data
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info.get("currentPrice")
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {str(e)}")
            return None
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get detailed stock information"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return {}