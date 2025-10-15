"""
Scanner Agent - Hunts for trading opportunities across all pairs
Ultra-fast market scanning for shark0locker
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ScannerAgent(BaseAgent):
    """Scans markets for high-probability trading opportunities"""
    
    def __init__(self, name: str, config: Dict[str, Any], api_client, message_queue):
        super().__init__(name, config)
        self.api_client = api_client
        self.message_queue = message_queue
        self.scan_interval = config.get("scan_interval_seconds", 0.1)
        self.symbols = config.get("preferred_pairs", [])
        self.last_prices = {}
        
    async def run(self):
        """Main scanning loop"""
        logger.info(f"{self.name} scanning {len(self.symbols)} pairs")
        
        while self.is_running:
            try:
                # Get all tickers at once for speed
                tickers = await self.api_client.get_all_tickers(self.symbols)
                
                # Analyze each ticker for opportunities
                opportunities = []
                for symbol, ticker in tickers.items():
                    opportunity = await self.analyze_ticker(symbol, ticker)
                    if opportunity:
                        opportunities.append(opportunity)
                
                # Send opportunities to analyzer agents
                if opportunities:
                    await self.message_queue.put({
                        "type": "opportunities",
                        "data": opportunities,
                        "source": self.name,
                        "timestamp": datetime.now()
                    })
                    logger.debug(f"{self.name} found {len(opportunities)} opportunities")
                
                self.update_stats(success=True)
                await asyncio.sleep(self.scan_interval)
                
            except Exception as e:
                logger.error(f"{self.name} error: {e}")
                self.update_stats(success=False)
                await asyncio.sleep(1)
                
    async def analyze_ticker(self, symbol: str, ticker: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Quick analysis to detect potential opportunities"""
        try:
            if not ticker or "bid" not in ticker or "ask" not in ticker:
                return None
                
            bid = float(ticker["bid"])
            ask = float(ticker["ask"])
            mid = (bid + ask) / 2
            spread = ask - bid
            
            # Calculate velocity (price change rate)
            velocity = 0.0
            if symbol in self.last_prices:
                last_price = self.last_prices[symbol]["price"]
                last_time = self.last_prices[symbol]["time"]
                time_diff = (datetime.now() - last_time).total_seconds()
                if time_diff > 0:
                    velocity = (mid - last_price) / time_diff
            
            # Update last price
            self.last_prices[symbol] = {
                "price": mid,
                "time": datetime.now()
            }
            
            # Detect strong momentum (potential opportunity)
            abs_velocity = abs(velocity)
            if abs_velocity > 0.001:  # Significant movement
                direction = "buy" if velocity > 0 else "sell"
                
                # Calculate opportunity score
                score = abs_velocity * 1000  # Scale to readable number
                
                return {
                    "symbol": symbol,
                    "direction": direction,
                    "bid": bid,
                    "ask": ask,
                    "mid": mid,
                    "spread": spread,
                    "velocity": velocity,
                    "score": score,
                    "timestamp": datetime.now()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return None
