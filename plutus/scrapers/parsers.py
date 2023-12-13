from typing import Protocol, Union

from plutus.scrapers.schemaorg import SchemaOrgAvail, SchemaOrgDelivery


class OfferParserProtocol(Protocol):
    def __init__(self, offer: dict):
        ...

    def to_json(self) -> dict:
        ...


class DefaultOfferParser:
    def _normalize_availability(self, avail: Union[str, int]):
        if avail is None:
            return None
        if isinstance(avail, int):
            return SchemaOrgAvail.IN_STOCK if avail > 0 else SchemaOrgAvail.OUT_OF_STOCK
        if "schema.org" in avail:
            return SchemaOrgAvail(avail.rsplit("/", 1)[1])
        else:
            raise ValueError(f"Unknown availability format: {avail}")

    def _normalize_pickup(self, pickup: str):
        if pickup is None:
            return SchemaOrgDelivery.ON_SITE_PICKUP
        if "schema.org" in pickup:
            return SchemaOrgDelivery(pickup.rsplit("/", 1)[1])
        raise ValueError(f"Unknown pickup format: {pickup}")

    def __init__(self, offer):
        self.offer = offer

    def to_json(self) -> dict:
        price = self.offer.get("price", None)
        if price is not None:
            price = str(price)
        return {
            "price": price,
            "priceCurrency": self.offer.get("priceCurrency", None),
            "availability": self._normalize_availability(
                self.offer.get("availability", None)
            ),
            "pickup": self._normalize_pickup(
                self.offer.get("availableDeliveryMethod", None)
            ),
        }


class ImageParserProtocol(Protocol):
    def __init__(self, image: dict):
        ...

    def to_json(self) -> dict:
        ...


class DefaultImageParser:
    def __init__(self, image):
        self.image = image

    def to_json(self):
        return self.image
