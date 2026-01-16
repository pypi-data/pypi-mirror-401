from pydantic import BaseModel


class BooleanStatus(BaseModel):
    status: bool

