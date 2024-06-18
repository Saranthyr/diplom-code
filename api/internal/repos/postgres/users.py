import datetime
from typing import Literal
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import and_, asc, delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.postgres import User


class UserRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory
        
    # async def create(
    #     self,
    #     username: EmailStr,
    #     password: str,
    #     nickname: str,
    #     first_name: str,
    #     last_name: str,
    #     role: int
    # ) -> Literal[0, 1]:
    #     return 0

    async def create(
        self,
        uid: UUID,
        username: str,
        password: str,
        nickname: str,
        first_name: str,
        last_name: str,
        role: int,
    ):
        user = User(
            id=uid,
            username=username,
            password=password,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        async with self.session_factory() as s:
            s.add(user)
            await s.flush()
        return 0


    async def read_by_username(self, username: str):
        async with self.session_factory() as s:
            stmt = select(User.id, User.password, User.role, User.active).where(
                User.username == username
            )
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def read(self, uid: UUID):
        async with self.session_factory() as s:
            stmt = select(
                User.id,
                User.nickname,
                User.first_name,
                User.last_name,
                User.about,
                User.posts_total,
                User.created_at,
                User.location,
                User.rating,
            ).where(User.id == uid)
            res = await s.execute(stmt)
            res = res.mappings().one_or_none()
            return res

    async def update(
        self,
        uid: UUID,
        password: str,
        nickname: str,
        first_name: str,
        last_name: str,
        about: str,
        location: int,
        link_telegram: str,
    ):
        try:
            async with self.session_factory() as s:
                user = await s.get(User, uid)
                user.password = password
                user.nickname = nickname
                user.first_name = first_name
                user.last_name = last_name
                user.about = about
                user.location = location
                user.link_tg = link_telegram
                await s.commit()
            return 0
        except Exception:
            return -1

    async def delete(self, uid: UUID):
        async with self.session_factory() as s:
            stmt = delete(User).where(User.id == uid)
            await s.execute(stmt)
        return 0

    async def read_id_by_nickname(self, nickname: str):
        async with self.session_factory() as s:
            stmt = select(User.id).where(User.nickname == nickname)
            res = await s.execute(stmt)
            res = res.scalar_one_or_none()
            return res

    async def activate(self, username: str):
        async with self.session_factory() as s:
            stmt = (
                update(User).values({"active": True}).where(User.username == username)
            )
            await s.execute(stmt)
        return 0

    async def update_avatar(self, uid: UUID, avatar: UUID):
        async with self.session_factory() as s:
            stmt = update(User).values({"avatar": avatar}).where(User.id == uid)
            await s.execute(stmt)
        return 0

    async def update_header(self, uid: UUID, header: UUID):
        async with self.session_factory() as s:
            stmt = update(User).values({"header": header}).where(User.id == uid)
            await s.execute(stmt)
        return 0

    async def read_all_by_region(
        self,
        region: int,
        way: Literal["asc", "desc"],
        order_by: Literal["created_at", "region", "nickname"],
        tf,
    ):
        async with self.session_factory() as s:
            stmt = select(User).where(User.location == region)
            if tf is not None:
                earliest = datetime.datetime.now() - tf + datetime.timedelta(days=1)
                stmt = stmt.where(User.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def read_all_by_rating(self, rating, way, order_by, tf):
        async with self.session_factory() as s:
            stmt = select(User).where(User.rating >= rating)
            if tf is not None:
                earliest = datetime.datetime.now() - tf + datetime.timedelta(days=1)
                stmt = stmt.where(User.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res

    async def read_all(self, region, rating, way, order_by, tf):
        async with self.session_factory() as s:
            stmt = select(User).where(
                and_(User.location == region, User.rating >= rating)
            )
            if tf is not None:
                earliest = datetime.datetime.now() - tf + datetime.timedelta(days=1)
                stmt = stmt.where(User.created_at <= (earliest))
            match way:
                case "asc":
                    stmt = stmt.order_by(asc(order_by))
                case "desc":
                    stmt = stmt.order_by(desc(order_by))
            res = await s.execute(stmt)
            res = res.mappings().all()
            return res
