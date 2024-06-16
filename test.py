from dataclasses import dataclass
import json
from typing import Any, Coroutine, Dict, List, Optional, Sequence
from uuid import uuid4
import uuid
from wsgiref.util import request_uri
from fastapi import Request
from fastapi.datastructures import FormData
from sqlalchemy import (
    ForeignKey,
    create_engine,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, lazyload, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.sql import Select
import anyio.to_thread
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from libcloud.storage.types import Provider
from libcloud.storage import providers
from libcloud.storage.drivers.s3 import S3StorageDriver
from sqlalchemy_file.storage import StorageManager
from sqlalchemy_file import File, FileField, ImageField
from sqlalchemy_file.processors import Processor
from starlette_admin import BaseField, HasMany, HasOne, RelationField, RequestAction, RowActionsDisplayType, StringField
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.contrib.sqla.helpers import build_query
from starlette_admin.fields import IntegerField, ImageField as IF, FileField as FF


class TestProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()
    
    def process(self, file: File, upload_storage: str | None = None) -> None:
        print(file)
        file.update({'url': file['url'].split('?')[0]})


class Base(DeclarativeBase):
    pass


class IDMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base, IDMixin):
    __tablename__ = "user"
    name: Mapped[str]
    avatar: Mapped[str] = mapped_column(ForeignKey('file.id',
                                                   ondelete="SET NULL",
                                                   onupdate="CASCADE"), nullable=True)
    # avatar: Mapped[dict[str, Any]] = mapped_column(FileField(processors=[TestProcessor()]))
    # av: AssociationProxy[dict] = association_proxy('avatar_',
    #                                      'content')
    
    avatar_: Mapped['FileMod'] = relationship(cascade="all, delete-orphan", single_parent=True)
    
class FileMod(Base):
    __tablename__ = 'file'
    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    content: Mapped[dict[str, Any]] = mapped_column(ImageField(upload_storage='default',
                                                               processors=[TestProcessor()]))


# class Task(Base, IDMixin):
#     __tablename__ = "task"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str]
#     description: Mapped[str]
#     assignees: Mapped[list[User]] = relationship(
#         "User",
#         secondary="assignment",
#     )


# class Assignment(Base, IDMixin):
#     __tablename__ = "assignment"
#     user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
#     task_id: Mapped[int] = mapped_column(ForeignKey(Task.id))


class UserView(ModelView):
    label = "Users"
    name = "User"
    fields = [
        StringField('name',
                    'name'),
        StringField('id',
                    'id'),
        IF("avatar_.content", 'AVATAR', id='av',
           exclude_from_detail=True),
        IF("_meta", 'ava', read_only=True, exclude_from_list=True),
        StringField("avatar_"),
        HasOne('avatar_', identity='avatar_', multiple=False, 
               disabled=True,
               exclude_from_create=True,
               exclude_from_edit=True)
        
    ]
    
    
    async def create(self, request: Request, data: Dict[str, Any]):
        session = request.state.session
        avatar = data['avatar_.content'][0]
        data = {'name': data['name']}
        avatar = File(await avatar.read(), filename=avatar.filename)
        avatar = FileMod(
            content=avatar
        )
        session.add(avatar)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(avatar)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
        data['avatar'] = avatar.id
        obj = User(
            **data
        )
        session.add(obj)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(avatar)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
        
        
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        session = request.state.session
        if isinstance(session, AsyncSession):
            obj = await session.get(User, pk)
            avatar = await session.get(FileMod, obj.avatar)
            await session.delete(avatar)
            await session.commit()
        else:
            obj = avatar = await anyio.to_thread.run_sync(session.get, User, pk)
            avatar = await anyio.to_thread.run_sync(session.get, FileMod, obj.avatar)
            await anyio.to_thread.run_sync(session.delete, avatar)
            await anyio.to_thread.run_sync(session.commit)
        avatar = data['avatar_.content'][0]
        data = {'name': data['name']}
        avatar = File(await avatar.read(), filename=avatar.filename)
        avatar = FileMod(
            content=avatar
        )
        session.add(avatar)
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(avatar)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
        obj.avatar = avatar.id
        obj.name = data['name']
        if isinstance(session, AsyncSession):
            await session.commit()
            await session.refresh(avatar)
        else:
            await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
            await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]

    
