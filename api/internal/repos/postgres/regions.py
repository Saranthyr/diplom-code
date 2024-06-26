from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import Region


class RegionRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(
                Region.id,
                Region.name,
                Region.description,
                Region.longitude,
                Region.latitude,
                Region.thumbnail,
            ).where(Region.id == id)
            res = await s.execute(stmt)
            res = res.mappings().first()
            return res

    async def read_all(self):
        async with self.session_factory() as s:
            stmt = select(Region.id, Region.name)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def search(self, q):
        async with self.session_factory() as s:
            stmt = select(
                Region.id, Region.name, Region.thumbnail, Region.description
            ).where(Region.name.ilike(f"%{q}%"))
            res = await s.execute(stmt)
            return res.mappings().all()
