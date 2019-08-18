from redis import Redis

__all__ = (
    'RedisSortedSet',
)


class RedisSortedSet:
    def __init__(self, redis: Redis, key: str, withscores: bool = False, desc: bool = False):
        """
        A queryset wrapper for redis sorted sets

        :param redis: redis-py client instance
        :param key:
        :param withscores:
        :param desc:
        """

        self.redis: Redis = redis
        self.key: str = key
        self.withscores: bool = withscores
        self.desc: bool = desc

    def __len__(self) -> int:
        return self.redis.zcard(self.key)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.redis.zrange(self.key, item.start, item.stop - 1, desc=self.desc, withscores=self.withscores)
