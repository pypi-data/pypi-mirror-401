from __future__ import annotations
from contextvars import ContextVar
from typing import Optional
from functools import cached_property
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)
from entities.models import BaseEntity
from entities import Project
from starlette.requests import Request
from starlette.responses import Response
from server.configs import settings


_session_ctx: ContextVar[Optional[Session]] = ContextVar("session", default=None)


class DatabaseManager:
    def __init__(self):
        self._engine = None
        self._session_factory = None
        self.initialized = False

    def get_url(self) -> str:
        return settings.get("DATABASE_URL", "sqlite:///./app.db")

    def setup(self):
        """Initializes the engine and session factory."""
        if self._engine:
            return

        database_url = self.get_url()
        connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}

        self._engine = create_engine(
            database_url,
            future=True,
            connect_args=connect_args,
            pool_pre_ping=True
        )

        if "sqlite" in database_url:
            with self._engine.connect() as con:
                con.exec_driver_sql("PRAGMA journal_mode=WAL")
                con.exec_driver_sql("PRAGMA synchronous=NORMAL")

        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True
        )

        self.initialized = True

    def create_empty_project(self) -> None:
        if not self._engine or not self.initialized:
            return
        session = self.get_session()
        project = Project(name="Untitled Project", description="My very first project!")
        project.save(session)

    def get_session(self) -> Session:
        if not self._session_factory:
            raise RuntimeError("Database not initialized. Call setup() first.")
        return self._session_factory()

    @property
    def engine(self):
        """Expose engine publicly so other modules can use it for table creation."""
        return self._engine

    def create_tables(self) -> None:
        BaseEntity.metadata.create_all(db.engine)

    @cached_property
    def is_empty_project(self) -> bool:
        if not self._engine or not self.initialized:
            return False
        session = self.get_session()
        query = select(Project).limit(1) # noqa F821
        result = session.execute(query).scalars().first()
        return True if result is None else False


# Singleton Instance
db = DatabaseManager()


def get_db_session() -> Session:
    """Retrieves the session for the current context (request)."""
    session = _session_ctx.get()
    if session is None:
        raise RuntimeError("No DB session found in current context. Are you inside a request?")
    return session


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        session = db.get_session()
        token = _session_ctx.set(session)
        try:
            response = await call_next(request)
            return response
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            _session_ctx.reset(token)