"""Schema.org parser and enumerations for product data.

This is a contrived derivation of `https://github.com/hhursev/recipe-scrapers/blob/main/recipe_scrapers/_schemaorg.py#L20`.
Refer to that file and `https://schema.org/Product` for more information.
"""

import extruct

from scrapers.exc import SchemaOrgException

import enum

SCHEMA_ORG_HOST = "schema.org"

SYNTAXES = ["json-ld", "microdata"]


class SchemaOrg:
    @staticmethod
    def _contains_schematype(item, schematype):
        itemtype = item.get("@type", "")
        itemtypes = itemtype if isinstance(itemtype, list) else [itemtype]
        return schematype.lower() in "\n".join(itemtypes).lower()

    def _find_entity(self, item, schematype):
        if self._contains_schematype(item, schematype):
            return item
        for graph_item in item.get("@graph", []):
            if self._contains_schematype(graph_item, schematype):
                return graph_item

    def __init__(self, page_data, raw=False):
        if raw:
            self.format = "raw"
            self.data = page_data
            self.product = {}
            self.ratingsdata = {}
            return
        self.format = None
        self.data = {}
        self.product = {}
        self.ratingsdata = {}

        data = extruct.extract(
            page_data,
            syntaxes=SYNTAXES,
            errors="log",
            uniform=True,
        )

        # Extract product references
        for syntax in SYNTAXES:
            syntax_data = data.get(syntax, [])
            for item in syntax_data:
                if product := self._find_entity(item, "Product"):
                    key = product.get("sku") or product.get("gtin13")
                    if key:
                        self.product[key] = product
                        self.format = syntax
                        self.data = product


class SchemaOrgAvail(enum.Enum):
    """Availability enumeration."""

    IN_STOCK = "InStock"
    OUT_OF_STOCK = "OutOfStock"
    PRE_ORDER = "PreOrder"
    IN_STORE_ONLY = "InStoreOnly"
    ONLINE_ONLY = "OnlineOnly"
    SOLD_OUT = "SoldOut"
    DISCONTINUED = "Discontinued"
    LIMITED_AVAILABILITY = "LimitedAvailability"
    BACK_ORDER = "BackOrder"
    PRE_SALE = "PreSale"


class SchemaOrgDelivery(enum.Enum):
    LOCKER_DELIVERY = "LockerDelivery"
    ON_SITE_PICKUP = "OnSitePickup"
    PARCEL_SERVICE = "ParcelService"
