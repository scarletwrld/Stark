"""
Main entry point for shark0locker trading bot
"""
import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.trading_system import TradingSystem
from utils.telegram_bot import TelegramBotController
from utils.terminal_ui import TerminalUI
from config.settings import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Shark0Locker:
    """Main application class"""
    
    def __init__(self):
        self.trading_system = TradingSystem()
        self.telegram_bot: Optional[TelegramBotController] = None
        self.terminal_ui: Optional[TerminalUI] = None
        self.shutdown_event = asyncio.Event()
        
    async def initialize(self):
        """Initialize all components"""
        logger.info("Initializing shark0locker...")
        
        # Initialize trading system
        await self.trading_system.initialize()
        
        # Initialize Telegram bot
        self.telegram_bot = TelegramBotController(
            token=config.telegram.bot_token,
            chat_id=config.telegram.chat_id,
            trading_system=self.trading_system
        )
        await self.telegram_bot.start()
        
        # Initialize terminal UI
        self.terminal_ui = TerminalUI(self.trading_system)
        self.terminal_ui.print_startup_banner()
        
        logger.info("shark0locker initialized successfully")
        
    async def start(self):
        """Start the bot"""
        logger.info("🦈 Starting shark0locker... 🦈")
        
        # Start trading system
        await self.trading_system.start()
        
        # Start terminal UI
        await self.terminal_ui.start()
        
        logger.info("🦈 shark0locker is HUNTING! 🦈")
        
    async def stop(self):
        """Stop the bot"""
        logger.info("🛑 Stopping shark0locker... 🛑")
        
        # Stop terminal UI
        if self.terminal_ui:
            await self.terminal_ui.stop()
        
        # Stop trading system
        await self.trading_system.stop()
        
        # Stop Telegram bot
        if self.telegram_bot:
            await self.telegram_bot.stop()
        
        logger.info("🛑 shark0locker stopped 🛑")
        
    async def shutdown(self):
        """Shutdown the bot"""
        await self.stop()
        await self.trading_system.shutdown()
        logger.info("Shutdown complete")
        
    async def run(self):
        """Main run loop"""
        try:
            # Setup signal handlers
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(
                    sig,
                    lambda: asyncio.create_task(self.handle_shutdown())
                )
            
            # Initialize
            await self.initialize()
            
            # Start
            await self.start()
            
            # Wait for shutdown signal
            await self.shutdown_event.wait()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            await self.shutdown()
            
    async def handle_shutdown(self):
        """Handle shutdown signal"""
        logger.info("Received shutdown signal")
        self.shutdown_event.set()

async def main():
    """Main entry point"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT  🦈         ║
║                                                               ║
║         Aggressive • Intelligent • Profitable                 ║
║                                                               ║
║  ⚠️  WARNING: HIGH-RISK TRADING SYSTEM                        ║
║  Trade at your own risk. Past performance ≠ future results   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    bot = Shark0Locker()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦈 shark0locker terminated by user 🦈")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
