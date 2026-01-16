import asyncio
import datetime
import re
from typing import Optional, Union

from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from loguru import logger

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.utils.catch_error import catch_error
from mpets.utils.constants import HOST_URL


class Profile:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    @catch_error
    def get_ava_id(self, bs_content) -> Optional[int]:
        img_ava = bs_content.find('img', {'class': 'ava_prof'}).get('src', None)
        ava_id = img_ava.split('avatar')[1].split('.')[0]

        return ava_id

    @catch_error
    def get_name(self, bs_content) -> Optional[str]:
        name = bs_content.find("div", {"class": "stat_item"}) \
            .text.split(", ")[0].replace(' ', '')
        return name.replace('\n', '')

    @catch_error
    def get_level(self, bs_content) -> Optional[int]:
        level = bs_content.find("div", {"class": "stat_item"})
        level = level.find("a",
                           {"class": "darkgreen_link", "href": "/avatars"})
        level = int(
            level.next_element.next_element.split(", ")[1].split(" ")[0])

        return level

    @catch_error
    def get_level_view_profile(self, bs_content) -> Optional[int]:
        level = \
            bs_content.find("div", {"class": "stat_item"}).text.rsplit(", ", 1)[1].split(" ")[0]
        level = int(level)
        return level

    @catch_error
    def get_rank(self, bs_content) -> Optional[list]:
        rank = bs_content.find("div", {"class": "left font_14 pet_profile_stat"}) \
            .find_all("div", {"class": "stat_item"})
        return rank

    @catch_error
    def get_last_seen(self, bs_content) -> Optional[str]:
        last_login = "online"
        try:
            last_login = bs_content.find("span", {''}).text
        except Exception as ex:
            last_login = bs_content.find("span", {'c_red'}).text
        last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)  # noqa
        return last_login

    @catch_error
    def get_vip_effect(self, bs_content) -> Optional[int]:
        effect = bs_content.text.split(": ")[1].rsplit('  ', maxsplit=1)[0]
        return effect

    @catch_error
    def get_premium_effect(self, bs_content) -> Optional[int]:
        effect = bs_content.text.split(": ")[1].rsplit(' ', maxsplit=1)[0]
        return effect

    @catch_error
    def get_family_id(self, bs_content) -> Optional[int]:
        family_id = int(bs_content.find("a", {'darkgreen_link'})['href'].split("=")[1])

        return family_id

    @catch_error
    def get_family_name(self, bs_content) -> Optional[str]:
        family_name = bs_content.find("a", {'darkgreen_link'}).text
        return family_name

    @catch_error
    def get_club_id(self, bs_content) -> Optional[int]:
        club_id = int(
            bs_content.find("a", {'class': 'darkgreen_link'})[
                'href'].split(
                "=")[1])
        return club_id

    @catch_error
    def get_club_name(self, bs_content) -> Optional[int]:
        club_name = bs_content.text.split(": ")[1].split(",")[0]
        return club_name

    @catch_error
    def get_rank_club(self, bs_content) -> Optional[int]:
        rank_club = bs_content.text.split(", ")[1]
        return rank_club

    @catch_error
    def get_club_cost(self, bs_content) -> Optional[int]:
        club_const = int(bs_content.text.split(": ")[1].split("%")[0])
        return club_const

    @catch_error
    def get_club_day(self, bs_content) -> Optional[int]:
        club_day = bs_content.text.split(": ")[1]
        club_day = int(club_day.split(" ")[0].replace('\t', ''))
        return club_day

    @catch_error
    def get_day_in_game(self, bs_content) -> Optional[int]:
        return int(bs_content.text.split(": ")[1].replace('\t', ''))

    @catch_error
    def get_coins(self, bs_content) -> Optional[int]:
        coins = int(bs_content.text.split(": ")[1].replace('\t', ''))
        return coins

    @catch_error
    def get_hearts(self, bs_content) -> Optional[int]:
        return int(bs_content.text.split(": ")[1].replace('\t', ''))

    async def profile(self, ) -> Union[models.Profile, models.Error]:
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/profile")
            club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = register_date = None
            club_day_date = None
            last_login = None
            beauty = coins = hearts = day = 0
            prof = BeautifulSoup(await response.text(), 'lxml')

            ava_id = self.get_ava_id(bs_content=prof)
            name = self.get_name(bs_content=prof)
            level = self.get_level(bs_content=prof)
            rank = self.get_rank(bs_content=prof)
            if rank is None:
                raise Exception("Error")
            for ac in rank:
                if 'Посл. вход:' in ac.text:
                    last_login = self.get_last_seen(bs_content=ac)
                elif 'VIP-аккаунт' in ac.text:
                    effect = self.get_vip_effect(bs_content=ac)
                elif 'Премиум-аккаунт' in ac.text:
                    effect = self.get_premium_effect(bs_content=ac)
                elif 'Семья' in ac.text:
                    family_id = self.get_family_id(bs_content=ac)
                    family_name = self.get_family_name(bs_content=ac)
                elif 'Красота:' in ac.text:
                    beauty = int(ac.text.split(": ")[1])
                elif 'Клуб:' in ac.text:
                    club_id = self.get_club_id(bs_content=ac)
                    club = self.get_club_name(bs_content=ac)
                    rank_club = self.get_rank_club(bs_content=ac)
                elif 'Верность клубу' in ac.text:
                    club_const = self.get_club_cost(bs_content=ac)
                elif 'Дней в клубе:' in ac.text:
                    club_day = self.get_club_day(bs_content=ac)
                    club_day_date = datetime.datetime.today() - datetime.timedelta(days=club_day)
                elif 'Дней в игре:' in ac.text:
                    day = self.get_day_in_game(bs_content=ac)
                    register_date = datetime.datetime.today() - datetime.timedelta(days=day)
                elif 'Монеты:' in ac.text:
                    coins = self.get_coins(bs_content=ac)
                elif 'Сердечки:' in ac.text:
                    hearts = self.get_hearts(bs_content=ac)
            return models.Profile(
                status=True,
                pet_id=0,
                name=name,
                level=level,
                ava_id=ava_id,
                last_login=last_login,
                effect=effect,
                beauty=beauty,
                coins=coins,
                hearts=hearts,
                family_id=family_id,
                family_name=family_name,
                club_id=club_id,
                club=club,
                rank=rank_club,
                club_const=club_const,
                club_day=club_day,
                club_day_date=club_day_date,
                day=day,
                register_day=register_date
            )
        except Exception as ex:
            # logger.exception("")
            return models.Error(status=False,
                                code=0,
                                message=str(ex))

    async def view_profile(self, pet_id) -> Union[models.ViewProfile, models.Error]:
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/view_profile",
                                                                   params={"pet_id": pet_id})
            club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = None
            club_day_date = None
            last_login = "online"
            resp = BeautifulSoup(await response.text(), "lxml")
            if "Питомец не найден!" in resp.text:
                return models.Error(
                    status=False,
                    code=404,
                    message="Питомец не найден"
                )
            ava_id = self.get_ava_id(bs_content=resp)

            ava_id = int(ava_id)
            name = self.get_name(bs_content=resp)
            level = self.get_level_view_profile(bs_content=resp)
            rank = self.get_rank(bs_content=resp)
            # level = \
            #     resp.find("div", {"class": "stat_item"}).text.rsplit(", ", 1)[
            #         1].split(" ")[0]
            # level = int(level)
            # rank = resp.find("div", {
            #     "class": "left font_14 pet_profile_stat"}).find_all("div", {
            #     "class": "stat_item"})
            for ac in rank:
                if 'Посл. вход:' in ac.text:
                    last_login = self.get_last_seen(bs_content=ac)
                elif 'VIP-аккаунт' in ac.text:
                    effect = 'VIP'
                elif 'Премиум-аккаунт' in ac.text:
                    effect = 'premium'
                elif 'Семья' in ac.text:
                    family_id = self.get_family_id(bs_content=ac)
                    family_name = self.get_family_name(bs_content=ac)
                elif 'Красота:' in ac.text:
                    beauty = int(ac.text.split(": ")[1])
                elif 'Клуб:' in ac.text:
                    club_id = self.get_club_id(bs_content=ac)
                    club = self.get_club_name(bs_content=ac)
                    rank_club = self.get_rank_club(bs_content=ac)
                elif 'Верность клубу' in ac.text:
                    club_const = self.get_club_cost(bs_content=ac)
                elif 'Дней в клубе:' in ac.text:
                    club_day = self.get_club_day(bs_content=ac)
                    club_day_date = datetime.datetime.today() - datetime.timedelta(days=club_day)
                elif 'Дней в игре:' in ac.text:
                    day = self.get_day_in_game(bs_content=ac)
                    register_date = datetime.datetime.today() - datetime.timedelta(days=day)
            return models.ViewProfile(
                status=True,
                pet_id=pet_id,
                name=name,
                level=level,
                ava_id=ava_id,
                last_login=last_login,
                effect=effect,
                beauty=beauty,
                family_id=family_id,
                family_name=family_name,
                club_id=club_id,
                club=club,
                rank=rank_club,
                club_const=club_const,
                club_day=club_day,
                club_day_date=club_day_date,
                day=day,
                register_day=register_date
            )
        except Exception as ex:
            raise
            return models.Error(
                status=False,
                code=0,
                message=repr(ex)
            )


