# Oil service - fetch oil prices using yfinance
import yfinance as yf
from app.core.config import Config
from app.core.logger import logger
from app.services.price_cache_service import cache_service
from datetime import datetime

class OilService:
    """Service for oil price data"""
    
    @staticmethod
    def get_wti_price() -> dict:
        """Get WTI crude oil price (CL=F)"""
        cached = cache_service.get("wti_oil")
        if cached:
            return cached
        
        try:
            logger.info("Fetching WTI oil price...")
            
            # Fetch WTI crude oil price
            wti = yf.Ticker("CL=F")
            data = wti.history(period="1d")
            
            if not data.empty:
                price = float(data['Close'].iloc[-1])
                
                result = {
                    "asset": "WTI Crude Oil",
                    "symbol": "CL=F",
                    "price_usd": price,
                    "unit": "per barrel",
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "Yahoo Finance"
                }
                
                cache_service.set("wti_oil", result, Config.OIL_CACHE_MINUTES)
                logger.info(f"WTI price fetched: ${price}")
                return result
        
        except Exception as e:
            logger.error(f"Error fetching WTI price: {str(e)}")
            return None
    
    @staticmethod
    def get_brent_price() -> dict:
        """Get Brent crude oil price (BZ=F)"""
        cached = cache_service.get("brent_oil")
        if cached:
            return cached
        
        try:
            logger.info("Fetching Brent oil price...")
            
            # Fetch Brent crude oil price
            brent = yf.Ticker("BZ=F")
            data = brent.history(period="1d")
            
            if not data.empty:
                price = float(data['Close'].iloc[-1])
                
                result = {
                    "asset": "Brent Crude Oil",
                    "symbol": "BZ=F",
                    "price_usd": price,
                    "unit": "per barrel",
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "Yahoo Finance"
                }
                
                cache_service.set("brent_oil", result, Config.OIL_CACHE_MINUTES)
                logger.info(f"Brent price fetched: ${price}")
                return result
        
        except Exception as e:
            logger.error(f"Error fetching Brent price: {str(e)}")
            return None