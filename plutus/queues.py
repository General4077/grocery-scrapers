"""Queue data structure."""

import json
from typing import Any, Protocol


class QueueProtocol(Protocol):
    def push(self, item: Any) -> None:
        ...

    def pop(self) -> Any:
        ...

    def __len__(self) -> int:
        ...


class RedisQueue(QueueProtocol):
    """Redis-backed queue."""

    def __init__(self, redis, key: str):
        self.redis = redis
        self.key = key

    def push(self, item: Any) -> None:
        """Push an item onto the queue.

        Item must be JSON serializable.

        Args:
            item (Any): The item to push onto the queue.
        """
        self.redis.rpush(self.key, json.dumps(item))

    def pop(self) -> Any:
        """Pop an item from the queue."""
        item = self.redis.lpop(self.key)
        if item is None:
            return None
        return json.loads(item)

    def extend(self, items: list[Any]) -> None:
        """Push a list of items onto the queue.

        Items must be JSON serializable. If items is empty, this method does nothing.

        Args:
            items (list[Any]): The items to push onto the queue.
        """
        if items:
            self.redis.rpush(self.key, *map(json.dumps, items))

    def __len__(self) -> int:
        """Return the length of the queue."""
        return self.redis.llen(self.key)
