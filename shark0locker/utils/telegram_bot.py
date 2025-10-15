"""
Telegram Bot Integration for shark0locker
Remote control and notifications
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import io
from PIL import Image, ImageDraw, ImageFont
import random

logger = logging.getLogger(__name__)

class TelegramBotController:
    """Telegram bot for controlling shark0locker"""
    
    def __init__(self, token: str, chat_id: str, trading_system):
        self.token = token
        self.chat_id = chat_id
        self.trading_system = trading_system
        self.bot = Bot(token=token)
        self.app = None
        self.notification_task = None
        
    async def start(self):
        """Start the Telegram bot"""
        try:
            self.app = Application.builder().token(self.token).build()
            
            # Register command handlers
            self.app.add_handler(CommandHandler("start", self.cmd_start))
            self.app.add_handler(CommandHandler("stop", self.cmd_stop))
            self.app.add_handler(CommandHandler("status", self.cmd_status))
            self.app.add_handler(CommandHandler("stats", self.cmd_stats))
            self.app.add_handler(CommandHandler("balance", self.cmd_balance))
            self.app.add_handler(CommandHandler("trades", self.cmd_trades))
            self.app.add_handler(CommandHandler("closeall", self.cmd_close_all))
            
            # Start bot in background
            await self.app.initialize()
            await self.app.start()
            
            # Start periodic notifications
            self.notification_task = asyncio.create_task(self.send_periodic_updates())
            
            # Send startup message
            await self.send_message("🦈 shark0locker is ONLINE and ready to hunt! 🦈")
            
            logger.info("Telegram bot started")
            
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            
    async def stop(self):
        """Stop the Telegram bot"""
        try:
            if self.notification_task:
                self.notification_task.cancel()
                
            if self.app:
                await self.app.stop()
                await self.app.shutdown()
                
            await self.send_message("🦈 shark0locker is going offline. See you soon! 🦈")
            logger.info("Telegram bot stopped")
            
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")
            
    async def send_message(self, text: str):
        """Send a message to the user"""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    async def send_photo(self, photo: bytes, caption: str = ""):
        """Send a photo to the user"""
        try:
            await self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=caption)
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            
    async def send_pnl_update(self, performance: Dict[str, Any]):
        """Send PNL update with visualization"""
        try:
            # Generate PNL chart/image
            image = self.generate_pnl_image(performance)
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Create caption
            caption = f"""
🦈 SHARK FEEDING UPDATE 🦈
💰 Balance: ${performance.get('current_balance', 0):.2f}
📈 PNL: ${performance.get('total_pnl', 0):.2f} ({performance.get('roi_percent', 0):.2f}%)
⏱️ Hourly: ${performance.get('hourly_pnl', 0):.2f}
🎯 Win Rate: {performance.get('win_rate', 0):.2f}%
            """.strip()
            
            await self.send_photo(img_bytes, caption)
            
        except Exception as e:
            logger.error(f"Error sending PNL update: {e}")
            
    def generate_pnl_image(self, performance: Dict[str, Any]) -> Image:
        """Generate PNL visualization image"""
        try:
            # Create image
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color='#1a1a2e')
            draw = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default
            try:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw shark emoji (text)
            draw.text((350, 50), "🦈", fill='#00d9ff', font=font_large)
            
            # Draw performance metrics
            y_pos = 150
            metrics = [
                f"Balance: ${performance.get('current_balance', 0):.2f}",
                f"PNL: ${performance.get('total_pnl', 0):.2f}",
                f"ROI: {performance.get('roi_percent', 0):.2f}%",
                f"Win Rate: {performance.get('win_rate', 0):.2f}%",
                f"Trades: {performance.get('total_trades', 0)}"
            ]
            
            for metric in metrics:
                color = '#00ff00' if 'PNL' in metric or 'ROI' in metric else '#ffffff'
                draw.text((50, y_pos), metric, fill=color, font=font_medium)
                y_pos += 70
            
            # Draw shark fin pattern at bottom
            for i in range(5):
                x = 100 + i * 150
                points = [(x, 550), (x + 50, 450), (x + 100, 550)]
                draw.polygon(points, fill='#0066cc')
            
            return img
            
        except Exception as e:
            logger.error(f"Error generating PNL image: {e}")
            # Return simple blank image
            return Image.new('RGB', (800, 600), color='#1a1a2e')
            
    async def send_periodic_updates(self):
        """Send periodic performance updates"""
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                if self.trading_system and self.trading_system.is_running:
                    performance = await self.trading_system.get_performance()
                    if performance:
                        await self.send_pnl_update(performance)
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic updates: {e}")
                
    # Command handlers
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start trading command"""
        try:
            if self.trading_system:
                await self.trading_system.start()
                await update.message.reply_text("🦈 shark0locker STARTED! Hunting for profits... 🦈")
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop trading command"""
        try:
            if self.trading_system:
                await self.trading_system.stop()
                await update.message.reply_text("🛑 shark0locker STOPPED! Taking a break... 🛑")
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get system status"""
        try:
            if self.trading_system:
                status = await self.trading_system.get_status()
                await update.message.reply_text(f"📊 Status:\n{status}")
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get performance statistics"""
        try:
            if self.trading_system:
                stats = await self.trading_system.get_performance_summary()
                await update.message.reply_text(stats)
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get current balance"""
        try:
            if self.trading_system:
                balance = await self.trading_system.get_balance()
                equity = await self.trading_system.get_equity()
                await update.message.reply_text(
                    f"💰 Balance: ${balance:.2f}\n"
                    f"📈 Equity: ${equity:.2f}"
                )
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_trades(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get recent trades"""
        try:
            if self.trading_system:
                trades = await self.trading_system.get_recent_trades(limit=10)
                if trades:
                    trade_text = "📋 Recent Trades:\n\n"
                    for trade in trades:
                        trade_text += (
                            f"• {trade['symbol']} {trade['direction']} "
                            f"@ {trade['entry_price']:.5f} "
                            f"PNL: ${trade.get('pnl', 0):.2f}\n"
                        )
                    await update.message.reply_text(trade_text)
                else:
                    await update.message.reply_text("No recent trades")
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            
    async def cmd_close_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Close all positions"""
        try:
            if self.trading_system:
                count = await self.trading_system.close_all_positions()
                await update.message.reply_text(f"✅ Closed {count} positions")
            else:
                await update.message.reply_text("❌ Trading system not initialized")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
