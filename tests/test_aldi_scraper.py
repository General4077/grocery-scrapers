from plutus.scrapers.parsers import SchemaOrgAvail, SchemaOrgDelivery
from plutus.scrapers.builtin_scrapers import AldiHTTPScrapper


def test_walmart_scraper():
    with open("tests/data/aldi.html", "rb") as f:
        html = f.read()
    url = "https://new.aldi.us/product/friendly-farms-1-milk-4099100144185"
    scraper = AldiHTTPScrapper(
        url=url,
        html=html,
    )
    assert scraper.offers == {
        "availability": SchemaOrgAvail.IN_STOCK,
        "pickup": SchemaOrgDelivery.ON_SITE_PICKUP,
        "price": "2.55",
        "priceCurrency": "USD",
    }


def test_minified_data_is_recoverable():
    with open("tests/data/aldi.html", "rb") as f:
        html = f.read()
    url = "https://new.aldi.us/product/friendly-farms-1-milk-4099100144185"
    scraper = AldiHTTPScrapper(
        url=url,
        html=html,
    )
    scraper = AldiHTTPScrapper(
        url=url,
        html=scraper.small_soup,
    )
    assert scraper.offers == {
        "availability": SchemaOrgAvail.IN_STOCK,
        "pickup": SchemaOrgDelivery.ON_SITE_PICKUP,
        "price": "2.55",
        "priceCurrency": "USD",
    }
