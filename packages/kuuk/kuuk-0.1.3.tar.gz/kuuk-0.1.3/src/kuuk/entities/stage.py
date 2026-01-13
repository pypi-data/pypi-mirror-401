from __future__ import annotations

import datetime as dt
from typing import Optional
from sqlalchemy.types import  Boolean, DateTime, Integer, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from entities.models import BaseEntity, Registrable
from entities.graph import GraphNodeMixin


class Stage(BaseEntity, Registrable, GraphNodeMixin):
    """
    Shared base entity class to be used for any "Node"-like entity in the graph
    """
    __tablename__ = "Stage"

    __table_args__ = (
        UniqueConstraint("slug", "position", name="uq_stage_slug_position"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    slug: Mapped[str] = mapped_column(
        String(64), nullable=False, doc="Stable, URL-safe identifier."
    )
    display_name: Mapped[str] = mapped_column(
        String(128), nullable=False, doc="Human readable name."
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(512), nullable=True, doc="Optional explanation of the stage."
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Ordering of the stage in the lifecycle (lower comes first).",
    )
    is_terminal: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether this stage represents a terminal/published state.",
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
        doc="UTC timestamp when the stage was first created.",
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        onupdate=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False,
        doc="UTC timestamp when the stage was last modified.",
    )


    def __repr__(self) -> str:
        return (
            f"Stage(id={self.id!r}, slug={self.slug!r}, "
            f"display_name={self.display_name!r}, position={self.position})"
        )
