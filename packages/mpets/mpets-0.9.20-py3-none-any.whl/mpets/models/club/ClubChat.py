from typing import List

from mpets.models.BaseResponse import BaseResponse
from mpets.models.club.ClubChatMessage import ClubChatMessage


class ClubChat(BaseResponse):
    club_id: int
    page: int
    messages: List[ClubChatMessage]
