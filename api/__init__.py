import os.path
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request, Response
from sqlalchemy_file.storage import StorageManager
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from .configuration.storage import S3Storage
from .pkg.models.containers import Container
from .internal.routes.admin import admin
from .internal.routes.auth import router as auth
from .internal.routes.posts import router as posts
from .internal.routes.user import router as user
from .internal.routes.searches import router as search
from .internal.routes.regions import router as regions
from .internal.routes.tourism import router as tourism

load_dotenv()

container = Container()
container.config.from_ini(os.path.abspath("/configs/config.ini"))
container.wire(
    modules=[
        ".internal.routes.auth",
        ".internal.routes.posts",
        ".internal.routes.user",
        ".internal.routes.searches",
        ".internal.routes.regions",
        ".internal.routes.tourism",
        ".internal.routes.admin",
        "__main__",
    ]
)
container.init_resources()

app = FastAPI()
admin = admin()

@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "*"
    return response

app.include_router(auth)
app.include_router(posts)
app.include_router(user)
app.include_router(search)
app.include_router(regions)
app.include_router(tourism)

app.container = container
admin.mount_to(app)
