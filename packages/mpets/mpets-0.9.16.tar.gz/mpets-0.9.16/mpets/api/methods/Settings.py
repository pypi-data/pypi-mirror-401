from typing import Union

from aiohttp import ClientResponse
from bs4 import BeautifulSoup

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.utils.constants import HOST_URL
from mpets.utils.functions import random_string


class Settings:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    async def change_pw(self, password: str) -> Union[models.NewPassword, models.Error]:
        try:
            if password is None:
                password = await random_string(len=12)
            if 3 > len(password) > 20:
                # TODO response code
                return models.Error(status=False,
                                    code=7,
                                    message="Пароль должен быть от 3 до 20 символов.")
            response = await self.base_api.request(type="POST",
                                                   method="/change_pw",
                                                   data={"pw": password})
            return models.NewPassword(status=True,
                                      password=password)
            # TODO Добавить проверку обновился пароль или нет
            # if "Пароль успешно изменен!" in response.text:
            #     return {"status": True}
            # else:
            #     return {"status": False,
            #             "code": 8,
            #             "msg": "error"}
        except Exception as ex:
            return models.Error(
                status=False,
                code=0,
                message=str(ex)
            )


async def settings_game(session):
    pass


async def change_name(name, session):
    try:
        if name is None:
            async with session.get(f"{HOST_URL}/change_name") as resp:
                if "change_name" in str(resp.url):
                    resp = BeautifulSoup(await resp.read(), "lxml")
                    name = resp.find("input",
                                     {"class": "login_input mb5"})['value']
                    changed = resp.find("div", {"class": "mb3"}).text
                    changed = changed.split("Изменяли: ")[1].split(" ")[0]
                    changed = int(changed)
                return {'status': True,
                        'name': name,
                        'changed': changed}
        else:
            if len(name) < 3 or len(name) > 12:
                return {"status": False,
                        "code": 1,
                        "msg": "Имя должно быть от 3 до 12 символов!"}
            data = {'name': name}
            async with session.post(f"{HOST_URL}/change_name",
                                    data=data) as resp:
                if "Имя питомца успешно изменено!" in await resp.text():
                    resp = BeautifulSoup(await resp.read(), "lxml")
                    name = resp.find("input",
                                     {"class": "login_input mb5"})['value']
                    changed = resp.find("div", {"class": "mb3"}).text
                    changed = changed.split("Изменяли: ")[1].split(" ")[0]
                    changed = int(changed)
                    return {'status': True,
                            'name': name,
                            'changed': changed}
                if "Питомец с таким именем уже зарегистрирован!" in await resp.text():
                    return {"status": False,
                            "code": 2,
                            "msg": "Питомец с таким именем уже "
                                   "зарегистрирован!"}
                elif "Вам не хватает монет" in await resp.text():
                    return {"status": False,
                            "code": 3,
                            "msg": "Вам не хватает монет"}
                else:
                    return {"status": False,
                            "code": 4,
                            "msg": "error"}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def set_email(email, session):
    pass


async def get_id(session):
    pass


async def logout(session):
    pass
