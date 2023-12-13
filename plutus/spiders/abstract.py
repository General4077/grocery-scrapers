from abc import ABC, abstractclassmethod, abstractmethod
from typing import Protocol

from plutus.scrapers import scraper_registry
from plutus.scrapers.abstract import Scraper

# TODO: sanitize links


class Spider(Protocol):
    """Spider protocol."""

    host: str
    filter: str
    link: str
    scraper: Scraper
    links: callable
    target_link_filter: callable
    spider_links_filter: callable


class AbstractSpider(ABC):
    """Abstract class for HTTP-based spiders."""

    def __init__(self, url: str = None, filter: str = "strict", html: str = None):
        """Initialize the spider.

        Args:
            url (str): The main entry point for the spider.
            filter (str, optional): The filter to apply to the scraper. Defaults to "strict".
        """
        self.filter = filter
        self.link = url or f"https://{self.host}"
        self.html = html
        self._soup = None
        self._scraper = None

    @abstractclassmethod
    def host(cls) -> str:
        """get the host of the url, so we can use the correct scraper"""

    @staticmethod
    @abstractmethod
    def target_link_filter(link: str) -> bool:
        """Filter links to good target candidates."""

    @staticmethod
    @abstractmethod
    def spider_links_filter(link: str) -> bool:
        """Filter links to good spider candidates."""

    @property
    def small_soup(self) -> str:
        """Return the small soup for this spider.

        Returns:
            str: The small soup for this spider.
        """
        return self.scraper.small_soup

    @property
    def status_code(self) -> int:
        """Return the status code for this spider.

        Returns:
            int: The status code for this spider.
        """
        return self.scraper.status_code

    @property
    def scraper(self) -> Scraper:
        """Return the scraper for this spider.

        Override this property for a custom scraper.
        By default, this property returns the scraper for the host of this spider.

        Returns:
            BaseScraper: The scraper for this spider.
        """
        if self._scraper:
            return self._scraper
        registry = scraper_registry()
        return registry.get(self.host)

    @scraper.setter
    def scraper(self, scraper: Scraper) -> None:
        self._scraper = scraper

    def load_data(self, *args, force_reload=False, **kwargs) -> None:
        """Load data into the scraper.

        Args:
            *args: Positional arguments to pass to the scraper.
            **kwargs: Keyword arguments to pass to the scraper.
        """
        if not self._scraper or force_reload:
            self.scraper = self.scraper(*args, url=self.link, html=self.html, **kwargs)

    def links(self, *args, **kwargs) -> dict:
        """Begin crawling the spider, starting at the main entry point.

        Args:
            *args: Positional arguments to pass to the scraper.
            **kwargs: Keyword arguments to pass to the scraper.

        Returns:
            dict: keys are "spiderables" and "targets", values are lists of links.

        """
        self.load_data(*args, **kwargs)
        return {
            "spiderables": self.scraper.links(
                strictness=self.filter, filter_function=self.spider_links_filter
            ),
            "targets": self.scraper.links(
                strictness=self.filter, filter_function=self.target_link_filter
            ),
        }
