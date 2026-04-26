# Price history model - stores historical price data
from datetime import datetime

class PriceHistory:
    """Store historical price data for charts and analysis"""
    
    def __init__(self, asset_type: str, asset_name: str, 
                 price: float, currency: str = "IRR"):
        self.asset_type = asset_type  # crypto, currency, gold, oil
        self.asset_name = asset_name  # bitcoin, usd, gold, oil
        self.price = price
        self.currency = currency
        self.timestamp = datetime.utcnow()
    
    def to_dict(self):
        return {
            "asset_type": self.asset_type,
            "asset_name": self.asset_name,
            "price": self.price,
            "currency": self.currency,
            "timestamp": self.timestamp
        }