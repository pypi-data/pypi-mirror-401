from typing import Optional

from pydantic import BaseModel


class ClubChatMessage(BaseModel):
    pet_id: int
    name: str
    message_id: int
    message: Optional[str]
    message_deleted: bool
    moderator_id: Optional[int]
