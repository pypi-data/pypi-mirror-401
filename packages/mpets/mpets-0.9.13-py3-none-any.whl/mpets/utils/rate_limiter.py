import asyncio
import time
from typing import Optional


class RateLimiter:
    def __init__(self, requests_per_second: Optional[float] = None):
        self._lock = asyncio.Lock()
        self._requests_per_second: Optional[float] = None
        self._min_interval: float = 0.0
        self._next_time: float = 0.0
        self.set_rate(requests_per_second)

    @property
    def requests_per_second(self) -> Optional[float]:
        return self._requests_per_second

    def set_rate(self, requests_per_second: Optional[float]):
        if requests_per_second and requests_per_second > 0:
            self._requests_per_second = float(requests_per_second)
            self._min_interval = 1.0 / self._requests_per_second
        else:
            self._requests_per_second = None
            self._min_interval = 0.0
        self._next_time = 0.0

    async def wait(self):
        if not self._requests_per_second:
            return
        async with self._lock:
            now = time.monotonic()
            if self._next_time > now:
                await asyncio.sleep(self._next_time - now)
                now = time.monotonic()
            self._next_time = max(self._next_time, now) + self._min_interval
