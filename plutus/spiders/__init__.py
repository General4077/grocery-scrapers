from plutus.spiders.builtin_spiders import *

from plutus.spiders.abstract import AbstractSpider, Spider


def spider_registry() -> dict[str, Spider]:
    """Returns a registry of all spiders.

    Returns:
        dict: A dictionary of all spiders.
    """
    return {cls.host: cls for cls in AbstractSpider.__subclasses__()}
