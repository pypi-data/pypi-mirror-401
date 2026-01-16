from typing import Union

from aiohttp import ClientSession, ClientTimeout, ClientResponse
from bs4 import BeautifulSoup
from loguru import logger

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.api.methods.parsers import club_parser
from mpets.models.BaseResponse import BaseResponse
from mpets.models.club.ClubChat import ClubChat
from mpets.models.club.ClubChatMessage import ClubChatMessage
from mpets.utils.constants import HOST_URL


class Club:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    async def club(self, club_id, page):
        try:
            if club_id:
                params = {"id": club_id, "page": page}
            else:
                params = {"id": 0}
            club_inf = await self.base_api.request(type="GET",
                                                                   method="/club",
                                                                   params=params)
            url = str(club_inf.url)
            if "?id=" in url:
                club_id = club_parser.get_club_id(url=url)
                bs_content = BeautifulSoup(await club_inf.text(), "lxml")
                club_name = club_parser.get_club_name(bs_content=bs_content)
                about_club = club_parser.get_about_club(bs_content=bs_content)
                founded = club_parser.get_founded(bs_content=bs_content)
                level = club_parser.get_level(bs_content=bs_content)
                exp = club_parser.get_exp(bs_content=bs_content)
                build_level = club_parser.get_builds(bs_content=bs_content)
                player_amount = club_parser.get_player_amount(bs_content=bs_content)
                pets = club_parser.get_pets(bs_content=bs_content)
                return models.Club(status=True,
                                   is_club=True,
                                   club_id=club_id,
                                   name=club_name,
                                   about=about_club,
                                   founded=founded,
                                   level=level,
                                   exp=exp,
                                   build_level=build_level,
                                   pets_amount=player_amount,
                                   pets=pets)
            else:
                return BaseResponse(status=False,
                                    error=0,
                                    error_message="Клуб не найден")
                # if "Бонусы клуба" in await club_inf.text():
                #     club_inf = BeautifulSoup(await club_inf.text(), "lxml")
                #     club_inf = club_inf.find("div", {'class': 'wr_c1'})
                #     club_name = club_inf.find("b").text
                #     club_id = club_inf.find("a", {"class": "darkgreen_link"})[
                #         'href'].split("=")[1]
                #     bonus_heart = \
                #         club_inf.find_all("span", {"class": "succes"})[
                #             0].text.split("+")[1].split("%")[0]
                #     bonus_exp = club_inf.find_all("span", {"class": "succes"})[
                #         1].text.split("+")[1].split("%")[0]
                #     return models.Club(status=True,
                #                        is_club=False,
                #                        club_id=club_id,
                #                        name=club_name)
                # else:
                #     return models.Club(status=True,
                #                        is_club=False,
                #                        club_id=club_id,
                #                        name=club_name)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(ex))

    async def want(self):
        try:
            params = {'want': 1}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/clubs",
                                                                   params=params)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(ex))

    async def accept_invite(self, club_id):
        try:
            params = {'id': club_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/accept_invite",
                                                                   params=params)
            return models.BooleanStatus(status=True)

        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(ex))

    async def decline_invite(self, club_id):
        try:
            params = {'id': club_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/decline_invite",
                                                                   params=params)

            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(ex))

    async def enter_club(self, club_id, decline):
        try:
            if decline is False:
                params = {'id': club_id, 'yes': 1}
            else:
                params = {'id': club_id, 'decline': 1}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/enter_club",
                                                                   params=params)
            invited_code = response.url.query.get('invited')
            logger.debug("invited code " + invited_code)
            if invited_code is None:
                return BaseResponse(status=False,
                                    error=0,
                                    error_message="Ошибка отправки заявки")
            if invited_code == "1":
                return models.BooleanStatus(status=True)
            if invited_code == "2":
                return BaseResponse(status=False,
                                    error=0,
                                    error_message="Вы уже состоите в клубе")
            if invited_code == "3":
                return BaseResponse(status=False,
                                    error=0,
                                    error_message="Вы уже отправляли в этот клуб заявку")
            if invited_code == "4":
                return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message="Вы уже отправляли в этот клуб заявку")

    async def create_club(self, name):
        try:
            data = {'name': name}
            response: ClientResponse = await self.base_api.request(type="POST",
                                                                   method="/create_club",
                                                                   data=data)
            bs_content = BeautifulSoup(await response.text(), "lxml")
            error_code = response.url.query.get('error')
            if error_code is not None:
                error_message = bs_content.find("span", {"class": "warning"}).text
                return BaseResponse(status=False,
                                    error=0,
                                    error_message="Вы уже отправляли в этот клуб заявку")
            return models.BooleanStatus(status=True)

        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message="Вы уже отправляли в этот клуб заявку")

    async def builds(self, club_id) -> Union[models.ClubBuilds, BaseResponse]:
        try:
            params = {'id': club_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/builds",
                                                                   params=params)
            bs_content = BeautifulSoup(await response.text(), "lxml")
            builds_list = []
            all_builds = club_parser.get_all_builds(bs_content=bs_content)
            for club_build in all_builds:
                improving = False
                build_name = club_parser.get_build_name(bs_content=club_build)
                build_type = club_parser.get_build_type(bs_content=club_build)
                current_level = club_parser.get_current_level(bs_content=club_build)
                max_level = club_parser.get_max_level(bs_content=club_build)
                build_bonus = club_parser.get_bonus(bs_content=club_build)

                left_time = club_parser.get_left_time(bs_content=club_build)
                if left_time is not None:
                    improving = True

                build_bonus = club_parser.get_fix_build_bonus_if_build_is_improving(build_bonus=build_bonus)

                builds_list.append(models.ClubBuild(
                    name=build_name,
                    type=build_type,
                    level=current_level,
                    max_level=max_level,
                    bonus=build_bonus,
                    improving=improving,
                    left_time=left_time
                ))
            hearts_bonus = club_parser.get_health_bonus(bs_content=bs_content)
            exp_bonus = club_parser.get_exp_bonus(bs_content=bs_content)
            club_level = club_parser.get_club_level(bs_content=bs_content)
            return models.ClubBuilds(status=True,
                                     level=club_level,
                                     hearts_bonus=hearts_bonus,
                                     exp_bonus=exp_bonus,
                                     builds=builds_list)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                message=str(ex))

    async def club_history(self, club_id, type, page):
        try:
            params = {'id': club_id, 'type': type, 'page': page}
            history = []
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/club_history",
                                                                   params=params)
            if "Вы кликаете слишком быстро." in await response.text():
                return await self.club_history(club_id=club_id,
                                               type=type,
                                               page=page)
            resp = BeautifulSoup(await response.text(), "lxml")
            resp = resp.find("div", {'class': 'msg mrg_msg1 mt5 c_brown4'})
            resp = resp.find_all("div", {'class': 'mb2'})
            for his in resp:
                try:
                    date = his.find("span", {"class": "c_gray"}).text
                    owner_id = int(his.find("a")["href"].split("=")[1])
                    owner_name = his.find("a").next_element
                    member_id = int(his.find_all("a")[1]["href"].split("=")[1])
                    member_name = his.find_all("a")[1].next_element
                    action = his.find_all("span")[1].text
                    history.append(
                        {'owner_id': owner_id,
                         'owner_name': owner_name,
                         'member_id': member_id,
                         'member_name': member_name,
                         'action': action,
                         'date': date})
                except:
                    if "покинул клуб" in his:
                        owner_id = int(his.find("a")["href"].split("=")[1])
                        owner_name = his.find("a").next_element
                        action = his.find_all("span")[1].text
                        history.append(
                            {'owner_id': owner_id,
                             'owner_name': owner_name,
                             'member_id': None,
                             'member_name': None,
                             'action': action})
                    pass
            return {'status': True,
                    'club_id': club_id,
                    'page': page,
                    'history': history}
        except Exception as e:
            return {'status': False,
                    'error': 0,
                    'msg': e}

    async def chat_message(self, club_id, message):
        try:
            data = {'message_text': message,
                    'club_id': club_id,
                    'page': 1}
            response: ClientResponse = await self.base_api.request(type="POST",
                                                                   method="/chat_message",
                                                                   data=data)
            return {"status": True}
        except Exception as e:
            return {'status': False,
                    'error': 0,
                    'msg': e}

    async def chat(self, club_id, page):
        try:
            params = {'id': club_id, 'page': page}
            messages = []
            resp = await self.base_api.request(
                "GET",
                f"/chat",
                params=params)
            if "Вы кликаете слишком быстро." in await resp.text():
                return await self.chat(club_id=club_id,
                                       page=page)
            resp = BeautifulSoup(await resp.text(), "lxml")
            pets = resp.find_all("div", {'class': 'post_chat'})
            for pet in pets:
                moderator_id = message_deleted = False
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                try:
                    message = pet.find("span", {"class": "pet_msg"}).text
                except AttributeError as e:
                    message_deleted = True
                    moderator_id = pet.find("a", {"class": "gray_link"})[
                        'href']
                    moderator_id = int(moderator_id.split("=")[1])
                    message = None
                try:
                    message_id = pet.find("a", {"class": "post_control"})[
                        'href']
                    message_id = int(message_id.split("=")[1].split("&")[0])
                except Exception as e:
                    message_id = 0
                messages.append(
                    ClubChatMessage(pet_id=pet_id,
                                    name=name,
                                    message_id=message_id,
                                    message=message,
                                    message_deleted=message_deleted,
                                    moderator_id=moderator_id))
            return ClubChat(status=True,
                            error=None,
                            error_message=None,
                            club_id=club_id,
                            page=page,
                            messages=messages)

        except Exception as e:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(e))


