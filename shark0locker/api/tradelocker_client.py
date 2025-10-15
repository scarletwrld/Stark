"""
TradeLocker API Client for shark0locker
High-performance async client for ultra-fast order execution
"""
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class TradeLockerClient:
    """TradeLocker API client with async support"""
    
    def __init__(self, email: str, password: str, server: str, account_number: str, api_url: str = None):
        self.email = email
        self.password = password
        self.server = server
        self.account_number = account_number
        # Use correct API URL for TradeLocker DEMO
        self.base_url = api_url or "https://demo.tradelocker.com/backend-api"
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.account_id: Optional[str] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
        
    async def connect(self):
        """Establish connection and authenticate"""
        self.session = aiohttp.ClientSession()
        await self.authenticate()
        logger.info(f"Connected to TradeLocker - Account: {self.account_number}")
        
    async def disconnect(self):
        """Close connection"""
        if self.session:
            await self.session.close()
        logger.info("Disconnected from TradeLocker")
        
    async def authenticate(self):
        """Authenticate with TradeLocker API"""
        try:
            url = f"{self.base_url}/auth/jwt/token"
            payload = {
                "email": self.email,
                "password": self.password,
                "server": self.server
            }
            
            logger.info(f"Authenticating to TradeLocker API: {url}")
            logger.info(f"Email: {self.email}, Server: {self.server}")
            
            async with self.session.post(url, json=payload) as response:
                logger.info(f"Authentication response status: {response.status}")
                response_text = await response.text()
                logger.info(f"Authentication response: {response_text[:500]}")
                
                # TradeLocker returns 201 (Created) for successful auth
                if response.status in [200, 201]:
                    data = await response.json()
                    self.access_token = data.get("accessToken")
                    self.refresh_token = data.get("refreshToken")
                    self.account_id = data.get("accNum", self.account_number)
                    logger.info(f"✅ Authentication successful! Account: {self.account_id}")
                else:
                    logger.error(f"Authentication failed with status {response.status}")
                    logger.error(f"Response: {response_text}")
                    raise Exception(f"Auth failed (HTTP {response.status}): {response_text[:200]}")
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise
            
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
    async def get_account_info(self) -> Dict[str, Any]:
        """Get account information and balance"""
        try:
            url = f"{self.base_url}/auth/jwt/account/{self.account_id}"
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get account info: {await response.text()}")
                    return {}
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return {}
            
    async def get_balance(self) -> float:
        """Get current account balance"""
        account_info = await self.get_account_info()
        return float(account_info.get("balance", 0.0))
        
    async def get_equity(self) -> float:
        """Get current account equity"""
        account_info = await self.get_account_info()
        return float(account_info.get("equity", 0.0))
        
    async def get_available_symbols(self) -> List[str]:
        """Get list of available trading symbols"""
        try:
            url = f"{self.base_url}/trade/symbols"
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    return [symbol["name"] for symbol in data.get("symbols", [])]
                return []
        except Exception as e:
            logger.error(f"Error getting symbols: {e}")
            return []
            
    async def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed information about a symbol"""
        try:
            url = f"{self.base_url}/trade/symbols/{symbol}"
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {e}")
            return {}
            
    async def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get current ticker data for a symbol"""
        try:
            url = f"{self.base_url}/trade/symbols/{symbol}/quote"
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception as e:
            logger.error(f"Error getting ticker for {symbol}: {e}")
            return {}
            
    async def get_all_tickers(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get ticker data for multiple symbols concurrently"""
        tasks = [self.get_ticker(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        tickers = {}
        for symbol, result in zip(symbols, results):
            if not isinstance(result, Exception) and result:
                tickers[symbol] = result
        return tickers
        
    async def place_market_order(
        self,
        symbol: str,
        side: str,  # "buy" or "sell"
        volume: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Dict[str, Any]:
        """Place a market order - ultra fast execution"""
        try:
            url = f"{self.base_url}/trade/orders"
            payload = {
                "accNum": self.account_id,
                "symbolName": symbol,
                "tradeSide": side.lower(),
                "orderType": "market",
                "qty": volume,
                "timeInForce": "IOC"  # Immediate or Cancel for speed
            }
            
            if stop_loss:
                payload["stopLoss"] = stop_loss
            if take_profit:
                payload["takeProfit"] = take_profit
                
            async with self.session.post(url, json=payload, headers=self._get_headers()) as response:
                if response.status in [200, 201]:
                    result = await response.json()
                    logger.info(f"Order placed: {symbol} {side} {volume} - Order ID: {result.get('orderId')}")
                    return result
                else:
                    error = await response.text()
                    logger.error(f"Order failed: {error}")
                    return {"error": error}
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return {"error": str(e)}
            
    async def close_position(self, position_id: str) -> Dict[str, Any]:
        """Close an open position"""
        try:
            url = f"{self.base_url}/trade/positions/{position_id}/close"
            async with self.session.post(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Position closed: {position_id}")
                    return result
                else:
                    error = await response.text()
                    logger.error(f"Failed to close position: {error}")
                    return {"error": error}
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {"error": str(e)}
            
    async def get_open_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        try:
            url = f"{self.base_url}/trade/accounts/{self.account_id}/positions"
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("positions", [])
                return []
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []
            
    async def close_all_positions(self) -> int:
        """Close all open positions - emergency exit"""
        positions = await self.get_open_positions()
        tasks = [self.close_position(pos["id"]) for pos in positions]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        closed_count = sum(1 for r in results if not isinstance(r, Exception) and "error" not in r)
        logger.info(f"Closed {closed_count}/{len(positions)} positions")
        return closed_count
        
    async def get_order_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get order history"""
        try:
            url = f"{self.base_url}/trade/accounts/{self.account_id}/orders"
            params = {"limit": limit}
            async with self.session.get(url, params=params, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("orders", [])
                return []
        except Exception as e:
            logger.error(f"Error getting order history: {e}")
            return []
