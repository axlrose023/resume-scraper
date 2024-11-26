from abc import ABC, abstractmethod
from typing import List, Dict

class BaseParser(ABC):
    @abstractmethod
    def parse_page(self, html_content: str) -> List[Dict]:
        pass