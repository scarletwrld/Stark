#!/usr/bin/env python3
"""
shark0locker - DEMO MODE
Fully functional system with simulated trading (no real money)
All Telegram commands work, performance tracking works, but trades are simulated
"""
import asyncio
import logging
import sys
import signal
import random
from datetime import datetime

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

# Mock TradeLocker API Client
class MockTradeLockerClient:
    """Mock API client for demo mode"""
    
    def __init__(self, email, password, server, account_number, api_url=None):
        self.email = email
        self.account_number = account_number
        self.server = server
        self.api_url = api_url or "https://demo.mock.com"
        self.balance = 1000.00
        self.equity = 1000.00
        self.positions = []
        
    async def connect(self):
        logger.info(f"[DEMO MODE] Connected to mock TradeLocker - Account: {self.account_number}")
        await asyncio.sleep(0.1)
        
    async def disconnect(self):
        logger.info("[DEMO MODE] Disconnected")
        
    async def get_balance(self):
        return self.balance
        
    async def get_equity(self):
        return self.equity
        
    async def get_available_symbols(self):
        return ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD"]
        
    async def get_ticker(self, symbol):
        # Generate fake ticker data
        base_prices = {
            "EURUSD": 1.0850,
            "GBPUSD": 1.2650,
            "USDJPY": 149.50,
            "XAUUSD": 2050.00,
            "BTCUSD": 42000.00
        }
        base = base_prices.get(symbol, 1.0)
        spread = base * 0.0001
        return {
            "bid": base - spread / 2,
            "ask": base + spread / 2
        }
        
    async def get_all_tickers(self, symbols):
        tickers = {}
        for symbol in symbols:
            tickers[symbol] = await self.get_ticker(symbol)
        return tickers
        
    async def place_market_order(self, symbol, side, volume, stop_loss=None, take_profit=None):
        order_id = f"DEMO_{int(datetime.now().timestamp())}"
        # Simulate profit
        profit = random.uniform(5, 25)
        self.balance += profit
        self.equity = self.balance
        
        logger.info(f"[DEMO MODE] Order placed: {symbol} {side} {volume} lots - Profit: ${profit:.2f}")
        return {
            "orderId": order_id,
            "symbol": symbol,
            "side": side,
            "volume": volume
        }
        
    async def get_open_positions(self):
        return self.positions
        
    async def close_position(self, position_id):
        logger.info(f"[DEMO MODE] Position closed: {position_id}")
        return {"success": True}
        
    async def close_all_positions(self):
        count = len(self.positions)
        self.positions = []
        logger.info(f"[DEMO MODE] Closed {count} positions")
        return count

# Import and patch the modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Monkey patch the TradeLockerClient
import api.tradelocker_client as tl_module
tl_module.TradeLockerClient = MockTradeLockerClient

# Now import the rest
from core.trading_system import TradingSystem
from utils.telegram_bot import TelegramBotController
from config.settings import config

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
║    🦈  SHARK0LOCKER - DEMO MODE  🦈                          ║
║                                                               ║
║      ✅ FULLY FUNCTIONAL - SIMULATED TRADING ✅               ║
║         (No real money - Safe to test)                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        logger.info("Starting shark0locker in DEMO mode...")
        print("📝 DEMO MODE:")
        print("   - All Telegram commands work")
        print("   - Trading is simulated (no real money)")
        print("   - Perfect for testing and learning")
        print("   - Starting balance: $1,000 (virtual)")
        print()
        
        # Initialize trading system (with mocked API)
        logger.info("Initializing trading system...")
        trading_system = TradingSystem()
        await trading_system.initialize()
        logger.info("✅ Trading system initialized (DEMO MODE)")
        
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
        print("✅ SHARK0LOCKER DEMO MODE IS READY!")
        print("="*70)
        print()
        print("📱 Telegram Bot: @Elephant4Us_bot")
        print("💼 Mode: DEMO (Simulated Trading)")
        print("💰 Starting Balance: $1,000 (virtual)")
        print()
        print("Available Telegram Commands:")
        print("  /start    - ⚡ Start simulated trading")
        print("  /stop     - 🛑 Stop trading")
        print("  /status   - 📊 System status")
        print("  /stats    - 📈 Performance stats")
        print("  /balance  - 💰 Current balance (virtual)")
        print("  /trades   - 📋 Recent trades")
        print("  /closeall - 🚨 Close all positions")
        print()
        print("🦈 System is LIVE in DEMO mode!")
        print("📱 Send /start via Telegram to begin simulated trading")
        print()
        print("💡 This is perfect for:")
        print("   - Testing all features")
        print("   - Learning how the system works")
        print("   - Verifying Telegram integration")
        print("   - No risk - all trades are simulated!")
        print()
        print("Press Ctrl+C to shut down")
        print("="*70)
        print()
        
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
        print("\n✅ shark0locker DEMO stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦈 shark0locker DEMO terminated")
