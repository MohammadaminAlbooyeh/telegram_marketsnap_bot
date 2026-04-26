import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestHandlers:

    @pytest.mark.asyncio
    async def test_bitcoin_handler(self):
        from app.handlers.crypto_handlers import bitcoin

        update = MagicMock()
        update.effective_user.id = 123
        update.message.reply_text = AsyncMock()

        with patch("app.handlers.crypto_handlers.CryptoService.get_bitcoin_price", return_value=None):
            await bitcoin(update, MagicMock())
            update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_usd_handler(self):
        from app.handlers.currency_handlers import usd

        update = MagicMock()
        update.effective_user.id = 123
        update.message.reply_text = AsyncMock()

        with patch("app.handlers.currency_handlers.TGJUService.get_usd_to_irr", return_value=None):
            await usd(update, MagicMock())
            update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_gold_handler(self):
        from app.handlers.gold_handlers import gold

        update = MagicMock()
        update.effective_user.id = 123
        update.message.reply_text = AsyncMock()

        with patch("app.handlers.gold_handlers.TGJUService.get_gold_price", return_value=None):
            await gold(update, MagicMock())
            update.message.reply_text.assert_called_once()
