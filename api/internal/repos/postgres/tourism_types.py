from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import TourismType


class TourismTypeRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(TourismType.id, TourismType.name, TourismType.photo).where(
                TourismType.id == id
            )
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def read_all(self):
        async with self.session_factory() as s:
            stmt = select(TourismType.id, TourismType.name, TourismType.photo)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def search(self, q):
        async with self.session_factory() as s:
            stmt = select(TourismType.id, TourismType.name, TourismType.photo).where(
                TourismType.name.ilike(f"%{q}%")
            )
            res = await s.execute(stmt)
            return res.mappings().all()
