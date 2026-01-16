from typing import Optional

from mpets.models.BaseResponse import BaseResponse
from mpets.models.profile.ChestItemTypes import ChestItemTypes


class ChestItem(BaseResponse):
    type: ChestItemTypes
    item_id: int

    timeout: Optional[str]
    wear_item: bool = False


