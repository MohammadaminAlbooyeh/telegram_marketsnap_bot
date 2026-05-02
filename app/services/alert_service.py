# Compatibility layer for tests expecting `app.services.alert_service`
from services.stock_service import AlertService  # re-export

__all__ = ["AlertService"]
