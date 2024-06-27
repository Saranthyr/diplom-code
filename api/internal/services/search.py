from typing import Literal
from uuid import uuid4
import uuid

from api.internal.services.files import FileService
from api.internal.services.hashtag import HashtagService
from api.internal.services.post import PostService
from api.internal.services.post_hashtag import PostHashtagService
from api.internal.services.region import RegionService
from api.internal.services.tourism import TourismService
from api.internal.services.user import UserService
from api.pkg.models.exceptions import InvalidRefresh
from api.pkg.models.pydantic.responses import (
    SearchGlobalPost,
    SearchGlobalPostAuthor,
    SearchGlobalPostRegion,
    SearchGlobalRegion,
    SearchGlobalTourism,
    SearchGlobalUser,
    TokenResponse,
)


class SearchService:
    def __init__(
        self,
        user_service: UserService,
        post_service: PostService,
        region_service: RegionService,
        file_service: FileService,
        post_hashtag_service: PostHashtagService,
        hashtag_service: HashtagService,
        tourism_service: TourismService,
    ) -> None:
        self.post_service = post_service
        self.user_service = user_service
        self.region_service = region_service
        self.file_service = file_service
        self.post_hashtag_service = post_hashtag_service
        self.hashtag_service = hashtag_service
        self.tourism_service = tourism_service

    async def search(
        self,
        s: str,
        typ: Literal["1", "2", "3", "4"],
    ):
        res = []
        match typ:
            case "1":

                posts = await self.post_service.search_posts(s)
                for post in posts:
                    thumbnail = await self.file_service.read_file(post["thumbnail"])
                    if thumbnail is not None:
                        thumbnail = thumbnail["url"]

                    author = await self.user_service.read(post["author"])
                    avatar = None
                    if author["avatar"] is not None:
                        avatar = (await self.file_service.read_file(author["avatar"]))[
                            "url"
                        ]
                    author = SearchGlobalPostAuthor(**author)
                    if avatar is not None:
                        author.avatar = avatar

                    tags = []
                    tags_data = await self.post_hashtag_service.read(post["id"])
                    for tag in tags_data:
                        tag = await self.hashtag_service.read(tag)
                        tags.append(tag)

                    region = SearchGlobalPostRegion(
                        **(await self.region_service.read(post["region"]))
                    )

                    post_res = SearchGlobalPost(
                        **post,
                        hashtags=tags,
                    )
                    post_res.region = region
                    post_res.author = author
                    post_res.thumbnail = thumbnail

                    res.append(post_res)

            case "2":
                data = await self.region_service.search(s)
                thumbnail = None
                for region in data:
                    if region["thumbnail"] is not None:
                        thumbnail = (
                            await self.file_service.read_file(region["thumbnail"])
                        )["url"]

                    region = SearchGlobalRegion(**region)
                    region.thumbnail = thumbnail
                    res.append(region)

            case "3":
                data = await self.tourism_service.search(s)
                photo = None
                for tourism in data:
                    if tourism["photo"] is not None:
                        photo = (await self.file_service.read_file(tourism["photo"]))[
                            "url"
                        ]

                    tourism = SearchGlobalTourism(**tourism)
                    tourism.photo = photo
                    res.append(tourism)

            case "4":
                data = await self.user_service.search(s)
                # return type(data), data
                for user in data:
                    avatar = None
                    if user["avatar"] is not None:
                        avatar = (await self.file_service.read_file(user["avatar"]))[
                            "url"
                        ]

                    user = SearchGlobalUser(**user)
                    user.avatar = avatar
                    res.append(user)

            case _:
                pass
        return res

    async def post_search(
        self,
        q,
        region,
        tourism_type,
        rating,
        author,
        page,
        order_by,
        way,
        draft,
        archived,
        approved,
    ):
        res = []
        posts = await self.post_service.search_posts(
            q,
            region,
            tourism_type,
            rating,
            author,
            order_by,
            way,
            page,
            approved,
            draft,
            archived,
        )
        for post in posts:
            if post['thumbnail'] is not None:
                thumbnail = await self.file_service.read_file(post["thumbnail"])
                if thumbnail is not None:
                    thumbnail = thumbnail["url"]
            else:
                thumbnail = ''

            author = await self.user_service.read(post["author"])
            avatar = None
            if author["avatar"] is not None:
                avatar = (await self.file_service.read_file(author["avatar"]))["url"]
            author = SearchGlobalPostAuthor(**author)
            if avatar is not None:
                author.avatar = avatar

            tags = []
            tags_data = await self.post_hashtag_service.read(post["id"])
            for tag in tags_data:
                tag = await self.hashtag_service.read(tag)
                tags.append(tag)

            region = SearchGlobalPostRegion(
                **(await self.region_service.read(post["region"] if not None else 1))
            )

            post_res = SearchGlobalPost(
                **post,
                hashtags=tags,
            )
            post_res.region = region
            post_res.author = author
            post_res.thumbnail = thumbnail

            res.append(post_res)

        return res
