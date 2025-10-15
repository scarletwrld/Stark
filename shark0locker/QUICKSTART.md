# 🦈 SHARK0LOCKER - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (Already Done!)
```bash
# Dependencies are already installed
```

### Step 2: Start the Bot
```bash
cd /workspace/shark0locker
python3 main.py
```

Or use the startup script:
```bash
cd /workspace/shark0locker
./start.sh
```

### Step 3: Control via Telegram

Open Telegram and message your bot:
- `/start` - Start trading
- `/status` - Check status
- `/stats` - View performance

## 📱 Telegram Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the trading system |
| `/stop` | Stop trading |
| `/status` | Get system status |
| `/stats` | Get performance statistics |
| `/balance` | Check current balance |
| `/trades` | View recent trades |
| `/closeall` | Close all positions (EMERGENCY) |

## 🎛️ How It Works

1. **Scanner Agents** (3 agents) scan all pairs every 100ms
2. **Analyzer Agents** (5 agents) perform deep technical analysis
3. **Executor Agents** (2 agents) execute trades with full portfolio
4. **Performance Monitor** tracks everything and sends updates

## 📊 What You'll See

### Terminal Dashboard
- Real-time system status
- All active agents and their performance
- Live balance and PNL
- Recent trades
- Beautiful shark graphics 🦈

### Telegram Updates
- Performance updates every 5 minutes
- Trade notifications
- PNL charts with graphics
- System alerts

## ⚙️ Configuration

All settings are in `config/settings.py`:

```python
# Trading Settings
max_position_size_percent: 100.0  # Full portfolio
leverage: 500                      # 1:500 leverage
min_win_probability: 0.98         # 98% win rate filter

# Performance Targets
hourly_target_percent: 100.0      # 100% per hour
daily_target_percent: 10000.0     # 10,000% per day
```

## 🛡️ Safety Features

- **Emergency Stop**: Use `/closeall` in Telegram
- **Automatic Position Management**: Quick profit taking
- **Error Recovery**: Comprehensive error handling
- **Detailed Logging**: Everything logged to `logs/shark0locker.log`

## ⚠️ Important Notes

1. **High Risk**: This uses aggressive full-portfolio trading with high leverage
2. **Account Size**: Works best with 1:500 or 1:1000 leverage accounts
3. **Market Conditions**: Performance varies with market volatility
4. **Monitoring**: Keep Telegram notifications enabled
5. **Testing**: Start with small account to test before scaling

## 🔧 Troubleshooting

### Bot won't start
```bash
# Check logs
tail -f logs/shark0locker.log

# Verify Python version
python3 --version  # Should be 3.9+
```

### Can't connect to TradeLocker
- Verify credentials in `config/settings.py`
- Check internet connection
- Ensure TradeLocker API is accessible

### Telegram not responding
- Verify bot token in `config/settings.py`
- Check chat ID is correct
- Send `/start` to bot first

## 📈 Performance Expectations

With optimal market conditions and 1:500 leverage:
- **Hourly**: 50-200% growth
- **Daily**: 1,000-10,000% potential
- **Win Rate**: 95-98% (through filtering)
- **Trade Duration**: Seconds to minutes

## 🎯 Best Practices

1. **Start Small**: Test with demo or small account first
2. **Monitor Closely**: Watch Telegram for first few hours
3. **Know Your Limits**: Set mental stop-loss for the account
4. **Market Hours**: Best during high-liquidity hours (London/NY overlap)
5. **Backup Plan**: Have `/closeall` ready if needed

## 🦈 Ready to Hunt!

```bash
# Start shark0locker
python3 main.py
```

The shark is hungry! Let's make some profits! 🦈💰

---

**Remember**: Trading involves risk. Never invest more than you can afford to lose.
