from mpets.models.BaseResponse import BaseResponse


class EditThread(BaseResponse):
    status: bool
    forum_id: int
    id: int
    name: str
    message_id: int
    message: str
