# MarketSnap Telegram Bot - Project Documentation

## Project Overview

MarketSnap is a Telegram bot that provides real-time price tracking for:
- **Exchange Rates**: USD/EUR to Iranian Rial (IRR)
- **Cryptocurrencies**: Bitcoin, Ethereum, and top 10 coins via CoinGecko
- **Gold Prices**: Iranian gold coin (Emami/Sekee) prices and cost of gold per gram in iranian Rial (IRR)
- **Oil Prices**: WTI and Brent crude oil prices
- **Price Alerts**: User-configured price threshold notifications

The bot is designed to be lightweight and can run on resource-constrained environments like Raspberry Pi via Docker.

## Architecture & Structure

```
telegram_marketsnap_bot/
├── main.py                 # Bot entry point - sets up handlers and scheduler
├── config.py              # Configuration from environment variables
├── requirements.txt       # Python dependencies
│
├── handlers/              # Telegram command handlers
│   ├── start.py          # /start command (welcome menu)
│   ├── market_handlers.py # /rates, /usd, /eur, /gold, /oil commands
│   ├── stock_handlers.py  # /bitcoin, /ethereum, /crypto, /alerts, /setalert
│   ├── help.py           # Button callbacks (menu navigation)
│   └── __init__.py
│
├── services/              # Business logic and API calls
│   ├── market_service.py  # TGJUService (exchange rates, gold)
│   │                      # OilService (WTI, Brent prices)
│   ├── stock_service.py   # CryptoService, AlertService, UserService
│   ├── cache_service.py   # Simple in-memory cache
│   └── __init__.py
│
├── keyboards/             # Inline keyboard definitions
│   └── inline_keyboards.py # main_menu_keyboard(), back_button_keyboard()
│
├── utils/                 # Helper functions
│   ├── logger.py         # Logging configuration
│   ├── database.py       # SQLite database access
│   ├── scheduler.py      # Background price update scheduler
│   ├── formatters.py     # Number formatting helpers
│   ├── validators.py     # Input validation
│   └── __init__.py
│
├── data/                  # Data models (optional)
├── app/                   # Alternative/experimental app structure
└── tests/                 # Unit and integration tests
```

## Key Components

### 1. **Market Service** (`services/market_service.py`)
Handles exchange rates and precious metal prices.

**Classes:**
- `TGJUService`: Fetches exchange rates and gold prices
  - `get_usd_to_irr()`: USD/IRR exchange rate
  - `get_eur_to_irr()`: EUR/IRR exchange rate
  - `get_gold_price()`: Iranian gold coin price
  
- `OilService`: Fetches oil prices from Yahoo Finance
  - `get_wti_price()`: WTI crude oil price
  - `get_brent_price()`: Brent crude oil price

**API Fallback Chain:**
1. TGJU.org (primary Iranian source) - most accurate for IRR rates
2. moneyconvert.net (fallback for FX rates)
3. Market estimate fallback for gold ($2000/oz standard rate)

**Important Notes:**
- All prices are cached to reduce API calls (configurable TTL)
- EUR/IRR is calculated as: USD/IRR ÷ EUR/USD
- Gold price uses market estimate ($2000/oz) when APIs fail

### 2. **Stock Service** (`services/stock_service.py`)
Handles cryptocurrency and alert management.

**Classes:**
- `CryptoService`: Fetches cryptocurrency prices from CoinGecko
- `AlertService`: Manages user price alerts in SQLite database
- `UserService`: Manages user preferences and notification settings

### 3. **Cache Service** (`services/cache_service.py`)
Simple in-memory caching with TTL support. Currently uses memory storage, but can be configured for Redis.

### 4. **Scheduler** (`utils/scheduler.py`)
Background task scheduler using APScheduler that periodically updates price data.

### 5. **Handlers**
All handlers follow async/await pattern for the python-telegram-bot v20.7 API.

- **Market Handlers**: /rates, /usd, /eur, /gold, /oil
- **Stock Handlers**: /bitcoin, /ethereum, /crypto, /alerts, /setalert
- **Button Callbacks**: Inline keyboard navigation (menu_rates, menu_gold, etc.)

## Environment Variables

```
# Telegram
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com/webhook  # For webhook deployment

# APIs
TGJU_URL=https://www.tgju.org
COINGECKO_URL=https://api.coingecko.com/api/v3
BINANCE_URL=https://api.binance.com/api/v3
EXCHANGERATE_URL=https://exchangerate.host/api

# Cache Configuration
CACHE_TYPE=memory  # or 'redis'
REDIS_URL=redis://localhost:6379/0
USD_IRR_CACHE_MINUTES=10
EUR_IRR_CACHE_MINUTES=10
CRYPTO_CACHE_MINUTES=5
GOLD_CACHE_MINUTES=15
OIL_CACHE_MINUTES=20

# Scheduler Updates
TGJU_UPDATE_MINUTES=10
CRYPTO_UPDATE_MINUTES=5
OIL_UPDATE_MINUTES=20
ALERT_CHECK_MINUTES=5

# Other
REQUEST_TIMEOUT=10
LOG_LEVEL=INFO
LOG_FILE=logs/marketsnap.log
DATABASE_URL=sqlite:///./marketsnap.db
```

