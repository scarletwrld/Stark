#!/usr/bin/env python3
"""
Quick test script to verify Telegram bot works
"""
import asyncio
from telegram import Bot

async def test_telegram():
    """Test Telegram bot connection"""
    token = "8109433790:AAEf4tMrbNaoHOvkK43flFwgeN5zz2TeD60"
    chat_id = "941247256"
    
    print("🔧 Testing Telegram bot connection...")
    print(f"Token: {token[:20]}...")
    print(f"Chat ID: {chat_id}")
    
    try:
        bot = Bot(token=token)
        
        # Test 1: Get bot info
        print("\n✅ Test 1: Getting bot info...")
        me = await bot.get_me()
        print(f"   Bot username: @{me.username}")
        print(f"   Bot name: {me.first_name}")
        
        # Test 2: Send test message
        print("\n✅ Test 2: Sending test message...")
        message = await bot.send_message(
            chat_id=chat_id,
            text="🦈 TEST MESSAGE from shark0locker!\n\nIf you see this, the bot is working correctly! ✅"
        )
        print(f"   Message sent successfully! Message ID: {message.message_id}")
        
        print("\n✅ ALL TESTS PASSED!")
        print("\n📱 Check your Telegram - you should see the test message!")
        print("\n🦈 Your bot is ready to use!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPossible issues:")
        print("1. Invalid bot token")
        print("2. Invalid chat ID")
        print("3. You haven't started a chat with the bot yet")
        print("4. Internet connection issue")
        print("\nTo fix:")
        print("1. Open Telegram")
        print("2. Search for your bot")
        print("3. Click 'Start' button in the bot chat")
        print("4. Run this test again")

if __name__ == "__main__":
    asyncio.run(test_telegram())
