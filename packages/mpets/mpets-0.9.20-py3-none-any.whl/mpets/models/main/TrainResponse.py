from typing import List

from pydantic import BaseModel

from mpets.models.BaseResponse import BaseResponse


class Train(BaseModel):
    skill: str
    level: int
    price: int


class TrainResponse(BaseResponse):
    status: bool
    trains: List[Train]