@catch_error
def get_chest_item_key(bs_content) -> models.ChestItem:
    item_type = models.ChestItemTypes.KEY
    item_id = bs_content.find("a")['href'].split("=")[1]
    if "&" in item_id:
        item_id = item_id.split("&")[0]
    item_id = int(item_id)

    return models.ChestItem(type=item_type,
                            item_id=item_id,
                            )


@catch_error
def get_chest_item_lockbost(bs_content) -> models.ChestItem:
    item_type = models.ChestItemTypes.LOCKBOX
    item_id = bs_content.find("a")['href'].split("=")[1]
    if "&" in item_id:
        item_id = item_id.split("&")[0]
    item_id = int(item_id)
    timeout = \
        bs_content.find("span", {"class": "succes"}).text.split(" ")[
            2]
    # timeout = int(timeout)
    return models.ChestItem(
        type=item_type,
        item_id=item_id,
        timeout=timeout
    )


@catch_error
def get_chest_item_cloth(bs_content) -> models.ChestItem:
    item_id = bs_content.find("span", {"class": "nowrap"})
    item_id = item_id.find("a")['href'].split("=")[1]
    if "&" in item_id:
        item_id = item_id.split("&")[0]
    item_id = int(item_id)

    if "Продать" in bs_content.text:
        wear_item = True
    else:
        wear_item = False

    return models.ChestItem(
        type=models.ChestItemTypes.CLOTH,
        item_id=item_id,
        wear_item=wear_item
    )


