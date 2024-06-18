from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class Database:
    """Класс подключения к базе данных"""

    def __init__(self, uri: str):
        """Конструктор

        Args:
            uri (str): адресная ссылка подключения к базе
        """
        self.db_uri = uri
        self.engine = create_async_engine(self.db_uri)
        self.session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Функция генерации сессии подключения к базе данных

        Returns:
            AsyncGenerator[AsyncSession, None]: генератор сессии

        Yields:
            Iterator[AsyncGenerator[AsyncSession, None]]: одиночная сессия
        """
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logging.log(1, f"Session rollback because of exception {e}")
                await session.rollback()
            finally:
                await session.close()
