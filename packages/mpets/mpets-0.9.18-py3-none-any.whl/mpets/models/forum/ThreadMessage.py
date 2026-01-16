import datetime
from typing import Optional

from pydantic import BaseModel



class ThreadMessage(BaseModel):
    id: Optional[int]
    pet_id: int
    name: Optional[str]
    message_id: int
    message: str
    post_date: Optional[str]
    normal_date: Optional[datetime.datetime]


