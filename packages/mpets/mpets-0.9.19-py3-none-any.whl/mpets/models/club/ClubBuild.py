from typing import Optional


from mpets.models.BaseResponse import BaseResponse


class ClubBuild(BaseResponse):
    name: str
    type: str
    level: int
    max_level: int
    bonus: str
    improving: bool
    left_time: Optional[str]
