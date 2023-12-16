from enum import Enum

from plutus.scrapers.abstract import (
    AbstractBrowserScraper,
    AbstractHTTPScraper,
    Scraper,
)
from plutus.scrapers.builtin_scrapers import *


class ScrapeType(Enum):
    """Scrape type."""

    PRODUCT = "PRODUCT"
    SPIDER = "SPIDER"


def scraper_registry() -> dict[str, Scraper]:
    """Returns a registry of all scrapers.

    The registry prefers http scrapers over browser scrapers.

    Returns:
        dict: A dictionary of all scrapers.
    """
    reg = {cls.host: cls for cls in AbstractBrowserScraper.__subclasses__()}
    reg.update({cls.host: cls for cls in AbstractHTTPScraper.__subclasses__()})
    return reg
