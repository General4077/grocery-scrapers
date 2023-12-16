import os
from enum import Enum
from urllib.parse import urlparse

from redis import Redis

from plutus.orchestration.typing import CrawlTodo, Result
from plutus.orchestration.utils import get_ip
from plutus.queues import QueueProtocol, RedisQueue
from plutus.scrapers import ScrapeType, scraper_registry
from plutus.spiders import spider_registry


class Director:
    def __init__(self):
        self.redis = Redis(
            host=os.environ.get("PLUTUS_REDIS_HOST"),
            port=6379,
            db=0,
            password=os.environ.get("PLUTUS_REDIS_PASSWORD", ""),
        )
        self.scraper_registry = scraper_registry()
        self.spider_registry = spider_registry()
        self.queue: QueueProtocol = RedisQueue(self.redis, "plutus:incoming:queue")
        self.results: QueueProtocol = RedisQueue(self.redis, "plutus:results:queue")
        self.commands: QueueProtocol = RedisQueue(
            self.redis, "plutus:commands:queue"
        )  # This should be pub/sub
        self.config = {}

    def start_loop(self):
        while True:
            # TODO: handle commands
            todo: CrawlTodo = self.queue.pop()
            if todo is None:
                continue
            result = None
            host = urlparse(todo["url"]).netloc  # TODO handle subdomains
            if todo["type"] == ScrapeType.PRODUCT.value:
                scraper = self.scraper_registry[host](url=todo["url"])
                spider = self.spider_registry[host](
                    url=todo["url"], html=scraper.page_data
                )
                offer = scraper.offers
                availability = offer.get("availability", None)
                if availability is not None:
                    availability = str(availability)
                pickup = offer.get("pickup", None)
                if pickup is not None:
                    pickup = str(pickup)
                result = Result(
                    ip=get_ip(),
                    url=todo["url"],
                    link_id=todo["link_id"],
                    price=offer.get("price", None),
                    sale_price=None,
                    availability=availability,
                    pickup=pickup,
                    source=scraper.small_soup,
                    status_code=scraper.status_code,
                    **spider.links(),
                )
            elif todo["type"] == ScrapeType.SPIDER.value:
                spider = self.spider_registry[host](url=todo["url"])
                result = Result(
                    ip=get_ip(),
                    url=todo["url"],
                    link_id=todo["link_id"],
                    price=None,
                    sale_price=None,
                    availability=None,
                    source=spider.small_soup,
                    status_code=spider.status_code,
                    **spider.links(),
                )
            else:
                raise ValueError(f"Unknown scrape type: {todo['type']}")
            self.results.push(result)
