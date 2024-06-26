from datetime import timedelta
import os
from typing import Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.repos.postgres.ratings import RatingRepository
from api.pkg.models.base.enums import TimeframeEnum
from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.exceptions import (
    IncorrectUsernameOrPassword,
    NicknameInUse,
    PasswordsNotMatch,
    UsernameInUse,
    IncorrectCurrentPassword,
    UserNotFound,
    MissingCurrentPassword,
)
from api.configuration.security import (
    decode_token,
)
from api.pkg.models.pydantic.responses import TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RatingService:
    def __init__(self, ratings_repo: RatingRepository) -> None:
        self.repository = ratings_repo

    async def create(self, post_id, user_id, rating):
        return await self.repository.create(post_id, user_id, rating)

    async def read(self, post_id, user_id):
        return await self.repository.read(post_id, user_id)

    async def read_all_for_post(self, id):
        return await self.repository.read_all(id)

    async def read_count(self, id):
        return await self.repository.read_count(id)

    async def read_total(self, id):
        res = await self.repository.read_total(id)
        if res is None:
            return 0
        return res

    async def delete(self, id, user_id):
        return await self.repository.delete(id, user_id)