class FileView(ModelView):
    fields = [
        IF('content')
    ]
    
    # async def create(self, request: Request, data: dict) -> Any:
    #     session = request.state.session
    #     avatar = FileMod()
    #     data['content'] = data['avatar']
    #     avatar = await self._populate_obj(request, avatar, data)
    #     session.add(avatar)
    #     if isinstance(session, AsyncSession):
    #         await session.commit()
    #         await session.refresh(avatar)
    #     else:
    #         await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
    #         await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
    #     data['avatar'] = avatar.id
    #     print(data)
    #     obj = User()
    #     obj = await self._populate_obj(request, obj, data)
    #     session.add(obj)
    #     if isinstance(session, AsyncSession):
    #         await session.commit()
    #         await session.refresh(avatar)
    #     else:
    #         await anyio.to_thread.run_sync(session.commit)  # type: ignore[arg-type]
    #         await anyio.to_thread.run_sync(session.refresh, avatar)  # type: ignore[arg-type]
    # def after_edit(self, request: Request, obj: User):
    #     print(obj.avatar)
    #     return request

# class TaskView(ModelView):
#     label = "Tasks"
#     name = "Task"
#     fields = [
#         Task.id,
#         Task.title,
#         Task.description,
#         Task.assignees,
#     ]
#     def get_list_query(self) -> Select:
#         return super().get_list_query().where(Task.id == 1)
    
#     def get_count_query(self) -> Select:
#         return super().get_count_query().where(Task.id == 1)


# class AssignmentView(ModelView):
#     # def can_create(self, request: Request) -> bool:
#     #     return False
#     # def can_view_details(self, request: Request) -> bool:
#     #     return True
#     # def can_delete(self, request: Request) -> bool:
#     #     return False
#     # def can_edit(self, request: Request) -> bool:
#     #     return True
#     row_actions_display_type = RowActionsDisplayType.DROPDOWN
#     # row_actions = ["view"]
#     # actions = []
#     export_fields = []
#     export_types = []
#     label = "Assignments"
#     name = "Assignment"
#     column_visibility = False
#     search_builder = False
#     responsive_table = True
#     save_state = True
#     fields = [
#         IntegerField(
#             name="id",
#             label="ID",
#             help_text="ID of the record.",
#             read_only=True,
#         ),
#         IntegerField(
#             name="user_id",
#             label="User ID",
#             help_text="User ID of the record.",
#             read_only=True,
#         ),
#         IntegerField(
#             name="task_id",
#             label="Task ID",
#             help_text="Task ID of the record.",
#             read_only=True,
#         )
        
#     ]


engine = create_engine(
    "sqlite:///db.sqlite3",
    connect_args={"check_same_thread": False},
    echo=True,
)
session = sessionmaker(bind=engine, autoflush=False)


def init_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session() as db:
        pass


app = Starlette(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    # on_startup=[init_database],
)

drv = providers.get_driver(Provider.S3)
print(isinstance(drv, S3StorageDriver))
drv = S3StorageDriver('key1', 'key2', False, 'localhost', port=8333)
# cnx = drv('key1', 'key2', False, host='127.0.0.1', port=8333)
try:
    drv.create_container('avatars')
except Exception:
    pass
ct = drv.get_container('avatars')
obj = drv.upload_object('Screenshot from 2024-03-15 14-28-10.png', ct, str(uuid4()))
# print(obj.get_cdn_url())
StorageManager.add_storage("default", ct)

# Create admin
admin = Admin(engine, title="Example: Association Objects")

# Add views
# admin.add_view(AssignmentView(model=Assignment))
# admin.add_view(TaskView(model=Task))
admin.add_view(UserView(User))
admin.add_view(FileView(FileMod, identity='avatar_'))

# Mount admin
admin.mount_to(app)