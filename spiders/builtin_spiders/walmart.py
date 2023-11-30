from urllib.parse import urlparse

from spiders.abstract import AbstractSpider


class WalmartSpider(AbstractSpider):
    host = "walmart.com"

    def __init__(self, *args, **kwargs):
        main_entry_point = kwargs.pop(
            "main_entry_point",
            "https://www.walmart.com/cp/food/976759?povid=GlobalNav_rWeb_Grocery_Grocery_ShopAll",
        )
        super().__init__(*args, main_entry_point=main_entry_point, **kwargs)

    @staticmethod
    def target_link_filter(url) -> bool:
        return urlparse(url).path.startswith("/ip/")

    @staticmethod
    def spider_links_filter(url) -> bool:
        return urlparse(url).path.startswith(("/browse/", "/cp/"))
