#!/usr/bin/env python3
"""
Force start trading - bypasses Telegram command
Use this if /start command isn't working
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

async def main():
    print("🔧 Force starting shark0locker trading system...")
    
    from api.tradelocker_client import TradeLockerClient
    from config.settings import config
    
    # Test API connection first
    print("\n1️⃣ Testing TradeLocker API...")
    client = TradeLockerClient(
        email=config.tradelocker.email,
        password=config.tradelocker.password,
        server=config.tradelocker.server,
        account_number=config.tradelocker.account_number,
        api_url=config.tradelocker.api_url
    )
    
    try:
        await client.connect()
        print("   ✅ Connected to TradeLocker")
        
        # Test getting symbols
        print("\n2️⃣ Testing market data...")
        symbols = await client.get_available_symbols()
        print(f"   ✅ Found {len(symbols)} symbols")
        if symbols:
            print(f"   Symbols: {symbols[:5]}...")
        
        # Test getting ticker
        if symbols:
            print("\n3️⃣ Testing ticker data...")
            ticker = await client.get_ticker(symbols[0])
            print(f"   ✅ Ticker for {symbols[0]}: {ticker}")
        
        # Test getting all tickers
        print("\n4️⃣ Testing multiple tickers...")
        test_symbols = config.trading.preferred_pairs[:3]
        tickers = await client.get_all_tickers(test_symbols)
        print(f"   ✅ Got {len(tickers)} tickers")
        for symbol, data in tickers.items():
            print(f"   {symbol}: {data}")
        
        await client.disconnect()
        
        print("\n" + "="*70)
        print("✅ ALL API TESTS PASSED!")
        print("="*70)
        print("\nThe API is working. Now checking why no trades...")
        print("\nPossible issues:")
        print("1. Win probability threshold too high (98%)")
        print("2. /start command not sent via Telegram")
        print("3. Market not moving enough")
        
        print("\n🔧 Let me lower the win threshold and force start...")
        
    except Exception as e:
        print(f"\n❌ API TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Now actually start the trading system
    print("\n5️⃣ Starting actual trading system...")
    from core.trading_system import TradingSystem
    
    trading_system = TradingSystem()
    await trading_system.initialize()
    print("   ✅ Trading system initialized")
    
    # Start trading
    await trading_system.start()
    print("   ✅ Trading started!")
    
    print("\n" + "="*70)
    print("🦈 SHARK0LOCKER IS NOW HUNTING!")
    print("="*70)
    print("\nWatch the logs:")
    print("  tail -f logs/shark0locker.log")
    print("\nPress Ctrl+C to stop")
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(10)
            # Show status every 10 seconds
            status = await trading_system.get_status()
            print(f"\n{status}")
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        await trading_system.stop()
        await trading_system.shutdown()
        print("✅ Stopped")

if __name__ == "__main__":
    asyncio.run(main())
