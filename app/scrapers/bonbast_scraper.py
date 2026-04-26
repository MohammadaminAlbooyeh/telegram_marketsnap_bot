import requests
from bs4 import BeautifulSoup
from app.core.logger import logger


class BonbastScraper:
    """Scraper for Bonbast.com - alternative USD/EUR source."""

    URL = "https://bonbast.com"

    @staticmethod
    def get_usd_rate() -> float:
        """Fetch USD to IRR rate from Bonbast."""
        try:
            response = requests.get(BonbastScraper.URL, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            usd_element = soup.find("td", string="USD")
            if usd_element:
                rate = float(usd_element.find_next("td").text.replace(",", ""))
                logger.info(f"Bonbast USD rate: {rate}")
                return rate
        except Exception as e:
            logger.error(f"Bonbast scraper error: {e}")
        return 0

    @staticmethod
    def get_eur_rate() -> float:
        """Fetch EUR to IRR rate from Bonbast."""
        try:
            response = requests.get(BonbastScraper.URL, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            eur_element = soup.find("td", string="EUR")
            if eur_element:
                rate = float(eur_element.find_next("td").text.replace(",", ""))
                logger.info(f"Bonbast EUR rate: {rate}")
                return rate
        except Exception as e:
            logger.error(f"Bonbast scraper error: {e}")
        return 0
