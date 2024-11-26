from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def fetch_page(self, endpoint: str) -> str:
        pass