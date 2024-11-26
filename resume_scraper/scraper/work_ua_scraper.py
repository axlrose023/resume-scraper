import requests
from .base_scraper import BaseScraper
from resume_scraper.exceptions.Exceptions import ScraperException

class WorkUaScraper(BaseScraper):
    BASE_URL = "https://www.work.ua"

    def __init__(self, user_agent: str = "Mozilla/5.0"):
        self.headers = {"User-Agent": user_agent}

    def fetch_page(self, endpoint: str) -> str:
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ScraperException(f"Error fetching {endpoint}: {e}")