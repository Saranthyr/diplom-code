from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import File


class FileRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(self, file, filename):
        async with self.session_factory() as s:
            file = File(content=file, name=filename)
            s.add(file)
            await s.commit()
            await s.refresh(file)
            return file.id

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(File).where(File.id == id)
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def delete(self, id):
        async with self.session_factory() as s:
            stmt = delete(File).where(File.id == id)
            await s.execute(stmt)
            return 0
