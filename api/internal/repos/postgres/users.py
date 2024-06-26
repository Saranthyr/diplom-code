import datetime
from typing import Literal
from uuid import UUID

from asyncpg import UniqueViolationError
from pydantic import EmailStr
from sqlalchemy import and_, asc, delete, desc, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from api.pkg.models.base.exception import BaseAPIException
from api.pkg.models.exceptions.users import NicknameInUse, UsernameInUse
from api.pkg.models.postgres import User


class UserRepository:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(
        self,
        uid: UUID,
        username: EmailStr,
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
            role=role,
        )
        async with self.session_factory() as s:
            s.add(user)
            try:
                await s.flush()
                await s.refresh(user)
            except DBAPIError as e:
                if isinstance(e.orig.__cause__, UniqueViolationError):
                    raise UsernameInUse
            user.nickname = nickname
            user.first_name = first_name
            user.last_name = last_name
            try:
                await s.flush()
            except DBAPIError as e:
                if isinstance(e.orig.__cause__, UniqueViolationError):
                    raise NicknameInUse
        return 0

    async def activate_user(self, username: EmailStr):
        async with self.session_factory() as s:
            stmt = (
                update(User).where(User.username == username).values({"active": True})
            )
            await s.execute(stmt)
        return 0

    async def update_base(
        self,
        uid: UUID,
        nickname: str,
        first_name: str,
        last_name: str,
        about: str,
        location: int,
        link_telegram: str,
    ):
        try:
            async with self.session_factory() as s:
                user: User = await s.get(User, uid)
                user.nickname = nickname
                user.first_name = first_name
                user.last_name = last_name
                user.about = about
                user.location = location
                user.link_tg = link_telegram
        except SQLAlchemyError as e:
            raise BaseAPIException(message=str(e.__dict__))
        return 0

    async def read_by_username(self, username: EmailStr):
        async with self.session_factory() as s:
            stmt = select(User.active, User.password, User.id).where(
                User.username == username
            )
            res = await s.execute(stmt)
            return res.one_or_none()

    async def read(self, id):
        async with self.session_factory() as s:
            stmt = select(
                User.id,
                User.header,
                User.avatar,
                User.created_at,
                User.rating,
                User.first_name,
                User.last_name,
                User.nickname,
                User.link_tg,
                User.about,
                User.password,
                User.posts_total,
                User.username,
                User.location,
            ).where(User.id == id)
            res = await s.execute(stmt)
            return res.mappings().first()

    async def update_password(self, id, password):
        async with self.session_factory() as s:
            stmt = update(User).where(User.id == id).values({"password": password})
            await s.execute(stmt)
        return 0

    async def update_avatar(self, uid, avatar):
        async with self.session_factory() as s:
            stmt = update(User).where(User.id == uid).values({"avatar": avatar})
            await s.execute(stmt)
        return 0

    async def update_header(self, uid, header):
        async with self.session_factory() as s:
            stmt = update(User).where(User.id == uid).values({"header": header})
            await s.execute(stmt)
        return 0

    async def delete(self, uid):
        async with self.session_factory() as s:
            stmt = delete(User).where(User.id == uid)
            await s.execute(stmt)
        return 0

    async def change_channel(self, uid, ch):
        async with self.session_factory() as s:
            stmt = (
                update(User).where(User.id == uid).values({"notification_channel": ch})
            )
            await s.execute(stmt)
        return 0

    async def read_by_nickname(self, nickname):
        async with self.session_factory() as s:
            stmt = select(
                User.header,
                User.avatar,
                User.created_at,
                User.rating,
                User.first_name,
                User.last_name,
                User.nickname,
                User.link_tg,
                User.about,
            ).where(User.nickname == nickname)
            res = await s.execute(stmt)
            return res.mappings().first()

    async def search(self, q):
        async with self.session_factory() as s:
            stmt = select(
                User.id,
                User.nickname,
                User.first_name,
                User.last_name,
                User.about,
                User.created_at,
                User.avatar,
                User.rating,
                User.posts_total,
            ).where(
                or_(
                    User.nickname.ilike(f"%{q}%"),
                    User.first_name.ilike(f"%{q}%"),
                    User.last_name.ilike(f"%{q}%"),
                )
            )
            res = await s.execute(stmt)
        return res.mappings().all()
