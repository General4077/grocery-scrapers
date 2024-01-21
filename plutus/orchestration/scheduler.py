import os
import time

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
                Link.active == "ACTIVE",
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


def process_result(result):
    """Process result.

    This function is responsible for processing results.
    """
    pass


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
