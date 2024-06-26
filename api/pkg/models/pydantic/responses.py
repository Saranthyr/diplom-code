import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    username: str
    password: str
    nickname: str
    first_name: str
    last_name: str
    avatar: str | None | UUID
    header: str | None | UUID
    about: str | None
    posts_total: int
    created_at: datetime.datetime
    location: int
    link_tg: str | None
    rating: float


class SearchGlobalResponse(BaseModel):
    res: (
        list["SearchGlobalPost"]
        | list["SearchGlobalRegion"]
        | list["SearchGlobalTourism"]
        | list["SearchGlobalUser"]
    )


class SearchGlobalPost(BaseModel):
    id: UUID
    name: str
    header: str
    thumbnail: str | UUID
    created_at: datetime.datetime
    author: "SearchGlobalPostAuthor | UUID "
    hashtags: list[str] | None = Field(None)
    region: "str | int | SearchGlobalPostRegion"
    rating: float
    approved: int
    draft: bool
    archived: bool


class SearchGlobalPostAuthor(BaseModel):
    avatar: str | UUID | None
    first_name: str
    last_name: str
    nickname: str


class SearchGlobalPostRegion(BaseModel):
    id: int
    name: str


class SearchGlobalRegion(BaseModel):
    id: int
    name: str
    description: str | None
    thumbnail: str | UUID | None


class SearchGlobalTourism(BaseModel):
    id: int
    name: str
    photo: str | UUID | None


class SearchGlobalUser(BaseModel):
    id: UUID
    nickname: str
    about: str | None
    rating: float
    first_name: str
    last_name: str
    created_at: datetime.datetime
    avatar: str | None | UUID
    posts_total: int


class PostResponse(BaseModel):
    id: UUID
    header: str
    name: str
    body: str
    rating: float
    created_at: datetime.datetime
    link: str | None
    thumbnail: str
    coordinates: tuple[float, float] | None
    author: "PostAuthorResponse"
    attachments: list[dict[UUID, str]]
    region: dict[int, str]
    tourism_type: dict[int, str]
    tags: list[dict[int, str]]
    approved: int


class PostAuthorResponse(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    avatar: str | None
    rating: float = Field(0)


class RegionResponse(BaseModel):
    id: int
    name: str
    description: str | None
    longitude: float
    latitude: float
    thumbnail: str | UUID | None
    attachments: list[str] | None


class TourismResponse(BaseModel):
    id: int
    name: str
    photo: str | UUID | None
