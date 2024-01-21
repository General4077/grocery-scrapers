from typing import Optional, TypedDict


class CrawlTodo(TypedDict):
    """Crawl todo."""

    type: str
    url: str
    link_id: Optional[str]


class Result(TypedDict):
    """Result."""

    ip: str
    url: str
    link_id: Optional[str]
    price: Optional[str]
    sale_price: Optional[str]
    availability: Optional[str]
    pickup: Optional[str]
    source: str  # TODO use htmlmin to minify html
    targets: list[str]
    spiderables: list[str]
    status_code: int
