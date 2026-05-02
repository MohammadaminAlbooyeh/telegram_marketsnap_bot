# Help handlers - callback and error handling
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from services.market_service import TGJUService, OilService
from services.stock_service import CryptoService, AlertService, UserService
from keyboards.inline_keyboards import main_menu_keyboard, back_button_keyboard

MENU_TEXT = (
    "👋 Welcome!\n\n"
    "📊 MarketSnap Bot - Real-time Price Tracker\n\n"
    "Get instant updates on:\n"
    "• 💱 Exchange Rates (USD, EUR to IRR)\n"
    "• 🥇 Gold & Coin Prices\n"
    "• ₿ Cryptocurrency Prices\n"
    "• 🛢️ Oil Prices (WTI, Brent)\n"
    "• 🔔 Price Alerts\n\n"
    "Choose an option below:"
)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()

    callback = query.data
    user_id = update.effective_user.id
    back_kb = back_button_keyboard()

    if callback == "menu_rates":
        usd_data = TGJUService.get_usd_to_irr()
        eur_data = TGJUService.get_eur_to_irr()
        if usd_data and eur_data:
            text = (
                "💱 Current Exchange Rates\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🇺🇸 USD → IRR\n1 USD = {usd_data['price']:,.0f} IRR\n\n"
                f"🇪🇺 EUR → IRR\n1 EUR = {eur_data['price']:,.0f} IRR"
            )
        else:
            text = "❌ Failed to fetch exchange rates."
        await query.edit_message_text(text, reply_markup=back_kb)

    elif callback == "menu_crypto":
        cryptos = CryptoService.get_top_cryptos(limit=5)
        if cryptos:
            text = "📊 Top 5 Cryptocurrencies\n━━━━━━━━━━━━━━━━━━━\n\n"
            for c in cryptos:
                text += (
                    f"{c['rank']}. {c['name']} ({c['symbol']})\n"
                    f"   ${c['price_usd']:,.2f}\n"
                    f"   24h: {c['change_24h']:+.2f}%\n\n"
                )
        else:
            text = "❌ Failed to fetch cryptocurrency data."
        await query.edit_message_text(text, reply_markup=back_kb)

    elif callback == "menu_gold":
        gold_data = TGJUService.get_gold_price()
        if gold_data:
            text = (
                f"🥇 Gold Price\n━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"💰 Gold Coin (Sekee)\n"
                f"   {gold_data['price_coin']:,.0f} IRR ({gold_data['weight_grams']:.2f}g)\n\n"
                f"📊 Price Per Gram\n"
                f"   {gold_data['price_per_gram']:,.0f} IRR/g\n\n"
                f"Source: {gold_data['source']}"
            )
        else:
            text = "❌ Failed to fetch gold price."
        await query.edit_message_text(text, reply_markup=back_kb)

    elif callback == "menu_oil":
        wti = OilService.get_wti_price()
        brent = OilService.get_brent_price()
        if wti and brent:
            text = (
                f"🛢️ Oil Prices\n━━━━━━━━━━━━━━━━━━━\n\n"
                f"WTI: ${wti['price_usd']:.2f} / barrel\n"
                f"Brent: ${brent['price_usd']:.2f} / barrel"
            )
        else:
            text = "❌ Failed to fetch oil prices."
        await query.edit_message_text(text, reply_markup=back_kb)

    elif callback == "menu_alerts":
        user_alerts = AlertService.get_user_alerts(user_id)
        if user_alerts:
            text = "🔔 Your Price Alerts\n━━━━━━━━━━━━━━━━━━━\n\n"
            for i, alert in enumerate(user_alerts, 1):
                text += (
                    f"{i}. {alert['asset_name'].upper()} "
                    f"{alert['condition']} {alert['target_price']:,.0f} "
                    f"{alert['currency']}\n"
                )
        else:
            text = "📭 You have no active alerts."
        await query.edit_message_text(text, reply_markup=back_kb)

    elif callback == "menu_settings":
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 Toggle Notifications", callback_data="toggle_notif")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_back")]
        ])
        await query.edit_message_text("⚙️ Settings\n\nChoose an option:", reply_markup=keyboard)

    elif callback == "menu_back":
        await query.edit_message_text(MENU_TEXT, reply_markup=main_menu_keyboard())

    elif callback == "toggle_notif":
        user = UserService.get_user(user_id)
        if user:
            new_state = not bool(user.get("notifications_enabled", 1))
            UserService.toggle_notifications(user_id, new_state)
            status = "enabled ✅" if new_state else "disabled 🔕"
            text = f"Notifications {status}."
        else:
            text = "❌ Could not update settings."
        await query.edit_message_text(text, reply_markup=back_kb)

    logger.info(f"User {user_id} clicked callback: {callback}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    logger.error(f"Exception while handling an update: {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request. Please try again later."
        )