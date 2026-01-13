from abc import abstractmethod
from typing import Any
from sqlalchemy.orm import Session


class Registrable():
    @abstractmethod
    def register(self, graph: Any) -> None:
        """Register the entity with the system."""
        pass

    @abstractmethod
    def unregister(self, graph: Any) -> None:
        """Unregister the entity from the system."""
        pass

    def save(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self
