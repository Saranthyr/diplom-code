from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token


class HashtagService:
    def __init__(self, hashtag_repo) -> None:
        self.repository = hashtag_repo

    async def read_all(self):
        return await self.repository.read_all()
