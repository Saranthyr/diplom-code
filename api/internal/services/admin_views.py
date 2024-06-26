import json
from typing import Any, Dict
import uuid

import aio_pika
from fastapi import Request
from dependency_injector.wiring import Provide, inject
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_file import File as F
from starlette_admin import row_action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import (
    ImageField,
    StringField,
    HasOne,
    HasMany,
    TinyMCEEditorField,
)

from api.pkg.connectors.rabbitmq import RabbitMQ
from api.pkg.models.containers import Container

from ...pkg.models.postgres import (
    File,
    Hashtag,
    Post,
    Region,
    RegionPhoto,
    TourismType,
    User,
    UserRole,
)


class UserView(ModelView):
    fields = [
        StringField(
            "avatar",
            exclude_from_create=True,
            exclude_from_edit=True,
            exclude_from_detail=True,
            exclude_from_list=True,
        ),
        StringField(
            "header",
            exclude_from_create=True,
            exclude_from_edit=True,
            exclude_from_detail=True,
            exclude_from_list=True,
        ),
        User.nickname,
        User.first_name,
        User.last_name,
        HasOne("_role", "Role", identity="role", disabled=True, read_only=True),
        ImageField(
            "_avatar.content", "Avatar_file", exclude_from_detail=True, read_only=True
        ),
        HasOne(
            "_avatar",
            "Avatar",
            identity="file",
            exclude_from_create=True,
            exclude_from_edit=True,
            read_only=True,
        ),
    ]

    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data["_avatar.content"][0]
        thumbnail_name = (thumbnail.filename,)
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name[0], content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_avatar.content"]
        data["id"] = uuid.uuid4()
        data["avatar"] = thumbnail.id
        obj = User(**data)
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        if isinstance(session, AsyncSession):
            obj = await session.get(User, pk)
            thumbnail = await session.get(File, obj.avatar)
            if thumbnail is not None:
                await session.delete(thumbnail)
                await session.commit()
        thumbnail = data["_avatar.content"][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name, content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_avatar.content"]
        data["avatar"] = thumbnail.id
        obj.avatar = data["avatar"]
        obj.nickname = data["nickname"]
        obj.first_name = data["first_name"]
        obj.last_name = data["last_name"]
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)


class FileView(ModelView):
    fields = [StringField("id"), File.name, ImageField("content")]


class UserRoleView(ModelView):
    fields = [UserRole.name]


