from entities.models import TypeEntity
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy.types import Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from entities.models.base import BaseEntity
from entities.models.registrable import Registrable
import datetime as dt


class Link(BaseEntity, Registrable):

    __tablename__ = "Link"
    __table_args__ = (
        UniqueConstraint("source_id", "target_id", name="uq_edge_source_target"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("Stage.id"), nullable=False)  # noqa: E501
    target_id: Mapped[str] = mapped_column(String(36), ForeignKey("Stage.id"), nullable=False)  # noqa: E501
    link_type: Mapped[TypeEntity] = mapped_column(Enum(TypeEntity), nullable=False)
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
