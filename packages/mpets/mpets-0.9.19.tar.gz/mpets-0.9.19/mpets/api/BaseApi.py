from typing import Optional, Dict, TYPE_CHECKING

import aiohttp
from aiohttp_socks import ProxyConnector
from loguru import logger

from mpets.api import api
from mpets.utils.rate_limiter import RateLimiter

if TYPE_CHECKING:
    from mpets import MpetsApi


class BaseApi:
    def __init__(self, cookie, timeout, connector, proxy, mpets_api,
                 requests_per_second: Optional[float] = None):
        self._cookie = cookie
        self._timeout = aiohttp.ClientTimeout(timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._connector = connector
        self._proxy = proxy
        self._mpets_api: MpetsApi = mpets_api
        self._rate_limiter = RateLimiter(requests_per_second)

    @property
    def session(self):
        return self._session

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        self._cookie = value

    async def get_new_session(self, cookie=None) -> aiohttp.ClientSession:
        if self._session is not None:
            logger.debug("Закрыл сессию")
            try:
                await self._session.close()
            except Exception as ex:
                pass

        if cookie is not None:
            self._cookie = cookie
        return aiohttp.ClientSession(
            cookies=self._cookie,
            timeout=self._timeout,
            connector=self._connector,
        )

    async def get_session(self, cookies=None) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = await self.get_new_session(cookie=cookies)

        if not self._session._loop.is_running():  # NOQA
            # Hate `aiohttp` devs because it juggles event-loops and breaks already opened session
            # So... when we detect a broken session need to fix it by re-creating it
            # @asvetlov, if you read this, please no more juggle event-loop inside aiohttp, it breaks the brain.
            await self._session.close()
            self._session = await self.get_new_session(cookie=cookies)

        return self._session

    async def request(self, type: str,
                      method: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None):
        """
        Запрос
        """
        if type == "GET":
            return await api.make_get_request(await self.get_session(),
                                              method,
                                              params,
                                              proxy=self._proxy,
                                              rate_limiter=self._rate_limiter)
        elif type == "POST":
            return await api.make_post_request(await self.get_session(),
                                               method,
                                               data,
                                               proxy=self._proxy,
                                               rate_limiter=self._rate_limiter)

    async def close_session(self):
        if self._session is not None:
            await self._session.close()

    @property
    def mpets_api(self):
        return self._mpets_api

    @property
    def rate_limit(self) -> Optional[float]:
        return self._rate_limiter.requests_per_second

    def set_rate_limit(self, requests_per_second: Optional[float]):
        self._rate_limiter.set_rate(requests_per_second)
