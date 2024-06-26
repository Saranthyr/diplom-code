from re import L
from typing import Literal, Optional
from uuid import UUID
import uuid
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.networks import AnyUrl
from pydantic_core import Url

from api.configuration.as_form import as_form
from api.internal.routes import tourism
from api.pkg.models.pydantic import QueryModel


class UserBaseFields(BaseModel):
    """Базовые поля для пользователя"""

    username: EmailStr = Field(examples=["example@example.com"])
    nickname: str = Field(
        examples=["nickname"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
    first_name: str
    last_name: str


@as_form
class UserRegister(UserBaseFields):
    """Класс данных для регистрации"""

    password: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
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


class UserPasswordUpdate(BaseModel):
    current_password: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
    new_password: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )
    new_password_repeat: str = Field(
        examples=["password"], pattern=r"[\w!?-]+", min_length=6, max_length=32
    )


@as_form
class UserActivate(BaseModel):
    username: str
    code: int


@as_form
class PostCreate(BaseModel):
    """Класс полей для создания поста"""

    region: int
    tourism_type: int
    name: str
    header: str
    longitude: float | None = Field(None)
    latitude: float | None = Field(None)
    link: str | None = Field(None)
    body: str
    draft: bool = Field(False)


@as_form
class PostUpdate(BaseModel):
    id: uuid.UUID
    region: int
    tourism_type: int
    name: str
    header: str
    longitude: float | None = Field(None)
    latitude: float | None = Field(None)
    link: str | None = Field(None)
    body: str


class PostHashtagCreateDelete(BaseModel):
    id: uuid.UUID
    tag: int


@as_form
class PostComment(BaseModel):
    """Класс полей для создания комментария"""

    post_id: UUID
    responding_to: int | None = None
    contents: str


class PostRate(BaseModel):
    id: uuid.UUID
    rating: float


class SearchQueryParams(BaseModel):
    s: str = Field("", description="Search string")
    # way: Literal["asc", "desc"] = Field("desc", description="sort order")
    typ: Literal["1", "2", "3", "4"] = Field(
        "1",
        description="Search type; 1 - posts, 2 - regions, 3 - tourism_types, 4 - users",
    )
    # order_by: Literal["created_at", "rating", "nickname", "name"] = Field(
    #     "created_at", description="Sort by"
    # )
    # region: list[int] = Field([], description="Search posts by region; default is ANY")
    # rating: float | None = Field(
    #     None,
    #     description="Seach posts by rating (must be higher or equal); default is ANY",
    # )
    # tourism_type: list[int] = Field(
    #     [], description="Search posts by tourism type; default is ANY"
    # )
    # author: list[uuid.UUID] = Field(
    #     [], description="Search posts by author; default is ANY"
    # )


class SearchQueryPostParams(BaseModel):
    q: str = Field("", description="Search string")
    order_by: Literal["created_at", "rating", "nickname", "name"] = Field(
        "created_at", description="Sort by"
    )
    region: list[int] = Field([], description="Search posts by region; default is ANY")
    rating: float | None = Field(
        0,
        description="Seach posts by rating (must be higher or equal); default is ANY",
    )
    tourism_type: list[int] = Field(
        [], description="Search posts by tourism type; default is ANY"
    )
    author: list[uuid.UUID] = Field(
        [], description="Search posts by author; default is ANY"
    )
    way: Literal["asc", "desc"] = Field("desc", description="sort order")
    page: int = Field(1)
    approved: list[int] = Field(
        [],description='Approval status'
    )
    draft: bool = Field(False, description='Search for drafted posts')
    archived: bool = Field(False, description="Search for archived posts")
