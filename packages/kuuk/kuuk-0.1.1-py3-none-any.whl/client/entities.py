from dataclasses import dataclass

@dataclass
class EntityWrapper:
    name: str
    description: str
    position: int


def Stage(EntityWrapper):
    pass