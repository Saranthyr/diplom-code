from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import PostRating


class PostRatingRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def read(self, post_uid, user_uid):
        async with self.session_factory() as s:
            stmt = select(PostRating.rating).where(
                and_(PostRating.post_id == post_uid, PostRating.user_id == user_uid)
            )
            res = await s.execute(stmt)
            res = res.scalar_one_or_none()
            return res

    async def create(self, post_uid, user_uid, rating):
        async with self.session_factory() as s:
            rating = PostRating(post_id=post_uid, user_id=user_uid, rating=rating)
            s.add(rating)
        return 0

    async def update(self, post_uid, user_uid, rating):
        async with self.session_factory() as s:
            rating = await s.get(PostRating, {"post_id": post_uid, "user_id": user_uid})
            rating.rating = rating
        return 0

    async def delete(self, post_uid, user_uid):
        async with self.session_factory() as s:
            stmt = delete(PostRating).where(
                and_(PostRating.post_id == post_uid, PostRating.user_id == user_uid)
            )
            await s.execute(stmt)
        return 0
