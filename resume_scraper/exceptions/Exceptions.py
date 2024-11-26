class ScraperException(Exception):
    """Exception raised for errors in the scraping process."""
    pass


class ParserException(Exception):
    """Exception raised for errors in the parsing process."""
    pass


class ScorerException(Exception):
    """Exception raised for errors in the scoring process."""
    pass
