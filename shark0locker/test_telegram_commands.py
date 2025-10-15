#!/usr/bin/env python3
"""
Test Telegram bot commands without the full trading system
This lets you test the Telegram integration quickly
"""
import asyncio
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Your bot credentials
BOT_TOKEN = "8109433790:AAEf4tMrbNaoHOvkK43flFwgeN5zz2TeD60"
CHAT_ID = "941247256"

# Mock trading system state
class MockTradingSystem:
    def __init__(self):
        self.is_running = False
        self.balance = 1000.00
        self.equity = 1000.00
    
    async def start(self):
        self.is_running = True
        logger.info("Mock trading started")
    
    async def stop(self):
        self.is_running = False
        logger.info("Mock trading stopped")
    
    async def get_status(self):
        return f"""
🦈 SHARK0LOCKER STATUS 🦈
━━━━━━━━━━━━━━━━━━━━━━━━━━
System: {"🟢 RUNNING" if self.is_running else "🔴 STOPPED"}
Mode: TEST MODE (mock data)
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
    
    async def get_performance_summary(self):
        return f"""
🦈 SHARK0LOCKER PERFORMANCE 🦈
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: ${self.balance:.2f}
📈 Equity: ${self.equity:.2f}
💵 Total PNL: $0.00 (TEST MODE)
📊 ROI: 0.00%
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
    
    async def get_balance(self):
        return self.balance
    
    async def get_equity(self):
        return self.equity
    
    async def get_recent_trades(self, limit=10):
        return []
    
    async def close_all_positions(self):
        return 0

# Command handlers
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await mock_system.start()
    await update.message.reply_text("🦈 shark0locker STARTED! (TEST MODE) 🦈\n\nThis is test mode. No real trading is happening.")

async def cmd_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop command"""
    await mock_system.stop()
    await update.message.reply_text("🛑 shark0locker STOPPED! 🛑")

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status command"""
    status = await mock_system.get_status()
    await update.message.reply_text(status)

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stats command"""
    stats = await mock_system.get_performance_summary()
    await update.message.reply_text(stats)

async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Balance command"""
    balance = await mock_system.get_balance()
    equity = await mock_system.get_equity()
    await update.message.reply_text(
        f"💰 Balance: ${balance:.2f}\n"
        f"📈 Equity: ${equity:.2f}\n\n"
        f"(TEST MODE - mock data)"
    )

async def cmd_trades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trades command"""
    await update.message.reply_text("📋 No trades yet (TEST MODE)")

async def cmd_closeall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Close all command"""
    await update.message.reply_text("✅ No positions to close (TEST MODE)")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
🦈 SHARK0LOCKER COMMANDS 🦈

/start - Start trading
/stop - Stop trading  
/status - Get system status
/stats - View performance
/balance - Check balance
/trades - Recent trades
/closeall - Emergency exit
/help - Show this help

Currently in TEST MODE
No real trading is happening
This is just to test Telegram commands!
    """.strip()
    await update.message.reply_text(help_text)

# Global mock system
mock_system = MockTradingSystem()

async def main():
    """Main function"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - TELEGRAM BOT TEST  🦈                  ║
║                                                               ║
║              Testing Telegram Commands                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("🔧 Starting Telegram bot...")
    print(f"📱 Bot: @Elephant4Us_bot")
    print(f"💬 Chat ID: {CHAT_ID}")
    print()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("balance", cmd_balance))
    app.add_handler(CommandHandler("trades", cmd_trades))
    app.add_handler(CommandHandler("closeall", cmd_closeall))
    app.add_handler(CommandHandler("help", cmd_help))
    
    # Start bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    # Send startup message
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🦈 shark0locker Telegram bot is ONLINE! 🦈\n\n"
             "⚠️ TEST MODE - No real trading\n\n"
             "Try these commands:\n"
             "/start - Start (test)\n"
             "/status - Check status\n"
             "/stats - View stats\n"
             "/help - Show all commands"
    )
    
    print("✅ Telegram bot is running!")
    print()
    print("="*60)
    print("📱 Go to Telegram and try these commands:")
    print("   /start")
    print("   /status")
    print("   /stats")
    print("   /help")
    print("="*60)
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
    
    # Cleanup
    await app.updater.stop()
    await app.stop()
    await app.shutdown()
    
    print("✅ Stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bye!")
