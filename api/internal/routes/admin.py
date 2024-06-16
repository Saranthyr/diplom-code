from typing import Any, Dict

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_admin import HasOne
from starlette_admin.contrib.sqla import Admin, ModelView
from sqlalchemy_file import File as F
from dependency_injector.wiring import Provide, inject
from starlette_admin.fields import (
    ImageField,
    IntegerField,
    FloatField,
    StringField,
    FileField,
    HasOne,
    HasMany
)
import anyio.to_thread

from ...pkg.connectors.database import Database
from ...pkg.models.containers import Container
from ...pkg.models.postgres import File, Post, Region, RegionPhoto, TourismType, User, UserRole


class UserView(ModelView):
    fields = [StringField('id', read_only=True, disabled=True),
              StringField('avatar', exclude_from_create=True, exclude_from_edit=True, exclude_from_detail=True, exclude_from_list=True),
              StringField('header',  exclude_from_create=True, exclude_from_edit=True, exclude_from_detail=True, exclude_from_list=True),
            User.nickname,
              User.first_name, 
              User.last_name,
              HasOne('_role', 'Role', identity='role', disabled=True, read_only=True),
              ImageField('_avatar.content', 'Avatar_file', exclude_from_detail=True, read_only=True),
              HasOne('_avatar', "Avatar", identity='file',exclude_from_create=True, exclude_from_edit=True, read_only=True),]


class FileView(ModelView):
    fields = [StringField('id'),
        File.name,
        ImageField('content')]


class UserRoleView(ModelView):
    fields = [
        UserRole.name
    ]


class RegionView(ModelView):
    fields = [
        Region.latitude,
        Region.longitude,
        Region.name,
        HasOne('_thumbnail', 'Thumbnail', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('_thumbnail.content', 'Thumbnail_pic', exclude_from_detail=True),
        HasMany('photos', 'Photos', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('photos.content', 'Photos', multiple=True,  exclude_from_detail=True, exclude_from_list=True)
    ]
    
    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data['_thumbnail.content'][0]
        thumbnail_name = thumbnail.filename,
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(
            name=thumbnail_name[0],
            content=thumbnail
        )
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, thumbnail)  # type: ignore[arg-type]
        del data['_thumbnail.content']
        data['thumbnail'] = thumbnail.id
        photos = data['photos.content'][0]
        del data['photos.content']
        obj = Region(
            **data
        )
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, obj)  # type: ignore[arg-type]
        for photo in photos:
            photo_name = photo.filename,
            photo = F(await photo.read(), filename=photo.filename)
            photo = File(
                name=photo_name[0],
                content=photo
            )
            session.add(photo)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(photo)
                photo = RegionPhoto(
                    region_id=obj.id,
                    photo_id=photo.id
                )
                session.add(photo)
                await session.commit()
                await session.refresh(photo)
            else:
                await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
                await anyio.to_thread.run_sync(session.refresh, photo)  # type: ignore[arg-type]
                photo = RegionPhoto(
                    region_id=obj.id,
                    photo_id=photo.id
                )
                await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
                await anyio.to_thread.run_sync(session.refresh, photo)  # type: ignore[arg-type]
        
        
        
    # async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
    #     session = request.state.session
    #     if isinstance(session, AsyncSession):
    #         obj = await session.get(User, pk)
    #         avatar = await session.get(FileMod, obj.avatar)
    #         await session.delete(avatar)
    #         await session.commit()
    #     else:
    #         obj = avatar = await anyio.to_thread.run_sync(session.get, User, pk)
    #         avatar = await anyio.to_thread.run_sync(session.get, FileMod, obj.avatar)
    #         await anyio.to_thread.run_sync(session.delete, avatar)
    #         await anyio.to_thread.run_sync(session.commit)
    #     avatar = data['avatar_.content'][0]
    #     data = {'name': data['name']}
    #     avatar = File(await avatar.read(), filename=avatar.filename)
    #     avatar = FileMod(
    #         content=avatar
    #     )
    #     session.add(avatar)
    #     if isinstance(session, AsyncSession):
    #         await session.commit()
    #         await session.refresh(avatar)
    #     else:
    #         await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
    #         await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
    #     obj.avatar = avatar.id
    #     obj.name = data['name']
    #     if isinstance(session, AsyncSession):
    #         await session.commit()
    #         await session.refresh(avatar)
    #     else:
    #         await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
    #         await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]


class TourismTypeView(ModelView):
    fields = [
        TourismType.name,
        HasOne('_photo', 'Thumbnail', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('_photo.content', 'Thumbnail_pic', exclude_from_detail=True)
    ]
    
    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data['_photo.content'][0]
        thumbnail_name = thumbnail.filename,
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(
            name=thumbnail_name[0],
            content=thumbnail
        )
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, thumbnail)  # type: ignore[arg-type]
        del data['_photo.content']
        data['photo'] = thumbnail.id
        obj = TourismType(
            **data
        )
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, obj)  # type: ignore[arg-type]
            
            
class PostView(ModelView):
    fields = [
        Post.name,
        Post.header,
        HasOne('_region', 'region', identity='region'),
        HasOne('_tourism_type', 'tourism type', identity='tourism_type'),
        HasOne('_thumbnail', 'Thumbnail', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('_thumbnail.content', 'Thumbnail_pic', exclude_from_detail=True),
        HasMany('tags', 'tags', identity='tags'),
        Post.body,
        HasMany('atttachments', 'atttachments', identity='file'),
    ]
    


@inject
def admin(engine: Database = Provide[Container.db]) -> Admin:
    _ = Admin(engine.engine, title="Admin")
    _.add_view(UserView(User))
    _.add_view(FileView(File, identity="file"))
    _.add_view(UserRoleView(UserRole, identity='role'))
    _.add_view(RegionView(Region, identity='region'))
    _.add_view(TourismTypeView(TourismType, identity='tourism_type'))
    return _
