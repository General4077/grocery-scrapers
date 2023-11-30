from abc import ABC, abstractclassmethod, abstractmethod
from queue import Queue

from scrapers import reigistry_factory
from scrapers.abstract import Scraper

# TODO: sanitize links


class AbstractSpider(ABC):
    """Abstract class for HTTP-based spiders."""

    def __init__(self, main_entry_point: str = None, filter: str = "strict"):
        """Initialize the spider.

        Args:
            main_entry_point (str): The main entry point for the spider.
            filter (str, optional): The filter to apply to the scraper. Defaults to "strict".
        """
        self.filter = filter
        self.main_entry_point = main_entry_point or f"https://{self.host}"
        self.queue = (
            []
        )  # TODO: orchestrate this with at a higher level  (e.g. a queue service)
        self.history = set()
        self.targets = []  # TODO: hand these off to persistence layer
        self._join = False

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
    def scraper(self) -> Scraper:
        """Return the scraper for this spider.

        Override this property for a custom scraper.
        By default, this property returns the scraper for the host of this spider.

        Returns:
            BaseScraper: The scraper for this spider.
        """
        registry = reigistry_factory()
        return registry.get(self.host)

    def crawl(self, *args, cap: int = None, **kwargs):
        """Begin crawling the spider, starting at the main entry point.

        Args:
            *args: Positional arguments to pass to the scraper.
            cap (int, optional): The maximum number of links to crawl. Defaults to None.
            **kwargs: Keyword arguments to pass to the scraper.
        """
        # TODO: there is opportunity to parallelize this
        cntr = 0
        link = self.main_entry_point
        while link:
            scraper = self.scraper(*args, url=link, **kwargs)
            self.enqueue(
                *scraper.links(
                    strictness=self.filter, filter_function=self.spider_links_filter
                )
            )
            self.targets.extend(
                scraper.links(
                    strictness=self.filter, filter_function=self.target_link_filter
                )
            )
            cntr += 1
            if self._join or (cap and cntr >= cap):
                break
            # TODO: rate limiting/ IP balancing / target balancing, generally play nice
            link = self.dequeue()

    def join(self):
        """Join the spider."""
        self._join = True

    def enqueue(self, *links: str):
        """Enqueue links to the spider.

        Args:
            *links (str): Links to enqueue.
        """
        self.queue.extend(
            set(links).difference(set(self.queue).union(set(self.history)))
        )

    def dequeue(self) -> str:
        """Dequeue a link from the spider.

        Returns:
            str: The dequeued link.
        """
        try:
            return self.queue.pop(0)
        except IndexError:
            return None
