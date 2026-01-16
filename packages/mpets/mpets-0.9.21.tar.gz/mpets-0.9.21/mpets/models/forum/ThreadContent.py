from typing import List, Optional

from mpets.models.BaseResponse import BaseResponse
from mpets.models.forum.ThreadMessage import ThreadMessage


class ThreadContent(BaseResponse):
    status: bool
    id: int
    name: str
    page: int
    messages: List[ThreadMessage]
    closed: str
    moderator_id: Optional[int]
    moderator: Optional[str]

