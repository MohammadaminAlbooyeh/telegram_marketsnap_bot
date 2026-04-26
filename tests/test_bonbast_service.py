from unittest.mock import patch, MagicMock
from app.scrapers.bonbast_scraper import BonbastScraper


class TestBonbastScraper:

    @patch("app.scrapers.bonbast_scraper.requests.get")
    def test_get_usd_rate(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><td>USD</td><td>50,000</td></html>"
        mock_get.return_value = mock_response

        with patch("app.scrapers.bonbast_scraper.BeautifulSoup") as mock_bs:
            mock_soup = MagicMock()
            mock_element = MagicMock()
            mock_element.find_next.return_value.text = "50,000"
            mock_soup.find.return_value = mock_element
            mock_bs.return_value = mock_soup

            rate = BonbastScraper.get_usd_rate()
            assert rate == 50000.0

    def test_get_eur_rate_fallback(self):
        with patch("app.scrapers.bonbast_scraper.requests.get", side_effect=Exception("network")):
            rate = BonbastScraper.get_eur_rate()
            assert rate == 0
