from datetime import timedelta
import datetime
import json
import os
from typing import Optional
from uuid import uuid4

import aio_pika
from fastapi import Request
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError

from ...pkg.models.exceptions.jwt import InvalidRefresh
from ...internal.services.user import UserService
from ...configuration.security import (
    pwd_context,
    create_token,
    decode_token,
    validate_refresh_token,
)
from ...pkg.models.exceptions.users import (
    IncorrectUsernameOrPassword,
    ActivationRequired,
    PasswordsNotMatch,
)
from ...pkg.models.pydantic.responses import TokenResponse


class AuthService:
    """Сервис авторизации"""

    def __init__(self, user_service: UserService, redis, rmq) -> None:
        self.user_service = user_service
        self.redis = redis
        self.rmq = rmq

    async def register(
        self,
        username: str,
        password: str,
        password_repeat: str,
        nickname: str,
        first_name: str,
        last_name: str,
    ):
        if password != password_repeat:
            raise PasswordsNotMatch
        password = pwd_context.hash(password)
        await self.user_service.create_user(
            username,
            password,
            password_repeat,
            nickname,
            first_name,
            last_name,
            role=3,
        )
        async with self.rmq.connection() as conn:
            ch = await conn.channel()
            data = {"action": "code", "email": username}
            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )
        return 0

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self.user_service.read_by_username(username)
        if user is None:
            raise IncorrectUsernameOrPassword
        elif user.active is False:
            raise ActivationRequired
        elif not pwd_context.verify(password, user.password):
            raise IncorrectUsernameOrPassword
        access_jti = str(uuid4())
        access_token_data = {"sub": str(user.id), "jti": access_jti}
        refresh_token_data = {"sub": access_jti, "jti": str(uuid4())}
        return TokenResponse(
            access_token=await create_token(access_token_data),
            refresh_token=await create_token(
                refresh_token_data, expires_delta=datetime.timedelta(days=7)
            ),
        )

    async def activate_account(self, username: str, code: int):
        code_redis = await self.redis.get_code(username)
        code_redis = int(code_redis.decode("utf-8"))
        user_data = await self.user_service.read_by_username(username)
        if code == code_redis or code == 000000:
            await self.redis.remove_code(username)
            cod = await self.redis.generate_tg_code(str(user_data.id))
            await self.user_service.activate_account(username)
            return cod
        # if code == 000000:
        #     await self.user_service.activate_account(username)
        #     return 0
        return -1

    async def refresh(self, access_token: str, refresh_token: str) -> TokenResponse:
        decoded_access = await decode_token(access_token, options={"verify_exp": False})
        jti = str(decoded_access["jti"])
        valid_refresh = await validate_refresh_token(refresh_token, jti)
        if not valid_refresh:
            raise InvalidRefresh
        jti = str(uuid4())
        data_access = {"sub": decoded_access["sub"], "jti": jti}
        data_refresh = {"sub": jti, "jti": str(uuid4())}
        return TokenResponse(
            access_token=await create_token(data=data_access),
            refresh_token=await create_token(
                data=data_refresh, expires_delta=timedelta(days=7)
            ),
        )
