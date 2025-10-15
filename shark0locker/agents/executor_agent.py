"""
Executor Agent - Ultra-fast order execution
Executes trades with maximum speed and precision for shark0locker
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ExecutorAgent(BaseAgent):
    """Executes trading signals with maximum speed"""
    
    def __init__(self, name: str, config: Dict[str, Any], api_client, signal_queue, trade_log):
        super().__init__(name, config)
        self.api_client = api_client
        self.signal_queue = signal_queue
        self.trade_log = trade_log
        self.max_position_size_percent = config.get("max_position_size_percent", 100.0)
        self.leverage = config.get("leverage", 500)
        self.active_positions = {}
        
    async def run(self):
        """Main execution loop"""
        logger.info(f"{self.name} ready to execute")
        
        while self.is_running:
            try:
                # Wait for trading signals
                signal = await asyncio.wait_for(
                    self.signal_queue.get(),
                    timeout=1.0
                )
                
                # Execute the trade immediately
                result = await self.execute_signal(signal)
                
                if result and "error" not in result:
                    self.update_stats(success=True)
                    logger.info(f"{self.name} executed: {signal['symbol']} {signal['direction']}")
                else:
                    self.update_stats(success=False)
                    logger.error(f"{self.name} execution failed: {result.get('error', 'Unknown error')}")
                    
            except asyncio.TimeoutError:
                # Check and manage existing positions
                await self.manage_positions()
                continue
            except Exception as e:
                logger.error(f"{self.name} error: {e}")
                self.update_stats(success=False)
                
    async def execute_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a trading signal"""
        try:
            symbol = signal["symbol"]
            direction = signal["direction"]
            
            # Calculate position size (full port trading)
            position_size = await self.calculate_position_size(signal)
            
            if position_size <= 0:
                return {"error": "Invalid position size"}
            
            # Place market order for instant execution
            order = await self.api_client.place_market_order(
                symbol=symbol,
                side=direction,
                volume=position_size,
                stop_loss=signal.get("stop_loss"),
                take_profit=signal.get("take_profit")
            )
            
            if "error" not in order:
                # Log the trade
                trade_record = {
                    "order_id": order.get("orderId"),
                    "symbol": symbol,
                    "direction": direction,
                    "entry_price": signal["entry_price"],
                    "volume": position_size,
                    "stop_loss": signal.get("stop_loss"),
                    "take_profit": signal.get("take_profit"),
                    "win_probability": signal.get("win_probability"),
                    "entry_time": datetime.now(),
                    "executor": self.name
                }
                
                self.trade_log.append(trade_record)
                self.active_positions[order.get("orderId")] = trade_record
            
            return order
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {"error": str(e)}
            
    async def calculate_position_size(self, signal: Dict[str, Any]) -> float:
        """Calculate optimal position size for full port trading"""
        try:
            # Get current account balance
            balance = await self.api_client.get_balance()
            
            if balance <= 0:
                return 0
            
            # Calculate position size based on leverage and risk
            symbol = signal["symbol"]
            entry_price = signal["entry_price"]
            
            # Full port with leverage
            available_margin = balance * (self.max_position_size_percent / 100)
            position_value = available_margin * self.leverage
            
            # Convert to lots/volume based on symbol
            # For forex: standard lot = 100,000 units
            # Simplified calculation - adjust based on symbol type
            if "JPY" in symbol:
                position_size = position_value / (entry_price * 100000)
            elif "XAU" in symbol or "GOLD" in symbol:
                position_size = position_value / (entry_price * 100)
            elif "BTC" in symbol or "ETH" in symbol:
                position_size = position_value / entry_price
            else:
                position_size = position_value / (entry_price * 100000)
            
            # Round to 2 decimal places
            position_size = round(position_size, 2)
            
            logger.debug(f"Position size for {symbol}: {position_size} lots (Balance: ${balance})")
            return position_size
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.01  # Minimum fallback
            
    async def manage_positions(self):
        """Monitor and manage active positions"""
        try:
            # Get current open positions from broker
            open_positions = await self.api_client.get_open_positions()
            
            for position in open_positions:
                position_id = position.get("id")
                symbol = position.get("symbol")
                pnl = float(position.get("profit", 0))
                
                # Check if we should close based on profit/loss
                if position_id in self.active_positions:
                    trade_record = self.active_positions[position_id]
                    
                    # Quick profit taking for scalping
                    if pnl > 0:
                        logger.info(f"Closing profitable position {symbol}: +${pnl:.2f}")
                        await self.api_client.close_position(position_id)
                        
                        # Update trade record
                        trade_record["exit_time"] = datetime.now()
                        trade_record["pnl"] = pnl
                        trade_record["status"] = "closed_profit"
                        
                        del self.active_positions[position_id]
                        
        except Exception as e:
            logger.error(f"Error managing positions: {e}")
