from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Return main menu inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("💱 Exchange Rates", callback_data="menu_rates")],
        [InlineKeyboardButton("₿ Cryptocurrencies", callback_data="menu_crypto")],
        [InlineKeyboardButton("🥇 Gold Price", callback_data="menu_gold")],
        [InlineKeyboardButton("🛢️ Oil Prices", callback_data="menu_oil")],
        [InlineKeyboardButton("🔔 My Alerts", callback_data="menu_alerts")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_button_keyboard() -> InlineKeyboardMarkup:
    """Return keyboard with back button."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")]
    ])
