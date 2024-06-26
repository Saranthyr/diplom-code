from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.repos.postgres.tourism_types import TourismTypeRepository
from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token


class TourismService:
    def __init__(self, tourism_repo: TourismTypeRepository) -> None:
        self.repository = tourism_repo

    async def read_all(self):
        return await self.repository.read_all()

    async def read(self, id):
        return await self.repository.read(id)

    async def search(self, s):
        return await self.repository.search(s)
