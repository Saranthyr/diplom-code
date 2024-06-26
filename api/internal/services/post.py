from datetime import timedelta
import os
from typing import Literal, Optional, Tuple, Union, Dict
from uuid import UUID, uuid4

from passlib.context import CryptContext

from api.internal.repos.postgres.posts import PostRepository
from api.pkg.models.base.exception import BaseAPIException
from api.configuration.security import decode_token
from api.pkg.models.base.enums import TimeframeEnum


class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.repository = post_repository

    async def create(
        self,
        author,
        region,
        tourism_type,
        name,
        header,
        lat,
        long,
        link,
        thumbnail,
        body,
        draft,
    ):
        return await self.repository.create(
            uuid4(),
            region,
            tourism_type,
            name,
            header,
            author,
            lat,
            long,
            link,
            thumbnail,
            body,
            draft,
        )

    async def update(
        self,
        id,
        name,
        header,
        body,
        longitude,
        latitude,
        link,
        region,
        tourism_type,
        thumbnail,
    ):
        data = {
            "name": name,
            "header": header,
            "body": body,
            "longitude": longitude,
            "latitude": latitude,
            "link": link,
            "region": region,
            "tourism_type": tourism_type,
        }
        if thumbnail is not None:
            data["thumbnail"] = thumbnail
        return await self.repository.update(id, data)

    async def read(self, id):
        return await self.repository.read(id)

    async def delete(self, id):
        return await self.repository.delete_post(id)

    async def set_rating(self, id, rating):
        return await self.repository.set_rating(id, rating)

    async def draft(self, id):
        return await self.repository.draft(id)

    async def archive(self, id):
        return await self.repository.archive(id)

    async def search_posts(
        self,
        s,
        region=None,
        tourism_type=None,
        rating=0,
        author=None,
        order_by="created_at",
        way="desc",
        page=1,
        approved=[2],
        draft=None,
        archived=None
    ):
        return await self.repository.search_posts(
            s, region, tourism_type, rating, author, order_by, way, page, approved, draft, archived
        )
