from datetime import timedelta
import json
import os
from typing import Optional
from uuid import uuid4

import aio_pika
from fastapi import Request
from fastapi.responses import RedirectResponse

from api.configuration.security import (
    create_token,
    decode_token,
    validate_refresh_token,
)
from api.pkg.models.exceptions import InvalidRefresh
from api.pkg.models.exceptions.users import (
    IncorrectUsernameOrPassword,
    ActivationRequired,
)
from api.pkg.models.pydantic.responses import TokenResponse


class AuthService:
    """Сервис авторизации"""

    def __init__(self, user_service, redis, rmq) -> None:
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
        role: int = 3,
    ):
        """Функция регистрации

        Args:
            username (str): имя пользователя - почта
            password (str): пароль
            password_repeat (str): повтор пароля
            nickname (str): никнейм
            first_name (str): имя
            last_name (str): фамилия
            role (int): роль пользователя

        Returns:
            int: 0 в случае успеха, при столкновении с проблемой вызывает ошибку с базовым классом BaseHTTPException
        """
        await self.user_service.create_user(
            username,
            password,
            password_repeat,
            nickname,
            first_name,
            last_name,
            role=role,
        )
        async with self.rmq.connection() as conn:
            ch = await conn.channel()
            data = {"action": "code", "email": username}
            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )
        return 0

    async def generate_code(self, username: str):
        async with self.rmq.connection() as conn:
            ch = await conn.channel()
            data = {"action": "code", "email": username}
            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )

    async def login(self, username: str, password: str) -> TokenResponse:
        """Функция авторизации

        Args:
            username (str): почта
            password (str): пароль

        Returns:
            TokenResponse: комплект из токена доступа и токена обновления
        """
        user = await self.user_service.read_by_username(username)
        if user is None:
            raise IncorrectUsernameOrPassword
        elif user["active"] is False:
            await self.generate_code(username)
            raise ActivationRequired
        return await self.user_service.gentoken(user, password=password)

    async def activate_account(self, username: str, code: int):
        code_redis = await self.redis.get_code(username)
        code_redis = int(code_redis.decode("utf-8"))
        if code == code_redis:
            await self.redis.remove_code(username)
            await self.user_service.activate_account(username)
            return 0
        return -1

    async def refresh(self, access_token: str, refresh_token: str) -> TokenResponse:
        """Функция обновления токена

        Args:
            access_token (str): токен доступа
            refresh_token (str): токен обновления

        Raises:
            InvalidRefresh: недействительный токен обновления

        Returns:
            TokenResponse: новый комплект токенов
        """
        decoded_access = await decode_token(access_token)
        jti = str(decoded_access["jti"])
        valid_refresh = await validate_refresh_token(refresh_token, jti)
        if not valid_refresh:
            raise InvalidRefresh
        jti = str(uuid4())
        data_access = {
            "sub": decoded_access["sub"],
            "jti": jti,
            "role": decoded_access["role"],
        }
        data_refresh = {"sub": decoded_access["sub"], "name": jti}
        return TokenResponse(
            access_token=await create_token(data=data_access),
            refresh_token=await create_token(
                data=data_refresh, expires_delta=timedelta(days=30)
            ),
        )
