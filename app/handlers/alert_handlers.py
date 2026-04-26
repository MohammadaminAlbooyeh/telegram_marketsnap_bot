# Alert handlers - price alert management
from telegram import Update
from telegram.ext import ContextTypes
from app.services.alert_service import AlertService
from app.core.logger import logger

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /alerts command - show user's alerts"""
    
    user_id = update.effective_user.id
    user_alerts = AlertService.get_user_alerts(user_id)
    
    if not user_alerts:
        await update.message.reply_text("📭 You have no active alerts.")
        return
    
    message = "🔔 Your Price Alerts\n━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, alert in enumerate(user_alerts, 1):
        message += (
            f"{i}. {alert['asset_name'].upper()}\n"
            f"   Condition: {alert['asset_name']} {alert['condition']} {alert['target_price']:,.0f} {alert['currency']}\n"
            f"   Created: {alert['created_at']}\n\n"
        )
    
    logger.info(f"User {user_id} viewed alerts")
    await update.message.reply_text(message)

async def setalert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setalert command - create new alert"""
    
    # Example: /setalert bitcoin 3000000 above
    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /setalert <asset> <price> <above|below>\n"
            "Example: /setalert bitcoin 3000000 above"
        )
        return
    
    asset_name = context.args[0].lower()
    try:
        target_price = float(context.args[1])
        condition = context.args[2].lower()
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Invalid format. Please use correct numbers and condition.")
        return
    
    if condition not in ['above', 'below']:
        await update.message.reply_text("❌ Condition must be 'above' or 'below'.")
        return
    
    user_id = update.effective_user.id
    success = AlertService.create_alert(
        user_id=user_id,
        asset_type="crypto",
        asset_name=asset_name,
        target_price=target_price,
        condition=condition
    )
    
    if success:
        await update.message.reply_text(
            f"✅ Alert created!\n"
            f"Asset: {asset_name.upper()}\n"
            f"Condition: {condition} {target_price:,.0f} IRR"
        )
        logger.info(f"User {user_id} created alert for {asset_name}")
    else:
        await update.message.reply_text("❌ Failed to create alert.")