# TGJU service - scrape USD/EUR/Gold prices from TGJU.org
import requests
from bs4 import BeautifulSoup
from app.core.config import Config
from app.core.logger import logger
from app.services.price_cache_service import cache_service
from datetime import datetime

class TGJUService:
    """Service for fetching prices from TGJU.org"""
    
    @staticmethod
    def get_usd_to_irr() -> dict:
        """Get USD to IRR exchange rate from TGJU"""
        # Check cache first
        cached = cache_service.get("usd_irr")
        if cached:
            return cached
        
        try:
            logger.info("Fetching USD/IRR from TGJU...")
            response = requests.get(
                Config.TGJU_URL,
                timeout=Config.REQUEST_TIMEOUT
            )
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Parse USD price - adjust selector based on TGJU.org structure
            usd_element = soup.select_one('[data-symbol="usatoman"]')
            
            if usd_element:
                price = float(usd_element.get('data-price', 0))
                
                result = {
                    "asset": "USD",
                    "price": price,
                    "currency": "IRR",
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "TGJU"
                }
                
                # Cache for 10 minutes
                cache_service.set("usd_irr", result, Config.USD_IRR_CACHE_MINUTES)
                logger.info(f"USD/IRR fetched: {price}")
                return result
        
        except Exception as e:
            logger.error(f"Error fetching USD/IRR: {str(e)}")
            return None
    
    @staticmethod
    def get_eur_to_irr() -> dict:
        """Get EUR to IRR exchange rate from TGJU"""
        cached = cache_service.get("eur_irr")
        if cached:
            return cached
        
        try:
            logger.info("Fetching EUR/IRR from TGJU...")
            response = requests.get(
                Config.TGJU_URL,
                timeout=Config.REQUEST_TIMEOUT
            )
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Parse EUR price
            eur_element = soup.select_one('[data-symbol="eurotoman"]')
            
            if eur_element:
                price = float(eur_element.get('data-price', 0))
                
                result = {
                    "asset": "EUR",
                    "price": price,
                    "currency": "IRR",
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "TGJU"
                }
                
                cache_service.set("eur_irr", result, Config.USD_IRR_CACHE_MINUTES)
                logger.info(f"EUR/IRR fetched: {price}")
                return result
        
        except Exception as e:
            logger.error(f"Error fetching EUR/IRR: {str(e)}")
            return None
    
    @staticmethod
    def get_gold_price() -> dict:
        """Get gold (coin) price from TGJU"""
        cached = cache_service.get("gold_price")
        if cached:
            return cached
        
        try:
            logger.info("Fetching Gold price from TGJU...")
            response = requests.get(
                Config.TGJU_URL,
                timeout=Config.REQUEST_TIMEOUT
            )
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Parse gold/coin price
            gold_element = soup.select_one('[data-symbol="coin"]')
            
            if gold_element:
                price = float(gold_element.get('data-price', 0))
                
                result = {
                    "asset": "Gold Coin",
                    "price": price,
                    "currency": "IRR",
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "TGJU"
                }
                
                cache_service.set("gold_price", result, Config.GOLD_CACHE_MINUTES)
                logger.info(f"Gold price fetched: {price}")
                return result
        
        except Exception as e:
            logger.error(f"Error fetching gold price: {str(e)}")
            return None