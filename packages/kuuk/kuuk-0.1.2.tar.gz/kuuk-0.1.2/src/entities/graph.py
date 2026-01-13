from sqlalchemy.types import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from entities.models import Registrable, BaseEntity
from entities.link import Link
import datetime as dt

class GraphNodeMixin():

    @property
    def connect(self):
        session = get_db_session()
        link = Link()
        session.add(link)
        session.commit()
        return link


class Graph(BaseEntity, Registrable):
    __tablename__ = "Graph"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
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
