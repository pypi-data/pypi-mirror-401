from typing import Any, Union

from loguru import logger

from mpets import models


def catch_error(func) -> Union[Any, models.Error]:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            # logger.exception("Error")
            return models.Error(status=False,
                                code=0,
                                message=str(ex))

    return wrapper

