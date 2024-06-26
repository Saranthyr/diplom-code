import datetime

from asyncpg import UniqueViolationError
from sqlalchemy import and_, asc, delete, desc, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.exceptions.posts import PostRegionNameInUse
from api.pkg.models.postgres import Post


class PostRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(
        self,
        uid,
        region,
        tourist_type,
        name,
        header,
        author,
        lat,
        long,
        link,
        thumbnail,
        body,
        draft,
    ):
        async with self.session_factory() as s:
            post = Post(
                id=uid,
                region=region,
                tourism_type=tourist_type,
                name=name,
                header=header,
                author=author,
                latitude=lat,
                longitude=long,
                link=link,
                thumbnail=thumbnail,
                body=body,
                draft=draft,
            )
            s.add(post)
            await s.flush()
        return uid

    async def update_post(self, id, data):
        async with self.session_factory() as s:
            stmt = update(Post).where(Post.id == id).values(data)
            await s.execute(stmt)
        return 0

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(
                Post.id,
                Post.name,
                Post.header,
                Post.region,
                Post.tourism_type,
                Post.body,
                Post.author,
                Post.rating,
                Post.created_at,
                Post.link,
                Post.longitude,
                Post.latitude,
                Post.thumbnail,
                Post.approved,
            ).where(Post.id == id)
            res = await s.execute(stmt)
            return res.mappings().one_or_none()

    async def set_rating(self, id, rating):
        async with self.session_factory() as s:
            stmt = update(Post).where(Post.id == id).values({"rating": rating})
            await s.execute(stmt)
        return 0

    async def draft(self, id):
        async with self.session_factory() as s:
            stmt = update(Post).where(Post.id == id).values({"draft": ~Post.draft})
            await s.execute(stmt)
        return 0

    async def archive(self, id):
        async with self.session_factory() as s:
            stmt = (
                update(Post).where(Post.id == id).values({"archived": ~Post.archived})
            )
            await s.execute(stmt)
        return 0

    async def delete_post(self, id):
        async with self.session_factory() as s:
            stmt = delete(Post).where(Post.id == id)
            await s.execute(stmt)
        return 0

    async def search_posts(
        self, q, region, tourism_type, rating, author, order_by, way, page
    ):
        async with self.session_factory() as s:
            stmt = (
                select(
                    Post.id,
                    Post.name,
                    Post.header,
                    Post.thumbnail,
                    Post.author,
                    Post.created_at,
                    Post.region,
                    Post.rating,
                    Post.approved,
                    Post.draft,
                    Post.archived,
                )
                .where(
                    and_(
                        Post.name.ilike(f"%{q}%"),
                        (
                            Post.region.in_(region)
                            if (region is not None and len(region) > 1)
                            else True
                        ),
                        (
                            Post.tourism_type.in_(tourism_type)
                            if (tourism_type is not None and len(tourism_type) > 1)
                            else True
                        ),
                        Post.rating >= (rating),
                        (
                            Post.author.in_(author)
                            if (author is not None and len(author) > 1)
                            else True
                        ),
                    )
                )
                .order_by(text(f"{order_by} {way}"))
                .offset((page - 1) * 8)
                .limit(8)
            )
            res = await s.execute(stmt)
            return res.mappings().all()
