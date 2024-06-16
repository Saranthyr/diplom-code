import datetime
from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import and_, asc, delete, desc, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
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
        body,
        author,
        lat,
        long,
        link,
        thumbnail_id,
    ):
        async with self.session_factory() as s:
            post = Post(
                id=uid,
                region=region,
                tourism_type=tourist_type,
                name=name,
                header=header,
                body=body,
                author=author,
                latitude=lat,
                longitude=long,
                link=link,
                thumbnail=thumbnail_id,
            )
            s.add(post)
            await s.commit()
            return 0

    async def read(self, uid):
        async with self.session_factory() as s:
            stmt = select(Post).where(Post.id == uid)
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def read_post_author(self, uid):
        async with self.session_factory() as s:
            stmt = select(Post.author).where(Post.id == uid)
            res = await s.execute(stmt)
            res = res.scalar_one_or_none()
            return res

    async def update(self, uid, body, tourism_type, header, name, long, lat, link):
        try:
            async with self.session_factory() as s:
                post = await s.get(Post, uid)
                post.body = body
                post.tourism_type = tourism_type
                post.header = header
                post.name = name
                post.longitude = long
                post.latitude = lat
                post.link = link
            return 0
        except Exception:
            return -1

    async def delete(self, id):
        async with self.session_factory() as s:
            stmt = delete(Post).where(Post.id == id)
            await s.execute(stmt)
            return 0

    async def read_all_by_author(self, author):
        async with self.session_factory() as s:
            stmt = select(Post).where(Post.author == author)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def read_all_by_region_id(
        self, region_id, order_by, way, timeframe: datetime.timedelta | None
    ):
        async with self.session_factory() as s:
            stmt = select(Post).where(and_(Post.region == region_id, Post.approved))
            if timeframe is not None:
                earliest = (
                    datetime.datetime.now() - timeframe + datetime.timedelta(days=1)
                )
                stmt = stmt.where(Post.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            print(stmt)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def read_all_by_tourism_type(
        self, tourism_id, order_by, way, timeframe: datetime.timedelta | None
    ):
        async with self.session_factory() as s:
            stmt = select(Post).where(
                and_(Post.tourist_type == tourism_id, Post.approved)
            )
            if timeframe is not None:
                earliest = (
                    datetime.datetime.now() - timeframe + datetime.timedelta(days=1)
                )
                stmt = stmt.where(Post.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def read_all_by_both(
        self, region_id, tourism_id, order_by, way, timeframe: datetime.timedelta | None
    ):
        async with self.session_factory() as s:
            stmt = select(Post).where(
                and_(
                    Post.tourist_type == tourism_id,
                    Post.region == region_id,
                    Post.approved,
                )
            )
            if timeframe is not None:
                earliest = (
                    datetime.datetime.now() - timeframe + datetime.timedelta(days=1)
                )
                stmt = stmt.where(Post.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def draft(self, uid):
        async with self.session_factory() as s:
            stmt = update(Post).values({"draft": True}).where(Post.id == uid)
            await s.execute(stmt)
            return 0

    async def archive(self, uid):
        async with self.session_factory() as s:
            stmt = update(Post).values({"archived": True}).where(Post.id == uid)
            await s.execute(stmt)
            return 0

    async def update_rating(self, uid, rating):
        async with self.session_factory() as s:
            stmt = update(Post).values({"rating": rating}).where(Post.id == uid)
            await s.execute(stmt)
            return 0
        
    async def all(self):
        async with self.session_factory() as s:
            stmt = select(Post)
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res
