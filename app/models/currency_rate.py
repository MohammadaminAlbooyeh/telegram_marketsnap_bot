from datetime import datetime


class CurrencyRate:
    """Model for currency exchange rate data."""

    def __init__(self, base: str, target: str, rate: float, source: str = ""):
        self.base = base
        self.target = target
        self.rate = rate
        self.source = source
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "base": self.base,
            "target": self.target,
            "rate": self.rate,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }
