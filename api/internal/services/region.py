from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.repos.postgres.regions import RegionRepository
from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token


class RegionService:
    def __init__(self, region_repo: RegionRepository) -> None:
        self.repository = region_repo

    # async def create(self, name, long, lat):
    #     return await self.repository.create(name, long, lat)

    async def read_all(self):
        return await self.repository.read_all()

    async def read(self, id):
        return await self.repository.read(id)

    async def search(self, s):
        return await self.repository.search(s)
