from datetime import timedelta
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.services.files import FileService
from api.internal.services.notification import NotificationService
from api.internal.services.user import UserService
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
from api.pkg.models.pydantic.responses import TokenResponse, UserResponse


class UserMainService:
    def __init__(
        self,
        user_service: UserService,
        file_service: FileService,
        notification_service: NotificationService,
    ) -> None:
        self.user_service = user_service
        self.file_service = file_service
        self.notication_service = notification_service

    async def update_base(
        self, token, nickname, first_name, last_name, about, location, link_tg
    ):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        return await self.user_service.update_user(
            curr_user, nickname, first_name, last_name, about, location, link_tg
        )

    async def update_password(self, token, password, new_password, new_password_repeat):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        if new_password != new_password_repeat:
            raise PasswordsNotMatch
        return await self.user_service.update_password(
            curr_user, password, new_password
        )

    async def update_avatar(self, token, avatar):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        id = await self.file_service.create_file(avatar)
        return await self.user_service.update_avatar(curr_user, id)

    async def delete_avatar(
        self,
        token,
    ):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        return await self.file_service.delete_file(
            (await self.user_service.read(curr_user))["avatar"]
        )

    async def update_header(self, token, header):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        id = await self.file_service.create_file(header)
        return await self.user_service.update_header(curr_user, id)

    async def delete_header(
        self,
        token,
    ):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        return await self.file_service.delete_file(
            (await self.user_service.read(curr_user))["header"]
        )

    async def notification_channel_get(
        self,
        token,
    ):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        res = [1]
        if await self.notication_service.available(curr_user) is True:
            res.append(2)
        return res

    async def notification_channel_post(self, token, channel):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        return await self.user_service.change_channel(curr_user, channel)

    async def delete(self, token):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        return await self.user_service.delete(curr_user)

    async def read(self, token):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        data = await self.user_service.read(curr_user)

        res = UserResponse(**data)

        if data["avatar"] is not None:
            res.avatar = (await self.file_service.read_file(data["avatar"]))["url"]

        if data["header"] is not None:
            res.header = (await self.file_service.read_file(data["header"]))["url"]

        return res

    async def read_nickname(self, nickname):
        return await self.user_service.read_by_nickname(nickname)