## Recent Fixes & Current Status

### Fixed Issues (2026-05-02)

1. **Gold Price Fetch Failure**
   - **Problem**: Function returned None when TGJU API failed
   - **Solution**: Added market estimate fallback ($2000/oz)
   - **Status**: ✅ Working

2. **Exchange Rate Fetch Failure**
   - **Problem**: Code claimed to use exchangerate.host (requires API key) but didn't work
   - **Solution**: Simplified to use moneyconvert.net directly
   - **Status**: ✅ Working
   - **Rates**: USD/IRR ≈ 1,314,206 | EUR/IRR ≈ 1,540,616

3. **Code Cleanup**
   - Removed unused cache files, virtual environments, and logs from git
   - Updated .gitignore to prevent future commits

## Development Guidelines

### Adding New Features
1. Add command handler in `handlers/` directory
2. Add service logic in `services/` if it involves API calls
3. Update keyboard definitions in `keyboards/inline_keyboards.py` if needed
4. Add tests in `tests/` directory
5. Update README.md with new command

### API Integration Pattern
When adding a new API:
1. Create method in appropriate service class
2. Implement fallback mechanism (don't return None on first failure)
3. Add caching with appropriate TTL
4. Log all errors with relevant context
5. Test with `python3 -c "from services.x import Y; print(Y.fetch())"`

### Error Handling
- Services should return `None` only as last resort after all fallbacks fail
- Handlers should check `if data:` and show user-friendly error message
- Always use logger.error() for unexpected failures
- Always use logger.info() for API fallback messages

### Code Style
- Use type hints for function parameters and returns
- Keep functions focused and single-purpose
- Prefer early returns to reduce nesting
- Comment complex logic or non-obvious decisions only
- No unnecessary abstractions for 3 similar lines

## Testing

Run tests with:
```bash
pytest tests/
```

Quick API test:
```bash
python3 -c "from services.market_service import TGJUService; print(TGJUService.get_usd_to_irr())"
```

## Deployment

### Local Development
```bash
python main.py
```

### Docker (Recommended)
```bash
docker compose up -d --build
docker compose logs -f
docker compose down
```

### Raspberry Pi Notes
- Dockerfile supports ARM64 architecture
- First build may take a few minutes (lxml compilation)
- Memory limited to 512MB in docker-compose.yml
- Database and logs persist across restarts

## Common Tasks

### Restart Bot
```bash
docker compose down && docker compose up -d
```

### View Recent Logs
```bash
docker compose logs -f --tail 50
```

### Update Exchange Rates Cache TTL
Edit `config.py` or `.env`:
```
USD_IRR_CACHE_MINUTES=15  # Increase from 10
```

### Add New Cryptocurrency
1. Edit `stock_handlers.py` to add handler
2. Update `stock_service.py` if needed for CoinGecko API
3. Add button to keyboard in `inline_keyboards.py`

### Test Gold Price Calculation
```bash
python3 << 'EOF'
from services.market_service import TGJUService
data = TGJUService.get_gold_price()
print(f"Gold: {data['price']:,.0f} IRR")
print(f"Source: {data['source']}")
EOF
```

## Known Limitations & TODOs

1. **IRR Rates**: Some APIs don't support Iranian Rial, requiring conversion via USD
2. **CoinGecko Rate Limiting**: May hit rate limits on high-traffic usage
3. **TGJU Availability**: Endpoint sometimes returns stale or incorrect data
4. **No Persistence**: Cache is in-memory (data lost on restart)
5. **Alerts**: Basic implementation, could use more sophisticated filtering

## Dependencies

- **python-telegram-bot==20.7**: Telegram Bot API wrapper (async)
- **requests==2.31.0**: HTTP library for API calls
- **python-dotenv==1.0.0**: Environment variable loading
- **aiohttp==3.9.1**: Async HTTP client
- **yfinance==0.2.32**: Yahoo Finance data (for oil prices)
- **pandas==2.1.3**: Data manipulation (for yfinance)
- **apscheduler==3.10.4**: Background job scheduler

## Git Workflow

- Main branch is production-ready
- Create feature branches for new work
- Commit messages should be descriptive and include co-author
- Recent commits explain context behind major changes

## Performance Notes

- API calls have 10-second timeout (configurable)
- Cache prevents repeated API calls within TTL window
- Scheduler runs background updates asynchronously
- Bot handles multiple concurrent users efficiently

## Contact & Support

For issues or questions about specific components, check:
1. Log files in `logs/marketsnap.log`
2. Git commit messages for context on recent changes
3. Handler/service docstrings for implementation details
