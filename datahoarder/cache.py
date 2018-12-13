from cachetools import cached, TTLCache

cache = TTLCache(maxsize=100, ttl=172800)
