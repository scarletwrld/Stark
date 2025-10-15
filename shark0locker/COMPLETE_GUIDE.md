# 🦈 SHARK0LOCKER - Complete User Guide

## Welcome to shark0locker!

Your ultra-aggressive, AI-powered, multi-agent high-frequency trading bot is ready to dominate the markets! This guide will walk you through everything you need to know.

---

## 📋 Table of Contents

1. [What is shark0locker?](#what-is-shark0locker)
2. [How to Start](#how-to-start)
3. [Telegram Commands](#telegram-commands)
4. [Understanding the Dashboard](#understanding-the-dashboard)
5. [How the Bot Works](#how-the-bot-works)
6. [Configuration Options](#configuration-options)
7. [Monitoring Performance](#monitoring-performance)
8. [Safety & Risk Management](#safety--risk-management)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## What is shark0locker?

**shark0locker** is a sophisticated high-frequency trading bot that:

- 🔍 **Scans** all trading pairs every 100 milliseconds
- 🧠 **Analyzes** opportunities using AI-powered multi-factor analysis
- ⚡ **Executes** trades instantly with full portfolio positioning
- 📊 **Monitors** performance and sends real-time updates
- 🤖 **Adapts** to market conditions automatically

### The Shark Mentality

Like a shark hunting fish in the ocean, this bot:
- **Hunts aggressively** for profitable opportunities
- **Moves quickly** to capture profits
- **Grows bigger** with each successful trade
- **Never stops** scanning for the next opportunity

---

## How to Start

### Method 1: Quick Start (Recommended)

```bash
cd /workspace/shark0locker
python3 main.py
```

### Method 2: Using the Startup Script

```bash
cd /workspace/shark0locker
./start.sh
```

### What Happens When You Start?

1. **Initialization**: Connects to TradeLocker API
2. **Agent Deployment**: Launches 11 agents:
   - 3 Scanner Agents
   - 5 Analyzer Agents
   - 2 Executor Agents
   - 1 Performance Monitor
3. **Telegram Activation**: Connects to Telegram bot
4. **Dashboard Launch**: Opens terminal dashboard
5. **Ready to Hunt**: System waits for your `/start` command

---

## Telegram Commands

Your bot is waiting for you on Telegram! Here are all available commands:

### Essential Commands

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/start` | Start trading | When you're ready to begin |
| `/stop` | Stop trading | When you want to pause |
| `/status` | Get system status | Check if everything is running |

### Monitoring Commands

| Command | What It Does | Information Provided |
|---------|--------------|---------------------|
| `/stats` | Performance statistics | Balance, PNL, ROI, Win Rate, Trades |
| `/balance` | Current balance | Balance and Equity |
| `/trades` | Recent trades | Last 10 trades with PNL |

### Emergency Command

| Command | What It Does | ⚠️ Warning |
|---------|--------------|-----------|
| `/closeall` | Close ALL positions | Use ONLY in emergency! |

### Example Usage

```
You: /start
Bot: 🦈 shark0locker STARTED! Hunting for profits... 🦈

[5 minutes later]
Bot: 🦈 SHARK FEEDING UPDATE 🦈
     💰 Balance: $1,250.00
     📈 PNL: +$250.00 (+25%)
     🎯 Win Rate: 97.5%
     [Sends PNL chart]

You: /stats
Bot: [Detailed performance report]

You: /closeall
Bot: ✅ Closed 3 positions
```

---

## Understanding the Dashboard

When you start shark0locker, you'll see a beautiful terminal dashboard:

### Header
```
🦈🦈🦈🦈🦈🦈🦈🦈🦈🦈
  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT
🦈🦈🦈🦈🦈🦈🦈🦈🦈🦈
```

### System Status Panel (Top Left)
Shows:
- ✅ System status (HUNTING / STOPPED)
- ⏰ Current time
- 💼 Account number and server
- 📊 Queue status (opportunities and signals)

### Agent Workforce Panel (Bottom Left)
Shows all 11 agents:
- 🟢 Agent name and status
- ✅ Tasks completed
- ❌ Tasks failed

Example:
```
Agent           Status  Tasks   Failed
Scanner-1       🟢      1250    0
Scanner-2       🟢      1245    0
Scanner-3       🟢      1248    0
Analyzer-1      🟢      850     2
Analyzer-2      🟢      840     1
Analyzer-3      🟢      855     0
Analyzer-4      🟢      845     1
Analyzer-5      🟢      860     0
Executor-1      🟢      45      0
Executor-2      🟢      42      0
PerformanceMonitor 🟢   120     0
```

### Performance Panel (Top Right)
Shows:
- 💰 Current balance
- 📈 Current equity
- 💵 Total PNL
- 📊 ROI percentage
- 🎯 Win rate
- ⏱️ Hourly PNL

### Trades Panel (Bottom Right)
Shows last 10 trades:
- Symbol (e.g., EURUSD)
- Direction (🟢 BUY / 🔴 SELL)
- Entry price
- PNL (in green/red)
- Status

---

## How the Bot Works

### Step-by-Step Process

#### 1. Scanning Phase (3 Scanner Agents)
- **What**: Fetch live prices for all pairs
- **How**: Query TradeLocker API every 100ms
- **Output**: Price data with velocity calculations

#### 2. Opportunity Detection
- **What**: Identify strong price movements
- **How**: Calculate velocity (price change rate)
- **Threshold**: Significant movement > 0.001
- **Output**: Opportunities with scores

#### 3. Deep Analysis (5 Analyzer Agents)
- **What**: Perform comprehensive technical analysis
- **Factors**:
  - 📈 Momentum (25% weight)
  - 📊 Volatility (20% weight)
  - 💹 Spread quality (15% weight)
  - ⚡ Velocity (25% weight)
  - 🎯 Pattern recognition (15% weight)
- **Output**: Win probability score

#### 4. Signal Filtering
- **What**: Filter for high-probability trades
- **Threshold**: Only signals with 98%+ win probability
- **Output**: Trading signals with entry/exit levels

#### 5. Execution (2 Executor Agents)
- **What**: Place orders instantly
- **Position Size**: Full portfolio (100% of available capital)
- **Leverage**: 1:500 or 1:1000
- **Speed**: Market orders (instant fill)
- **Protection**: Stop loss and take profit set

#### 6. Position Management
- **What**: Monitor active positions
- **Strategy**: Close on profit (scalping)
- **Speed**: Real-time monitoring
- **Goal**: Lock in small, frequent gains

#### 7. Performance Tracking
- **What**: Track all metrics
- **Frequency**: Every 5 seconds
- **Output**: Performance reports to Telegram and dashboard

### The Complete Flow

```
Markets → Scan → Detect → Analyze → Filter → Execute → Manage → Profit 🦈
```

---

## Configuration Options

All settings are in `config/settings.py`. Here's what you can customize:

### Trading Parameters

```python
# Position sizing
max_position_size_percent = 100.0  # Use full portfolio
leverage = 500                      # 1:500 leverage

# Strategy
min_win_probability = 0.98         # Only take 98%+ trades
max_drawdown_percent = 5.0         # Maximum acceptable drawdown

# Speed
scan_interval_seconds = 0.1        # Scan every 100ms
order_timeout_seconds = 1.0        # 1 second timeout
max_concurrent_trades = 5          # Max 5 positions at once

# Targets
hourly_target_percent = 100.0      # 100% per hour
daily_target_percent = 10000.0     # 10,000% per day
```

### Trading Pairs

```python
preferred_pairs = [
    # Forex majors
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF",
    "AUDUSD", "USDCAD", "NZDUSD",
    
    # Forex crosses
    "EURJPY", "GBPJPY", "EURGBP",
    
    # Gold & Crypto
    "XAUUSD", "BTCUSD", "ETHUSD"
]
```

### Agent Configuration

```python
num_scanner_agents = 3    # More = faster scanning
num_analyzer_agents = 5   # More = deeper analysis
num_executor_agents = 2   # More = faster execution
```

### Customization Tips

1. **Conservative Mode**: Reduce `max_position_size_percent` to 50%
2. **Faster Scanning**: Decrease `scan_interval_seconds` to 0.05
3. **Higher Win Rate**: Increase `min_win_probability` to 0.99
4. **More Pairs**: Add to `preferred_pairs` list
5. **Focus Mode**: Reduce to only major pairs

---

## Monitoring Performance

### Real-Time Monitoring

#### Terminal Dashboard
- Always visible while bot is running
- Updates every 0.5 seconds
- Shows everything at a glance

#### Telegram Updates
- Automatic updates every 5 minutes
- PNL charts with shark graphics
- Trade notifications
- System alerts

### Key Metrics to Watch

#### 1. Balance & Equity
- **Balance**: Your account balance
- **Equity**: Balance + floating P/L
- **Goal**: Both should be increasing

#### 2. PNL (Profit & Loss)
- **Total PNL**: Total profit/loss since start
- **Hourly PNL**: Last hour performance
- **Goal**: Positive and growing

#### 3. ROI (Return on Investment)
- **Calculation**: (PNL / Initial Balance) × 100
- **Hourly ROI**: Performance per hour
- **Goal**: Meet target (100%/hour)

#### 4. Win Rate
- **Calculation**: (Winning Trades / Total Closed Trades) × 100
- **Goal**: Maintain 95%+ (target 98%)

#### 5. Trade Count
- **Total Trades**: All trades executed
- **Closed Trades**: Completed trades
- **Win/Loss**: Breakdown
- **Goal**: High volume, high win rate

#### 6. Drawdown
- **Current Drawdown**: % drop from peak
- **Goal**: Keep under 5%

### Understanding the Numbers

**Example Performance:**
```
Balance: $1,500 (started with $1,000)
Total PNL: +$500
ROI: +50%
Hourly PNL: +$250
Hourly ROI: +25%
Win Rate: 96.5%
Trades: 120 (115 wins, 5 losses)
```

This means:
- ✅ Made $500 profit (50% gain)
- ✅ Last hour made $250 (25% of initial capital)
- ✅ 115 out of 120 trades were profitable
- ✅ Win rate slightly below target (aim for 98%)

---

## Safety & Risk Management

### Built-in Safety Features

#### 1. Stop Loss Protection
- Automatically set on every trade
- Tight stops (5× spread)
- Prevents large losses

#### 2. Take Profit Targets
- Automatically set on every trade
- Quick profit taking (10× spread)
- Locks in gains

#### 3. Position Monitoring
- Real-time monitoring
- Automatic close on profit
- Quick exit strategy

#### 4. Error Handling
- Comprehensive error recovery
- Continues on non-fatal errors
- Logs all issues

#### 5. Emergency Controls
- `/closeall` command
- Immediate position exit
- System stop function

### Best Practices

#### Before Starting

1. ✅ **Check Account**: Verify TradeLocker connection
2. ✅ **Check Balance**: Ensure sufficient capital
3. ✅ **Check Leverage**: Confirm 1:500 or 1:1000
4. ✅ **Test Telegram**: Send `/status` command
5. ✅ **Review Settings**: Check `config/settings.py`

#### While Running

1. ✅ **Monitor Telegram**: Watch for updates
2. ✅ **Check Dashboard**: Glance at terminal regularly
3. ✅ **Watch Drawdown**: If > 5%, consider stopping
4. ✅ **Review Trades**: Check win rate stays high
5. ✅ **Be Ready**: Keep `/closeall` in mind

#### Risk Guidelines

1. **Start Small**: Test with small account first
2. **Don't Over-leverage**: 1:500 max recommended
3. **Set Limits**: Mental stop-loss for account
4. **Best Hours**: Trade during high liquidity (London/NY)
5. **Know When to Stop**: If not performing, pause and review

### Emergency Procedures

#### Market Crash
```
1. Send /closeall to Telegram bot
2. Verify all positions closed
3. Send /stop to halt trading
4. Check logs for issues
```

#### API Connection Lost
```
1. Bot will attempt auto-reconnect
2. Check logs/shark0locker.log
3. If persists, stop and restart
4. Verify TradeLocker API status
```

#### Unexpected Losses
```
1. Review recent trades in dashboard
2. Check /stats for win rate
3. If win rate < 90%, stop temporarily
4. Review configuration
5. Consider adjusting min_win_probability
```

---

## Troubleshooting

### Common Issues & Solutions

#### Bot Won't Start

**Symptom**: Error when running `python3 main.py`

**Solutions**:
1. Check Python version: `python3 --version` (need 3.9+)
2. Verify dependencies: `pip3 list | grep aiohttp`
3. Check logs: `cat logs/shark0locker.log`
4. Verify working directory: Should be in `/workspace/shark0locker`

#### Can't Connect to TradeLocker

**Symptom**: "Authentication failed" in logs

**Solutions**:
1. Verify credentials in `config/settings.py`
2. Check internet connection
3. Verify TradeLocker API is online
4. Try manual login to TradeLocker website
5. Check account status (not suspended)

#### Telegram Bot Not Responding

**Symptom**: Commands don't work

**Solutions**:
1. Verify bot token in `config/settings.py`
2. Check chat ID is correct
3. Send `/start` to bot first (initialize chat)
4. Check bot is running: Look for "Telegram bot started" in logs
5. Verify internet connection

#### No Trades Being Executed

**Symptom**: Bot running but not trading

**Solutions**:
1. Check if you sent `/start` command
2. Verify opportunities in queue (dashboard)
3. Check min_win_probability setting (might be too high)
4. Verify market is open and liquid
5. Check logs for errors

#### High Frequency of Losses

**Symptom**: Win rate < 90%

**Solutions**:
1. Increase min_win_probability to 0.99
2. Reduce scan_interval_seconds (be more selective)
3. Check market conditions (volatile?)
4. Reduce max_position_size_percent
5. Review preferred_pairs (remove problematic ones)

### Log Files

**Location**: `logs/shark0locker.log`

**View real-time**:
```bash
tail -f logs/shark0locker.log
```

**Search for errors**:
```bash
grep ERROR logs/shark0locker.log
```

**Look for specific symbol**:
```bash
grep EURUSD logs/shark0locker.log
```

---

## Advanced Usage

### Optimizing for Maximum Profits

#### 1. Tune the Win Rate Filter
- Start: 0.98 (default)
- More trades: 0.95
- Higher quality: 0.99

#### 2. Adjust Scan Speed
- Default: 100ms
- Faster: 50ms (more opportunities)
- Slower: 200ms (less load)

#### 3. Optimize Agent Count
- More scanners: Faster market coverage
- More analyzers: Better analysis quality
- More executors: Faster order placement

#### 4. Customize Trading Pairs
- Focus on most liquid pairs
- Add pairs with high volatility
- Remove pairs with wide spreads

#### 5. Time-Based Trading
- Best: London/NY overlap (13:00-17:00 UTC)
- Good: Asian session (00:00-08:00 UTC)
- Avoid: Sunday open, Friday close

### Performance Tuning

#### For Speed
```python
scan_interval_seconds = 0.05       # Faster scanning
num_scanner_agents = 5             # More scanners
num_executor_agents = 3            # More executors
```

#### For Quality
```python
min_win_probability = 0.99         # Higher threshold
num_analyzer_agents = 10           # More analysis
preferred_pairs = ["EURUSD", "GBPUSD"]  # Focus on majors
```

#### For Safety
```python
max_position_size_percent = 50.0   # Half portfolio
max_concurrent_trades = 2          # Fewer positions
max_drawdown_percent = 3.0         # Tighter limit
```

### Multiple Accounts

Want to run on multiple accounts?

1. Copy the shark0locker folder:
```bash
cp -r shark0locker shark0locker_account2
```

2. Edit `config/settings.py` in the copy with new credentials

3. Run both:
```bash
# Terminal 1
cd shark0locker
python3 main.py

# Terminal 2
cd shark0locker_account2
python3 main.py
```

### Data Analysis

Trade data is stored in the Trade Log. To analyze:

```python
# Add at end of performance_monitor.py
import json

# Save trades to file
with open('data/trades.json', 'w') as f:
    json.dump(self.trade_log, f, default=str)
```

Then analyze with pandas:
```python
import pandas as pd

df = pd.read_json('data/trades.json')
print(df.groupby('symbol')['pnl'].sum())
```

---

## 🦈 Final Tips

### The Shark Mindset

1. **Be Patient**: The shark waits for the right opportunity
2. **Be Aggressive**: When opportunity comes, strike hard
3. **Be Consistent**: Small frequent gains compound
4. **Be Adaptive**: Markets change, be ready to adjust
5. **Be Disciplined**: Stick to your strategy

### Success Formula

```
High Win Rate (98%) 
× Full Portfolio (100%)
× High Leverage (1:500)
× High Frequency (many trades/hour)
= Exponential Growth 🚀
```

### Remember

- The bot is a tool, not magic
- Trading involves risk
- Monitor performance actively
- Adjust settings as needed
- Take profits regularly
- Know when to stop

### Support

If you need help:
1. Check this guide
2. Review logs: `logs/shark0locker.log`
3. Test with `/status` command
4. Review configuration
5. Check system architecture docs

---

## 🎯 Ready to Hunt!

You now have everything you need to unleash shark0locker on the markets!

```bash
cd /workspace/shark0locker
python3 main.py
```

Then send `/start` via Telegram and watch the shark feast! 🦈💰

**Good luck and happy trading!**

---

*Remember: Trade responsibly. High leverage = high risk. Never invest more than you can afford to lose.*
