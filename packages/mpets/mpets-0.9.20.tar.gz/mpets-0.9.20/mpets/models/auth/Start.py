from typing import Optional

from pydantic import BaseModel


class Start(BaseModel):
    status: bool
    pet_id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    cookies: Optional[dict]
