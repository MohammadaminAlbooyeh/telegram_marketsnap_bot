# MarketSnap Telegram Bot

A Telegram bot for real-time price tracking of exchange rates, cryptocurrencies, gold, and oil prices.

## Features

- **Exchange Rates**: USD and EUR to IRR via TGJU.org
- **Cryptocurrencies**: Bitcoin, Ethereum, and top 10 coins via CoinGecko
- **Gold Price**: Iranian gold coin prices
- **Oil Prices**: WTI and Brent crude oil prices via Yahoo Finance
- **Price Alerts**: Set alerts for price thresholds
- **Inline Menu**: Interactive keyboard for easy navigation

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your `BOT_TOKEN`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome menu |
| `/bitcoin` | Bitcoin price |
| `/ethereum` | Ethereum price |
| `/crypto` | Top 10 cryptocurrencies |
| `/rates` | USD/EUR exchange rates |
| `/usd` | USD to IRR rate |
| `/eur` | EUR to IRR rate |
| `/gold` | Gold coin price |
| `/oil` | WTI and Brent oil prices |
| `/alerts` | List your alerts |
| `/setalert` | Create a new alert |

## Project Structure

```
.
├── main.py
├── requirements.txt
├── .env.example
├── app/
│   ├── core/         # Config, database, logger
│   ├── handlers/     # Telegram command handlers
│   ├── services/     # Business logic and API calls
│   ├── scrapers/     # Alternative data scrapers
│   ├── models/       # Data models
│   ├── utils/        # Helpers and formatters
│   └── middleware/   # Auth and logging middleware
└── tests/            # Unit tests
```

## License

MIT
