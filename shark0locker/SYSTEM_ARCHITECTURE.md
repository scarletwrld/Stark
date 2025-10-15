# 🦈 SHARK0LOCKER - System Architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SHARK0LOCKER SYSTEM                          │
│                  High-Frequency Trading Bot                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      CONTROL LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Telegram Bot                    Terminal UI                    │
│  ┌──────────────┐               ┌──────────────┐               │
│  │ Commands     │               │ Live         │               │
│  │ /start       │               │ Dashboard    │               │
│  │ /stop        │               │ Rich UI      │               │
│  │ /status      │               │ Real-time    │               │
│  │ /stats       │               │ Updates      │               │
│  └──────────────┘               └──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                    Trading System                               │
│  ┌──────────────────────────────────────────────────┐          │
│  │ • Manages all agents                              │          │
│  │ • Coordinates message/signal queues               │          │
│  │ • Handles system start/stop                       │          │
│  │ • Provides unified interface                      │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT WORKFORCE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────────┐  │
│  │  Scanner     │      │  Scanner     │     │  Scanner     │  │
│  │  Agent 1     │      │  Agent 2     │     │  Agent 3     │  │
│  └──────────────┘      └──────────────┘     └──────────────┘  │
│         │                     │                     │          │
│         └─────────────────────┴─────────────────────┘          │
│                              ↓                                  │
│                      [Message Queue]                            │
│                    (Opportunities)                              │
│                              ↓                                  │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐           │
│  │Analyz│  │Analyz│  │Analyz│  │Analyz│  │Analyz│           │
│  │er 1  │  │er 2  │  │er 3  │  │er 4  │  │er 5  │           │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘           │
│      │         │         │         │         │                │
│      └─────────┴─────────┴─────────┴─────────┘                │
│                        ↓                                        │
│                  [Signal Queue]                                 │
│               (Trading Signals)                                 │
│                        ↓                                        │
│            ┌──────────────┐  ┌──────────────┐                 │
│            │  Executor    │  │  Executor    │                 │
│            │  Agent 1     │  │  Agent 2     │                 │
│            └──────────────┘  └──────────────┘                 │
│                        ↓                                        │
│                  [Trade Log]                                    │
│                        ↓                                        │
│            ┌──────────────────────┐                            │
│            │ Performance Monitor  │                            │
│            └──────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│              TradeLocker API Client                             │
│  ┌──────────────────────────────────────────────────┐          │
│  │ • Authentication (JWT)                            │          │
│  │ • Market data fetching                            │          │
│  │ • Order execution                                 │          │
│  │ • Position management                             │          │
│  │ • Account information                             │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
├─────────────────────────────────────────────────────────────────┤
│  TradeLocker Platform          Telegram API                     │
│  ┌──────────────┐             ┌──────────────┐                │
│  │ Market Data  │             │ Bot Messages │                │
│  │ Order Exec   │             │ Notifications│                │
│  │ Positions    │             │ Commands     │                │
│  └──────────────┘             └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Market Scanning Flow
```
TradeLocker API → Scanner Agents → Price Analysis
                        ↓
                  Velocity Calculation
                        ↓
                  Opportunity Detection
                        ↓
                  Message Queue
```

### 2. Analysis Flow
```
Message Queue → Analyzer Agents → Multi-Factor Analysis
                     ↓
              Momentum Analysis
              Volatility Analysis
              Spread Analysis
              Velocity Analysis
              Pattern Analysis
                     ↓
              Win Probability Calculation
                     ↓
              Filter (>98% only)
                     ↓
              Signal Queue
```

### 3. Execution Flow
```
Signal Queue → Executor Agents → Position Size Calculation
                    ↓
              Market Order Placement
                    ↓
              Stop Loss / Take Profit
                    ↓
              Trade Log
                    ↓
              Position Monitoring
```

### 4. Monitoring Flow
```
Trade Log → Performance Monitor → Metrics Calculation
                 ↓
           Balance Tracking
                 ↓
           PNL Calculation
                 ↓
           Reports Generation
                 ↓
     ┌───────────┴───────────┐
     ↓                       ↓
Telegram Updates      Terminal UI Updates
```

## Component Details

### Scanner Agent
**Purpose**: Hunt for trading opportunities
- Fetches ticker data for all pairs
- Calculates price velocity
- Detects momentum changes
- Runs every 100ms
- Outputs: Opportunities with score

### Analyzer Agent
**Purpose**: Deep analysis of opportunities
- Receives opportunities from queue
- Performs multi-factor analysis
- Calculates composite win probability
- Filters for high-probability signals (98%+)
- Outputs: Trading signals with entry/exit levels

### Executor Agent
**Purpose**: Execute trades instantly
- Receives signals from queue
- Calculates optimal position size (full portfolio)
- Places market orders via API
- Manages active positions
- Closes profitable positions quickly

