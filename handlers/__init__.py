"""Handler modules for Telegram bot."""

from .start import start
from .market_handlers import (
    rates,
    usd,
    eur,
    gold,
    oil,
)
from .stock_handlers import bitcoin, ethereum, crypto, alerts, setalert
from .help import button_callback, error_handler

__all__ = [
    "start",
    "rates",
    "usd",
    "eur",
    "gold",
    "oil",
    "bitcoin",
    "ethereum",
    "crypto",
    "alerts",
    "setalert",
    "button_callback",
    "error_handler",
]