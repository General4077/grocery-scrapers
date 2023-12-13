from plutus.scrapers.parsers import SchemaOrgAvail, SchemaOrgDelivery
from plutus.scrapers.builtin_scrapers import WalmartHTTPScrapper


def test_walmart_scraper_offers():
    with open("tests/data/walmart.html", "rb") as f:
        html = f.read()
    scraper = WalmartHTTPScrapper(
        url="https://www.walmart.com/ip/Great-Value-Whole-Vitamin-D-Milk-Gallon-128-fl-oz/10450114",
        html=html,
    )
    assert scraper.offers == {
        "availability": SchemaOrgAvail.IN_STOCK,
        "pickup": SchemaOrgDelivery.ON_SITE_PICKUP,
        "price": "3.74",
        "priceCurrency": "USD",
    }


def test_minified_data_offer_is_recoverable():
    with open("tests/data/walmart.html", "rb") as f:
        html = f.read()
    url = "https://www.walmart.com/ip/Great-Value-Whole-Vitamin-D-Milk-Gallon-128-fl-oz/10450114"
    scraper = WalmartHTTPScrapper(
        url=url,
        html=html,
    )
    scraper = WalmartHTTPScrapper(
        url=url,
        html=scraper.small_soup,
    )
    assert scraper.offers == {
        "availability": SchemaOrgAvail.IN_STOCK,
        "pickup": SchemaOrgDelivery.ON_SITE_PICKUP,
        "price": "3.74",
        "priceCurrency": "USD",
    }
