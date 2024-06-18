from datetime import timedelta
from uuid import UUID, uuid4

from passlib.context import CryptContext

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
        if password != password_repeat:
            raise PasswordsNotMatch
        password = pwd_context.hash(password)
        if await self.repository.read_by_username(username) is not None:
            raise UsernameInUse
        elif await self.repository.read_id_by_nickname(nickname) is not None:
            raise NicknameInUse
        # try:
        return await self.repository.create(
            uid=uuid4(),
            username=username,
            password=password,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        # except Exception:
        #     raise BaseAPIException

    async def read_by_username(self, username: str):
        user = await self.repository.read_by_username(username)
        return user

    async def gentoken(self, user, password: str):
        if pwd_context.verify(password, user["password"]):
            jti = str(uuid4())
            data_access = {"sub": str(user["id"]), "jti": jti, "role": user["role"]}
            data_refresh = {"sub": jti}
            access_token = await create_token(
                data_access, expires_delta=timedelta(hours=1)
            )
            refresh_token = await create_token(
                data_refresh, expires_delta=timedelta(days=30)
            )
            return TokenResponse(access_token=access_token, refresh_token=refresh_token)

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
        decoded = await decode_token(token)
        id = UUID(decoded["sub"])
        password = pwd_context.hash(password)
        return await self.repository.update(
            id,
            username,
            password,
            nickname,
            first_name,
            last_name,
            about,
            location,
            link_telegram,
        )

    async def update_user_avatar(self, token, uid):
        decoded = await decode_token(token)
        id = UUID(decoded["sub"])
        return await self.repository.update_avatar(id, uid)

    async def update_user_header(self, token, uid):
        decoded = await decode_token(token)
        id = UUID(decoded["sub"])
        return await self.repository.update_header(id, uid)

    async def delete_user(self, token):
        decoded = await decode_token(token)
        id = UUID(decoded["sub"])
        return await self.repository.delete(id)

    async def read_user(self, data):
        try:
            decoded = await decode_token(data)
            id = UUID(decoded["sub"])
        except Exception:
            id = await self.repository.read_id_by_nickname(data)
        return await self.repository.read(id)

    async def read_all(self, region, rating, order_by, way, age):
        tf = None
        match age:
            case "30d":
                tf = TimeframeEnum.MONTH.value
            case "180d":
                tf = TimeframeEnum.HALFYEAR.value
            case "360d":
                tf = TimeframeEnum.YEAR.value
            case _:
                pass
        if region:
            return await self.repository.read_all_by_region(region, way, order_by, tf)
        if rating:
            return await self.repository.read_all_by_rating(rating, way, order_by, tf)
        return await self.repository.read_all(region, rating, way, order_by, tf)

    async def activate_account(self, username):
        return await self.repository.activate(username)
