"""
Main Trading System for shark0locker
Orchestrates the multi-agent workforce
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import signal
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.tradelocker_client import TradeLockerClient
from agents.scanner_agent import ScannerAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.executor_agent import ExecutorAgent
from agents.performance_monitor import PerformanceMonitor
from config.settings import config

logger = logging.getLogger(__name__)

class TradingSystem:
    """Main trading system orchestrating all agents"""
    
    def __init__(self):
        self.config = config
        self.is_running = False
        self.api_client: Optional[TradeLockerClient] = None
        
        # Communication queues
        self.message_queue = asyncio.Queue()  # Scanner -> Analyzer
        self.signal_queue = asyncio.Queue()   # Analyzer -> Executor
        
        # Shared data structures
        self.trade_log = []
        
        # Agents
        self.scanner_agents: List[ScannerAgent] = []
        self.analyzer_agents: List[AnalyzerAgent] = []
        self.executor_agents: List[ExecutorAgent] = []
        self.performance_monitor: Optional[PerformanceMonitor] = None
        
        # Agent tasks
        self.agent_tasks = []
        
    async def initialize(self):
        """Initialize the trading system"""
        logger.info("Initializing shark0locker trading system...")
        
        # Create API client
        self.api_client = TradeLockerClient(
            email=self.config.tradelocker.email,
            password=self.config.tradelocker.password,
            server=self.config.tradelocker.server,
            account_number=self.config.tradelocker.account_number,
            api_url=self.config.tradelocker.api_url
        )
        
        # Connect to TradeLocker
        await self.api_client.connect()
        
        # Create scanner agents
        for i in range(self.config.agents.num_scanner_agents):
            agent = ScannerAgent(
                name=f"Scanner-{i+1}",
                config={
                    "scan_interval_seconds": self.config.trading.scan_interval_seconds,
                    "preferred_pairs": self.config.trading.preferred_pairs
                },
                api_client=self.api_client,
                message_queue=self.message_queue
            )
            self.scanner_agents.append(agent)
            
        # Create analyzer agents
        for i in range(self.config.agents.num_analyzer_agents):
            agent = AnalyzerAgent(
                name=f"Analyzer-{i+1}",
                config={
                    "min_win_probability": self.config.trading.min_win_probability
                },
                api_client=self.api_client,
                message_queue=self.message_queue,
                signal_queue=self.signal_queue
            )
            self.analyzer_agents.append(agent)
            
        # Create executor agents
        for i in range(self.config.agents.num_executor_agents):
            agent = ExecutorAgent(
                name=f"Executor-{i+1}",
                config={
                    "max_position_size_percent": self.config.trading.max_position_size_percent,
                    "leverage": self.config.trading.leverage
                },
                api_client=self.api_client,
                signal_queue=self.signal_queue,
                trade_log=self.trade_log
            )
            self.executor_agents.append(agent)
            
        # Create performance monitor
        self.performance_monitor = PerformanceMonitor(
            name="PerformanceMonitor",
            config={
                "hourly_target_percent": self.config.trading.hourly_target_percent
            },
            api_client=self.api_client,
            trade_log=self.trade_log
        )
        
        logger.info(
            f"Initialized {len(self.scanner_agents)} scanners, "
            f"{len(self.analyzer_agents)} analyzers, "
            f"{len(self.executor_agents)} executors"
        )
        
    async def start(self):
        """Start the trading system"""
        if self.is_running:
            logger.warning("Trading system is already running")
            return
            
        logger.info("🦈 Starting shark0locker trading system... 🦈")
        self.is_running = True
        
        # Start all agents
        all_agents = (
            self.scanner_agents +
            self.analyzer_agents +
            self.executor_agents +
            [self.performance_monitor]
        )
        
        for agent in all_agents:
            await agent.start()
            task = asyncio.create_task(agent.run())
            self.agent_tasks.append(task)
            
        logger.info("🦈 shark0locker is HUNTING! 🦈")
        
    async def stop(self):
        """Stop the trading system"""
        if not self.is_running:
            logger.warning("Trading system is not running")
            return
            
        logger.info("🛑 Stopping shark0locker trading system... 🛑")
        self.is_running = False
        
        # Stop all agents
        all_agents = (
            self.scanner_agents +
            self.analyzer_agents +
            self.executor_agents +
            [self.performance_monitor]
        )
        
        for agent in all_agents:
            await agent.stop()
            
        # Cancel all tasks
        for task in self.agent_tasks:
            task.cancel()
            
        # Wait for tasks to complete
        await asyncio.gather(*self.agent_tasks, return_exceptions=True)
        self.agent_tasks.clear()
        
        # Close all positions
        await self.close_all_positions()
        
        logger.info("🛑 shark0locker stopped 🛑")
        
    async def shutdown(self):
        """Shutdown the trading system and cleanup"""
        await self.stop()
        
        if self.api_client:
            await self.api_client.disconnect()
            
        logger.info("Trading system shutdown complete")
        
    async def get_status(self) -> str:
        """Get system status"""
        status = f"""
🦈 SHARK0LOCKER STATUS 🦈
━━━━━━━━━━━━━━━━━━━━━━━━━━
System: {"🟢 RUNNING" if self.is_running else "🔴 STOPPED"}

Agents Active:
  Scanners: {sum(1 for a in self.scanner_agents if a.is_running)}/{len(self.scanner_agents)}
  Analyzers: {sum(1 for a in self.analyzer_agents if a.is_running)}/{len(self.analyzer_agents)}
  Executors: {sum(1 for a in self.executor_agents if a.is_running)}/{len(self.executor_agents)}
  Monitor: {"✅" if self.performance_monitor.is_running else "❌"}

Queue Status:
  Opportunities: {self.message_queue.qsize()}
  Signals: {self.signal_queue.qsize()}
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
        return status
        
    async def get_performance(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        if self.performance_monitor:
            return await self.performance_monitor.generate_report()
        return {}
        
    async def get_performance_summary(self) -> str:
        """Get formatted performance summary"""
        if self.performance_monitor:
            return await self.performance_monitor.get_performance_summary()
        return "Performance monitor not available"
        
    async def get_balance(self) -> float:
        """Get current balance"""
        if self.api_client:
            return await self.api_client.get_balance()
        return 0.0
        
    async def get_equity(self) -> float:
        """Get current equity"""
        if self.api_client:
            return await self.api_client.get_equity()
        return 0.0
        
    async def get_recent_trades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trades"""
        return self.trade_log[-limit:] if self.trade_log else []
        
    async def close_all_positions(self) -> int:
        """Close all open positions"""
        if self.api_client:
            return await self.api_client.close_all_positions()
        return 0
