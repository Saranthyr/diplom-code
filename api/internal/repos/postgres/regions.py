from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import Region


class RegionRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(self, name, long, lat):
        async with self.session_factory() as s:
            region = Region(
                name=name, coordinates_longitude=long, coordinates_latitude=lat
            )
            s.add(region)
            await s.commit()
            return 0

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(Region).where(Region.id == id)
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def read_all(self):
        async with self.session_factory() as s:
            stmt = select(Region)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res
