"""
Terminal UI for shark0locker
Live dashboard with rich terminal graphics
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

logger = logging.getLogger(__name__)

class TerminalUI:
    """Rich terminal UI for shark0locker"""
    
    def __init__(self, trading_system):
        self.trading_system = trading_system
        self.console = Console()
        self.live: Optional[Live] = None
        self.is_running = False
        self.update_task = None
        
    async def start(self):
        """Start the terminal UI"""
        self.is_running = True
        self.update_task = asyncio.create_task(self.update_loop())
        logger.info("Terminal UI started")
        
    async def stop(self):
        """Stop the terminal UI"""
        self.is_running = False
        if self.update_task:
            self.update_task.cancel()
        if self.live:
            self.live.stop()
        logger.info("Terminal UI stopped")
        
    async def update_loop(self):
        """Main update loop for terminal UI"""
        with Live(self.generate_layout(), refresh_per_second=2, console=self.console) as live:
            self.live = live
            while self.is_running:
                try:
                    layout = self.generate_layout()
                    live.update(layout)
                    await asyncio.sleep(0.5)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Terminal UI error: {e}")
                    
    def generate_layout(self) -> Layout:
        """Generate the terminal layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        # Header
        layout["header"].update(self.create_header())
        
        # Left panel - System status and agents
        layout["left"].split_column(
            Layout(name="status", size=12),
            Layout(name="agents")
        )
        layout["left"]["status"].update(self.create_status_panel())
        layout["left"]["agents"].update(self.create_agents_panel())
        
        # Right panel - Performance and trades
        layout["right"].split_column(
            Layout(name="performance", size=15),
            Layout(name="trades")
        )
        layout["right"]["performance"].update(self.create_performance_panel())
        layout["right"]["trades"].update(self.create_trades_panel())
        
        # Footer
        layout["footer"].update(self.create_footer())
        
        return layout
        
    def create_header(self) -> Panel:
        """Create header panel"""
        shark = "🦈" * 10
        title = Text(f"{shark}\n  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT  \n{shark}", justify="center")
        title.stylize("bold cyan")
        return Panel(title, border_style="bright_blue", box=box.DOUBLE)
        
    def create_status_panel(self) -> Panel:
        """Create system status panel"""
        try:
            is_running = self.trading_system.is_running
            
            status_text = Text()
            status_text.append("System Status: ", style="bold")
            if is_running:
                status_text.append("🟢 HUNTING", style="bold green")
            else:
                status_text.append("🔴 STOPPED", style="bold red")
            
            status_text.append(f"\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            status_text.append(f"Account: {self.trading_system.config.tradelocker.account_number}\n")
            status_text.append(f"Server: {self.trading_system.config.tradelocker.server}\n")
            
            # Queue status
            status_text.append(f"\n📊 Queues:\n", style="bold yellow")
            status_text.append(f"  Opportunities: {self.trading_system.message_queue.qsize()}\n")
            status_text.append(f"  Signals: {self.trading_system.signal_queue.qsize()}\n")
            
            return Panel(status_text, title="[bold]System Status[/bold]", border_style="green")
        except Exception as e:
            return Panel(f"Error: {e}", title="System Status", border_style="red")
            
    def create_agents_panel(self) -> Panel:
        """Create agents status panel"""
        try:
            table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
            table.add_column("Agent", style="cyan")
            table.add_column("Status", justify="center")
            table.add_column("Tasks", justify="right")
            table.add_column("Failed", justify="right")
            
            all_agents = (
                self.trading_system.scanner_agents +
                self.trading_system.analyzer_agents +
                self.trading_system.executor_agents +
                [self.trading_system.performance_monitor]
            )
            
            for agent in all_agents:
                stats = agent.get_stats()
                status = "🟢" if stats["running"] else "🔴"
                table.add_row(
                    stats["name"],
                    status,
                    str(stats["tasks_completed"]),
                    str(stats["tasks_failed"])
                )
            
            return Panel(table, title="[bold]Agent Workforce[/bold]", border_style="magenta")
        except Exception as e:
            return Panel(f"Error: {e}", title="Agents", border_style="red")
            
    def create_performance_panel(self) -> Panel:
        """Create performance panel"""
        try:
            if not self.trading_system.performance_monitor:
                return Panel("Performance monitor not available", title="Performance", border_style="yellow")
            
            # This would normally be async, but for UI we use cached data
            # In production, you'd want to cache the last report
            perf_text = Text()
            perf_text.append("💰 FINANCIAL STATS\n\n", style="bold green")
            perf_text.append("Balance: Loading...\n")
            perf_text.append("Equity: Loading...\n")
            perf_text.append("PNL: Loading...\n")
            perf_text.append("ROI: Loading...\n\n")
            
            perf_text.append("📊 TRADING STATS\n\n", style="bold yellow")
            perf_text.append("Total Trades: Loading...\n")
            perf_text.append("Win Rate: Loading...\n")
            perf_text.append("Hourly PNL: Loading...\n")
            
            return Panel(perf_text, title="[bold]Performance[/bold]", border_style="yellow")
        except Exception as e:
            return Panel(f"Error: {e}", title="Performance", border_style="red")
            
    def create_trades_panel(self) -> Panel:
        """Create recent trades panel"""
        try:
            table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE_HEAD)
            table.add_column("Symbol", style="cyan")
            table.add_column("Side", justify="center")
            table.add_column("Entry", justify="right")
            table.add_column("PNL", justify="right")
            table.add_column("Status")
            
            recent_trades = self.trading_system.trade_log[-10:] if self.trading_system.trade_log else []
            
            for trade in reversed(recent_trades):
                symbol = trade.get("symbol", "")
                direction = "🟢 BUY" if trade.get("direction") == "buy" else "🔴 SELL"
                entry = f"{trade.get('entry_price', 0):.5f}"
                pnl = trade.get("pnl", 0)
                pnl_str = f"${pnl:.2f}" if pnl else "-"
                pnl_style = "green" if pnl > 0 else "red" if pnl < 0 else "white"
                status = trade.get("status", "open")
                
                table.add_row(
                    symbol,
                    direction,
                    entry,
                    Text(pnl_str, style=pnl_style),
                    status
                )
            
            if not recent_trades:
                table.add_row("No trades yet", "-", "-", "-", "-")
            
            return Panel(table, title="[bold]Recent Trades[/bold]", border_style="cyan")
        except Exception as e:
            return Panel(f"Error: {e}", title="Trades", border_style="red")
            
    def create_footer(self) -> Panel:
        """Create footer panel"""
        footer_text = Text("🦈 The shark is hunting... Press Ctrl+C to stop", justify="center")
        footer_text.stylize("italic bright_black")
        return Panel(footer_text, border_style="bright_black")
        
    def print_startup_banner(self):
        """Print startup banner"""
        self.console.clear()
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🦈  SHARK0LOCKER - HIGH FREQUENCY TRADING BOT  🦈         ║
║                                                               ║
║         Aggressive • Intelligent • Profitable                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
        self.console.print("\n[bold yellow]Initializing multi-agent workforce...[/bold yellow]\n")
