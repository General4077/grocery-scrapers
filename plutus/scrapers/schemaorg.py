"""Schema.org parser and enumerations for product data.

This is a contrived derivation of `https://github.com/hhursev/recipe-scrapers/blob/main/recipe_scrapers/_schemaorg.py#L20`.
Refer to that file and `https://schema.org/Product` for more information.
"""

import enum

import extruct

from plutus.scrapers.exc import SchemaOrgException

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
                    self.format = syntax
                    self.data = product


class SchemaOrgAvail(enum.Enum):
    """Availability enumeration."""

    InStock = "InStock"
    OutOfStock = "OutOfStock"
    PreOrder = "PreOrder"
    InStoreOnly = "InStoreOnly"
    OnlineOnly = "OnlineOnly"
    SoldOut = "SoldOut"
    Discontinued = "Discontinued"
    LimitedAvailability = "LimitedAvailability"
    BackOrder = "BackOrder"
    PreSale = "PreSale"

    def __str__(self):
        return self.value


class SchemaOrgDelivery(enum.Enum):
    LockerDelivery = "LockerDelivery"
    OnSitePickup = "OnSitePickup"
    ParcelService = "ParcelService"

    def __str__(self) -> str:
        return self.value
