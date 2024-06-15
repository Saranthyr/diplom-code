from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from dependency_injector.resources import Resource
import redis.asyncio as aioredis


class RedisConn(Resource):
    def init(self, uri: str) -> aioredis.Redis:
        redis = aioredis.from_url(uri)
        return redis
