from pydantic import BaseModel


class CookieStatus(BaseModel):
    status: bool
    cookie: bool
