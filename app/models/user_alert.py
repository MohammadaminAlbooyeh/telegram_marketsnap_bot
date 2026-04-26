# User alert model - stores price alert configurations
from datetime import datetime

class UserAlert:
    """Price alert configuration for users"""
    
    def __init__(self, user_id: int, asset_type: str, asset_name: str,
                 target_price: float, condition: str, currency: str = "IRR"):
        self.user_id = user_id
        self.asset_type = asset_type  # crypto, currency, gold, oil
        self.asset_name = asset_name  # bitcoin, usd, gold, etc
        self.target_price = target_price
        self.condition = condition  # above or below
        self.currency = currency
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.triggered_at = None
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "asset_type": self.asset_type,
            "asset_name": self.asset_name,
            "target_price": self.target_price,
            "condition": self.condition,
            "currency": self.currency,
            "is_active": self.is_active,
            "created_at": self.created_at
        }