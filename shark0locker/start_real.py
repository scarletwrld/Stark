#!/usr/bin/env python3
"""
REAL shark0locker launcher - Full trading system with TradeLocker
⚠️ WARNING: This is REAL trading with REAL money!
"""
import asyncio
import logging
import sys
import signal
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/shark0locker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Global variables for cleanup
trading_system = None
telegram_bot = None
terminal_ui = None

async def shutdown(signal_received=None):
    """Graceful shutdown"""
    if signal_received:
        logger.info(f"Received signal {signal_received}")
    
    logger.info("🛑 Shutting down shark0locker...")
    
    if terminal_ui:
        await terminal_ui.stop()
    
    if trading_system:
        await trading_system.stop()
        await trading_system.shutdown()
    
    if telegram_bot:
        await telegram_bot.stop()
    
    logger.info("✅ Shutdown complete")

async def main():
    """Main function - REAL trading system"""
    global trading_system, telegram_bot, terminal_ui
    
    try:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - REAL TRADING SYSTEM  🦈                ║
║                                                               ║
║         ⚠️  WARNING: REAL MONEY - REAL TRADING  ⚠️           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        print("⚠️  HIGH RISK WARNING:")
        print("   - This system trades with REAL money")
        print("   - Uses aggressive full-portfolio strategy")
        print("   - High leverage (1:500)")
        print("   - Can result in rapid gains OR losses")
        print()
        input("Press ENTER to continue or Ctrl+C to cancel... ")
        print()
        
        print("📦 Importing modules...")
        from core.trading_system import TradingSystem
        from utils.telegram_bot import TelegramBotController
        from utils.terminal_ui import TerminalUI
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
        
        print("🖥️  Starting terminal UI...")
        terminal_ui = TerminalUI(trading_system)
        terminal_ui.print_startup_banner()
        
        print("\n" + "="*70)
        print("✅ SHARK0LOCKER IS READY FOR REAL TRADING!")
        print("="*70)
        print()
        print("📱 Telegram Bot: @Elephant4Us_bot")
        print("🏦 TradeLocker Account: 1550788")
        print("🌐 Server: GATESFX")
        print()
        print("⚠️  IMPORTANT:")
        print("   - Trading is NOT started yet")
        print("   - Send /start via Telegram to begin REAL trading")
        print("   - Use /closeall for emergency exit")
        print()
        print("Available Telegram Commands:")
        print("  /start    - ⚡ Start REAL trading")
        print("  /stop     - 🛑 Stop trading")
        print("  /status   - 📊 Get system status")
        print("  /stats    - 📈 View performance")
        print("  /balance  - 💰 Check REAL balance")
        print("  /trades   - 📋 Recent trades")
        print("  /closeall - 🚨 Emergency exit (close all positions)")
        print()
        print("🦈 System ready! Waiting for your /start command...")
        print()
        print("Press Ctrl+C to shut down the system")
        print("="*70)
        print()
        
        # Start terminal UI
        await terminal_ui.start()
        
        # Setup signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(shutdown(s))
            )
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ FATAL ERROR: {e}")
    finally:
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦈 shark0locker terminated by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
