import datetime
from typing import Any
import uuid

from sqlalchemy import ForeignKey, func, Identity
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import (
    VARCHAR,
    TEXT,
    INTEGER,
    UUID,
    TIMESTAMP,
    BOOLEAN,
    REAL,
    JSON,
)
from sqlalchemy_file import FileField

from api.configuration.processors import UrlProcessor
from api.pkg.models.resources import Base


class CoordinateFields:
    longitude: Mapped[float] = mapped_column(REAL)
    latitude: Mapped[float] = mapped_column(REAL)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(256))
    nickname: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(64))
    last_name: Mapped[str] = mapped_column(VARCHAR(64))
    avatar: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    header: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    about: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    posts_total: Mapped[int] = mapped_column(INTEGER, default=0)
    location: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    link_tg: Mapped[str] = mapped_column(VARCHAR(128))
    role: Mapped[int] = mapped_column(ForeignKey("user_roles.id"))
    rating: Mapped[float] = mapped_column(REAL, default=0)
    active: Mapped[bool] = mapped_column(BOOLEAN, server_default=expression.false())

    _avatar: Mapped["File"] = relationship("File", foreign_keys=[avatar], single_parent=True)
    _header: Mapped["File"] = relationship("File", foreign_keys=[header], single_parent=True)
    _role: Mapped["UserRole"] = relationship("UserRole")


class Region(Base, CoordinateFields):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(128))
    thumbnail: Mapped[uuid.UUID] = mapped_column(ForeignKey("files.id"))
    description: Mapped[str] = mapped_column(TEXT)

    _thumbnail: Mapped["File"] = relationship(single_parent=True, foreign_keys=[thumbnail],
                                              cascade='all, delete-orphan')
    photos: Mapped[list['File']] = relationship(single_parent=True,
                                                secondary='region_photos',
                                                cascade='all, delete-orphan')


class RegionPhoto(Base):
    __tablename__ = 'region_photos'

    region_id: Mapped[int] = mapped_column(ForeignKey('regions.id',), primary_key=True)
    photo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('files.id'), primary_key=True)


class File(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(128))
    content: Mapped[dict[str, Any]] = mapped_column(
        FileField(upload_storage='default',
                  processors=[UrlProcessor()])
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )


class Post(Base, CoordinateFields):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    region: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    tourism_type: Mapped[int] = mapped_column(ForeignKey("tourism_types.id"))
    name: Mapped[str] = mapped_column(VARCHAR(128))
    header: Mapped[str] = mapped_column(VARCHAR(512))
    body: Mapped[str] = mapped_column(TEXT)
    author: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    link: Mapped[str] = mapped_column(VARCHAR(128))
    draft: Mapped[bool] = mapped_column(BOOLEAN, default=expression.true())
    approved: Mapped[int] = mapped_column(BOOLEAN, default=1)
    thumbnail: Mapped[uuid.UUID] = mapped_column(ForeignKey("files.id"))

    _thumbnail: Mapped["File"] = relationship(primaryjoin="Post.thumbnail == File.id", single_parent=True)
    attachments: Mapped[list["File"]] = relationship(secondary="post_attachments",
                                                     single_parent=True,
                                                     cascade='all, delete-orphan')
    _tourism_type: Mapped["TourismType"] = relationship()
    _region: Mapped["Region"] = relationship()
    tags: Mapped[list['Hashtag']] = relationship(secondary='post_hashtags')


class PostAttachments(Base):
    __tablename__ = "post_attachments"

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    attachment: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id"), primary_key=True
    )


class PostHashtag(Base):
    __tablename__ = "post_hashtags"

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    tag: Mapped[uuid.UUID] = mapped_column(ForeignKey("hashtags.id"), primary_key=True)


class PostRating(Base):
    __tablename__ = "post_rates"

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    rating: Mapped[int] = mapped_column(default=1)


class Hashtag(Base):
    __tablename__ = "hashtags"

    id: Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    
    async def __admin_repr__(self, request):
        return f'{self.name}'


class TourismType(Base):
    __tablename__ = "tourism_types"

    id: Mapped[int] = mapped_column(Identity(start=1, increment=1), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    photo: Mapped[uuid.UUID] = mapped_column(ForeignKey("files.id"), nullable=True)
    
    _photo: Mapped['File'] = relationship(single_parent=True)
