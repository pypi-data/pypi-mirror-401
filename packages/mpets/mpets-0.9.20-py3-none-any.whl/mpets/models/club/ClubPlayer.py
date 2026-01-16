from mpets.models.BaseResponse import BaseResponse


class ClubPlayer(BaseResponse):
    pet_id: int
    name: str
    rank: str  # TODO сделать Enum
    exp: str  # TODO сделать пересчет в нормальные единицы

