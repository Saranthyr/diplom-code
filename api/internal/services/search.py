from datetime import timedelta
import mimetypes
import os
from typing import Literal, Optional
from uuid import uuid4

from api.pkg.models.exceptions import InvalidRefresh
from api.pkg.models.pydantic.responses import TokenResponse


class SearchService:
    def __init__(self, user_service, post_service) -> None:
        self.post_service = post_service
        self.user_service = user_service

    async def posts(
        self,
        region_id: int | None,
        tourism_type: int | None,
        order_by: Literal["created_at", "rating"],
        way: Literal["asc", "desc"],
        timeframe: Literal["1d", "7d", "30d", "all"],
    ):
        return await self.post_service.read_all(
            region_id, tourism_type, order_by, way, timeframe
        )

    async def users(
        self,
        region: int,
        rating: int,
        order_by: Literal["created_at", "rating"],
        way: Literal["asc", "desc"],
        age: Literal["30d", "180", "30d", "all"],
    ):
        return await self.user_service.read_all(region, rating, order_by, way, age)
