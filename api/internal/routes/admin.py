import asyncio
import datetime
import os
from typing import Any, Dict
import uuid

import anyio.from_thread
from fastapi import Request, Response
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select
from sqlalchemy_file import File as F
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import HasOne, row_action
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.auth import AuthProvider, AdminConfig, AdminUser
from starlette_admin.exceptions import FormValidationError, LoginFailed
from starlette_admin.fields import (
    ImageField,
    IntegerField,
    FloatField,
    StringField,
    FileField,
    HasOne,
    HasMany,
    TinyMCEEditorField
)
from dependency_injector.wiring import Provide, inject

from ...configuration.security import decode_token, create_token, pwd_context
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
    
    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        thumbnail = data['_avatar.content'][0]
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
        del data['_avatar.content']
        data['avatar'] = thumbnail.id
        obj = User(
            **data
        )
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
        thumbnail = data['_avatar.content'][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(
            name=thumbnail_name,
            content=thumbnail
        )
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data['_avatar.content']
        data['avatar'] = thumbnail.id
        obj.avatar = data['avatar']
        obj.nickname = data['nickname']
        obj.first_name = data['first_name']
        obj.last_name = data['last_name']
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)


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
        Region.thumbnail,
        TinyMCEEditorField('description'),
        HasOne('_thumbnail', 'Thumbnail', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('_thumbnail.content', 'Thumbnail_pic', exclude_from_detail=True),
        HasMany('photos', 'Photos', identity='file', exclude_from_create=True, exclude_from_edit=True)
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
        
        
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        if isinstance(session, AsyncSession):
            obj = await session.get(Region, pk)
            thumbnail = await session.get(File, obj.thumbnail)
            await session.delete(thumbnail)
            await session.commit()
        thumbnail = data['_thumbnail.content'][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(
            name=thumbnail_name,
            content=thumbnail
        )
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data['_thumbnail.content']
        photos = data['photos.content'][0]
        del data['photos.content']
        data['thumbnail'] = thumbnail.id
        stmt = delete(RegionPhoto).where(RegionPhoto.region_id == pk)
        session.add(stmt)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
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
        obj.latitude = data['latitude']
        obj.longitude = data['longitude']
        obj.name = data['name']
        obj.description = data['description']
        obj.thumbnail = data['thumbnail']
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
        


class TourismTypeView(ModelView):
    fields = [
        TourismType.name,
        TourismType.photo,
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
        del data['_photo.content']
        data['photo'] = thumbnail.id
        obj = TourismType(
            **data
        )
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
            
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        if isinstance(session, AsyncSession):
            obj = await session.get(TourismType, pk)
            thumbnail = await session.get(File, obj.photo)
            if thumbnail is not None:
                await session.delete(thumbnail)
                await session.commit()
        thumbnail = data['_photo.content'][0]
        thumbnail_name = thumbnail.filename
        thumbnail = F(await thumbnail.read(), filename=thumbnail.filename)
        thumbnail = File(
            name=thumbnail_name,
            content=thumbnail
        )
        session.add(thumbnail)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(thumbnail)
        del data['_photo.content']
        data['photo'] = thumbnail.id
        obj.name = data['name']
        obj.photo = data['photo']
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(obj)
            
            
class PostView(ModelView):
    fields = [
        Post.name,
        Post.header,
        HasOne('_region', 'region', identity='region'),
        HasOne('_tourism_type', 'tourism type', identity='tourism_type'),
        HasOne('_thumbnail', 'Thumbnail', identity='file', exclude_from_create=True, exclude_from_edit=True),
        ImageField('_thumbnail.content', 'Thumbnail_pic', exclude_from_detail=True),
        HasMany('tags', 'tags', identity='tags'),
        TinyMCEEditorField('body', exclude_from_list=True),
        HasMany('attachments', 'attachments', identity='file'),
    ]
    
    def can_edit(self, request: Request) -> bool:
        return False
    
    def can_create(self, request: Request) -> bool:
        return False
    
    def can_delete(self, request: Request) -> bool:
        return "1" == request.session.get('user_role', None)
    
    @row_action(
        name='approve_publication',
        text='Одобрить к публикации',
        confirmation="Вы точно хотите одобрить эту статью к публикации?",
        icon_class='fa-solid fa-check',
        exclude_from_list=True
    )
    async def approve_publication(self, request: Request, pk: Any) -> str:
        session = request.state.session
        post = await self.find_by_pk(request, pk)
        post.approved = 2
        session.add(post)
        await session.commit()
        return f'Publication accepted'
    
    @row_action(
        name='deny_publication',
        text="Отклонить публикацию",
        confirmation="Вы точно хотите отклонить эту статью к публикации?",
        icon_class='fa-solid fa-xmark',
        exclude_from_list=True
    )
    async def deny_publication(self, request: Request, pk: Any) -> str:
        session = request.state.session
        post = await self.find_by_pk(request, pk)
        post.approved = 3
        session.add(post)
        await session.commit()
        return f'Publication accepted'
    
    def get_list_query(self) -> Select:
        return super().get_list_query().where(Post.approved == 1)


class Auth(AuthProvider):
    async def login(self, username: str, password: str, remember_me: bool, request: Request, response: Response) -> Response:
        session = request.state.session
        user = select(User.id, User.role, User.password, User.first_name,
                      User.last_name, User.nickname, User.avatar).where(User.username == username)
        user = await session.execute(user)
        user = user.one_or_none()
        avatar = None
        if user.avatar is not None:
            avatar = select(File.content).where(File.id == User.avatar)
            avatar = await session.execute(avatar)
            avatar = avatar.scalar_one_or_none()
        if user is None:
            raise LoginFailed("Incorrect username or password")
        elif not pwd_context.verify(password, user.password):
            raise LoginFailed("Incorrect username or password")
        elif user.role not in [1,2]:
            raise LoginFailed('No permissions')
        else:
            data = {'user_id': str(user.id),
                    'user_role': user.role,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'nickname': user.nickname,
                    'avatar': avatar}
            request.session.update(data)
            return response
        
    async def is_authenticated(self, request: Request) -> bool:
        token = request.session.get('user_role', None)
        if token is None:
            return False
        try:
            if token not in [1, 2]:
                raise Exception
        except Exception:
            return False
        return True
    
    def get_admin_config(self, request: Request) -> AdminConfig | None:
        title = f"Hello, {request.session.get('first_name')} {request.session.get('last_name')}"
        return AdminConfig(
            app_title=title
        )
    
    def get_admin_user(self, request: Request) -> AdminUser | None:
        data = request.session.get('avatar')
        url = None
        if data is not None:
            url = data['url']
        return AdminUser(username=request.session.get('nickname'), photo_url=url)
    
    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
        

@inject
def admin(engine: Database = Provide[Container.db]) -> Admin:
    _ = Admin(engine.engine,
              title="Admin",
              auth_provider=Auth(),
              middlewares=[Middleware(SessionMiddleware, secret_key=os.environ['JWT_SECRET'], max_age=None)])
    _.add_view(UserView(User))
    _.add_view(FileView(File, identity="file"))
    _.add_view(UserRoleView(UserRole, identity='role'))
    _.add_view(RegionView(Region, identity='region'))
    _.add_view(TourismTypeView(TourismType, identity='tourism_type'))
    _.add_view(PostView(Post))
    return _