async def chest(response: ClientResponse) -> Union[models.Chest, models.Error]:
    try:
        items = []
        resp = BeautifulSoup(await response.text(), 'lxml')
        if "В шкафу пусто" in resp.text:
            return models.Chest(
                status=True,
                items=[]
            )
        chest_items = resp.find_all('div', {'class': 'item'})
        for item in chest_items:
            if "Стальной ключ" in item.text:
                items.append(get_chest_item_key(bs_content=item))
            if "Стальной сундук" in item.text:
                items.append(get_chest_item_lockbost(bs_content=item))
            if "Надеть" in item.text or "Продать" in item.text:
                items.append(get_chest_item_cloth(bs_content=item))
        return models.Chest(
            status=True,
            items=items
        )
    except Exception as ex:
        return models.Error(
            status=False,
            code=0,
            message=str(ex)
        )


async def wear_item(item_id, session):
    try:
        params = {"id": item_id, "type": "cloth", "back": "chest"}
        async with session.get(f"{HOST_URL}/wear_item",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def sell_item(item_id, session):
    try:
        params = {"id": item_id, "type": "cloth", "back": "chest"}
        async with session.get(f"{HOST_URL}/sell_item",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def gear(session):
    try:
        async with session.get(f"{HOST_URL}/gear") as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await gear(session=session)
            resp = BeautifulSoup(await resp.read(), 'lxml')
            clothes = []
            for item in resp.find_all("div", {"class": "item"}):
                if "Ничего не надето" in item.text:
                    clothes.append({"id": 0,
                                    "name": "",
                                    "beauty": "",
                                    "img": "",
                                    "is_exist": False})
                try:
                    ans = item.find("span", {"class": "span1"})
                    ans = ans.find("a")['href']
                    ans = ans.split("id=")[1].split("&")[0]
                    id = int(ans)
                    clothes.append({"id": id,
                                    "name": "",
                                    "beauty": "",
                                    "img": "",
                                    "is_exists": True})
                except:
                    clothes.append({"id": 0,
                                    "name": "",
                                    "beauty": "",
                                    "img": "",
                                    "is_exist": False})
            return {"status": True,
                    "clothes": clothes}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def view_posters(session):
    try:
        params = {"r": 1}
        async with session.get(f"{HOST_URL}/view_posters",
                               params=params) as resp:
            resp = BeautifulSoup(await resp.read(), "lxml")
            players = resp.find_all("div", {"class": "poster mb3"})
            posters = []
            for player in players:
                unread = False
                pet_id = player.find_all("a")[0]['href'].split("=")[1]
                pet_id = int(pet_id)
                name = player.find_all("a")[0].text
                text = player.find_all("a")[1].text.replace("	",
                                                            "").replace(
                    "\r", "").replace("\n", "")
                post_date = player.find("div",
                                        {"class": "pl_date"}).text.replace(
                    "	", "")
                post_date = post_date.replace("\n\r\n", "").replace("\n", "")
                # Опредлеяем прочитано сообщение или нет
                temp = \
                    player.find("div", {"class": "pl_cont"}).find_all("a")[1][
                        'class'][
                        0]
                if temp == 'unread_post':
                    unread = True
                posters.append({"pet_id": pet_id,
                                "name": name,
                                "text": text,
                                "post_date": post_date,
                                "unread": unread})
            return {'status': True,
                    "players": posters}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def post_message(pet_id, page, session):
    try:
        params = {"pet_id": pet_id, "page": page}
        async with session.get(f"{HOST_URL}/post_message",
                               params=params) as resp:
            resp = BeautifulSoup(await resp.read(), "lxml")
            msgs = resp.find_all("div", {"class": "msg mrg_msg1 mt5 c_brown4"})
            messages = []
            for message in msgs:
                pet_id = message.find("a")['href'].split("=")[1]
                pet_id = int(pet_id)
                name = message.find_all("a")[0].text
                text = message.find("div", {"class": "post_content"}).text
                post_date = message.find("span", {
                    "class": "post_date nowrap"}).text.replace("	", "")
                post_date = post_date.replace("\n\r\n", "").replace("\n", "")
                messages.append({"pet_id": pet_id,
                                 "name": name,
                                 "text": text,
                                 "post_date": post_date})
            return {'status': True,
                    "messages": messages}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def view_anketa(pet_id, session):
    try:
        about = real_name = gender = city = birthday = ank = None
        params = {'pet_id': pet_id}
        async with session.get(f"{HOST_URL}/view_anketa",
                               params=params) as resp:
            prof = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in await resp.text():
                return await view_anketa(pet_id=pet_id, session=session)
            anketa = prof.find_all("span", {"class": "anketa_head ib mb3"})
            for i in range(len(anketa)):
                if "себе" in str(anketa[i].text):
                    about = prof.find_all("div", {"class": "mb10"})[i].text
                elif "Реальное имя" in anketa[i].text:
                    real_name = prof.find_all("div", {"class": "mb10"})[i].text
                elif "Пол" in anketa[i].text:
                    gender = prof.find_all("div", {"class": "mb10"})[i].text
                    gender = gender.replace("\r", "").replace("\n", "")
                    gender = gender.replace("\t", "")
                elif "Город" in anketa[i].text:
                    city = prof.find_all("div", {"class": "mb10"})[i].text
                    city = city.replace("\r\n\r\n\t\t\t", "").replace(
                        "\r\n\t\t\t\t\t\t\t\n", "")
                elif "Дата рождения" in anketa[i].text:
                    birthday = prof.find_all("div", {"class": "mb10"})[i].text
                    birthday = birthday.replace("\r\n\t\t\t\t", "").replace(
                        "\t\t\t\t\t\t\t", "")
                elif "Анкета" in anketa[i].text:
                    ank = prof.find_all("div", {"class": "mb10"})[i].text
            return {'status': True,
                    'pet_id': int(pet_id),
                    'about': about,
                    'real_name': real_name,
                    'gender': gender,
                    'city': city,
                    'birthday': birthday,
                    'ank': ank}
    except asyncio.TimeoutError as e:
        return await view_anketa(pet_id=pet_id,
                                 session=session)
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def view_gifts(pet_id, page, session):
    try:
        params = {'pet_id': pet_id, "page": page}
        players = []
        async with session.get(f"{HOST_URL}/view_gifts",
                               params=params) as resp:
            gifts = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in await resp.text():
                return await view_gifts(pet_id=pet_id,
                                        page=page,
                                        session=session)
            items = gifts.find_all('div', {'class': 'item'})
            for item in items:
                name, pet_id = None, None
                present_id = item.find("img", {"class": "item_icon"})["src"]
                present_id = present_id.split("present")[1].split(".")[0]
                pet_id = item.find("a", {"class": "pet_name il"})
                if pet_id:
                    name = pet_id.text
                    pet_id = pet_id["href"].split("=")[1]
                date = item.find("span", {"class": "gray_color font_13"}).text
                date = date.split("получен")[1]
                # НЕ ДЕЛАЙ PET_ID B PRESENT_ID ЧИСЛОВЫМ ТИПОМ

                # 25.06.2021
                # добавили в уп капчу, половину нормального кода
                # приходится переписывать на быструю руку.
                # короче pet_id в принципе можно сделать интовым,
                # но нужна проверка - скрытый подарок или нет

                # 03.01.2022
                # в уп всё еще капча. однако замотивировался
                # в этом году всё-таки доделать эту библиотеку
                # понял, что каждый раз создавать сессию - неправильно вообще.
                # поэтому переписываю весь код под одну сессию
                players.append({"pet_id": pet_id, "name": name,
                                "present_id": present_id, "date": date})
            return {'status': True,
                    'page': page,
                    'players': players}
    except asyncio.TimeoutError as e:
        return {'status': False,
                'code': -1,
                'msg': e}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def post_send(message_text, pet_id, page, session):
    try:
        data = {"message_text": message_text,
                "pet_id": pet_id,
                "page": page}
        async with session.post(f"{HOST_URL}/post_send", data=data) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}
