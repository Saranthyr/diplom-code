import os

from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin
from starlette_admin.auth import AuthProvider, AdminConfig, AdminUser
from starlette_admin.exceptions import LoginFailed
from dependency_injector.wiring import Provide, inject

from ...configuration.security import pwd_context
from ...pkg.connectors.database import Database
from ...pkg.models.containers import Container
from ..services.admin_views import (
    UserRoleView,
    UserView,
    TagView,
    FileView,
    PostView,
    RegionView,
    TourismTypeView,
)
from ...pkg.models.postgres import (
    File,
    Hashtag,
    Post,
    Region,
    TourismType,
    User,
    UserRole,
)


class Auth(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        session = request.state.session
        user = select(
            User.id,
            User.role,
            User.password,
            User.first_name,
            User.last_name,
            User.nickname,
            User.avatar,
        ).where(User.username == username)
        user = await session.execute(user)
        user = user.one_or_none()
        if user is None:
            raise LoginFailed("Incorrect username or password")
        elif not pwd_context.verify(password, user.password):
            raise LoginFailed("Incorrect username or password")
        elif user.role not in [1, 2]:
            raise LoginFailed("No permissions")
        avatar = None
        if user.avatar is not None:
            avatar = select(File.content).where(File.id == User.avatar)
            avatar = await session.execute(avatar)
            avatar = avatar.scalar_one_or_none()
        data = {
            "user_id": str(user.id),
            "user_role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "nickname": user.nickname,
            "avatar": avatar,
        }
        request.session.update(data)
        return response

    async def is_authenticated(self, request: Request) -> bool:
        token = request.session.get("user_role", None)
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
        return AdminConfig(app_title=title)

    def get_admin_user(self, request: Request) -> AdminUser | None:
        data = request.session.get("avatar")
        url = None
        if data is not None:
            url = data["url"]
        return AdminUser(username=request.session.get("nickname"), photo_url=url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response


@inject
def admin(engine: Database = Provide[Container.db]) -> Admin:
    _ = Admin(
        engine.engine,
        title="Admin",
        auth_provider=Auth(),
        middlewares=[
            Middleware(
                SessionMiddleware, secret_key=os.environ["JWT_SECRET"], max_age=None
            )
        ],
        i18n_config=I18nConfig(default_locale='ru')
    )
    _.add_view(UserView(User, identity="user", label="Пользователи"))
    _.add_view(FileView(File, identity="file", label="Файлы"))
    _.add_view(UserRoleView(UserRole, identity="role", label="Роли"))
    _.add_view(RegionView(Region, identity="region", label="Регионы"))
    _.add_view(TourismTypeView(TourismType, identity="tourism_type", label="Типы туризма"))
    _.add_view(PostView(Post, label="Статьи к модерации"))
    _.add_view(TagView(Hashtag, identity="tags", label="Хештеги"))
    return _
