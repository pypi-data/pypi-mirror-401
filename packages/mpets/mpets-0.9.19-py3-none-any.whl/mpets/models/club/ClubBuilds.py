from typing import List

from mpets.models.BaseResponse import BaseResponse
from mpets.models.club.ClubBuild import ClubBuild


class ClubBuilds(BaseResponse):
    status: bool
    level: int
    hearts_bonus: str
    exp_bonus: str
    builds: List[ClubBuild]


