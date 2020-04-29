from fastapi import FastAPI

from .api.routes import api_router
from .core.config import settings
from .core.db import register_db
from .core.middlewares import add_middlewares
from .core.redis import connect_redis, disconnect_redis


async def on_startup_event() -> None:
    await connect_redis()


async def on_shutdown_event() -> None:
    await disconnect_redis()


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_TITLE,
    # Required to load deployed api docs. Result of bug expected to be fixed soon.
    openapi_url="/api/openapi.json"
)
app.include_router(api_router)
app.add_event_handler("startup", on_startup_event)
app.add_event_handler("shutdown", on_shutdown_event)
add_middlewares(app)
register_db(app)
