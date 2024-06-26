from typing import Any, Dict, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import and_, delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import PostAttachments


class PostAttachmentRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def read(self, uid):
        async with self.session_factory() as s:
            stmt = select(PostAttachments.attachment).where(
                PostAttachments.post_id == uid
            )
            res = await s.execute(stmt)
            res = res.scalars().all()
            return res

    async def create(self, uid, attachment):
        try:
            async with self.session_factory() as s:
                attachment = PostAttachments(post_id=uid, attachment=attachment)
                s.add(attachment)
        except Exception:
            pass
        return 0

    async def delete(self, uid, attachment):
        try:
            async with self.session_factory() as s:
                stmt = delete(PostAttachments).where(
                    and_(
                        PostAttachments.post_id == uid,
                        PostAttachments.attachment == attachment,
                    )
                )
                await s.execute(stmt)
        except Exception:
            pass
        return 0
