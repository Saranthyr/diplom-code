from redis.asyncio import Redis as RedisSess
from random import randint

class Redis:
    def __init__(self, redis_conn: RedisSess) -> None:
        self.conn = redis_conn

    async def get_code(self, key: str) -> int:
        return await self.conn.get(key)

    async def remove_code(self, key: str) -> int:
        return await self.conn.delete(key)

    async def generate_tg_code(self, key: str) -> str:
        code = []
        for _ in range(0,6):
            code.append(str(randint(0,9)))
        code = ''.join(code)
        await self.conn.set(code, key)
        return code