from sqlalchemy import and_, delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import PostRating


class RatingRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(self, post_id, user_id, rating):
        """Создать запись в таблице

        Args:
            post_id (uuid): идентификатор поста
            user_id (uuid): идентификатор пользователя
            rating (float): оценка

        Returns:
            int: 0 в случае успеха, -1 в случае ошибки
        """
        try:
            async with self.session_factory() as s:
                rate = PostRating(post_id=post_id, user_id=user_id, rating=rating)
                s.add(rate)
            return 0
        except Exception:
            return -1

    async def read(self, post_id, user_id):
        """Получить сведения об оценка поста пользователем

        Args:
            post_id (uuid): идентификатор поста
            user_id (uuid): идентификатор пользователя

        Returns:
            float: оценка при наличии записи в базе
            None: пост не оценен пользователем
        """
        async with self.session_factory() as s:
            stmt = select(PostRating.rating).where(
                and_(PostRating.post_id == post_id, PostRating.user_id == user_id)
            )
            res = await s.execute(stmt)
            res = res.scalar_or_none()
            return res

    async def read_all(self, id):
        """Получить сведения об оценках конкретного поста

        Args:
            id (uuid): идентификатор поста

        Returns:
            list[float]: массив оценок
        """
        async with self.session_factory() as s:
            stmt = select(PostRating.rating).where(PostRating.post_id == id)
            res = await s.execute(stmt)
            res = res.scalars().all()
            return res

    async def read_count(self, id):
        async with self.session_factory() as s:
            stmt = select(func.count(PostRating.user_id)).where(
                PostRating.post_id == id
            )
            return (await s.execute(stmt)).scalar_one()

    async def read_total(self, id):
        async with self.session_factory() as s:
            stmt = select(func.sum(PostRating.rating)).where(PostRating.post_id == id)
            return (await s.execute(stmt)).scalar_one()

    async def delete(self, id, user_id):
        try:
            async with self.session_factory() as s:
                stmt = delete(PostRating).where(
                    and_(PostRating.post_id == id, PostRating.user_id == user_id)
                )
                await s.execute(stmt)
        except Exception:
            pass
        return 0
