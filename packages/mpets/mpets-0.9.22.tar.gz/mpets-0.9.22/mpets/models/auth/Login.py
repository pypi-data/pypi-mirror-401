from typing import Optional

from pydantic import BaseModel


class Login(BaseModel):
    status: bool
    pet_id: Optional[int]
    name: Optional[str]
    cookies: Optional[dict]

