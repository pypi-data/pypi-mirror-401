import string
import random


async def random_name(len: int = 10):
    # TODO сделать правдоподобную генерацию никнеймов
    return ''.join(random.sample(string.ascii_lowercase, k=len))


async def random_about():
    # TODO сделать правдоподобную генерацию анкет для аккаунта
    pass


async def random_string(len: int = 12):
    """
    Возвращает случайную строку длинной len.
    """
    return ''.join(random.sample(string.ascii_lowercase, k=len))


