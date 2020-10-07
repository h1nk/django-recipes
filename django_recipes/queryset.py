import pickle

from redis import Redis

__all__ = (
    'RedisSortedSet',
)


class RedisSortedSet:
    """
    A QuerySet wrapper for redis sorted sets

    :param redis: :class:`redis-py client <redis.Redis>` instance
    :param key: Database key of sorted set
    :param withscores: Whether to return the scores of the elements together with the elements
    :param desc: Whether set members should be in descending lexicographical order or not
    """

    def __init__(self, redis: Redis, key: str, withscores: bool = False, desc: bool = False):
        self.redis = redis
        self.key = key
        self.withscores = withscores
        self.desc = desc

    def __len__(self) -> int:
        return self.redis.zcard(self.key)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.redis.zrange(self.key, item.start, item.stop - 1, desc=self.desc, withscores=self.withscores)


class RedisList:
    def __init__(self, *, redis: Redis, key: str, pickled: bool = False):
        self.redis: Redis = redis
        self.key = key
        self.pickled = pickled

    def __len__(self) -> int:
        return self.redis.llen(self.key)

    def __getitem__(self, item):
        if isinstance(item, slice):
            item = self.redis.lrange(self.key, item.start, item.stop - 1)

            return item if not self.pickled else [pickle.loads(i) for i in item]
