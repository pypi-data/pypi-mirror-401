from entities.models import BaseEntity, Registrable
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class Project(BaseEntity, Registrable):
    __tablename__ = "Project"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)