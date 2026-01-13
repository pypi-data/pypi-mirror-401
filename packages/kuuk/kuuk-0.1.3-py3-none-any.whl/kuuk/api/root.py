import logging
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from server.database import DBSessionMiddleware
from server.database import db
from api.routes import (
    health,
    register_entity,
)


# Setup local logger
logger = logging.getLogger("app")


def create_uvicorn_app() -> Starlette:
    """
    Factory function required by uvicorn --factory.
    """
    routes = [
        Route("/register-stage", register_entity, methods=["POST"]),
        Route("/health", health, methods=["GET"]),
    ]
    middleware = [
        Middleware(DBSessionMiddleware)
    ]

    db.setup()
    db.create_tables()
    if db.is_empty_project:
        db.create_empty_project()

    return Starlette(debug=True, routes=routes, middleware=middleware)