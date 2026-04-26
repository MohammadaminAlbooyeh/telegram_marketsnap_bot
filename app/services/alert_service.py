# Alert service - manage price alerts and check triggers
from app.core.database import db
from app.core.logger import logger
from datetime import datetime

class AlertService:
    """Service for managing price alerts"""
    
    @staticmethod
    def create_alert(user_id: int, asset_type: str, asset_name: str,
                    target_price: float, condition: str, currency: str = "IRR") -> bool:
        """Create new price alert for user"""
        try:
            db.execute_update(
                """INSERT INTO user_alerts 
                   (user_id, asset_type, asset_name, target_price, condition, currency)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, asset_type, asset_name, target_price, condition, currency)
            )
            logger.info(f"Alert created for user {user_id}: {asset_name} {condition} {target_price}")
            return True
        except Exception as e:
            logger.error(f"Error creating alert: {str(e)}")
            return False
    
    @staticmethod
    def get_user_alerts(user_id: int) -> list:
        """Get all active alerts for user"""
        results = db.execute_query(
            """SELECT * FROM user_alerts 
               WHERE user_id = ? AND is_active = 1
               ORDER BY created_at DESC""",
            (user_id,)
        )
        return [dict(row) for row in results]
    
    @staticmethod
    def delete_alert(alert_id: int) -> bool:
        """Delete alert by ID"""
        try:
            db.execute_update(
                "UPDATE user_alerts SET is_active = 0 WHERE id = ?",
                (alert_id,)
            )
            logger.info(f"Alert deleted: {alert_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting alert: {str(e)}")
            return False
    
    @staticmethod
    def check_all_alerts(current_prices: dict) -> list:
        """Check all active alerts and trigger if condition met"""
        triggered_alerts = []
        
        try:
            # Get all active alerts
            results = db.execute_query(
                "SELECT * FROM user_alerts WHERE is_active = 1"
            )
            
            for row in results:
                alert = dict(row)
                asset_key = f"{alert['asset_type']}_{alert['asset_name']}"
                
                if asset_key in current_prices:
                    current_price = current_prices[asset_key]
                    
                    # Check condition
                    if alert['condition'] == 'above' and current_price >= alert['target_price']:
                        triggered_alerts.append(alert)
                        AlertService._mark_triggered(alert['id'])
                    
                    elif alert['condition'] == 'below' and current_price <= alert['target_price']:
                        triggered_alerts.append(alert)
                        AlertService._mark_triggered(alert['id'])
            
            if triggered_alerts:
                logger.info(f"{len(triggered_alerts)} alerts triggered")
            
            return triggered_alerts
        
        except Exception as e:
            logger.error(f"Error checking alerts: {str(e)}")
            return []
    
    @staticmethod
    def _mark_triggered(alert_id: int):
        """Mark alert as triggered"""
        db.execute_update(
            """UPDATE user_alerts 
               SET triggered_at = ?, is_active = 0
               WHERE id = ?""",
            (datetime.utcnow().isoformat(), alert_id)
        )