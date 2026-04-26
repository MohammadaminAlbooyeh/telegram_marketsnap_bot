import requests
from bs4 import BeautifulSoup
from app.core.logger import logger


class OilScraper:
    """Alternative oil price scraper."""

    URL = "https://www.oilprice.com"

    @staticmethod
    def get_wti_price() -> float:
        """Scrape WTI crude oil price."""
        try:
            response = requests.get(OilScraper.URL, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            wti_text = soup.find("td", string=lambda t: t and "WTI" in t)
            if wti_text:
                price = float(wti_text.find_next("td").text.replace("$", ""))
                logger.info(f"OilPrice WTI: {price}")
                return price
        except Exception as e:
            logger.error(f"Oil scraper error: {e}")
        return 0

    @staticmethod
    def get_brent_price() -> float:
        """Scrape Brent crude oil price."""
        try:
            response = requests.get(OilScraper.URL, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            brent_text = soup.find("td", string=lambda t: t and "Brent" in t)
            if brent_text:
                price = float(brent_text.find_next("td").text.replace("$", ""))
                logger.info(f"OilPrice Brent: {price}")
                return price
        except Exception as e:
            logger.error(f"Oil scraper error: {e}")
        return 0
