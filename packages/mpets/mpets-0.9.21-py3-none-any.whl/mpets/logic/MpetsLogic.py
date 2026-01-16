from typing import List, Optional, Union

from mpets.models.BaseResponse import BaseResponse
from mpets.models.club.ClubPlayer import ClubPlayer


class MpetsLogic:
    def __init__(self, mpets_api):
        self._api = mpets_api

    async def collect_club_members(
        self,
        club_id: int,
        start_page: int = 1,
        max_pages: Optional[int] = None,
    ) -> Union[List[ClubPlayer], BaseResponse]:
        members: List[ClubPlayer] = []
        page = start_page
        pages_fetched = 0

        while True:
            response = await self._api.club(club_id=club_id, page=page)
            print(response)
            if not getattr(response, "status", False):
                return response

            members.extend(response.pets or [])
            pages_fetched += 1

            if len(response.pets or []) < 10:
                break

            if max_pages is not None and pages_fetched >= max_pages:
                break

            page += 1

        return members

    async def collectMembers(
        self,
        club_id: int,
        start_page: int = 1,
        max_pages: Optional[int] = None,
    ) -> Union[List[ClubPlayer], BaseResponse]:
        return await self.collect_club_members(
            club_id=club_id,
            start_page=start_page,
            max_pages=max_pages,
        )
