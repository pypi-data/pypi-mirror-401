import asyncio
import random

from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from loguru import logger

from mpets.api.BaseApi import BaseApi
from mpets.models.BaseResponse import BaseResponse
from mpets.models.main.TrainResponse import Train, TrainResponse
from mpets.utils.constants import HOST_URL


class Main:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    async def gold_chest(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/gold_chest")
            if "Вы кликаете слишком быстро" in await response.text():
                return await self.gold_chest()

            resp = BeautifulSoup(await response.text(), "lxml")

            keys = resp.find("div", {"class": "mb5 cntr small"}).text
            keys = keys.split("с ")[1].split(" ")[0]
            rewards = []
            players = resp.find("table", {"class": "travel_records"})
            players = players.find_all("tr", {"class": ""})
            for player in players:
                pet_id = player.find("a")['href'].split("=")[1]
                name = player.find("a").text
                reward = player.find("td", {"class": "td_r"}).text.split(" ",
                                                                         maxsplit=1)[
                    1]
                rewards.append({"pet_id": int(pet_id),
                                "name": name,
                                "reward": reward})
            return {"status": True,
                    "amount_keys": int(keys),
                    "rewards": rewards}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def actions(self, amount):
        try:
            for a in range(amount):
                logger.debug(f"Разбудка #{a}")
                for b in range(5):
                    await self.action(action_type="food")
                    await asyncio.sleep(0.4)
                    await self.action(action_type="food")
                    await asyncio.sleep(0.4)
                logger.debug(f"Выставка #{a}")
                await self.show()
                await self.wakeup()
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def action(self, action_type: str, rand: int = random.randint(100, 9000)):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/",
                                                                   params={"action": action_type,
                                                                           "rand": rand})
            logger.debug(await response.text())
            if "Разбудить за" in await response.text() or "Играть ещё" in await response.text():
                return {"status": True, "play": False}
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def show(self):
        try:
            while True:
                response: ClientResponse = await self.base_api.request(type="GET",
                                                                       method="/show")
                await asyncio.sleep(0.5)
                if "Соревноваться" in await response.text():
                    continue
                elif "Вы кликаете слишком быстро." in await response.text():
                    await asyncio.sleep(1)
                    continue
                else:
                    break
            return {"status": True}
        except Exception as e:
            return {"status": False}

    async def wakeup_sleep_info(session):
        pass

    async def wakeup_sleep(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/wakeup_sleep")

            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def wakeup_sleep_auto(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/wakeup_sleep_auto")

            return {"status": True}

        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def wakeup(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/wakeup")

            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def glade_dig(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/glade_dig")
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def travel(self):
        try:
            left_time, travel_status, ids, records = 0, False, [], []
            resp: ClientResponse = await self.base_api.request(type="GET",
                                                               method="/travel")
            response = BeautifulSoup(await resp.text(), "lxml")
            if "Ваш питомец гуляет" in await resp.text():
                travel_status = True
                left_time = \
                    response.find("span", {"class": "green_dark"}).text.split(
                        "осталось ")[1]
            elif "Прогулка завершена!" in await resp.text():
                return await self.travel()
            elif "Рекорд за сутки" in await resp.text():
                travel_ids = response.find("div", {"class": "travel"})
                for link in travel_ids.find_all("a", href=True):
                    ids.append(int(link["href"].split("=")[1]))
                records_list = response.find("table",
                                             {"class": "travel_records"})
                nick = records_list.find_all("td", {"class": "cntr td_un"})
                coins = records_list.find_all("td", {"class": "td_r"})
                for i in range(3):
                    records.append({"pet_id": int(
                        nick[i].find("a")["href"].split("=")[1]),
                        "name": nick[i].text,
                        "coins": int(coins[i].text)})
            return {"status": True,
                    "travel": travel_status,
                    "left_time": left_time,
                    "ids": ids,
                    "records": records}

        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def go_travel(self, travel_id):
        try:
            params = {"id": travel_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/go_travel",
                                                                   params=params)
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def task(self):
        try:
            tasks_list = []
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/task")
            resp = BeautifulSoup(await response.text(), "lxml")
            tasks = resp.find_all("div", {"class": "wr_c3 m-3"})
            for task in tasks:
                task_id = 0
                status = False
                if "Забрать награду" in task.text:
                    status = True
                    task_id = task.find("div", {"class": "span3"})
                    task_id = int(task_id.find("a")["href"].split("=")[1])
                name = task.find("div", {"class": "tc"}).text
                desc = task.find("div", {"class": "mt7 font_13"}).text
                progress = \
                    task.find("span", {"class": "c_gray"}).text.split(": ")[
                        1].split(" из ")
                progress = [int(i) for i in progress]
                reward = None
                tasks_list.append({"status": status,
                                   "name": name,
                                   "description": desc,
                                   "progress": progress,
                                   "reward": reward,
                                   "id": task_id})
            return {"status": True,
                    "tasks": tasks_list}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def task_reward(self, task_id):
        try:
            params = {"id": task_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/task_reward",
                                                                   params=params)
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def buy(self, category, item_id):
        try:
            params = {"category": category, "id": item_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/buy",
                                                                   params=params)
            return {"status": True}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def open_gold_chest(self):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/gold_chest/open")

            resp = BeautifulSoup(await response.text(), "lxml")
            chest = resp.find("div", {"class": "lplate mt10"})
            if "VIP-аккаунт" in chest.text:
                return {"status": True,
                        "found": "VIP-аккаунт на 48ч"}
            elif "новый" in chest.text:
                return {"status": True,
                        "found": "Еда или игра"}
            elif "семени" in chest.text or "семян" in chest.text or "семя" in chest.text or "опыт" in chest.text:
                return {"status": True,
                        "found": "Семена или опыт"}
            elif "В нем вы нашли +1 тренировку работника!" in chest.text:
                return {"status": True,
                        "found": "В нем вы нашли +1 тренировку работника!"}
            elif "В нем вы нашли +1 сборку камня!" in chest.text:
                return {"status": True,
                        "found": "В нем вы нашли +1 сборку камня!"}
            elif "300" in chest.text:
                return {"status": True,
                        "found": "300 монет"}
            elif "Простой ошейник" in chest.text or \
                    "Простой медальон" in chest.text:
                return {"status": True,
                        "found": "Одежду"}
            else:
                found = chest.find("div", {"class": "c_green mt3"}).text
            return {"status": True,
                    "found": chest,
                    "text": found}
        except Exception as e:
            return {"status": False,
                    "code": 0,
                    "msg": e}

    async def train(self):
        try:
            trains, upgrade, upgrade_price = [], False, 0
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/train")

            resp = BeautifulSoup(await response.text(), "lxml")
            amount = 0
            skills = ['cloth', 'accessory', 'style', 'glade']
            for i in resp.find_all("div",
                                   {"class": "msg mrg_msg1 mt10 c_brown"}):
                level = i.find("div", {"class": "mb3 ml2_price_img"}).text
                level = level.split(": ")[1].split(" ")[0]
                if "%" in level:
                    level = int(level.split("%")[0])
                level = int(level)
                if "Тренировать" in i.text:
                    upgrade_price = \
                        i.find("span", {"class": "bc"}).text.rsplit(" ", 2)[1]
                trains.append(
                    Train(skill=skills[amount],
                          level=level,
                            price=upgrade_price)
                )

                amount += 1
            return TrainResponse(
                status=True,
                trains=trains,
            )
        except Exception as e:
            return BaseResponse(
                status=False,
                error=0,
                error_message=str(e)
            )

async def charm(session):
    try:
        async with session.get(f"{HOST_URL}/charm") as resp:
            task = False
            if "Вы кликаете слишком быстро." in await resp.text():
                return await charm(session=session)
            elif "Результаты" in await resp.text():
                if "Прогресс 2 из 2" in await resp.text():
                    task = False
                elif "Проведи 2 игры в снежки" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
            elif "В очереди" in await resp.text():
                return {"status": True,
                        "queue": True,
                        "game": False,
                        "task": task}
            elif "Снежный бой начинается!" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            elif "выбил Вас" in await resp.text() or "бросил в Вас" in await \
                    resp.text() or "Уворот" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            else:
                if "Проведи 2 игры в снежки" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
    except Exception as e:
        return {"status": False,
                'code': 0,
                'msg': e}


async def charm_in_queue(session):
    try:
        params = {"in_queue": 1}
        async with session.get(f"{HOST_URL}/charm", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                'code': 0,
                'msg': e}


async def charm_out_queue(session):
    try:
        params = {"out_queue": 1}
        async with session.get(f"{HOST_URL}/charm", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def charm_attack(session):
    try:
        params = {"attack": 1, "r": random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/charm", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def charm_change(session):
    try:
        params = {"change": 1, "r": random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/charm", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def charm_dodge(session):
    try:
        params = {"dodge": 1, "r": random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/charm", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def races(session):
    try:
        async with session.get(f"{HOST_URL}/races") as resp:
            task = False
            if "Вы кликаете слишком быстро." in await resp.text():
                return await races(session=session)
            elif "Результаты" in await resp.text():
                if "Прогресс 2 из 2" in await resp.text():
                    task = False
                elif "Стань призером скачек 2 раза" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
            elif "В очереди" in await resp.text():
                return {"status": True,
                        "queue": True,
                        "game": False,
                        "task": task}
            elif "Заезд начинается!" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            elif "Сменить" in await resp.text() and "Толкнуть" in await \
                    resp.text() and "Бежать" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            else:
                if "Стань призером скачек 2 раза" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def races_in_queue(session):
    try:
        params = {"in_queue": 1}
        async with session.get(f"{HOST_URL}/races", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def races_out_queue(session):
    try:
        params = {"out_queue": 1}
        async with session.get(f"{HOST_URL}/races", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def races_go(session):
    try:
        params = {"go": 1, "r": random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/races", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def races_attack(session):
    try:
        params = {"attack": 0, "r": random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/races", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def races_change(session):
    try:
        params = {'change': 1, 'r': random.randint(10, 999)}
        async with session.get(f"{HOST_URL}/races", params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                'code': 0,
                'msg': e}


async def glade(session):
    pass





async def train_skill(skill, session):
    try:
        params = {"skill": skill}
        async with session.get(f"{HOST_URL}/train_skill",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def assistants(session):
    pass


async def assistants_train(session):
    pass


async def jewels(session):
    pass


async def collect_jewel(jewel_id, session):
    try:
        params = {"id": jewel_id, "confirm": 1}
        async with session.get(f"{HOST_URL}/collect_jewel",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def home(session):
    pass


async def garden(session):
    pass


async def garden_collect(garden_id, session):
    pass


async def items(category, session):
    try:
        params = {"category": category}
        if category == "home":
            pass
        elif category == "effect":
            async with session.get(f"{HOST_URL}/items",
                                   params=params) as resp:
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await items(category=category, session=session)
                resp = BeautifulSoup(await resp.read(), "lxml")
                effects = resp.find_all("div", {"class": "shop_item"})
                if len(effects) == 1:
                    if "VIP-аккаунт" in effects[0].text:
                        if "Осталось" in effects[0].text:
                            left_time = \
                                effects[0].find("div", {"class": "succes "
                                                                 "mt3"}).text.split(
                                    "Осталось: ")[1]
                            return {"status": True,
                                    "effect": "VIP",
                                    "left_time": left_time}
                        return {"status": True,
                                "effect": "None"}
                elif len(effects) == 2:
                    for effect in effects:
                        if "Премиум-аккаунт" in effect.text:
                            if "Осталось" in effect.text:
                                left_time = effect.find("div", {
                                    "class": "succes mt3"}).text.split(
                                    "Осталось: ")[1]
                                return {"status": True,
                                        "effect": "premium",
                                        "left_time": left_time}
                        if "VIP-аккаунт" in effect.text:
                            return {"status": True,
                                    "effect": "None"}
        elif category == "food":
            async with session.get(f"{HOST_URL}/items",
                                   params=params) as resp:
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await items(category=category,
                                       session=session)
                resp = BeautifulSoup(await resp.read(), "lxml")
                shop_item = resp.find("div", {"class": "shop_item"})
                name = shop_item.find("span", {"class": "disabled"}).text
                beauty = shop_item.find("img", {
                    "src": "/view/image/icons/beauty.png"}).next_element.split(
                    " ")[0]
                exp = shop_item.find("img", {
                    "src": "/view/image/icons/expirience.png"}).next_element.split(
                    " ")[0]
                heart = shop_item.find("img", {
                    "src": "/view/image/icons/heart.png"}).next_element.split(
                    " ")[
                    0]
                if "Купить за" in shop_item.text:
                    item_id = \
                        shop_item.find("a")['href'].split("id=")[1].split("&")[
                            0]
                    item_id = int(item_id)
                    can_buy = True
                    coins = \
                        shop_item.find("span",
                                       {"class": "bc plr5"}).text.split(
                            "за ")[
                            1]
                    coins = int(coins)
                elif "требуется" in shop_item.text:
                    item_id = \
                        shop_item.find("a")['href'].split("id=")[1].split("&")[
                            0]
                    item_id = int(item_id)
                    item_id = 0
                    can_buy = False
                return {"status": True,
                        "name": name,
                        "beauty": beauty,
                        "exp": exp,
                        "heart": heart,
                        "can_buy": False if 'can_buy' not in locals() else can_buy,
                        "item_id": 0 if 'item_id' not in locals() else item_id,
                        "coins": 0 if 'coins' not in locals() else coins,
                        }
        elif category == "play":
            async with session.get(f"{HOST_URL}/items",
                                   params=params) as resp:
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await items(category=category,
                                       session=session)
                resp = BeautifulSoup(await resp.read(), "lxml")
                shop_item = resp.find("div", {"class": "shop_item"})
                name = shop_item.find("span", {"class": "disabled"}).text
                beauty = shop_item.find("img", {
                    "src": "/view/image/icons/beauty.png"}).next_element.split(
                    " ")[0]
                beauty = int(beauty)
                exp = shop_item.find("img", {
                    "src": "/view/image/icons/expirience.png"}).next_element.split(
                    " ")[0]
                exp = int(exp)
                heart = shop_item.find("img", {
                    "src": "/view/image/icons/heart.png"}).next_element.split(
                    " ")[
                    0]
                heart = int(heart)
                if "Купить за" in shop_item.text:
                    item_id = \
                        shop_item.find("a")['href'].split("id=")[1].split("&")[
                            0]
                    item_id = int(item_id)
                    can_buy = True
                    coins = \
                        shop_item.find("span",
                                       {"class": "bc plr5"}).text.split(
                            "за ")[
                            1]
                    coins = int(coins)
                elif "требуется" in shop_item.text:
                    item_id = \
                        shop_item.find("a")['href'].split("id=")[1].split("&")[
                            0]
                    item_id = int(item_id)
                    item_id = 0
                    can_buy = False
                return {"status": True,
                        "name": name,
                        "beauty": beauty,
                        "exp": exp,
                        "heart": heart,
                        "can_buy": False if 'can_buy' not in locals() else can_buy,
                        "item_id": 0 if 'item_id' not in locals() else item_id,
                        "coins": coins,
                        }
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def best(type, page, session):
    try:
        def has_class(tag):
            return not tag.has_attr("class")

        params = {type: "true", "page": page}
        pets = []
        async with session.get(f"{HOST_URL}/best", params=params) as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await best(type=type,
                                  page=page,
                                  session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            class_style = "players tlist font_14 td_un"
            if type == 'club':
                class_style = "players ib tlist font_14"
            resp = resp.find("table", {"class": class_style})
            resp = resp.find_all(has_class, recursive=False)
            for pet in resp:
                place = int(pet.find("td").text)
                pet_id = pet.find("a", {"class": "c_brown3"})["href"]
                pet_id = int(pet_id.split("id=")[1])
                name = pet.find("a", {"class": "c_brown3"}).text
                beauty = int(pet.find_all("td")[2].text)
                pets.append({"place": place,
                             "pet_id": pet_id,
                             "name": name,
                             "beauty": beauty})
            return {"status": True,
                    "pets": pets}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def buy_heart(heart, session):
    try:
        params = {"heart": heart}
        async with session.get(f"{HOST_URL}/buy_heart",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def find_pet(name, session):
    try:
        data, account_status = {"name": name}, None
        async with session.post(f"{HOST_URL}/find_pet", data=data) as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await find_pet(name, session)
            elif "Имя должно быть от 3 до 12 символов!" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Имя должно быть от 3 до 13 символов"}
            elif "Питомец не найден!" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Питомец не найден!"}
            elif "Игрок заблокирован" in await resp.text():
                account_status = "block"
            elif "Игрок забанен" in await resp.text():
                account_status = "ban"
            if "view_profile" in str(resp.url):
                pet_id = str(resp.url).split("id=")[1].split("&")[0]
            return {"status": True,
                    "pet_id": pet_id,
                    "name": name,
                    "account_status": account_status}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def find_club(name, session):
    pass


async def show_coin(session):
    pass


async def show_coin_get(session):
    try:
        async with session.get(f"{HOST_URL}/show_coin_get") as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await show_coin_get(session=session)
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def online(page, session):
    try:
        def has_class(tag):
            return not tag.has_attr("class")

        params = {"page": page}
        pets = []
        async with session.get(f"{HOST_URL}/online",
                               params=params) as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await online(page=page, session=session)
            elif "Список пуст" in await resp.text():
                resp = BeautifulSoup(await resp.read(), "lxml")
                total_online = resp.find("div", {
                    "class": "small mt20 mb20 c_lbrown cntr td_un"})
                total_online = \
                    total_online.find_all("a", {"class": "ib mlr8"})[
                        1].text.split(
                        ": ")[1]
                total_online = int(total_online)
                max_page = (total_online // 15) + 1
                return {"status": True,
                        "page": page,
                        "online": total_online,
                        "max_page": max_page,
                        "pets": pets}
            resp = BeautifulSoup(await resp.read(), "lxml")
            total_online = resp.find("div", {
                "class": "small mt20 mb20 c_lbrown cntr td_un"})
            total_online = \
                total_online.find_all("a", {"class": "ib mlr8"})[1].text.split(
                    ": ")[1]
            total_online = int(total_online)
            max_page = (total_online // 15) + 1
            resp = resp.find("table", {"class": "tlist mt5 mb10"})
            resp = resp.find_all(has_class, recursive=False)
            for pet in resp:
                pet_id = pet.find("a", {"class": "c_brown3"})['href']
                pet_id = int(pet_id.split("id=")[1])
                name = pet.find("a", {"class": "c_brown3"}).text
                beauty = int(pet.find("td", {"class": "cntr"}).text)
                pets.append({"pet_id": pet_id,
                             "name": name,
                             "score": beauty})
            return {"status": True,
                    "page": page,
                    "online": total_online,
                    "max_page": max_page,
                    "pets": pets}
    except asyncio.exceptions.TimeoutError as e:
        return await online(page=page, session=session)
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def game_time(session):
    try:
        async with session.get(f"{HOST_URL}/main") as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await game_time(session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div",
                             {"class": "small mt20 mb20 c_lbrown cntr td_un"})
            time = \
                resp.find("div", {"class": "mt5 mb5"}).text.split(", ")[
                    1].split(
                    "\n")[0]
            h, m, s = map(int, time.split(":"))
            return {"status": True,
                    "time": time,
                    "h": h,
                    "m": m,
                    "s": s}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def gold_chest(session):
    try:
        async with session.get(f"{HOST_URL}/gold_chest") as resp:
            if "Вы кликаете слишком быстро" in await resp.text():
                return await gold_chest(session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            keys = resp.find("div", {"class": "mb5 cntr small"}).text
            keys = keys.split("с ")[1].split(" ")[0]
            rewards = []
            players = resp.find("table", {"class": "travel_records"})
            players = players.find_all("tr", {"class": ""})
            for player in players:
                pet_id = player.find("a")['href'].split("=")[1]
                name = player.find("a").text
                reward = player.find("td", {"class": "td_r"}).text.split(" ",
                                                                         maxsplit=1)[
                    1]
                rewards.append({"pet_id": int(pet_id),
                                "name": name,
                                "reward": reward})
            return {"status": True,
                    "amount_keys": int(keys),
                    "rewards": rewards}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def open_gold_chest_key(session):
    try:
        async with session.get(f"{HOST_URL}/gold_chest/key") as resp:
            resp = BeautifulSoup(await resp.read(), "lxml")
            chest = resp.find("div", {"class": "lplate mt10"})
            if "VIP-аккаунт" in chest:
                return {"status": True,
                        "found": "VIP-аккаунт на 48ч"}
            elif "новый" in chest:
                return {"status": True,
                        "found": "Еда или игра"}
            else:
                found = chest.find("div", {"class": "c_green mt3"}).text
            return {"status": True,
                    "found": chest}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def check_ban(session):
    try:
        async with session.get(f"{HOST_URL}/chat") as resp:
            if "На вас наложен бан" in await resp.text() and "осталось" in await resp.text():
                return {"status": True,
                        "ban": True}
            else:
                return {"status": True,
                        "ban": False}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def set_avatar(avatar_id, session):
    try:
        params = {"id": avatar_id}
        async with session.get(f"{HOST_URL}/set_avatar",
                               params=params) as resp:
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}
