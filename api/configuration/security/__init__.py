from datetime import timedelta, datetime
import os
import time
from typing import Dict, Tuple

from dotenv import load_dotenv
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from api.pkg.models.exceptions.users import NoPermission


load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


async def create_token(
    data: dict,
    key: str = os.environ["JWT_SECRET"],
    expires_delta: timedelta = timedelta(hours=1),
) -> str:
    """Функция создания токена

    Args:
        data (dict): полезная нагрузка токена
        key (str, optional): секретный ключ, по умолчанию используется переменная среды JWT_SECRET
        expires_delta (timedelta, optional): время действия токена

    Returns:
        str: Access токен
    """
    data["iat"] = int(time.time())
    data["exp"] = int(
        datetime.timestamp(datetime.fromtimestamp(data["iat"]) + expires_delta)
    )
    token = jwt.encode(data, key, algorithm="HS384")
    return token


async def decode_token(token: str) -> Dict[str, int | str]:
    """Функция декодирования токена

    Args:
        token (str): токен для декодирования

    Returns:
        Dict[str, int|str]: Полезная нагрузка токена
    """
    decoded = jwt.decode(token, "str", algorithms="HS384")
    return decoded


async def validate_token_iat(token: str) -> Tuple[bool, Dict[str, int | str]]:
    """Функция проверки токена на действительность

    Args:
        token (str): токен

    Returns:
        Tuple[bool, Dict[str, int|str]]: результат декодирования и полезная нагрузка
    """
    decoded = await decode_token(token=token)
    exp = int(decoded["exp"])
    if (exp - datetime.now().timestamp()) < 0:
        return (False, decoded)
    return (True, decoded)


async def validate_access_token(token: str) -> bool:
    """Функция валидации токена доступа (Access)

    Args:
        token (str): токен

    Returns:
        bool: результат проверки
    """
    valid, _ = await validate_token_iat(token=token)
    if valid:
        return True
    return False


async def validate_refresh_token(token: str, access_jti: str) -> bool:
    """Функция валидации токена обновления (Refresh)

    Args:
        token (str): токен
        access_jti (str): идентификатор токена доступа

    Returns:
        bool: результат проверки
    """
    valid, decoded = await validate_token_iat(token=token)
    if valid:
        if decoded["name"] == access_jti:
            return True
    return False


async def validate_user_role(token: str, required_role: list[int]) -> bool:
    """Функция проверки роли пользователя

    Args:
        token (str): токен
        required_role (list[int]): допустимые роли

    Raises:
        NoPermission: возвращает ошибку, если пользователь не имеет доступа

    Returns:
        bool: пользователь имеет доступ
    """
    decoded = await decode_token(token=token)
    if decoded["role"] not in required_role:
        raise NoPermission
    return True
