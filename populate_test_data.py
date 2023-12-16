import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from plutus.orchestration.models.links import Link
from plutus.scrapers import ScrapeType

engine = create_engine(os.environ["PLUTUS_DB_URI"])


def func():
    with Session(engine) as session:
        session.add(
            Link(
                url="https://www.walmart.com/ip/Great-Value-Whole-Vitamin-D-Milk-Gallon-128-fl-oz/10450114?athbdg=L1200&from=/search",
                type=ScrapeType.PRODUCT,
            )
        )
        session.commit()


if __name__ == "__main__":
    func()
