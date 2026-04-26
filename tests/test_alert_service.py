import pytest
from app.services.alert_service import AlertService
from app.core.database import db


class TestAlertService:

    def setup_method(self):
        # Ensure clean state for each test
        pass

    def test_create_alert(self):
        result = AlertService.create_alert(
            user_id=123456,
            asset_type="crypto",
            asset_name="bitcoin",
            target_price=100000,
            condition="above"
        )
        assert result is True

    def test_get_user_alerts(self):
        AlertService.create_alert(123456, "crypto", "bitcoin", 100000, "above")
        alerts = AlertService.get_user_alerts(123456)
        assert len(alerts) >= 1
        assert alerts[0]["asset_name"] == "bitcoin"

    def test_delete_alert(self):
        AlertService.create_alert(123456, "crypto", "ethereum", 5000, "below")
        alerts = AlertService.get_user_alerts(123456)
        if alerts:
            result = AlertService.delete_alert(alerts[0]["id"])
            assert result is True

    def test_check_all_alerts(self):
        AlertService.create_alert(123456, "crypto", "bitcoin", 100, "above")
        triggered = AlertService.check_all_alerts({"crypto_bitcoin": 200})
        assert isinstance(triggered, list)