class RegionView(ModelView):
    fields = [
        Region.latitude,
        Region.longitude,
        Region.name,
        StringField("thumbnail"),
        TinyMCEEditorField("description"),
        HasOne(
            "_thumbnail",
            "Thumbnail",
            identity="file",
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        ImageField("_thumbnail.content", "Thumbnail_pic", exclude_from_detail=True),
        HasMany(
            "photos",
            "Photos",
            identity="file",
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        ImageField(
            "_photos",
            "Photos",
            exclude_from_detail=True,
            exclude_from_list=True,
            multiple=True,
        ),
    ]

    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data["_thumbnail.content"][0]
        thumbnail_name = (thumbnail.filename,)
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name[0], content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_thumbnail.content"]
        data["thumbnail"] = thumbnail.id
        photos = data["_photos"][0]
        del data["_photos"]
        obj = Region(**data)
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
        for photo in photos:
            photo_name = (photo.filename,)
            photo = F(await photo.read(), filename=photo.filename)
            photo = File(name=photo_name[0], content=photo)
            session.add(photo)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(photo)
                photo = RegionPhoto(region_id=obj.id, photo_id=photo.id)
                session.add(photo)
                await session.commit()
                await session.refresh(photo)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        obj = await session.get(Region, int(pk))
        thumbnail = await session.get(File, obj.thumbnail)
        if thumbnail is not None:
            await session.delete(thumbnail)
            await session.commit()
        thumbnail = data["_thumbnail.content"][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name, content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_thumbnail.content"]
        photos = data["_photos"][0]
        del data["_photos"]
        data["thumbnail"] = thumbnail.id
        stmt = delete(RegionPhoto).where(RegionPhoto.region_id == int(pk))
        await session.execute(stmt)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
        for photo in photos:
            photo_name = (photo.filename,)
            photo = F(await photo.read(), filename=photo.filename)
            photo = File(name=photo_name[0], content=photo)
            session.add(photo)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(photo)
                photo = RegionPhoto(region_id=obj.id, photo_id=photo.id)
                session.add(photo)
                await session.commit()
                await session.refresh(photo)
        obj.latitude = data["latitude"]
        obj.longitude = data["longitude"]
        obj.name = data["name"]
        obj.description = data["description"]
        obj.thumbnail = data["thumbnail"]
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)


class TourismTypeView(ModelView):
    fields = [
        TourismType.name,
        TourismType.photo,
        HasOne(
            "_photo",
            "Thumbnail",
            identity="file",
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        ImageField("_photo.content", "Thumbnail_pic", exclude_from_detail=True),
    ]

    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data["_photo.content"][0]
        thumbnail_name = (thumbnail.filename,)
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name[0], content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_photo.content"]
        data["photo"] = thumbnail.id
        obj = TourismType(**data)
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        if isinstance(session, AsyncSession):
            obj = await session.get(TourismType, int(pk))
            thumbnail = await session.get(File, obj.photo)
            if thumbnail is not None:
                await session.delete(thumbnail)
                await session.commit()
        thumbnail = data["_photo.content"][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(name=thumbnail_name, content=thumbnail)
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data["_photo.content"]
        data["photo"] = thumbnail.id
        obj.name = data["name"]
        obj.photo = data["photo"]
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)


class TagView(ModelView):
    fields = [Hashtag.name]


class PostView(ModelView):
    fields = [
        StringField("id", read_only=True, disabled=True),
        Post.name,
        Post.header,
        HasOne("_author", identity="user"),
        HasOne("_region", "region", identity="region"),
        HasOne("_tourism_type", "tourism type", identity="tourism_type"),
        HasOne(
            "_thumbnail",
            "Thumbnail",
            identity="file",
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        ImageField("_thumbnail.content", "Thumbnail_pic", exclude_from_detail=True),
        HasMany("tags", "tags", identity="tags"),
        TinyMCEEditorField("body", exclude_from_list=True),
        HasMany("attachments", "attachments", identity="file"),
    ]

    def can_edit(self, request: Request) -> bool:
        return False

    def can_create(self, request: Request) -> bool:
        return False

    def can_delete(self, request: Request) -> bool:
        return "1" == request.session.get("user_role", None)

    @row_action(
        name="approve_publication",
        text="Одобрить к публикации",
        confirmation="Вы точно хотите одобрить эту статью к публикации?",
        icon_class="fa-solid fa-check",
        exclude_from_list=True,
    )
    @inject
    async def approve_publication(
        self, request: Request, pk: Any, rmq: RabbitMQ = Provide[Container.rabbitmq]
    ) -> str:
        session = request.state.session
        post = await self.find_by_pk(request, pk)
        if post.approved != 1:
            return f"Пост уже обработан"
        post.approved = 2
        session.add(post)
        await session.commit()
        async with rmq.connection() as con:
            ch = await con.channel()
            data = {
                "action": "post_published",
                "email": post._author.username,
                "post_name": post.name,
            }
            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )
        return f"Publication accepted"

    @row_action(
        name="deny_publication",
        text="Отклонить публикацию",
        confirmation="Вы точно хотите отклонить эту статью к публикации?",
        icon_class="fa-solid fa-xmark",
        exclude_from_list=True,
    )
    async def deny_publication(
        self, request: Request, pk: Any, rmq: RabbitMQ = Provide[Container.rabbitmq]
    ) -> str:
        session = request.state.session
        post = await self.find_by_pk(request, pk)
        if post.approved != 1:
            return f"Пост уже обработан"
        post.approved = 3
        session.add(post)
        await session.commit()
        async with rmq.connection() as con:
            ch = await con.channel()
            data = {
                "action": "post_rejected",
                "email": post._author.username,
                "post_name": post.name,
            }
            await ch.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()), routing_key="mailer"
            )
        return f"Publication denied"

    def get_list_query(self) -> Select:
        return super().get_list_query().where(Post.approved == 1)

    def get_count_query(self) -> Select:
        return super().get_count_query().where(Post.approved == 1)
