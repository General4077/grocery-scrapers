from typing import Union

from scrapers.abstract import AbstractHTTPScraper, AbstractBrowserScraper, Scraper
from scrapers.builtin_scrapers import *


def reigistry_factory() -> dict[str, Scraper]:
    """Returns a registry of all scrapers.

    The registry prefers http scrapers over browser scrapers.

    Returns:
        dict: A dictionary of all scrapers.
    """
    reg = {cls.host: cls for cls in AbstractBrowserScraper.__subclasses__()}
    reg.update({cls.host: cls for cls in AbstractHTTPScraper.__subclasses__()})
    return reg
