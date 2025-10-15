#!/usr/bin/env python3
"""
Test TradeLocker API endpoints to find the correct one
"""
import asyncio
import aiohttp

# Your credentials
EMAIL = "tiggysurf@gmail.com"
PASSWORD = "!2e375iW"
SERVER = "GATESFX"
ACCOUNT = "1550788"

# Possible API endpoints
ENDPOINTS_TO_TRY = [
    {
        "name": "Demo Backend API",
        "base": "https://demo.tradelocker.com/backend-api",
        "auth": "/auth/jwt/token"
    },
    {
        "name": "Demo API",
        "base": "https://demo.tradelocker.com",
        "auth": "/auth/jwt/token"
    },
    {
        "name": "Demo API v1",
        "base": "https://demo.tradelocker.com/api/v1",
        "auth": "/auth/jwt/token"
    },
    {
        "name": "API Demo subdomain",
        "base": "https://api-demo.tradelocker.com",
        "auth": "/auth/jwt/token"
    },
    {
        "name": "Main API",
        "base": "https://api.tradelocker.com",
        "auth": "/auth/jwt/token"
    },
]

async def test_endpoint(session, endpoint):
    """Test a single endpoint"""
    url = endpoint["base"] + endpoint["auth"]
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "server": SERVER
    }
    
    print(f"\n{'='*70}")
    print(f"Testing: {endpoint['name']}")
    print(f"URL: {url}")
    print(f"{'='*70}")
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
            status = response.status
            text = await response.text()
            
            print(f"Status: {status}")
            print(f"Response: {text[:500]}")
            
            if status == 200:
                print("✅ SUCCESS! This endpoint works!")
                try:
                    data = await response.json()
                    if "accessToken" in data or "access_token" in data:
                        print("✅ Got access token!")
                        return endpoint, True
                except:
                    pass
            elif status == 404:
                print("❌ 404 - Endpoint not found")
            elif status == 401:
                print("⚠️  401 - Authentication failed (but endpoint exists)")
            else:
                print(f"⚠️  Status {status}")
                
            return endpoint, False
            
    except asyncio.TimeoutError:
        print("❌ Timeout")
        return endpoint, False
    except Exception as e:
        print(f"❌ Error: {e}")
        return endpoint, False

async def main():
    """Test all endpoints"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         TRADELOCKER API ENDPOINT FINDER                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("Testing TradeLocker API endpoints...")
    print(f"Account: {ACCOUNT}")
    print(f"Server: {SERVER}")
    print()
    
    async with aiohttp.ClientSession() as session:
        results = []
        
        for endpoint in ENDPOINTS_TO_TRY:
            result = await test_endpoint(session, endpoint)
            results.append(result)
            await asyncio.sleep(0.5)  # Be nice to the API
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        working = [r for r in results if r[1]]
        if working:
            print("\n✅ Working endpoints found:")
            for endpoint, _ in working:
                print(f"   - {endpoint['name']}: {endpoint['base']}{endpoint['auth']}")
        else:
            print("\n❌ No working endpoints found")
            print("\nPossible issues:")
            print("1. Incorrect credentials")
            print("2. Demo account not activated")
            print("3. Server name incorrect")
            print("4. Different API structure")
            print("\nRecommendation: Contact TradeLocker support for API documentation")

if __name__ == "__main__":
    asyncio.run(main())
