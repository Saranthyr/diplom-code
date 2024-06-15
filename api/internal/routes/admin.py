from starlette_admin import HasOne
from starlette_admin.contrib.sqla import Admin, ModelView
from dependency_injector.wiring import Provide, inject
from starlette_admin.fields import (
    ImageField,
    IntegerField,
    FloatField,
    StringField,
    FileField,
)

from ...pkg.connectors.database import Database
from ...pkg.models.containers import Container
from ...pkg.models.postgres import File, Region, User, UserRole


class UserView(ModelView):
    fields = [User.id, User.nickname]


class FileView(ModelView):
    fields = [File.name, File.content]


class UserRoleView(ModelView):
    pass


class RegionView(ModelView):
    pass


@inject
def admin(engine: Database = Provide[Container.db]) -> Admin:
    _ = Admin(engine.engine, title="Admin")
    _.add_view(UserView(User))
    _.add_view(FileView(File, identity="file"))
    _.add_view(UserRoleView(UserRole))
    _.add_view(RegionView(Region))
    return _
