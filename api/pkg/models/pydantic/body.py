from typing import Literal, Optional
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.networks import AnyUrl
from pydantic_core import Url

from api.configuration.as_form import as_form
from api.pkg.models.pydantic import QueryModel


class UserBaseFields(BaseModel):
    """Базовые поля для пользователя"""

    username: EmailStr = Field(examples=["example@example.com"])
    nickname: str = Field(
        examples=["nickname"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
    password: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
    first_name: str
    last_name: str


@as_form
class UserRegister(UserBaseFields):
    """Класс данных для регистрации"""

    password_repeat: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )


@as_form
class UserUpdate(UserBaseFields):
    """Класс для обновления данных о пользователе

    Args:
        BaseModel (_type_): _description_
    """

    about: str
    location: int
    avatar: UploadFile


@as_form
class UserActivate(BaseModel):
    username: str
    code: int


@as_form
class PostCreate(BaseModel):
    """Класс полей для создания поста"""

    region: int
    tourist_type: int
    name: str
    header: str
    body: str
    lat: float
    long: float
    link: str


@as_form
class PostComment(BaseModel):
    """Класс полей для создания комментария"""

    post_id: UUID
    responding_to: int | None = None
    contents: str


@as_form
class PostDraft(BaseModel):
    """Класс полей для пометки поста как черновик"""

    id: UUID


@as_form
class PostArchive(BaseModel):
    """Класс полей для пометки поста как архивный"""

    id: UUID


class PostSearchQuery(QueryModel):
    """Класс полей для поиска постов по параметру"""

    region_id: Optional[int] = None
    tourism_type: Optional[int] = None
    order_by: Literal["created_at", "rating"]
    way: Literal["asc", "desc"]
    timeframe: Literal["1d", "7d", "30d", "all"]


class UserSearchQuery(QueryModel):
    """Класс полей для поиска пользователя по параметру"""

    region: Optional[int] = None
    rating: Optional[int] = None
    order_by: Literal["created_at", "rating", "location"]
    way: Literal["asc", "desc"]
    age: Literal["30d", "180d", "360d", "all"]
