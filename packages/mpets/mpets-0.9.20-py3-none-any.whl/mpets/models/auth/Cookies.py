from pydantic import BaseModel


class Cookies(BaseModel):
    id: int
    hash: str
    verify: str
    PHPSESSID: str