### Performance Monitor
**Purpose**: Track all metrics
- Monitors account balance/equity
- Tracks all trades
- Calculates PNL, ROI, win rate
- Generates performance reports
- Sends periodic updates

### Trading System
**Purpose**: Orchestrate everything
- Initializes all components
- Manages agent lifecycle
- Coordinates communication
- Provides unified interface
- Handles start/stop/shutdown

### Telegram Bot
**Purpose**: Remote control interface
- Processes user commands
- Sends notifications
- Generates PNL visualizations
- Provides system status
- Enables emergency actions

### Terminal UI
**Purpose**: Local monitoring interface
- Displays live dashboard
- Shows all agents status
- Updates performance metrics
- Displays recent trades
- Beautiful Rich UI

## Technical Architecture

### Concurrency Model
- **Async/Await**: All I/O operations are asynchronous
- **Event Loop**: Single event loop manages all agents
- **Queues**: AsyncIO queues for inter-agent communication
- **Tasks**: Each agent runs as an independent task
- **Parallelism**: Multiple agents run concurrently

### Communication Patterns
- **Producer-Consumer**: Scanners → Analyzers → Executors
- **Publish-Subscribe**: Performance Monitor broadcasts updates
- **Command Pattern**: Telegram bot sends commands
- **Observer Pattern**: Terminal UI observes trading system

### Error Handling
- **Try-Except**: All critical operations wrapped
- **Graceful Degradation**: Agents continue on non-fatal errors
- **Logging**: All errors logged with context
- **Recovery**: Automatic reconnection and retry logic
- **Emergency Stop**: Can halt everything safely

### State Management
- **Shared State**: Trade log, queues, API client
- **Agent State**: Each agent tracks own statistics
- **Immutable Messages**: Queue messages are read-only
- **Thread-Safe**: AsyncIO provides inherent safety

## Performance Characteristics

### Latency
- Market scan: ~50-100ms
- Analysis: ~10-50ms per opportunity
- Order execution: ~100-500ms
- Total opportunity-to-order: ~200-700ms

### Throughput
- Scanner: 10-30 opportunities/second
- Analyzer: 100+ opportunities/second (5 agents)
- Executor: 10+ orders/second (2 agents)
- Overall: Limited by high-probability filtering

### Scalability
- **Horizontal**: Add more agents
- **Vertical**: Faster hardware helps
- **Bottleneck**: TradeLocker API rate limits
- **Optimal**: Current configuration is well-balanced

## Security Architecture

### Credentials
- Stored in config files (not version controlled)
- API tokens in memory only
- No credentials in logs

### API Security
- JWT authentication
- HTTPS only
- Token refresh mechanism
- Rate limiting compliance

### Risk Controls
- Position size limits
- Stop loss on all trades
- Emergency close all function
- Maximum concurrent trades limit

## Deployment Architecture

### File Organization
```
shark0locker/
├── agents/          # Agent modules
├── api/             # API clients
├── config/          # Configuration
├── core/            # Core system
├── utils/           # Utilities
├── data/            # Runtime data
├── logs/            # Log files
└── main.py          # Entry point
```

### Process Model
- Single Python process
- AsyncIO event loop
- Multiple concurrent tasks
- Graceful shutdown handling

### Dependencies
- External: TradeLocker API, Telegram API
- Python: aiohttp, python-telegram-bot, rich, numpy, pandas, Pillow
- System: Python 3.9+, internet connection

## Monitoring & Observability

### Metrics Tracked
- System: Agent status, queue sizes, task counts
- Trading: Balance, equity, PNL, ROI, win rate
- Performance: Trade count, avg profit/loss, hourly PNL
- Health: Error rates, API latency, uptime

### Logging Levels
- DEBUG: Detailed operation logs
- INFO: General system activities
- WARNING: Non-fatal issues
- ERROR: Errors requiring attention
- CRITICAL: System-threatening issues

### Alerting
- Telegram: All critical events
- Logs: All events recorded
- Terminal: Real-time visual feedback

## Resilience & Reliability

### Fault Tolerance
- Agent failure: Other agents continue
- API error: Retry logic and reconnection
- Network issues: Automatic recovery
- Data corruption: Validation and sanitization

### Disaster Recovery
- Emergency stop: `/closeall` command
- Manual intervention: Stop system, close positions
- State recovery: System can restart safely
- Data backup: Trade log persisted

### Availability
- 24/7 Operation: Designed for continuous running
- Auto-reconnect: Handles temporary disconnections
- Health checks: Self-monitoring
- Graceful shutdown: Clean exit on signals

---

This architecture enables shark0locker to hunt the markets with speed, intelligence, and efficiency! 🦈💰
