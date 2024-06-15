from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractConnection


class RabbitMQ:
    def __init__(self, uri: str):
        self.uri = uri

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[AbstractConnection, None]:
        connection = await aio_pika.connect_robust(self.uri)
        async with connection as conn:
            try:
                yield conn
            except Exception as e:
                print(e)
