from typing import List

from pydantic import BaseModel

from mpets.models.BaseResponse import BaseResponse

class Thread(BaseModel):
    id: int
    name: str
    is_forum: bool


class Forum(BaseResponse):
    status: bool
    threads: List[Thread]
