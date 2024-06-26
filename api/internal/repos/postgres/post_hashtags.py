from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import and_, delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import PostHashtag


class PostHashtagRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def read(self, uid):
        async with self.session_factory() as s:
            stmt = select(PostHashtag.tag).where(PostHashtag.post_id == uid)
            res = await s.execute(stmt)
            res = res.scalars().all()
            return res

    async def create(self, uid, tag):
        try:
            async with self.session_factory() as s:
                post_tag = PostHashtag(post_id=uid, tag=tag)
                s.add(post_tag)
        except Exception:
            pass
        return 0

    async def delete(self, uid, tag):
        try:
            async with self.session_factory() as s:
                stmt = delete(PostHashtag).where(
                    and_(PostHashtag.post_id == uid, PostHashtag.tag == tag)
                )
                await s.execute(stmt)
        except Exception:
            pass
        return 0
