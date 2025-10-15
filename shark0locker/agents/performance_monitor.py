"""
Performance Monitor Agent - Tracks trading performance and PNL
Real-time performance monitoring for shark0locker
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class PerformanceMonitor(BaseAgent):
    """Monitors trading performance and generates reports"""
    
    def __init__(self, name: str, config: Dict[str, Any], api_client, trade_log):
        super().__init__(name, config)
        self.api_client = api_client
        self.trade_log = trade_log
        self.initial_balance = 0
        self.balance_history = deque(maxlen=1000)
        self.performance_snapshots = []
        self.hourly_targets = config.get("hourly_target_percent", 100.0)
        
    async def run(self):
        """Main monitoring loop"""
        logger.info(f"{self.name} monitoring performance")
        
        # Get initial balance
        self.initial_balance = await self.api_client.get_balance()
        logger.info(f"Initial balance: ${self.initial_balance:.2f}")
        
        while self.is_running:
            try:
                # Update performance metrics
                await self.update_metrics()
                
                # Generate performance report
                report = await self.generate_report()
                
                # Log key metrics
                logger.info(
                    f"Performance: Balance: ${report['current_balance']:.2f} | "
                    f"PNL: ${report['total_pnl']:.2f} ({report['roi_percent']:.2f}%) | "
                    f"Trades: {report['total_trades']} | "
                    f"Win Rate: {report['win_rate']:.2f}%"
                )
                
                self.update_stats(success=True)
                
                # Update every 5 seconds
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"{self.name} error: {e}")
                self.update_stats(success=False)
                await asyncio.sleep(5)
                
    async def update_metrics(self):
        """Update performance metrics"""
        try:
            current_balance = await self.api_client.get_balance()
            current_equity = await self.api_client.get_equity()
            
            self.balance_history.append({
                "timestamp": datetime.now(),
                "balance": current_balance,
                "equity": current_equity
            })
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            
    async def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            current_balance = await self.api_client.get_balance()
            current_equity = await self.api_client.get_equity()
            
            # Calculate PNL
            total_pnl = current_balance - self.initial_balance
            roi_percent = (total_pnl / self.initial_balance * 100) if self.initial_balance > 0 else 0
            
            # Analyze trades
            total_trades = len(self.trade_log)
            closed_trades = [t for t in self.trade_log if t.get("status") == "closed_profit"]
            winning_trades = [t for t in closed_trades if t.get("pnl", 0) > 0]
            losing_trades = [t for t in closed_trades if t.get("pnl", 0) <= 0]
            
            win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
            
            # Calculate average profit/loss
            avg_profit = sum(t.get("pnl", 0) for t in winning_trades) / len(winning_trades) if winning_trades else 0
            avg_loss = sum(t.get("pnl", 0) for t in losing_trades) / len(losing_trades) if losing_trades else 0
            
            # Calculate hourly performance
            hourly_pnl = self._calculate_hourly_pnl()
            hourly_roi = (hourly_pnl / self.initial_balance * 100) if self.initial_balance > 0 else 0
            
            # Drawdown calculation
            max_balance = max([h["balance"] for h in self.balance_history], default=current_balance)
            current_drawdown = ((max_balance - current_balance) / max_balance * 100) if max_balance > 0 else 0
            
            report = {
                "current_balance": current_balance,
                "current_equity": current_equity,
                "initial_balance": self.initial_balance,
                "total_pnl": total_pnl,
                "roi_percent": roi_percent,
                "total_trades": total_trades,
                "closed_trades": len(closed_trades),
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": win_rate,
                "avg_profit": avg_profit,
                "avg_loss": avg_loss,
                "hourly_pnl": hourly_pnl,
                "hourly_roi": hourly_roi,
                "current_drawdown": current_drawdown,
                "timestamp": datetime.now()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {}
            
    def _calculate_hourly_pnl(self) -> float:
        """Calculate PNL for the last hour"""
        try:
            if not self.balance_history:
                return 0
                
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            # Find balance from 1 hour ago
            hour_ago_balance = None
            for snapshot in self.balance_history:
                if snapshot["timestamp"] >= one_hour_ago:
                    hour_ago_balance = snapshot["balance"]
                    break
            
            if hour_ago_balance is None:
                hour_ago_balance = self.balance_history[0]["balance"]
            
            current_balance = self.balance_history[-1]["balance"]
            hourly_pnl = current_balance - hour_ago_balance
            
            return hourly_pnl
            
        except Exception as e:
            logger.error(f"Error calculating hourly PNL: {e}")
            return 0
            
    async def get_performance_summary(self) -> str:
        """Get formatted performance summary"""
        report = await self.generate_report()
        
        summary = f"""
🦈 SHARK0LOCKER PERFORMANCE 🦈
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: ${report['current_balance']:.2f}
📈 Equity: ${report['current_equity']:.2f}
💵 Total PNL: ${report['total_pnl']:.2f}
📊 ROI: {report['roi_percent']:.2f}%
⏱️ Hourly PNL: ${report['hourly_pnl']:.2f} ({report['hourly_roi']:.2f}%)
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Trades: {report['total_trades']} ({report['closed_trades']} closed)
✅ Wins: {report['winning_trades']}
❌ Losses: {report['losing_trades']}
🎯 Win Rate: {report['win_rate']:.2f}%
💚 Avg Profit: ${report['avg_profit']:.2f}
❤️ Avg Loss: ${report['avg_loss']:.2f}
📉 Drawdown: {report['current_drawdown']:.2f}%
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
        
        return summary
