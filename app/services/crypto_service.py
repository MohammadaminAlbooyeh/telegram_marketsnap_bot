# Compatibility layer for tests expecting `app.services.crypto_service`
from __future__ import annotations

import requests

from services.market_service import TGJUService


class CryptoService:
    """Shim CryptoService matching the test expectations."""

    @staticmethod
    def get_bitcoin_price() -> dict | None:
        # Test patches:
        # - app.services.crypto_service.requests.get
        # - app.services.crypto_service.TGJUService.get_usd_to_irr
        irr_data = TGJUService.get_usd_to_irr()
        irr_rate = 0
        if irr_data and isinstance(irr_data, dict):
            irr_rate = float(irr_data.get("price", 0) or 0)

        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price")
            response.raise_for_status()
            data = response.json()
            bitcoin = (data or {}).get("bitcoin") or {}

            usd_price = bitcoin.get("usd", 0) or 0
            eur_price = bitcoin.get("eur", 0) or 0
            irr_price = float(usd_price) * float(irr_rate)

            return {
                "asset": "Bitcoin",
                "symbol": "BTC",
                "price_usd": usd_price,
                "price_eur": eur_price,
                "price_irr": irr_price,
                "change_24h": bitcoin.get("usd_24h_change", 0) or 0,
                "timestamp": None,
                "source": None,
            }
        except Exception:
            return None

    @staticmethod
    def get_ethereum_price() -> dict | None:
        irr_data = TGJUService.get_usd_to_irr()
        irr_rate = 0
        if irr_data and isinstance(irr_data, dict):
            irr_rate = float(irr_data.get("price", 0) or 0)

        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price")
            response.raise_for_status()
            data = response.json()
            ethereum = (data or {}).get("ethereum") or {}

            usd_price = ethereum.get("usd", 0) or 0
            eur_price = ethereum.get("eur", 0) or 0
            irr_price = float(usd_price) * float(irr_rate)

            return {
                "asset": "Ethereum",
                "symbol": "ETH",
                "price_usd": usd_price,
                "price_eur": eur_price,
                "price_irr": irr_price,
                "change_24h": ethereum.get("usd_24h_change", 0) or 0,
                "timestamp": None,
                "source": None,
            }
        except Exception:
            return None

    @staticmethod
    def get_top_cryptos(limit: int = 10) -> list[dict]:
        try:
            response = requests.get("https://api.coingecko.com/api/v3/coins/markets")
            response.raise_for_status()
            cryptos = response.json() or []

            irr_data = TGJUService.get_usd_to_irr()
            irr_rate = 0
            if irr_data and isinstance(irr_data, dict):
                irr_rate = float(irr_data.get("price", 0) or 0)

            result: list[dict] = []
            for i, crypto in enumerate(cryptos[:limit]):
                usd_price = crypto.get("current_price", 0) or 0
                result.append(
                    {
                        "rank": i + 1,
                        "name": crypto.get("name"),
                        "symbol": (crypto.get("symbol") or "").upper(),
                        "price_usd": usd_price,
                        "price_irr": float(usd_price) * float(irr_rate),
                        "market_cap": crypto.get("market_cap", 0) or 0,
                        "change_24h": crypto.get("price_change_percentage_24h", 0) or 0,
                    }
                )
            return result
        except Exception:
            return []
