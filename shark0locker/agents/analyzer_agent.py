"""
Analyzer Agent - Deep technical analysis for high-probability trades
AI-powered analysis for shark0locker
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class AnalyzerAgent(BaseAgent):
    """Performs deep technical analysis on opportunities"""
    
    def __init__(self, name: str, config: Dict[str, Any], api_client, message_queue, signal_queue):
        super().__init__(name, config)
        self.api_client = api_client
        self.message_queue = message_queue
        self.signal_queue = signal_queue
        self.min_win_probability = config.get("min_win_probability", 0.98)
        self.analysis_cache = {}
        
    async def run(self):
        """Main analysis loop"""
        logger.info(f"{self.name} ready for analysis")
        
        while self.is_running:
            try:
                # Wait for opportunities from scanners
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )
                
                if message["type"] == "opportunities":
                    opportunities = message["data"]
                    
                    # Analyze each opportunity
                    for opp in opportunities:
                        signal = await self.analyze_opportunity(opp)
                        if signal and signal["win_probability"] >= self.min_win_probability:
                            # Send high-probability signal to executors
                            await self.signal_queue.put(signal)
                            logger.info(
                                f"{self.name} generated signal: {signal['symbol']} "
                                f"{signal['direction']} - Win rate: {signal['win_probability']:.2%}"
                            )
                    
                    self.update_stats(success=True)
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"{self.name} error: {e}")
                self.update_stats(success=False)
                
    async def analyze_opportunity(self, opp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Perform deep analysis on an opportunity"""
        try:
            symbol = opp["symbol"]
            
            # Multi-factor analysis
            factors = {
                "momentum": self._analyze_momentum(opp),
                "volatility": self._analyze_volatility(opp),
                "spread": self._analyze_spread(opp),
                "velocity": self._analyze_velocity(opp),
                "pattern": self._analyze_pattern(opp)
            }
            
            # Calculate composite win probability
            win_probability = self._calculate_win_probability(factors)
            
            # Calculate optimal entry and exit
            entry_price, stop_loss, take_profit = self._calculate_levels(opp, factors)
            
            if win_probability >= self.min_win_probability:
                return {
                    "symbol": symbol,
                    "direction": opp["direction"],
                    "entry_price": entry_price,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "win_probability": win_probability,
                    "factors": factors,
                    "urgency": "high" if opp["score"] > 5 else "normal",
                    "timestamp": datetime.now()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Analysis error for {opp.get('symbol')}: {e}")
            return None
            
    def _analyze_momentum(self, opp: Dict[str, Any]) -> float:
        """Analyze momentum strength (0-1)"""
        velocity = abs(opp.get("velocity", 0))
        # Strong velocity indicates strong momentum
        momentum_score = min(velocity * 500, 1.0)
        return momentum_score
        
    def _analyze_volatility(self, opp: Dict[str, Any]) -> float:
        """Analyze volatility favorability (0-1)"""
        spread = opp.get("spread", 0)
        mid = opp.get("mid", 1)
        spread_pct = (spread / mid) * 100 if mid > 0 else 1
        
        # Lower spread is better for scalping
        volatility_score = max(0, 1 - (spread_pct / 0.1))
        return volatility_score
        
    def _analyze_spread(self, opp: Dict[str, Any]) -> float:
        """Analyze spread quality (0-1)"""
        spread = opp.get("spread", 0)
        # Tighter spread = higher score
        if spread < 0.00001:
            return 1.0
        elif spread < 0.0001:
            return 0.8
        elif spread < 0.001:
            return 0.6
        else:
            return 0.4
            
    def _analyze_velocity(self, opp: Dict[str, Any]) -> float:
        """Analyze price velocity (0-1)"""
        velocity = abs(opp.get("velocity", 0))
        # Higher velocity = higher score (but cap it)
        velocity_score = min(velocity * 300, 1.0)
        return velocity_score
        
    def _analyze_pattern(self, opp: Dict[str, Any]) -> float:
        """Analyze price pattern (0-1)"""
        # Simple pattern recognition based on score
        score = opp.get("score", 0)
        pattern_score = min(score / 10, 1.0)
        return pattern_score
        
    def _calculate_win_probability(self, factors: Dict[str, float]) -> float:
        """Calculate composite win probability from factors"""
        # Weighted average of factors
        weights = {
            "momentum": 0.25,
            "volatility": 0.20,
            "spread": 0.15,
            "velocity": 0.25,
            "pattern": 0.15
        }
        
        win_prob = sum(factors[k] * weights[k] for k in weights)
        
        # Boost win probability (aggressive shark mode)
        win_prob = min(win_prob * 1.1, 0.99)
        
        return win_prob
        
    def _calculate_levels(self, opp: Dict[str, Any], factors: Dict[str, float]) -> tuple:
        """Calculate entry, stop loss, and take profit levels"""
        direction = opp["direction"]
        mid = opp["mid"]
        spread = opp["spread"]
        
        if direction == "buy":
            entry_price = opp["ask"]
            # Tight stop loss for quick exit if wrong
            stop_loss = entry_price - (spread * 5)
            # Aggressive take profit for scalping
            take_profit = entry_price + (spread * 10)
        else:  # sell
            entry_price = opp["bid"]
            stop_loss = entry_price + (spread * 5)
            take_profit = entry_price - (spread * 10)
        
        return entry_price, stop_loss, take_profit
