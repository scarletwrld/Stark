"""
Base agent class for shark0locker multi-agent system
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all trading agents"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.is_running = False
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "start_time": None,
            "last_activity": None
        }
        
    async def start(self):
        """Start the agent"""
        self.is_running = True
        self.stats["start_time"] = datetime.now()
        logger.info(f"Agent {self.name} started")
        
    async def stop(self):
        """Stop the agent"""
        self.is_running = False
        logger.info(f"Agent {self.name} stopped")
        
    @abstractmethod
    async def run(self):
        """Main agent loop - must be implemented by subclasses"""
        pass
        
    def update_stats(self, success: bool = True):
        """Update agent statistics"""
        if success:
            self.stats["tasks_completed"] += 1
        else:
            self.stats["tasks_failed"] += 1
        self.stats["last_activity"] = datetime.now()
        
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "name": self.name,
            "running": self.is_running,
            **self.stats
        }
