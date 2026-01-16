from mpets.models.BaseResponse import BaseResponse


class MessageEdit(BaseResponse):
    status: bool
    thread_id: int
    message_id: int
    message: str

