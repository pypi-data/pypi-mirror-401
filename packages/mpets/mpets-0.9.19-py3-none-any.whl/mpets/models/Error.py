from pydantic import BaseModel


class Error(BaseModel):
    status: bool
    code: int
    message: str
