import datetime
from uuid import UUID
from pydantic import BaseModel


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
    profile_photo: str
    profile_header_photo: str
    about: str
    posts_total: int
    created_at: datetime.datetime
    location: str
    link_telegram: str
    rating: float
