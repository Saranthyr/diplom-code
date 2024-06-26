import uuid

from sqlalchemy import ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import INTEGER, UUID

from ..resources import Base


class User(Base):
    __tablename__ = "users"

    pk: Mapped[int] = mapped_column(
        Identity(True, start=1, increment=1), primary_key=True
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, default=uuid.uuid4)


class UserTelegeramChat(Base):
    __tablename__ = "user_telegram_chats"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    chat: Mapped[int] = mapped_column(INTEGER, nullable=False)
