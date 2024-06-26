from datetime import timedelta
from uuid import UUID, uuid4
import uuid

from pydantic import EmailStr

from api.internal.repos.postgres.users import UserRepository
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
from api.configuration.security import create_token, decode_token, pwd_context
from api.pkg.models.pydantic.responses import TokenResponse


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository = user_repository

    async def create_user(
        self,
        username: str,
        password: str,
        password_repeat: str,
        nickname: str,
        first_name: str,
        last_name: str,
        role: int,
    ):
        return await self.repository.create(
            uid=uuid4(),
            username=username,
            password=password,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

    async def activate_account(self, username):
        return await self.repository.activate_user(username)

    async def update_user(
        self,
        id: uuid.UUID,
        first_name: str,
        last_name: str,
        nickname: str,
        about: str,
        location: int,
        link_tg: str,
    ):
        return await self.repository.update_base(
            id, nickname, first_name, last_name, about, location, link_tg
        )

    async def read_by_username(self, username: EmailStr):
        return await self.repository.read_by_username(username)

    async def read(self, id):
        return await self.repository.read(id)

    async def update_password(self, id, password, new_password):
        data = await self.repository.read(id)
        if pwd_context.verify(password, data.password):
            raise PasswordsNotMatch
        return await self.repository.update_password(id, pwd_context.hash(new_password))

    async def update_avatar(self, uid, avatar):
        return await self.repository.update_avatar(uid, avatar)

    async def update_header(self, uid, header):
        return await self.repository.update_header(uid, header)

    async def delete(
        self,
        uid,
    ):
        return await self.repository.delete(uid)

    async def change_channel(self, uid, ch):
        return await self.repository.change_channel(uid, ch)

    async def read_by_nickname(self, nickname):
        return await self.repository.read_by_nickname(nickname)

    async def search(self, s):
        return await self.repository.search(s)
