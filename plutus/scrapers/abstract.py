from abc import ABC, abstractclassmethod
from contextlib import suppress
from typing import Any, Dict, Optional, Protocol, Tuple, Union
from urllib.parse import urljoin, urlparse

import htmlmin
import requests
from bs4 import BeautifulSoup

from plutus.scrapers.parsers import (
    DefaultImageParser,
    DefaultOfferParser,
    ImageParserProtocol,
    OfferParserProtocol,
)
from plutus.scrapers.schemaorg import SchemaOrg
from plutus.scrapers.user_agents import random_user_agent
from plutus.typing import Result
from plutus.utils import get_ip


class Scraper(Protocol):
    host: str
    status_code: int
    soup: BeautifulSoup
    small_soup: str
    schema: SchemaOrg
    offer_parser: OfferParserProtocol
    image_parser: ImageParserProtocol
    spider_filter: callable
    to_json: callable
    canonical_url: callable
    links: callable
    target_links: callable
    spider_links: callable
    brand: str
    name: str
    image: Union[str, bytes, None]
    description: str
    sku: str
    barcode: dict[str, str]
    reviews: dict[str, str]
    aggregate_rating: dict[str, str]
    model_number: str
    offers: dict[str, str]


class AbstractHTTPScraper(ABC):
    """Abstract class for HTTP-based scrapers."""

    page_data: Union[str, bytes]

    def __init__(
        self,
        url: Union[str, None],
        proxies: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, Tuple[float, float], Tuple[float, None]]] = None,
        headers: Optional[Dict[str, str]] = None,
        html: Union[str, bytes, None] = None,
    ):
        if url is None and html is None:
            raise ValueError("Url required for fetching recipe data")

        if not headers:
            headers = {"User-Agent": random_user_agent()}
        else:
            headers["User-Agent"] = (
                headers.get("User-Agent", None) or random_user_agent()
            )

        if html:
            self.page_data = html
            self.url = url
            self.status_code = 200
        else:
            resp = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
            )
            self.page_data = resp.content
            self.url = resp.url
            self.status_code = resp.status_code
        self._soup = None
        self._schema = None

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
    def host(*cls) -> str:
        """get the host of the url, so we can use the correct scraper"""

    @property
    def soup(self) -> BeautifulSoup:
        """Return the BeautifulSoup data for this scraper.

        Returns:
            BeautifulSoup: The BeautifulSoup data for this scraper.
        """
        if self._soup is None:
            self._soup = BeautifulSoup(self.page_data, "html.parser")
        return self._soup

    @property
    def small_soup(self) -> BeautifulSoup:
        """Return the BeautifulSoup data for this scraper.

        Returns:
            BeautifulSoup: The BeautifulSoup data for this scraper.
        """
        return htmlmin.minify(
            str(self.soup),
            remove_empty_space=True,
            remove_comments=True,
            remove_all_empty_space=True,
        )

    @property
    def schema(self) -> SchemaOrg:
        """Return the schema.org data for this scraper.

        Returns:
            SchemaOrg: The schema.org data for this scraper.
        """
        if self._schema is None:
            self._schema = SchemaOrg(self.page_data)
        return self._schema

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

    def to_result(self) -> Result:
        return Result(
            ip=get_ip(),
            url=self.url,
            link_id=self.link_id,
            price=self.offers.get("price", None),
            sale_price=self.offers.get("sale_price", None),
            availability=self.offers.get("availability", None),
            pickup=self.offers.get("pickup", None),
            status_code=self.status_code,
            source=self.small_soup,
            product_info={
                "brand": self.brand,
                "name": self.name,
                "image": self.image,
                "description": self.description,
                "sku": self.sku,
                "barcode": self.barcode,
                "reviews": self.reviews,
                "aggregate_rating": self.aggregate_rating,
                "model_number": self.model_number,
                "offers": self.offers,
            },
        )

    def canonical_url(self):
        canonical_link = self.soup.find("link", {"rel": "canonical", "href": True})
        if canonical_link:
            return urljoin(self.url, canonical_link["href"])
        return self.url

    def links(
        self, strictness: str = "loose", filter_function: callable = lambda url: True
    ) -> list[str]:
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
        return [l for l in set(links) if filter_function(l)]

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
    def offers(self) -> dict[str, Any]:
        return self.offer_parser(self.schema.data.get("offers")).to_json()


class AbstractBrowserScraper(ABC):
    """Abstract class for browser-based scrapers."""

    def __init__(self) -> None:
        pass
