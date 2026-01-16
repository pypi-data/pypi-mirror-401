import datetime
from typing import Optional

from mpets.models.BaseResponse import BaseResponse


class Profile(BaseResponse):
    status: bool
    pet_id: int
    name: str
    level: int
    ava_id: int
    last_login: Optional[str]
    effect: Optional[str]
    beauty: int
    coins: int
    hearts: int
    family_id: Optional[int]
    family_name: Optional[str]
    club_id: Optional[int]
    club: Optional[str]
    rank: Optional[str]
    club_const: Optional[int]
    club_day: Optional[int]
    club_day_date: Optional[datetime.datetime]
    day: int
    register_day: datetime.datetime
