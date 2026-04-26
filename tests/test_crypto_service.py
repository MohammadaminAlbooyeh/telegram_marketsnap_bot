import pytest
from unittest.mock import patch, MagicMock
from app.services.crypto_service import CryptoService


class TestCryptoService:

    @patch("app.services.crypto_service.requests.get")
    @patch("app.services.crypto_service.TGJUService.get_usd_to_irr")
    def test_get_bitcoin_price(self, mock_irr, mock_get):
        mock_irr.return_value = {"price": 50000}
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "bitcoin": {"usd": 50000, "eur": 45000, "usd_24h_change": 2.5}
        }
        mock_get.return_value = mock_response

        result = CryptoService.get_bitcoin_price()
        assert result is not None
        assert result["symbol"] == "BTC"
        assert result["price_usd"] == 50000
        assert result["price_irr"] == 50000 * 50000

    @patch("app.services.crypto_service.requests.get")
    @patch("app.services.crypto_service.TGJUService.get_usd_to_irr")
    def test_get_ethereum_price(self, mock_irr, mock_get):
        mock_irr.return_value = {"price": 50000}
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ethereum": {"usd": 3000, "eur": 2700, "usd_24h_change": -1.2}
        }
        mock_get.return_value = mock_response

        result = CryptoService.get_ethereum_price()
        assert result is not None
        assert result["symbol"] == "ETH"
        assert result["price_usd"] == 3000

    @patch("app.services.crypto_service.requests.get")
    @patch("app.services.crypto_service.TGJUService.get_usd_to_irr")
    def test_get_top_cryptos(self, mock_irr, mock_get):
        mock_irr.return_value = {"price": 50000}
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "name": "Bitcoin",
                "symbol": "btc",
                "current_price": 50000,
                "market_cap": 1000000000000,
                "price_change_percentage_24h": 2.5
            }
        ]
        mock_get.return_value = mock_response

        result = CryptoService.get_top_cryptos(limit=1)
        assert len(result) == 1
        assert result[0]["name"] == "Bitcoin"
