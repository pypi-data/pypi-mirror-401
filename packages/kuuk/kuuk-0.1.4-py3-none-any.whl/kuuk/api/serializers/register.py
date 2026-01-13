from pydantic import BaseModel
from typing import Optional
import datetime as dt


class StageSchema(BaseModel):
    slug: str
    display_name: str
    description: Optional[str] = None
    position: int
    is_terminal: bool
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        orm_mode = True