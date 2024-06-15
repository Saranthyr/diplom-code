from datetime import timedelta
from uuid import UUID, uuid4

from passlib.context import CryptContext

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
from api.configuration.security import create_token, decode_token
from api.pkg.models.pydantic.responses import TokenResponse


class UserMainService:
    def __init__(self, user_service, file_service) -> None:
        self.user_service = user_service
        self.file_service = file_service

    async def update_user(
        self,
        token,
        username,
        password,
        nickname,
        first_name,
        last_name,
        about,
        location,
        link_telegram,
    ):
        return await self.user_service.update_user(
            token,
            username,
            password,
            nickname,
            first_name,
            last_name,
            about,
            location,
            link_telegram,
        )

    async def update_user_avatar(self, token, file):
        uid = await self.file_service.create_file(file)
        return await self.user_service.update_user_avatar(token, uid)

    async def update_user_header(self, token, file):
        uid = await self.file_service.create_file(file)
        return await self.user_service.update_user_header(token, uid)

    async def delete_user(self, token):
        return await self.user_service.delete_user(token)

    async def read_user(self, data):
        return await self.user_service.read_user(data)

    async def read_all(self, region, rating, order_by, way, age):
        return await self.user_service.read_all(region, rating, order_by, way, age)
