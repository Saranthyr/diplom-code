import decimal
import json
from uuid import UUID, uuid4

import aio_pika

from api.configuration.security import decode_token
from api.internal.services.comment import CommentService
from api.internal.services.files import FileService
from api.internal.services.hashtag import HashtagService
from api.internal.services.post import PostService
from api.internal.services.post_attachment import PostAttachmentService
from api.internal.services.post_hashtag import PostHashtagService
from api.internal.services.rating import RatingService
from api.internal.services.region import RegionService
from api.internal.services.tourism import TourismService
from api.internal.services.user import UserService
from api.pkg.connectors.rabbitmq import RabbitMQ
from api.pkg.models.exceptions import InvalidRefresh
from api.pkg.models.exceptions.posts import NotYourPost
from api.pkg.models.pydantic.responses import (
    PostAuthorResponse,
    PostResponse,
    TokenResponse,
)


class PostServiceMain:
    def __init__(
        self,
        file_service: FileService,
        post_service: PostService,
        rating_service: RatingService,
        comments: CommentService,
        post_attachment_service: PostAttachmentService,
        post_hashtag_service: PostHashtagService,
        hashtag_service: HashtagService,
        user_service: UserService,
        region_service: RegionService,
        tourism_service: TourismService,
        rabbitmq: RabbitMQ,
    ) -> None:
        self.post_service = post_service
        self.file_service = file_service
        self.rating_service = rating_service
        self.post_attachment_service = post_attachment_service
        self.post_hashtag_service = post_hashtag_service
        self.hashtag_service = hashtag_service
        self.user_service = user_service
        self.region_service = region_service
        self.tourism_service = tourism_service
        self.comments = comments
        self.rabbitmq = rabbitmq

    async def create_post(
        self,
        token,
        thumbnail,
        region,
        tourism_type,
        name,
        header,
        longitude,
        latitude,
        link,
        body,
        draft,
    ):
        thumbnail_id = await self.file_service.create_file(thumbnail)
        decoded = await decode_token(token)
        author = UUID(decoded["sub"])
        id = await self.post_service.create(
            author,
            region,
            tourism_type,
            name,
            header,
            longitude,
            latitude,
            link,
            thumbnail_id,
            body,
            draft,
        )
        return id

    async def update_post(
        self,
        token,
        thumbnail,
        name,
        body,
        header,
        longitude,
        latitude,
        link,
        region,
        tourism_type,
        id,
    ):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        post_data = await self.post_service.read(id)
        if post_data["author"] != curr_user:
            raise NotYourPost

        if thumbnail is not None:
            await self.file_service.delete_file(post_data["thumbnail"])
            thumbnail = await self.file_service.create_file(thumbnail)

        return await self.post_service.update(
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
        )

    async def read_post(self, id):
        attachments = []
        tags = []

        data = await self.post_service.read(id)
        attachments_data = await self.post_attachment_service.read(id)
        tags_data = await self.post_hashtag_service.read(id)

        for attachment in attachments_data:
            attachment = {
                attachment: (await self.file_service.read_file(attachment))["url"]
            }
            attachments.append(attachment)

        for tag in tags_data:
            tag = {tag: await self.hashtag_service.read(tag)}
            tags.append(tag)

        author = PostAuthorResponse(**await self.user_service.read(data["author"]))

        res = PostResponse(
            id=data["id"],
            header=data["header"],
            name=data["name"],
            body=data["body"],
            rating=data["rating"],
            created_at=data["created_at"],
            link=data["link"],
            coordinates=(data["longitude"], data["latitude"]),
            author=author,
            region={
                data["region"]: (await self.region_service.read(data["region"]))["name"]
            },
            attachments=attachments,
            tourism_type={
                data["tourism_type"]: (
                    await self.tourism_service.read(data["tourism_type"])
                )["name"]
            },
            tags=tags,
            thumbnail=(await self.file_service.read_file(data["thumbnail"]))["url"],
            approved=data["approved"],
        )
        return res

    async def delete_post(self, token, id):
        return await self.post_service.delete(id)

    async def draft(self, token, id):
        return await self.post_service.draft(id)

    async def archive(self, token, id):
        return await self.post_service.archive(id)

    async def create_attachment(self, id, attachment):
        attachment_id = await self.file_service.create_file(attachment)
        return await self.post_attachment_service.create(id, attachment_id)

    async def delete_attachment(self, id, attachment_id):
        return await self.post_attachment_service.delete(id, attachment_id)

    async def create_hashtag(self, id, tag):
        return await self.post_hashtag_service.create(id, tag)

    async def delete_hashtag(self, id, tag):
        return await self.post_hashtag_service.delete(id, tag)

    async def rate(self, token, id, rating):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        try:
            await self.rating_service.create(id, curr_user, rating)
        except Exception:
            pass
        new_rating = (await self.rating_service.read_total(id)) / (
            await self.rating_service.read_count(id)
        )
        await self.post_service.set_rating(id, new_rating)
        return 0

    async def create_comment(self, token, post_id, responding_to, contents):
        decoded = await decode_token(token)
        curr_user = UUID(decoded["sub"])
        post_data = await self.post_service.read(post_id)
        async with self.rabbitmq.connection() as con:
            ch = await con.channel()
            data = {
                "action": "new_comment",
                "email": (await self.user_service.read(post_data["author"]))[
                    "username"
                ],
                "post_name": post_data["name"],
            }
            if responding_to is not None:
                data = {
                    "action": "response_comment",
                    "email": (await self.user_service.read(post_data["author"]))[
                        "username"
                    ],
                    "post_name": post_data["name"],
                }

            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )
        return await self.comments.insert_comment(
            curr_user, post_id, responding_to, contents
        )

    async def read_comment(self, id, base_comment=None):
        return await self.comments.comments_with_replies(id, base_comment)
