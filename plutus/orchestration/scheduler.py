import os
import time
from typing import Optional

from redis import Redis
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from plutus.orchestration.models.links import Link, LinkStatistics, Result, engine
from plutus.queues import RedisQueue
from plutus.scrapers import ScrapeType
from plutus.typing import CrawlTodo
from plutus.typing import Result as ResultDTO

QUEUE_THRESHOLD = os.environ.get("PLUTUS_QUEUE_THRESHOLD", 100)


def scheduler():
    """Main scheduler function.

    This function is responsible for scheduling the execution of the
    different components of the system.
    """
    redis = Redis(
        host=os.environ.get("PLUTUS_REDIS_HOST"),
        port=6379,
        db=0,
        password=os.environ.get("PLUTUS_REDIS_PASSWORD", ""),
    )
    push_queue = RedisQueue(redis, "plutus:incoming:queue")
    results_queue = RedisQueue(redis, "plutus:results:queue")
    queue_memory = (
        []
    )  # TODO: Find a better way to prevent duplicate links from being queued
    initialize()  # push intial commands/configs
    while True:
        q_size = len(push_queue)
        queue_memory[q_size - 1 :]
        if q_size < QUEUE_THRESHOLD:
            prospect_links = get_links_to_queue(QUEUE_THRESHOLD - q_size)
            to_queue = list(set(prospect_links).difference(set(queue_memory)))
            push_queue.extend(to_queue)
            queue_memory.extend(to_queue)
        while len(results_queue) > 0:
            result = results_queue.pop()
            process_result(result)
        commands = anlytics()
        if commands:
            publish_commands(commands)
        notify()  # alert me if something is wrong
        time.sleep(5)


def get_links_to_queue(limit: int = QUEUE_THRESHOLD):
    """Get links to queue.

    This function is responsible for getting links to queue.
    """
    with Session(engine) as session:
        links = session.execute(
            select(Link.url, Link.id, Link.type, func.max(Result.created_at))
            .join(LinkStatistics, isouter=True)
            .join(Result, isouter=True)
            .where(
                Link.active == True,
                or_(Result.created_at < func.current_date(), Result.id == None),
            )
            .group_by(Link.id)
            .order_by(
                (LinkStatistics.churn / LinkStatistics.link_count)
                / (func.current_date() - func.max(Result.created_at))
                - (
                    LinkStatistics.failed_ratio
                    * (func.current_date() - func.max(Result.created_at))
                ),
                Link.type,
            )
            .limit(limit)
        )
        return [
            CrawlTodo(type=link.type.value, url=link.url, link_id=link.id)
            for link in links
        ]


# churn/link_count (days since last crawl) - failed_ratio (.5 * days since last crawl) - # TODO how to apply this: no_delta_ratio (.5 * days since last crawl)


def process_result(result: ResultDTO):
    """Process result.

    This function is responsible for processing results.
    """
    with Session(engine) as session:
        current_result = Result.from_result(result)
        current_result.links = [
            *get_or_create_links(
                session=session, links=result["targets"], type_=ScrapeType.PRODUCT
            ),
            *get_or_create_links(
                session=session, links=result["spiderables"], type_=ScrapeType.SPIDER
            ),
        ]
        last_result = get_the_last_result(session=session, link_id=result["link_id"])
        link_stats = get_or_create_link_stats(
            session=session, link_id=result["link_id"]
        )
        link_stats.churn = (
            len(
                set([l.url for l in current_result.links]).symmetric_difference(
                    set([l.url for l in last_result.links])
                )
            )
            if last_result
            else 0
        )
        link_stats.link_count = len(result["targets"]) + len(result["spiderables"])
        link_stats.failed_count = link_stats.failed_count + (
            1 if result["status_code"] >= 200 and result["status_code"] < 300 else 0
        )
        link_stats.no_delta_count = link_stats.no_delta_count + (
            1 if last_result and last_result.price == result["price"] else 0
        )
        session.add(current_result)
        session.add(link_stats)
        # TODO: LinkProduct info

        session.commit()


def anlytics():
    """Analytics.

    This function is responsible for generating analytics.
    """
    pass


def publish_commands(commands):
    """Publish commands.

    This function is responsible for publishing commands.
    """
    pass


def notify():
    """Notify.

    This function is responsible for notifying.
    """
    pass


def initialize():
    """Initialize.

    This function is responsible for initializing.
    """
    pass


def get_or_create_links(
    session: Session, links: list[str], type_: ScrapeType
) -> list[Link]:
    """Get or create links.

    This function is responsible for getting or creating links.

    Args:
        session (Session): SQLAlchemy session
        links (list[str]): List of links
        type_ (ScrapeType): Type of link

    Returns:
        list[Link]: List of links
    """
    existing_links = next(
        zip(
            *session.execute(select(Link).where(Link.url.in_(links))).all()
        ),  # next(zip(...)) ensures that this returns a single tuple containing all the models
        (),
    )
    new_links = set(links) - set([link.url for link in existing_links])
    new_mdls = tuple(Link(url=link, type=type_) for link in new_links)
    session.add_all(new_mdls)
    return existing_links + new_mdls


def get_or_create_link_stats(session: Session, link_id: str) -> LinkStatistics:
    """Get or create link statistics.

    This function is responsible for getting or creating link statistics model.
    NOTE: This function does not add the model to the session.

    Args:
        session (Session): SQLAlchemy session
        link_id (str): Link ID

    Returns:
        LinkStatistics: Link statistics
    """
    try:
        return session.execute(
            select(LinkStatistics).where(LinkStatistics.link_id == link_id)
        ).first()[0]
    except (IndexError, TypeError):
        return LinkStatistics(link_id=link_id, failed_count=0, no_delta_count=0)


def get_the_last_result(session: Session, link_id: str) -> Optional[Result]:
    """Get the last result.

    This function is responsible for getting the last result.

    Args:
        session (Session): SQLAlchemy session
        link_id (str): Link ID

    Returns:
        Result: Result
    """
    with suppress(IndexError, TypeError):
        return session.execute(
            select(Result)
            .where(Result.link_id == link_id)
            .order_by(Result.created_at.desc())
            .limit(1)
        ).first()[0]
