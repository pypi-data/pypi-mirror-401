from typing import List

from mpets.models.BaseResponse import BaseResponse
from mpets.models.club.ClubPlayer import ClubPlayer


class Club(BaseResponse):
    status: bool
    is_club: bool
    club_id: int
    name: str
    about: str
    founded: str
    level: int
    exp: str
    build_level: int
    pets_amount: str
    pets: List[ClubPlayer]


