"""
Configuration settings for shark0locker trading bot
"""
import os
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TradeLockerConfig:
    """TradeLocker API configuration"""
    email: str = "tiggysurf@gmail.com"
    account_number: str = "1550788"
    password: str = "!2e375iW"
    server: str = "GATESFX"
    currency: str = "USD"
    # CORRECT API URL for TradeLocker DEMO
    api_url: str = "https://demo.tradelocker.com/backend-api"
    
@dataclass
class TelegramConfig:
    """Telegram bot configuration"""
    bot_token: str = "8109433790:AAEf4tMrbNaoHOvkK43flFwgeN5zz2TeD60"
    chat_id: str = "941247256"
    
@dataclass
class TradingConfig:
    """Trading strategy configuration"""
    # Risk management
    max_position_size_percent: float = 100.0  # Full port
    leverage: int = 500
    
    # Strategy parameters
    min_win_probability: float = 0.98  # Target 98% win rate
    max_drawdown_percent: float = 5.0
    
    # High frequency settings
    scan_interval_seconds: float = 0.1  # 100ms scan interval
    order_timeout_seconds: float = 1.0
    max_concurrent_trades: int = 5
    
    # Pair selection
    preferred_pairs: List[str] = None
    excluded_pairs: List[str] = None
    
    # Performance targets
    hourly_target_percent: float = 100.0  # 100% per hour minimum
    daily_target_percent: float = 10000.0  # 10,000% per day
    
    def __post_init__(self):
        if self.preferred_pairs is None:
            # Major forex pairs with high liquidity
            self.preferred_pairs = [
                "EURUSD", "GBPUSD", "USDJPY", "USDCHF", 
                "AUDUSD", "USDCAD", "NZDUSD",
                "EURJPY", "GBPJPY", "EURGBP",
                "XAUUSD", "BTCUSD", "ETHUSD"  # Gold and crypto
            ]
        if self.excluded_pairs is None:
            self.excluded_pairs = []

@dataclass
class AgentConfig:
    """Multi-agent workforce configuration"""
    num_scanner_agents: int = 3
    num_analyzer_agents: int = 5
    num_executor_agents: int = 2
    
    # Agent behavior
    scanner_speed_ms: int = 50  # Scan every 50ms
    analyzer_depth: int = 10  # Deep analysis
    executor_slippage_tolerance: float = 0.0001
    
@dataclass
class BotConfig:
    """Main bot configuration"""
    name: str = "shark0locker"
    version: str = "1.0.0"
    
    # Sub-configs
    tradelocker: TradeLockerConfig = None
    telegram: TelegramConfig = None
    trading: TradingConfig = None
    agents: AgentConfig = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/shark0locker.log"
    
    # Data storage
    data_dir: str = "data"
    
    def __post_init__(self):
        if self.tradelocker is None:
            self.tradelocker = TradeLockerConfig()
        if self.telegram is None:
            self.telegram = TelegramConfig()
        if self.trading is None:
            self.trading = TradingConfig()
        if self.agents is None:
            self.agents = AgentConfig()

# Global config instance
config = BotConfig()
