from typing import List

from mpets.models.BaseResponse import BaseResponse
from mpets.models.profile.ChestItem import ChestItem


class Chest(BaseResponse):
    status: bool
    items: List[ChestItem]


