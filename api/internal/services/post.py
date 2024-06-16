from datetime import timedelta
import os
from typing import Literal, Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token
from api.pkg.models.base.enums import TimeframeEnum


class PostService:
    def __init__(self, post_repository) -> None:
        self.repository = post_repository

    async def create(
        self,
        token,
        region,
        tourist_type,
        name,
        header,
        body,
        lat,
        long,
        link,
        thumbnail_id,
    ):
        decoded = await decode_token(token)
        author = UUID(decoded["sub"])
        return await self.repository.create(
            uuid4(),
            region,
            tourist_type,
            name,
            header,
            body,
            author,
            lat,
            long,
            link,
            thumbnail_id,
        )

    async def read(self, id):
        return await self.repository.read(id)

    async def delete(self, token, id):
        decoded = await decode_token(token)
        user = UUID(decoded["sub"])
        author = await self.repository.read_post_author(id)
        if user == author:
            await self.repository.delete(id)
            return 0
        raise BaseAPIException

    async def approve_post(self, id):
        return await self.repository.approve_post(id)

    async def all(self):
        return await self.repository.all()

    async def read_all(
        self,
        region_id: int | None,
        tourism_type: int | None,
        order_by: Literal["created_at", "rating"],
        way: Literal["asc", "desc"],
        timeframe: Literal["1d", "7d", "30d", "all"],
    ):
        tf = None

        match timeframe:
            case "1d":
                tf = TimeframeEnum.DAY.value
            case "7d":
                tf = TimeframeEnum.WEEK.value
            case "30d":
                tf = TimeframeEnum.MONTH.value
            case _:
                pass
        if region_id:
            return await self.repository.read_all_by_region_id(
                region_id, order_by, way, tf
            )
        elif tourism_type:
            return await self.repository.read_all_by_tourism_type(
                tourism_type, order_by, way, tf
            )
        return await self.repository.read_all_by_both(
            region_id, tourism_type, order_by, way, tf
        )

    async def draft(self, token, id):
        decoded = await decode_token(token)
        user = UUID(decoded["sub"])
        author = await self.repository.read_post_author(id)
        if user == author:
            await self.repository.draft(id)
            return 0
        raise BaseAPIException

    async def archive(self, token, id):
        decoded = await decode_token(token)
        user = UUID(decoded["sub"])
        author = await self.repository.read_post_author(id)
        if user == author:
            await self.repository.archive(id)
            return 0
        raise BaseAPIException

    async def calculate_rating(self, id, ratings):
        rating = ratings // len(ratings)
        return await self.repository.update_rating(id, rating)
