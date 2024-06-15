from redis.asyncio import Redis as RedisSess


class Redis:
    def __init__(self, conn: RedisSess) -> None:
        self.conn = conn

    async def set_code(self, key: str, val: str) -> int:
        await self.conn.set(key, val, 3600)
        return 0
