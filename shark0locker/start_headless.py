#!/usr/bin/env python3
"""
REAL shark0locker - Headless mode (no terminal UI)
Perfect for background operation
⚠️ WARNING: This is REAL trading with REAL money!
"""
import asyncio
import logging
import sys
import signal

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

# Global variables
trading_system = None
telegram_bot = None
shutdown_event = asyncio.Event()

async def handle_shutdown(sig=None):
    """Handle shutdown signal"""
    if sig:
        logger.info(f"Received signal {sig}")
    logger.info("🛑 Initiating shutdown...")
    shutdown_event.set()

async def main():
    """Main function"""
    global trading_system, telegram_bot
    
    try:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - REAL TRADING SYSTEM  🦈                ║
║                                                               ║
║         ⚠️  REAL MONEY - REAL TRADING - HEADLESS MODE ⚠️     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        logger.info("Starting shark0locker in headless mode...")
        
        # Import modules
        from core.trading_system import TradingSystem
        from utils.telegram_bot import TelegramBotController
        from config.settings import config
        
        # Initialize trading system
        logger.info("Initializing trading system...")
        trading_system = TradingSystem()
        await trading_system.initialize()
        logger.info("✅ Trading system initialized")
        
        # Start Telegram bot
        logger.info("Starting Telegram bot...")
        telegram_bot = TelegramBotController(
            token=config.telegram.bot_token,
            chat_id=config.telegram.chat_id,
            trading_system=trading_system
        )
        await telegram_bot.start()
        logger.info("✅ Telegram bot started")
        
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
        print("   - All updates will be sent via Telegram")
        print("   - Logs: logs/shark0locker.log")
        print()
        print("Available Telegram Commands:")
        print("  /start    - ⚡ Start REAL trading")
        print("  /stop     - 🛑 Stop trading")
        print("  /status   - 📊 System status")
        print("  /stats    - 📈 Performance")
        print("  /balance  - 💰 Real balance")
        print("  /trades   - 📋 Recent trades")
        print("  /closeall - 🚨 Emergency exit")
        print()
        print("🦈 System is LIVE and waiting for /start command...")
        print("="*70)
        print()
        logger.info("System ready. Waiting for commands via Telegram...")
        
        # Setup signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda: asyncio.create_task(handle_shutdown(sig))
            )
        
        # Wait for shutdown signal
        await shutdown_event.wait()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        
        if trading_system:
            try:
                await trading_system.stop()
                await trading_system.shutdown()
                logger.info("Trading system shut down")
            except Exception as e:
                logger.error(f"Error stopping trading system: {e}")
        
        if telegram_bot:
            try:
                await telegram_bot.stop()
                logger.info("Telegram bot stopped")
            except Exception as e:
                logger.error(f"Error stopping telegram bot: {e}")
        
        logger.info("✅ Shutdown complete")
        print("\n✅ shark0locker stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦈 shark0locker terminated")
