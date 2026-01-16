from pydantic import BaseModel


class NewPassword(BaseModel):
    status: bool
    password: str

