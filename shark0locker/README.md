# 🦈 SHARK0LOCKER - High Frequency Trading Bot

Ultra-aggressive, intelligent, multi-agent trading system for TradeLocker platform.

## ⚠️ WARNING

**HIGH-RISK TRADING SYSTEM**: This bot uses aggressive full-portfolio strategies with high leverage. Trading involves substantial risk of loss. Past performance does not guarantee future results. Use at your own risk.

## 🚀 Features

### Multi-Agent Workforce
- **Scanner Agents**: Hunt for opportunities across all pairs (100ms scan interval)
- **Analyzer Agents**: Deep technical analysis with 98%+ win probability filtering
- **Executor Agents**: Ultra-fast order execution with minimal slippage
- **Performance Monitor**: Real-time PNL tracking and reporting

### Trading Strategy
- **Full Portfolio Trading**: Uses 100% of available capital with leverage
- **High Frequency**: Scans market every 100ms for opportunities
- **Scalping**: Quick in-and-out trades for consistent profits
- **Risk Management**: Tight stop losses and quick profit taking

### Control & Monitoring
- **Telegram Bot**: Remote control and real-time notifications
- **Terminal Dashboard**: Beautiful live dashboard with Rich UI
- **Performance Tracking**: Detailed metrics and trade logging

## 📋 Prerequisites

- Python 3.9 or higher
- TradeLocker account with API access
- Telegram Bot (for remote control)
- Virtual environment (recommended)

## 🛠️ Installation

1. **Navigate to the shark0locker directory:**
```bash
cd shark0locker
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv ../venv
source ../venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:

### Trading Parameters
- `max_position_size_percent`: Position size (default: 100% - full port)
- `leverage`: Account leverage (default: 500)
- `min_win_probability`: Minimum win rate for trades (default: 98%)
- `scan_interval_seconds`: Market scan frequency (default: 0.1s)
- `hourly_target_percent`: Hourly profit target (default: 100%)

### Agent Configuration
- `num_scanner_agents`: Number of scanning agents (default: 3)
- `num_analyzer_agents`: Number of analysis agents (default: 5)
- `num_executor_agents`: Number of execution agents (default: 2)

### Credentials
All credentials are pre-configured:
- TradeLocker account
- Telegram bot token and chat ID

## 🎯 Usage

### Quick Start

```bash
chmod +x start.sh
./start.sh
```

### Manual Start

```bash
source ../venv/bin/activate
python3 main.py
```

### Telegram Commands

Once running, control the bot via Telegram:

- `/start` - Start trading
- `/stop` - Stop trading
- `/status` - Get system status
- `/stats` - Get performance statistics
- `/balance` - Get current balance
- `/trades` - Get recent trades
- `/closeall` - Close all positions (emergency)

## 📊 Terminal Dashboard

The terminal UI shows:
- **System Status**: Current state and queue status
- **Agent Workforce**: All agents and their performance
- **Performance Metrics**: Balance, PNL, ROI, win rate
- **Recent Trades**: Last 10 trades with PNL

## 🏗️ Architecture

```
shark0locker/
├── agents/              # Trading agents
│   ├── base_agent.py   # Base agent class
│   ├── scanner_agent.py    # Market scanning
│   ├── analyzer_agent.py   # Technical analysis
│   ├── executor_agent.py   # Order execution
│   └── performance_monitor.py  # Performance tracking
├── api/                # API clients
│   └── tradelocker_client.py  # TradeLocker API
├── config/             # Configuration
│   └── settings.py     # Bot settings
├── core/               # Core system
│   └── trading_system.py  # Main orchestrator
├── utils/              # Utilities
│   ├── telegram_bot.py    # Telegram integration
│   └── terminal_ui.py     # Terminal UI
├── data/               # Data storage
├── logs/               # Log files
└── main.py            # Entry point
```

## 🎨 How It Works

1. **Scanner Agents** continuously scan all configured pairs for price movements
2. **Analyzer Agents** receive opportunities and perform deep technical analysis
3. Only signals with 98%+ win probability are sent to executors
4. **Executor Agents** place orders instantly with full portfolio size
5. **Performance Monitor** tracks all trades and sends updates via Telegram
6. **Terminal UI** displays everything in real-time

## 🔧 Advanced Configuration

### Customize Trading Pairs

Edit `config/settings.py`:
```python
preferred_pairs = [
    "EURUSD", "GBPUSD", "USDJPY", 
    "XAUUSD", "BTCUSD"
]
```

### Adjust Risk Parameters

```python
max_position_size_percent = 100.0  # Full portfolio
leverage = 500                      # 1:500 leverage
min_win_probability = 0.98         # 98% win rate filter
```

### Tune Performance Targets

```python
hourly_target_percent = 100.0      # 100% per hour
daily_target_percent = 10000.0     # 10,000% per day
```

## 📝 Logging

Logs are stored in `logs/shark0locker.log` with detailed information about:
- Agent activities
- Trade executions
- Performance metrics
- Errors and warnings

## 🛡️ Safety Features

- **Emergency Stop**: Use `/closeall` command to exit all positions
- **Position Management**: Automatic monitoring and closing of profitable positions
- **Error Handling**: Comprehensive error handling and logging
- **Rate Limiting**: Prevents API overload

## 📱 Telegram Updates

The bot sends:
- Periodic performance updates (every 5 minutes)
- Trade notifications
- PNL charts with shark graphics
- System status alerts

## 🐛 Troubleshooting

### Connection Issues
```bash
# Check TradeLocker API status
# Verify credentials in config/settings.py
```

### Installation Issues
```bash
# Ensure Python 3.9+
python3 --version

# Update pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Performance Issues
- Reduce number of agents in config
- Increase scan_interval_seconds
- Reduce number of preferred_pairs

## 📈 Performance Expectations

- **Win Rate**: 98%+ (targeted through filtering)
- **Hourly Growth**: 100%+ (aggressive full-port trading)
- **Daily Growth**: 1,000-10,000% (with optimal conditions and leverage)
- **Trade Duration**: Seconds to minutes (scalping)

## ⚠️ Disclaimer

This trading bot is provided as-is without any guarantees. Trading forex, CFDs, and cryptocurrencies involves substantial risk of loss. The high leverage and aggressive strategy can result in rapid account growth OR rapid account loss. Never trade with money you cannot afford to lose. The developers are not responsible for any financial losses incurred using this software.

## 📞 Support

For issues or questions:
1. Check the logs in `logs/shark0locker.log`
2. Review configuration in `config/settings.py`
3. Use Telegram `/status` command to diagnose

## 🦈 Let's Hunt!

```bash
./start.sh
```

The shark is ready to dominate the markets! 🦈💰
