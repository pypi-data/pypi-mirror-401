import asyncio

from loguru import logger

from mpets.utils.constants import HOST_URL


class FastClick(Exception):
    def __init__(self, text):
        self.txt = text


def check_result(method_name: str, content_type: str, status_code: int, body: str):
    """
    """
    # logger.debug(f'Ответ метода {method_name}: [{status_code}] {body}')
    if "Предупреждение" in body:
        raise FastClick("Вы кликаете очень быстро")
    return True


async def make_get_request(session, method, params, proxy, rate_limiter=None):
    # logger.debug(f"Выполняется {method}")
    url = f"{HOST_URL}{method}"
    trace = {}
    try:
        if rate_limiter is not None:
            await rate_limiter.wait()
        async with session.get(url, params=params, proxy=proxy) as response:
            if check_result(url, response.content_type, response.status, await response.text()):
                return response
    except FastClick:
        return await make_get_request(session,
                                      method,
                                      params,
                                      proxy=proxy,
                                      rate_limiter=rate_limiter)
    except asyncio.TimeoutError as e:
        logger.debug(f"timeout error {url}")
        return await make_get_request(session,
                                      method,
                                      params,
                                      proxy=proxy,
                                      rate_limiter=rate_limiter)
    except Exception as e:
        raise e


async def make_post_request(session, method, data, proxy, rate_limiter=None):
    # logger.debug(f"Выполняется {method} с данными {data}")
    url = f"{HOST_URL}{method}"
    trace = {}
    try:
        if rate_limiter is not None:
            await rate_limiter.wait()
        async with session.post(url, data=data, proxy=proxy) as response:
            if check_result(url, response.content_type, response.status, await response.text()):
                return response
    except asyncio.TimeoutError as e:
        logger.debug(f"timeout error {url}")
        return await make_post_request(session,
                                       method,
                                       data,
                                       proxy=proxy,
                                       rate_limiter=rate_limiter)
    except Exception as e:
        raise e
