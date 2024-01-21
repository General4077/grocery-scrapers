import os

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, INET
from sqlalchemy.orm import DeclarativeBase, column_property, mapped_column, relationship

from plutus.scrapers import ScrapeType
from plutus.scrapers.schemaorg import SchemaOrgAvail, SchemaOrgDelivery
from plutus.typing import Result as ResultDTO

ACTIVE_STATUS_ENUM = ENUM("ACTIVE", "INACTIVE", name="active_status_enum")
SCRAPE_TYPE_ENUM = Enum(ScrapeType)


class Base(DeclarativeBase):
    pass


# TODO: Add indexes
# TODO: postgress Full Text search for matching products


engine = create_engine(os.environ.get("PLUTUS_DB_URI"))



product_to_link_table = Table(
    "plutus_product_links",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("plutus_products.id")),
    Column("link_id", Integer, ForeignKey("plutus_links.id")),
)


class Link(Base):
    __tablename__ = "plutus_links"

    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String, nullable=False, unique=True)
    type = mapped_column(SCRAPE_TYPE_ENUM, nullable=False)
    active = mapped_column(ACTIVE_STATUS_ENUM, nullable=False, server_default="ACTIVE")
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    products = relationship(
        "Product",
        secondary=product_to_link_table,
        back_populates="links",
    )


class Result(Base):
    __tablename__ = "plutus_results"
    __table_args__ = {
        "postgresql_partition_by": "RANGE (created_at)",
    }

    id = mapped_column(Integer, primary_key=True)
    url = mapped_column(String)
    # ip = mapped_column(INET, nullable=False) TODO: Fix when transitioning to postgres
    ip = mapped_column(String, nullable=False)
    link_id = mapped_column(ForeignKey("plutus_links.id"), nullable=False, index=True)
    price = mapped_column(Float, nullable=True)
    sale_price = mapped_column(Float, nullable=True)
    availability = mapped_column(Enum(SchemaOrgAvail), nullable=True)
    pickup = mapped_column(Enum(SchemaOrgDelivery), nullable=True)
    source = mapped_column(Text, nullable=True)
    status_code = mapped_column(Integer, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())


class LinkStatistics(Base):
    __tablename__ = "plutus_link_statistics"

    link_id = mapped_column(ForeignKey("plutus_links.id"), primary_key=True)
    link_count = mapped_column(
        Integer, nullable=False, default=os.environ.get("PLUTUS_LINK_COUNT_DEFAULT", 1)
    )
    churn = mapped_column(
        Integer, nullable=False, default=os.environ.get("PLUTUS_CHURN_DEFAULT", 100)
    )
    failed_count = mapped_column(Integer, nullable=False, default=0)
    no_delta_count = mapped_column(
        Integer, nullable=False, default=0
    )  # Number of times since the price/availability has changed
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    failed_ratio = column_property(
        failed_count / os.environ.get("PLUTUS_FAILURE_DENOMINATOR", 1)
    )

    # @property
    # def failed_ratio(self):
    #     return self.failed_count / os.environ.get("PLUTUS_FAILURE_DENOMINATOR", 1)


class Product(Base):
    __tablename__ = "plutus_products"

    id = mapped_column(Integer, primary_key=True)
    links = relationship(
        "Link",
        secondary=product_to_link_table,
        back_populates="products",
    )
    # TODO


class LinkProductInfo(Base):
    __tablename__ = "plutus_link_product_info"

    link_id = mapped_column(ForeignKey("plutus_links.id"), primary_key=True)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    brand = mapped_column(String, nullable=True)
    sku = mapped_column(String, nullable=True)
    model_number = mapped_column(String, nullable=True)
    gtin = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class ScraperStats(Base):
    __tablename__ = "plutus_client_statistics"

    id = mapped_column(Integer, primary_key=True)
    # ip = mapped_column(INET, nullable=False) TODO: Fix when transitioning to postgres
    ip = mapped_column(String, nullable=False)
    total_runs = mapped_column(Integer, nullable=False, default=0)
    total_failures = mapped_column(Integer, nullable=False, default=0)
    status = mapped_column(ACTIVE_STATUS_ENUM, nullable=False, default="ACTIVE")
