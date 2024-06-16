from datetime import timedelta
import mimetypes
import os
from typing import Optional
from uuid import UUID, uuid4

from api.configuration.security import decode_token
from api.pkg.models.exceptions import InvalidRefresh
from api.pkg.models.pydantic.responses import TokenResponse


class PostServiceMain:
    def __init__(
        self, file_service, post_service, rating_service, s3, comments
    ) -> None:
        self.post_service = post_service
        self.file_service = file_service
        self.s3 = s3
        self.rating_service = rating_service
        self.comments = comments

    async def create_post(
        self,
        token,
        thumbnail,
        region,
        tourist_type,
        name,
        header,
        body,
        lat,
        long,
        link,
    ):
        thumbnail_id = uuid4()
        ext = mimetypes.guess_extension(thumbnail.content_type)
        await self.s3.upload_file(
            await thumbnail.read(), f"{thumbnail_id}{ext}", "post_thumbnails"
        )
        await self.file_service.create_file(
            thumbnail_id, thumbnail.filename, ext, 1, thumbnail.content_type
        )
        return await self.post_service.create(
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
        )

    async def read_post(self, id):
        return await self.post_service.read(id)

    async def delete(self, token, id):
        return await self.post_service.delete(token, id)

    async def draft(self, token, id):
        return await self.post_service.draft(token, id)

    async def archive(self, token, id):
        return await self.post_service.archive(token, id)

    async def rate(self, token, id, rating):
        decoded = await decode_token(token)
        user_id = UUID(decoded["sub"])
        await self.rating_service.rate(id, user_id, rating)
        ratings = await self.rating_service.read_all_for_post(id)
        return await self.post_service.calculate_rating(id, ratings)

    async def comment(self, token, post_id, responding_to, contents):
        decoded = await decode_token(token)
        user_id = UUID(decoded["sub"])
        return await self.comments.insert_comment(
            user_id, post_id, responding_to, contents
        )

    async def all_comments(self, id, comment_id: int | None = None):
        return await self.comments.comments_with_replies(id, comment_id)
    
    async def all(self):
        return await self.post_service.all()