async def build(club_id, type, session):
    try:
        params = {'club_id': club_id, 'type': type}
        async with session.get(f"{HOST_URL}/build",
                               params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await build(club_id=club_id,
                                   session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {"class": "build_item"})
            name = resp.find("span", {"class": "cup ib mt3 mb3"}).text
            name = name.replace("\r", "").replace("\n", "").replace("\t", "")
            bonus = resp.find("div", {"class": "mb3"}).text
            bonus = bonus.replace("\r", "").replace("\n", "").replace("\t", "")
            level_info = resp.find("span", {"class": "font_14 ib"}).text
            level = int(level_info.split(" ")[1].split(" ")[0])
            max_level = int(level_info.split("из ")[1])
            if resp.find("a", {"class": "bbtn mt5 mb5"}) is not None:
                if "Ускорить" in resp.text:
                    fast_upgrade = int(resp.find("img", {
                        "src": "/view/image/icons/coin.png"}).next_element)
                    left_time = resp.find("span",
                                          {"class": "c_green mar5t"}).text
                    left_time = left_time.split("Осталось ")[1]
                else:
                    upgrade_coins = int(resp.find("img", {
                        "src": "/view/image/icons/coin.png"}).next_element)
                    upgrade_hearts = int(resp.find("img", {
                        "src": "/view/image/icons/heart.png"}).next_element)
            return {'status': True,
                    'name': name,
                    'bonus': bonus,
                    'level': level,
                    'max_level': max_level,
                    'upgrade_coins': None if 'upgrade_coins' not in locals() else upgrade_coins,
                    'upgrade_hearts': None if 'upgrade_hearts' not in locals() else upgrade_hearts,
                    'fast_upgrade': None if 'fast_upgrade' not in locals() else fast_upgrade,
                    'left_time': None if 'left_time' not in locals() else left_time}
    except Exception as e:
        return {"status": False,
                "error": 0,
                "msg": e}


async def build_upgrade(club_id, type, session):
    try:
        params = {'club_id': club_id, 'type': type}
        async with session.get(f"{HOST_URL}/build_upgrade",
                               params=params) as resp:

            if "Вы кликаете слишком быстро." in await resp.text():
                return await build_upgrade(club_id=club_id,
                                           type=type,
                                           session=session)
            elif "Вам не хватает " in await resp.text():
                resp = BeautifulSoup(await resp.read(), "lxml")
                try:
                    error = resp.find("span", {"class": "warning"}).text
                except:
                    error = None
                return {"status": False,
                        "error": 1,
                        "msg": error}
            return await build(club_id=club_id,
                               type=type,
                               session=session)
    except Exception as e:
        return {"status": False,
                "error": 0,
                "msg": e}


async def build_speed(club_id, type, session):
    try:
        params = {'club_id': club_id, 'type': type}
        async with session.get(f"{HOST_URL}/build_speed",
                               params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await build_speed(club_id=club_id,
                                         type=type,
                                         session=session)
            elif "Вам не хватает " in await resp.text():
                resp = BeautifulSoup(await resp.read(), "lxml")
                try:
                    error = resp.find("span", {"class": "warning"}).text
                except:
                    error = None
                return {"status": False,
                        "error": 1,
                        "msg": error}
            return await build(club_id=club_id,
                               type=type,
                               session=session)
    except Exception as e:
        return {"status": False,
                "error": 0,
                "msg": e}


async def club_budget(club_id, session):
    try:
        params = {'id': club_id}
        async with session.get(f"{HOST_URL}/club_budget",
                               params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget(club_id=club_id,
                                         session=session)
            elif "Копилка:" in await resp.text():
                resp = BeautifulSoup(await resp.read(), "lxml")
                coins = resp.find("div", {"class": "cntr"}).find_all("img", {
                    "class": "price_img"})[1].next_element
                hearts = resp.find("div", {"class": "cntr"}).find_all("img", {
                    "class": "price_img"})[2].next_element
                max_coins = \
                    resp.find("div", {"class": "p3 left"}).find_all("img", {
                        "class": "price_img"})[
                        0].next_element.split(
                        ": ")[1]
            return {'status': True,
                    'coins': coins,
                    'hearts': hearts,
                    'max_coins': max_coins}
    except Exception as e:
        return {"status": False,
                "error": 0,
                "msg": e}


async def add_club_budget(coin, heart, session):
    try:
        data = {'coin': coin, 'heart': heart}
        async with session.post(f"{HOST_URL}/add_club_budget",
                                data=data) as resp:
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'error': 0,
                'msg': e}


async def club_budget_history(club_id, sort, page, session):
    try:
        params = {'id': club_id, 'sort': sort, 'page': page}
        players, last_reset_pet_id, last_reset_name = [], None, None
        async with session.get(f"{HOST_URL}/club_budget_history",
                               params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget_history(club_id=club_id,
                                                 sort=sort,
                                                 page=page,
                                                 session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find("div", {"class": "wr_c4 left p10"}).find_all(
                "div", {"class": "td_un"})
            for pet in pets:
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                count = pet.text.split(": ")[1].replace("\t", "")
                count = int(count)
                players.append(
                    {'pet_id': pet_id, 'name': name, 'count': count})
            resp = resp.find("div", {"class": "msg mrg_msg1 mt10 c_brown4"})
            resp = resp.find("div", {"class": "wr_c4 td_un"})
            last_reset = \
                resp.text.replace("\n", "").replace("\t", "").replace("\r",
                                                                      "").split(
                    ": ")[1]
            last_reset = last_reset.split("(")[0]
            try:
                last_reset_pet_id = int(
                    resp.find("a", {"class": "club_member"})['href'].split(
                        "=")[1])
                last_reset_name = \
                    resp.text.replace("\n", "").replace("\t", "").replace("\r",
                                                                          "").split(
                        ": ")[1]
                last_reset_name = last_reset_name.split("(")[1].split(")")[0]
            except Exception as e:
                pass
            return {'status': True,
                    'club_id': club_id,
                    'sort': sort,
                    'page': page,
                    'players': players,
                    'last_reset': last_reset,
                    'last_reset_pet_id': last_reset_pet_id,
                    'last_reset_name': last_reset_name}
    except Exception as e:
        return {'status': False,
                'error': 0,
                'msg': e}


async def club_budget_history_all(club_id, sort, page, session):
    try:
        params = {'id': club_id, 'sort': sort, 'page': page}
        players = []
        async with session.get(
                f"{HOST_URL}/club_budget_history_all", params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget_history_all(club_id=club_id,
                                                     sort=sort,
                                                     page=page,
                                                     session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find("div", {"class": "wr_c4 left p10"}).find_all(
                "div", {'class': 'td_un'})
            for pet in pets:
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                count = int(pet.text.split(": ")[1].replace('\t', ''))
                players.append(
                    {'pet_id': pet_id, 'name': name, 'count': count})
            return {'status': True,
                    'club_id': club_id,
                    'sort': sort,
                    'page': page,
                    'players': players}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def forums(club_id, session):
    try:
        params = {'id': club_id}
        forums_id = []
        async with session.get(f"{HOST_URL}/forum",
                               params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await forums(club_id=club_id,
                                    session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            threads = resp.find_all("div", {"class": "mbtn orange"})
            for forum in threads:
                forum_id = int(forum.find("a")['href'].split("=")[1])
                name = forum.text
                forums_id.append(
                    {'forum_id': forum_id, 'name': name})
            return {'status': True,
                    'club_id': club_id,
                    'forums_id': forums_id}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def collection_changer(session):
    # TODO
    try:
        async with session.get(f"{HOST_URL}/collection_changer") as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await collection_changer(session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find_all("div", {'class': 'post_chat'})
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def collection_changer_select(type, collection_id, session):
    try:
        params = {"type": type,
                  "id": collection_id}
        async with session.get(
                f"{HOST_URL}/collection_changer_select",
                params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await collection_changer_select(type=type,
                                                       collection_id=collection_id,
                                                       session=session)
            return {"status": True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def reception(club_id, page, accept_id, decline_id, decline_all,
                    session):
    try:
        accepted = declined = None
        if accept_id is not None:
            accepted = False
            params = {'id': club_id, 'page': page, 'accept_id': accept_id}
        elif decline_id is not None:
            declined = False
            params = {'id': club_id, 'page': page, 'decline_id': decline_id}
        elif decline_id is not None:
            params = {'id': club_id, 'page': page, 'decline_all': decline_all}
        else:
            params = {'id': club_id, 'page': page}
        members = []
        async with session.get(
                f"{HOST_URL}/reception", params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_history(club_id=club_id,
                                          type=type,
                                          page=page,
                                          session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("table", {'class': 'ib table_p5 font_14'})
            resp = resp.find_all("tr")
            if accepted is False and "Заявка принята" in await resp.text():
                accepted = True
            if declined is False and "Заявка отклонена" in await resp.text():
                declined = True
            for member in resp:
                try:
                    level = member.find("img",
                                        {"class": "price_img"}).next_element
                    level = int(level)
                    pet_id = int(member.find("a")["href"].split("=")[1])
                    name = member.find("a").text
                    beauty = member.find("span", {"class": "nowrap"}).text
                    beauty = int(beauty)
                    members.append(
                        {'level': level,
                         'pet_id': pet_id,
                         'name': name,
                         'beauty': beauty})
                except:
                    pass
            return {'status': True,
                    'club_id': club_id,
                    'page': page,
                    'members': members,
                    'accepted': accepted,
                    'declined': declined,
                    }
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_hint_add(text, session):
    try:
        data = {'text': text}
        async with session.post(
                f"{HOST_URL}/club_hint_add", data=data) as resp:
            return {'status': True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_settings(club_id, session):
    try:
        params = {'id': club_id}
        async with session.get(
                f"{HOST_URL}/club_settings", params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_settings(club_id=club_id,
                                           session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {'class': 'wr_c4'})
            resp = resp.find_all("div", {'class': 'mbtn'})
            settings = []
            for item in resp:
                name = item.find("a").text
                action_url = item.find("a")['href']
                settings.append({"name": name,
                                 "action_url": action_url})
            return {'status': True,
                    'settings': settings}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def gerb(club_id, gerb_id, yes, session):
    try:
        if yes is not None:
            params = {'id': club_id, 'gerb_id': gerb_id, 'yes': yes}
        else:
            params = {'id': club_id}
        async with session.get(
                f"{HOST_URL}/gerb", params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await gerb(club_id=club_id,
                                  gerb_id=gerb_id,
                                  yes=yes,
                                  session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {'class': 'wr_c4'})
            resp = resp.find_all("a", {'class': 'nd'})
            gerbs = []
            for item in resp:
                action_url = item['href']
                gerbs.append({"action_url": action_url})
            return {'status': True,
                    'gerbs': gerbs}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_about(session):
    try:
        async with session.get(
                f"{HOST_URL}/club_about") as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_about(session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            about = resp.find("textarea", {'class': 'thread_text'}).text
            return {'status': True,
                    'about': about}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_about_action(about, session):
    try:
        data = {'about': about}
        async with session.post(
                f"{HOST_URL}/club_about_action", data=data) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_about_action(about=about,
                                               session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "?result=1" in str(resp.url):
                about = resp.find("textarea", {'class': 'thread_text'}).text
                return {'status': True,
                        'about': about}
            elif "?result=" in str(resp.url):
                try:
                    resp = BeautifulSoup(await resp.read(), "lxml")
                    text = resp.find("span", {"class": "warning"}).text
                except:
                    text = "Не удалось изменить описание клуба."
                return {'status': False,
                        'code': 1,
                        'msg': text}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_rename(session):
    try:
        async with session.get(
                f"{HOST_URL}/club_rename") as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_about(session=session)
            resp = BeautifulSoup(await resp.read(), "lxml")
            name = resp.find("input", {'name': 'name'}).text
            return {'status': True,
                    'club': name}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def club_rename_action(name, session):
    try:
        data = {'name': name}
        async with session.post(
                f"{HOST_URL}/club_rename_action", data=data) as resp:
            if "?result=1" in str(resp.url):
                return {'status': True,
                        'club': name}
            elif "?result=" in str(resp.url):
                try:
                    resp = BeautifulSoup(await resp.read(), "lxml")
                    text = resp.find("span", {"class": "warning"}).text
                except:
                    text = "Не удалось сменить название."
                return {'status': False,
                        'code': 1,
                        'msg': text}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def leave_club(session):
    try:
        params = {'confirm': 1, 'clear': 1}
        async with session.get(
                f"{HOST_URL}/leave_club", params=params) as resp:
            if "Вы кликаете слишком быстро." in await resp.text():
                return await leave_club(session=session)
            return {'status': True}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}
