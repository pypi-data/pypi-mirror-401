import time
from contextlib import contextmanager
from typing import Final, Generator, Optional


class RateLimitExceeded(Exception):
    pass


try:
    from redis import Redis

    class RateLimiter:
        """
        Distributed rate limiter using Redis sliding window algorithm.

        Limits the number of operations within a time window across all workers.
        Uses Redis sorted sets with Lua scripting for atomic operations. Based on:
        https://redis.io/tutorials/develop/java/spring/rate-limiting/fixed-window/reactive-lua/

        Example::

            limiter = RateLimiter(redis)

            with limiter.limit('ratelimit:api', limit=100, window_seconds=60):
                call_api()
        """

        _SLIDING_WINDOW_LUA: Final = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local limit = tonumber(ARGV[3])
        local ttl = tonumber(ARGV[4])

        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

        local count = redis.call('ZCARD', key)

        if count >= limit then
            return 0
        end

        redis.call('ZADD', key, now, now .. ':' .. math.random(1000000))
        redis.call('EXPIRE', key, ttl)

        return 1
        """

        def __init__(self, redis_client: Redis) -> None:
            """
            :param redis_client: Redis client instance
            """
            self._script = redis_client.register_script(self._SLIDING_WINDOW_LUA)

        @contextmanager
        def limit(
            self,
            key_name: str,
            limit: int,
            window_seconds: int,
            ttl: Optional[int] = None,
        ) -> Generator[None, None, None]:
            """
            :param key_name: Unique key for this rate limit (e.g., 'ratelimit:my_task')
            :param limit: Maximum number of operations allowed in the window
            :param window_seconds: Time window in seconds
            :param ttl: Key expiration in seconds (defaults to window_seconds * 2)
            :raises RateLimitExceeded: When the rate limit has been exceeded
            """
            if ttl is None:
                ttl = window_seconds * 2

            now = time.time()

            allowed = self._script(keys=[key_name], args=[now, window_seconds, limit, ttl])
            if not allowed:
                raise RateLimitExceeded()

            try:
                yield
            except Exception:
                raise

except ModuleNotFoundError:
    pass
