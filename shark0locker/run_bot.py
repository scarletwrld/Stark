#!/usr/bin/env python3
"""
Simple launcher for shark0locker - easier to use than main.py
"""
import asyncio
import logging
import sys
from pathlib import Path

# Setup logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function"""
    try:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT  🦈         ║
║                                                               ║
║         Aggressive • Intelligent • Profitable                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        print("📦 Importing modules...")
        from core.trading_system import TradingSystem
        from utils.telegram_bot import TelegramBotController
        from config.settings import config
        
        print("🔧 Initializing trading system...")
        trading_system = TradingSystem()
        await trading_system.initialize()
        
        print("📱 Starting Telegram bot...")
        telegram_bot = TelegramBotController(
            token=config.telegram.bot_token,
            chat_id=config.telegram.chat_id,
            trading_system=trading_system
        )
        await telegram_bot.start()
        
        print("\n" + "="*60)
        print("✅ SYSTEM READY!")
        print("="*60)
        print()
        print("📱 Telegram Bot: @Elephant4Us_bot")
        print()
        print("Available Commands:")
        print("  /start    - Start trading")
        print("  /stop     - Stop trading")
        print("  /status   - Get system status")
        print("  /stats    - View performance")
        print("  /balance  - Check balance")
        print("  /trades   - Recent trades")
        print("  /closeall - Emergency exit")
        print()
        print("🦈 The shark is ready! Send /start via Telegram to begin hunting!")
        print()
        print("Press Ctrl+C to stop the system")
        print("="*60)
        print()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
            
        # Cleanup
        await telegram_bot.stop()
        await trading_system.shutdown()
        
        print("✅ Shutdown complete")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦈 shark0locker terminated")
