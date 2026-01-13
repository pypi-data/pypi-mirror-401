from sqlalchemy.orm import DeclarativeBase, declared_attr
import enum


class TypeEntity(enum.Enum):
    STAGE = "stage"
    GROUP = "group"


class TypeLink(enum.Enum):
    REFERENCE = "reference"
    DISTINCT = "distinct"
    FORMULA = "formula"


class BaseEntity(DeclarativeBase):
    """
    Shared base entity class to be used for any "Node"-like entity in the graph
    """
    @declared_attr
    def __tablename__(cls) -> str:
        name = []
        for idx, ch in enumerate(cls.__name__):
            if ch.isupper() and idx > 0:
                name.append("_")
            name.append(ch.lower())
        return "".join(name)
