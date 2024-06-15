from redis.asyncio import Redis as RedisSess


class Redis:
    def __init__(self, redis_conn: RedisSess) -> None:
        self.conn = redis_conn

    async def get_code(self, key: str) -> int:
        return await self.conn.get(key)

    async def remove_code(self, key: str) -> int:
        return await self.conn.delete(key)
