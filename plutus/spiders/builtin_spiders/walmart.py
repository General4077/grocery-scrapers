from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from plutus.spiders.abstract import AbstractSpider


class WalmartSpider(AbstractSpider):
    host = "www.walmart.com"

    def __init__(self, url: str, *args, **kwargs):
        url_parts = urlparse(url)
        query = parse_qs(url_parts.query)
        facet = query.get("facet", [""])[0]
        if facet:
            query["facet"] = [facet + "||retailer_type:Walmart"]
        else:
            query["facet"] = ["retailer_type%3AWalmart"]
        url = urlunparse(
            (
                url_parts.scheme,
                url_parts.netloc,
                url_parts.path,
                url_parts.params,
                urlencode(query, doseq=True),
                url_parts.fragment,
            )
        )
        super().__init__(*args, url=url, **kwargs)

    @staticmethod
    def target_link_filter(url) -> bool:
        return urlparse(url).path.startswith("/ip/")

    @staticmethod
    def spider_links_filter(url) -> bool:
        return urlparse(url).path.startswith(("/browse/", "/cp/"))
