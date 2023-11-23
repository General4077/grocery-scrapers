from typing import Dict, Optional, Tuple, Union
from urllib.parse import urljoin, urlparse
from abc import ABC, abstractclassmethod
import requests
from bs4 import BeautifulSoup
from contextlib import suppress


from scrapers.schemaorg import SchemaOrg
from scrapers.parsers import (
    DefaultOfferParser,
    OfferParserProtocol,
    ImageParserProtocol,
    DefaultImageParser,
)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
}


class AbstractHTTPScraper(ABC):
    """Abstract class for HTTP-based scrapers."""

    page_data: Union[str, bytes]

    def __init__(
        self,
        url: Union[str, None],
        proxies: Optional[
            Dict[str, str]
        ] = None,  # allows us to specify optional proxy server
        timeout: Optional[
            Union[float, Tuple[float, float], Tuple[float, None]]
        ] = None,  # allows us to specify optional timeout for request
        headers: Optional[
            Dict[str, str]
        ] = None,  # allows us to specify optional headers
        html: Union[str, bytes, None] = None,
    ):
        if html:
            self.page_data = html
            self.url = url
        else:
            if url is None:
                raise ValueError("Url required for fetching recipe data")
            resp = requests.get(
                url,
                headers={**HEADERS, **(headers or {})},
                proxies=proxies,
                timeout=timeout,
            )
            self.page_data = resp.content
            self.url = resp.url

        self.soup = BeautifulSoup(self.page_data, "html.parser")
        self.schema = SchemaOrg(self.page_data)

        # attach the plugins as instructed in settings.PLUGINS
        # if not hasattr(self.__class__, "plugins_initialized"):
        #     for name, func in inspect.getmembers(self, inspect.ismethod):
        #         current_method = getattr(self.__class__, name)
        #         for plugin in reversed(settings.PLUGINS):
        #             if plugin.should_run(self.host(), name):
        #                 current_method = plugin.run(current_method)
        #         setattr(self.__class__, name, current_method)
        #     setattr(self.__class__, "plugins_initialized", True)

    @abstractclassmethod
    def host(cls) -> str:
        """get the host of the url, so we can use the correct scraper"""

    @property
    def offer_parser(self) -> OfferParserProtocol:
        """Return the offer parser class for this scraper.

        This is a class that takes a schema.org offer and returns json.
        Override this method to return a custom offer parser.
        Custom parsers must accept offer data as a `dict` on `__init__` and implement a `to_json` method.

        Returns:
            OfferParserProtocol: The offer parser class for this scraper.
        """
        return DefaultOfferParser

    @property
    def image_parser(self) -> ImageParserProtocol:
        """Return the image parser class for this scraper.

        This is a class that takes a schema.org image and returns json.
        Override this method to return a custom image parser.
        Custom parsers must accept image data as a `dict` on `__init__` and implement a `to_json` method.

        Returns:
            ImageParserProtocol: The image parser class for this scraper.
        """
        return DefaultImageParser

    def to_json(self):
        json_dict = {}
        public_method_names = [
            method
            for method in dir(self)
            if callable(getattr(self, method))
            if not method.startswith("_") and method not in ["soup", "links", "to_json"]
        ]
        for method in public_method_names:
            with suppress(Exception):
                if method == "ingredient_groups":
                    json_dict[method] = [i.__dict__ for i in getattr(self, method)()]
                else:
                    json_dict[method] = getattr(self, method)()
        return json_dict

    def canonical_url(self):
        canonical_link = self.soup.find("link", {"rel": "canonical", "href": True})
        if canonical_link:
            return urljoin(self.url, canonical_link["href"])
        return self.url

    def links(self, strictness: str = "loose") -> list[str]:
        """Return a list of links on the page.

        Args:
            strictness (str, optional): How strict to be when filtering links. Defaults to "strict".
                Strict will only return links that are on the same host as the url.
                Loose will return links that are on the same host or subdomain as the url.
                None will return all links.

        Returns:
            list: A list of links.
        """
        strictness = strictness.lower()
        links = []
        for a in self.soup.find_all("a", href=True):
            if a["href"].startswith("/"):
                a[
                    "href"
                ] = f'https://{self.host.rstrip("/").lstrip("http://").lstrip("https://")}{a["href"]}'
            if strictness == "strict" and urlparse(a["href"]).netloc != self.host:
                continue
            if strictness == "loose" and not urlparse(a["href"]).netloc.endswith(
                self.host
            ):
                continue
            links.append(a["href"])
        return list(set(links))

    @property
    def brand(self):
        return self.schema.data.get("brand", {}).get("name")

    @property
    def name(self):
        return self.schema.data.get("name")

    @property
    def image(self) -> Union[str, bytes, None]:
        return self.image_parser(self.schema.data.get("image")).to_json()

    @property
    def description(self):
        return self.schema.data.get("description")

    @property
    def sku(self):
        return self.schema.data.get("sku")

    @property
    def barcode(self) -> dict[str, str]:
        return {"gtin13": self.schema.data.get("gtin13")}

    @property
    def reviews(self):
        return self.schema.data.get("review")

    @property
    def aggregate_rating(self):
        return self.schema.data.get("aggregateRating")

    @property
    def model_number(self):
        return self.schema.data.get("model")

    @property
    def offers(self):
        return self.offer_parser(self.schema.data.get("offers")).to_json()


class AbstractBrowserScraper(ABC):
    """Abstract class for browser-based scrapers."""

    def __init__(self) -> None:
        pass
