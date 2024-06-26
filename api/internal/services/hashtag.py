from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.repos.postgres.hashtags import HashtagRepository
from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token


class HashtagService:
    def __init__(self, hashtag_repo: HashtagRepository) -> None:
        self.repository = hashtag_repo

    async def read_all(self):
        return await self.repository.read_all()

    async def read(self, id):
        return await self.repository.read(id)
