import argparse
import logging
from typing import List, Optional
from config import (
    OPENAI_API_KEY, DEFAULT_STOCKS, ANALYSIS_CONFIG,
    AGENT_CONFIG, DATA_CONFIG
)
from data_fetcher import StockDataFetcher
from stock_analyzer import StockAnalyzer
from recommendation_engine import RecommendationEngine
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockAIAgent:
    """Main AI agent for stock analysis and recommendations"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher(cache_enabled=True)
        self.analyzer = StockAnalyzer(ANALYSIS_CONFIG)
        self.recommendation_engine = RecommendationEngine(
            api_key=OPENAI_API_KEY,
            model=AGENT_CONFIG.get("model", "gpt-4"),
            temperature=AGENT_CONFIG.get("temperature", 0.3)
        )
    
    def analyze_stock(self, symbol: str) -> dict:
        """Analyze a single stock"""
        logger.info(f"Analyzing {symbol}...")
        
        # Fetch data
        df = self.data_fetcher.fetch_stock_data(
            symbol,
            period="1y",
            interval=DATA_CONFIG.get("interval", "1d")
        )
        
        if df.empty:
            return {"symbol": symbol, "error": "Could not fetch data"}
        
        # Analyze
        analysis = self.analyzer.analyze_stock(symbol, df)
        
        # Generate recommendation
        recommendation = self.recommendation_engine.generate_recommendation(analysis)
        
        result = {**analysis, **recommendation}
        return result
    
    def analyze_multiple_stocks(self, symbols: List[str]) -> List[dict]:
        """Analyze multiple stocks"""
        results = []
        for symbol in symbols:
            result = self.analyze_stock(symbol)
            results.append(result)
        return results
    
    def print_recommendation(self, result: dict):
        """Pretty print recommendation"""
        print("\n" + "="*60)
        print(f"Stock: {result.get('symbol', 'N/A')}")
        print(f"Current Price: ${result.get('current_price', 'N/A'):.2f}")
        print(f"Trend: {result.get('trend', 'N/A')}")
        print(f"Volatility: {result.get('volatility', 0)*100:.2f}%")
        print("-"*60)
        print(f"Recommendation: {result.get('recommendation', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Risk Level: {result.get('risk_level', 'N/A')}")
        print(f"Reasoning: {result.get('reasoning', 'N/A')}")
        
        if result.get('target_price'):
            print(f"Target Price: {result.get('target_price')}")
        
        if result.get('key_factors'):
            print(f"Key Factors: {', '.join(result.get('key_factors', []))}")
        
        print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Stock AI Agent - Analyze stocks and get recommendations")
    parser.add_argument(
        "--stocks",
        nargs="+",
        default=DEFAULT_STOCKS,
        help="Stock symbols to analyze"
    )
    parser.add_argument(
        "--output",
        choices=["json", "pretty"],
        default="pretty",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    # Validate API key
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set. Please configure it in .env file")
        return
    
    # Initialize agent
    agent = StockAIAgent()
    
    # Analyze stocks
    logger.info(f"Starting analysis of {', '.join(args.stocks)}")
    results = agent.analyze_multiple_stocks(args.stocks)
    
    # Output results
    if args.output == "json":
        print(json.dumps(results, indent=2, default=str))
    else:
        for result in results:
            agent.print_recommendation(result)
    
    logger.info("Analysis complete")

if __name__ == "__main__":
    main()