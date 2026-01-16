from __future__ import annotations

import os
import time

import aiohttp
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from pydantic import ValidationError
from python_rucaptcha.image_captcha import ImageCaptcha

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.utils import constants
from mpets.utils.constants import HOST_URL
from loguru import logger

from mpets.utils.functions import random_name


class Auth:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    async def check_cookie(self, ) -> models.CookieStatus | models.Error:
        response: ClientResponse = await self.base_api.request(type="GET",
                                                               method="/main")
        if "/main" in str(response.url):
            return models.CookieStatus(status=True,
                                       cookie=True)

        return models.CookieStatus(status=True,
                                   cookie=False)

    async def user_agreement(self, agreement_confirm: bool,
                             params: int) -> models.BooleanStatus | models.Error:
        try:
            response = await self.base_api.request(type="POST",
                                                   method="/user_agreement",
                                                   data={"agreement_confirm": agreement_confirm,
                                                         "params": params})
            if response.status == 200:
                return models.BooleanStatus(status=True)
            else:
                return models.Error(status=False,
                                    code=150,
                                    message=100)
        except Exception as ex:
            return models.Error(status=False,
                                code=0,
                                message=str(ex))

    async def get_captcha(self, ):
        # TODO придумать что можно сделать с этим
        try:
            async with ClientSession(timeout=aiohttp.ClientTimeout(10), connector=None) as ses:
                async with ses.get(f'{HOST_URL}/captcha?r=300') as resp:
                    for item in resp.cookies.items():
                        cookie = str(item[1]).split("=")[1].split(";")[0]
                    filename = f"{str(time.time())}.jpg"
                    with open(filename, 'wb') as fd:
                        fd.write(await resp.read())
                    await ses.close()
                    return {"status": True,
                            "captcha": filename,
                            "cookie": {"PHPSESSID": cookie}}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def extract_cookie(self) -> models.Cookies:
        cookies_dict = {}

        cookies = self.base_api.session.cookie_jar.filter_cookies(constants.HOST_URL)

        for cookie_key, cookie_value in cookies.items():
            # logger.debug(f"key {cookie_key} value {cookie_value}")
            cookies_dict[cookie_key] = cookie_value.value
        try:
            cookies_model = models.Cookies.parse_obj(cookies_dict)
        except ValidationError:
            return models.Cookies(PHPSESSID=cookies_dict['PHPSESSID'],
                                  id=0,
                                  hash="",
                                  verify="")
        return cookies_model

    async def save_gender(self, type: int):
        response = await self.base_api.request(type="GET",
                                               method="/save_gender",
                                               params={"type": type})
        if response.status == 200 and str(response.url) == HOST_URL + "/":
            return {"status": True}
        else:
            return models.Error(status=False,
                                code=1,
                                message="Не удалось создать питомца")

    async def handle_nickname(self, name: str, password: str):
        if name == "standard":
            resp = await self.base_api.mpets_api.change_pw(password=password)
            if resp.status:
                password = resp.password
            else:
                raise Exception
        elif name == "random":
            name = await random_name(len=10)
        else:
            await self.base_api.mpets_api._save(name, password)  # NOQA
        return name, password

    async def start(self, name: str, password: str, type: type) -> models.Start | models.Error:
        response: ClientResponse = await self.base_api.request(type="GET",
                                                               method="/start")
        cookies = await self.extract_cookie()
        logger.debug(cookies)
        self.base_api.cookie = {'PHPSESSID': cookies.PHPSESSID}
        self.base_api.mpets_api.id = cookies.id

        if "gender" not in str(response.url):
            return models.Error(status=False,
                                code=1,
                                message="Не удалось создать питомца")

        try:
            name, password = await self.handle_nickname(name=name, password=password)
        except Exception as ex:
            raise
            return models.Error(status=False,
                                code=2,
                                message="Не удалось создать питомца")
        await self.base_api.mpets_api.user_agreement()
        await self.save_gender(type=13)

        # TODO поменять этот метод на метод получения ника
        profile = await self.base_api.mpets_api.profile()
        # await self.base_api.mpets_api

        return models.Start(status=True,
                            pet_id=cookies.id,
                            name=profile.name,
                            password=password,
                            cookie=self.base_api.cookie)

    async def save(self, response: ClientResponse) -> models.BooleanStatus | models.Error:
        try:
            if "?error" in str(response.url):
                resp = BeautifulSoup(await response.text(), "lxml")
                text = resp.find("span", {"class": "warning"}).text
                # TODO status code
                return models.Error(status=False,
                                    code=1,
                                    message=text)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return models.Error(status=False,
                                code=0,
                                message=str(ex))

    async def solve_captcha(self, api_key, captcha_file):
        user_answer = await ImageCaptcha(rucaptcha_key=api_key)\
            .aio_captcha_handler(captcha_file=captcha_file)
        os.remove(f"{captcha_file}")
        if not user_answer['error']:
            return user_answer['captchaSolve']

    async def login(self, name, password, code: int) -> models.Login | models.Error:
        if self.base_api.cookie is not None:
            if await self.base_api.mpets_api.check_cookies():
                return models.Login(status=True)

        if code is None:
            resp = await self.base_api.mpets_api.get_captcha()
            if resp["status"]:
                self.base_api.mpets_api.captcha_file = resp["captcha"]
            if self.base_api.mpets_api.rucaptcha_api is None:
                code = input("Введите капчу: ")
                # import requests
                # requests.post("/solve")
                # code = None

            else:
                code = await self.solve_captcha(
                    api_key=self.base_api.mpets_api.rucaptcha_api,
                    captcha_file=self.base_api.mpets_api.captcha_file)

        response: ClientResponse = await self.base_api.request(type="POST",
                                                               method="/login",
                                                               data={"name": name,
                                                                     "password": password,
                                                                     "captcha": code})
        cookies = await self.extract_cookie()
        self.base_api.mpets_api.id = cookies.id
        self.base_api.cookie = {'PHPSESSID': cookies.PHPSESSID}
        try:
            if "Неверная captcha. " in await response.text():
                return models.Error(status=False,
                                    code=6,
                                    message="Неверная captcha. Неправильное Имя или Пароль")
            if "Неправильное Имя или Пароль" in await response.text():
                return models.Error(status=False,
                                    code=7,
                                    message="Неправильное Имя или Пароль")
            elif "Ваш питомец заблокирован" in await response.text():
                return models.Error(status=False,
                                    code=6,
                                    message="Ваш питомец заблокирован")
            elif "Прочтите, это важно!" in await response.text():
                return models.Error(status=True,
                                    code=6,
                                    message="")
            elif "Магазин" in await response.text():
                return models.Error(status=True,
                                    code=10,
                                    message="")
        except Exception as ex:
            return models.Error(status=False,
                                code=0,
                                message=ex)
