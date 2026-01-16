from typing import Union

from aiohttp import ClientResponse
from bs4 import BeautifulSoup

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.api.methods.parsers.forum_parser import get_all_threads, get_thread_id, get_thread_name, \
    get_thread_name_inner, get_author_id, get_author_name, get_message, get_post_date, \
    convert_post_date_to_normal_datetime, get_message_id
from mpets.models.BaseResponse import BaseResponse


class Forum:
    def __init__(self, base_api: BaseApi):
        self.base_api = base_api

    async def threads(self, forum_id: int, page: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/threads",
                                                                   params={"id": forum_id, "page": page})
            bs_content = BeautifulSoup(await response.text(), "lxml")
            raw_thread_list = get_all_threads(bs_content=bs_content)
            thread_list = []
            for i, raw_thread in enumerate(raw_thread_list):
                for thread in raw_thread:
                    thread_id = get_thread_id(bs_content=thread)
                    thread_name = get_thread_name(bs_content=thread)
                    is_forum = (i == 0)

                    _thread = models.Thread(id=thread_id,
                                            name=thread_name,
                                            is_forum=is_forum)
                    thread_list.append(_thread)

            return models.Forum(status=True,
                                threads=thread_list)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=15,
                                error_message=str(ex))

    async def thread(self, thread_id: int, page: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/thread",
                                                                   params={"id": thread_id, "page": page})
            moderator_id, moderator_name = None, None
            thread_status, messages = "Открыт", []
            url = response.url
            resp_text = await response.text()
            resp = BeautifulSoup(await response.text(), "lxml")
            if "Сообщений нет" in resp_text:
                return BaseResponse(
                    status=False,
                    error=100,
                    error_message="Сообщений нет"
                )
            elif "Форум/Топик не найден или был удален" in resp_text:
                return BaseResponse(
                    status=False,
                    error=101,
                    error_message="Форум/Топик не найден или был удален"
                )
            elif "club" in str(url):
                return BaseResponse(
                    status=False,
                    error=102,
                    error_message="Форум/Топик находятся в клубе"
                )
            thread_name = get_thread_name_inner(bs_content=resp)
            for a in range(
                    len(resp.find_all("div", {"class": "thread_title"}))):
                pet_id = get_author_id(bs_content=resp,
                                       message_num=a)
                name = get_author_name(bs_content=resp,
                                       message_num=a)
                message = get_message(bs_content=resp,
                                      message_num=a)
                post_date = get_post_date(bs_content=resp,
                                          message_num=a)

                normal_date = convert_post_date_to_normal_datetime(thread_id=thread_id,
                                                                   post_date=post_date)
                id = get_message_id(bs_content=resp, message_num=a)
                if id != 0:
                    try:
                        message = message.rsplit("\n[", 1)[0]
                    except:
                        pass
                else:
                    message = message.rsplit("\n", 1)[0]
                message_id = (15 * (int(page) - 1)) + a + 1
                message = models.ThreadMessage(id=id,
                                               pet_id=pet_id,
                                               name=name,
                                               message_id=message_id,
                                               message=message,
                                               post_date=post_date,
                                               normal_date=normal_date)
                messages.append(message)
            if "закрыл(а) топик" in resp_text:
                thread_status = "Закрыт"
                moderator_id = resp.find("div",
                                         {
                                             "class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_id = moderator_id.find("a", {"class": "pet_name"})
                moderator_id = moderator_id["href"].split("=")[1]
                moderator_id = int(moderator_id)
                moderator_name = resp.find("div",
                                           {
                                               "class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_name = moderator_name.find("a", {
                    "class": "pet_name"}).text
            elif "Топик закрыт" in resp_text:
                thread_status = "Закрыт системой."
            return models.ThreadContent(
                status=True,
                id=thread_id,
                name=thread_name,
                page=page,
                messages=messages,
                closed=thread_status,
                moderator_id=moderator_id,
                moderator=moderator_name
            )
        except Exception as ex:
            return BaseResponse(
                status=False,
                error=0,
                error_message=str(ex)
            )

    async def add_thread(self, forum_id, thread_name, thread_text, club_only):
        try:
            data = {"thread_name": thread_name,
                    "forum_id": forum_id,
                    "thread_text": thread_text,
                    "club_only": club_only}
            response = await self.base_api.request(type="POST",
                                                   method="/create_thread",
                                                   data=data)

            if "thread?id=" in str(response.url):
                thread_id = int(str(response.url).split("=")[1].split("&")[0])
                return await self.thread(thread_id=thread_id, page=1)
            elif "Не удалось cоздать топик" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Не удалось создать топик")
            elif "Вы не являетесь участником клуба" in await response.text():
                return BaseResponse(status=False,
                                    error=201,
                                    error_message="Вы не являетесь участником клуба")
            elif "Заголовок должен быть от 2 до 24 символов" in await response.text():
                return BaseResponse(status=False,
                                    error=202,
                                    error_message="Заголовок должен быть от 2 до 24 символов")
            elif "Содержание от 2 до 2500" in await response.text():
                return BaseResponse(status=False,
                                    error=203,
                                    error_message="Содержание должно быть от 2 до 2500")
            elif "Вы сможете создавать топики" in await response.text():
                return BaseResponse(status=False,
                                    error=204,
                                    error_message="Вы сможете создавать топики начиная с 18 уровня!")
        except Exception as ex:
            return BaseResponse(status=False,
                                error=204,
                                error_message=str(ex))

    async def add_vote(self, forum_id, thread_name, thread_text, vote1,
                       vote2, vote3, vote4, vote5, club_only) -> Union[models.ThreadContent, BaseResponse]:
        try:
            data = {"thread_name": thread_name, "forum_id": forum_id,
                    "thread_text": thread_text,
                    "club_only": club_only,
                    "vote1": vote1, "vote2": vote2, "vote3": vote3,
                    "vote4": vote4, "vote5": vote5, "vote": ""}
            response = await self.base_api.request(type="POST",
                                                   method="/create_thread",
                                                   data=data)
            if not vote1:
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Необходимо отправить хотя бы 1 вариант опроса")
            if "thread?id=" in str(response.url):
                thread_id = int(str(response.url).split("=")[1].split("&")[0])
                return await self.thread(thread_id=thread_id, page=1)
            elif "Не удалось cоздать топик" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Не удалось создать топик")
            elif "Вы не являетесь участником клуба" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Вы не являетесь участником клуба")
            elif "Вы сможете создавать топики" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Вы сможете создавать топики начиная с 18 уровня!")
            elif "Заголовок должен быть от 2 до 24 символов" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Заголовок должен быть от 2 до 24 символов")
            elif "Содержание от 2 до 2500" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Содержание от 2 до 2500")
            elif "Необходимо указать хотя бы один вариант опроса." in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Необходимо указать хотя бы один вариант опроса.")
            elif "Вариант должен быть от 2 до 24 символов" in await response.text():
                return BaseResponse(status=False,
                                    error=200,
                                    error_message="Вариант должен быть от 2 до 24 символов")
        except Exception as ex:
            return BaseResponse(
                status=False,
                error=0,
                error_message=str(ex)
            )

    async def thread_message(self, thread_id, message):
        try:
            data = {"message_text": message, "thread_id": thread_id}
            response = await self.base_api.request(type="POST",
                                                   method="/thread_message",
                                                   data=data)

            if "thread?id=" in str(response.url):
                return models.BooleanStatus(status=True)
            return BaseResponse(status=False,
                                error=210,
                                error_message="Форум/Топик не найден или был удален.")
        except Exception as ex:
            return BaseResponse(
                status=False,
                error=0,
                error_message=str(ex)
            )

    async def thread_vote(self, thread_id, vote) -> Union[models.BooleanStatus, BaseResponse]:
        try:
            data = {"vote_thread_id": thread_id,
                    "vote_forum_id": 3,
                    "vote": vote}
            response = await self.base_api.request(type="POST",
                                                   method="/thread_vote",
                                                   data=data)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(status=False,
                                error=0,
                                error_message=str(ex))

    async def message_edit(self, message_id, thread_id):
        try:
            params = {"id": message_id, "thread_id": thread_id,
                      "page": 1}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/message_edit",
                                                                   params=params)

            r_text = await response.text()
            resp = BeautifulSoup(await response.text(), "lxml")
            if "Содержание" in r_text:
                form = resp.find("form", {"method": "POST"})
                thread_id = form.find("input", {"name": "thread_id"})['value']
                message = form.find("textarea").text
                return models.MessageEdit(
                    status=True,
                    thread_id=thread_id,
                    message_id=message_id,
                    message=message
                )
            return BaseResponse(
                status=True,
                error=220,
                error_message="Нет доступа"
            )
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def update_message(self, message_id: int,
                             message: str,
                             thread_id: int):
        try:
            data = {"message_id": message_id,
                    "thread_id": thread_id,
                    "page": 1,
                    "message_text": message}
            response: ClientResponse = await self.base_api.request(type="POST",
                                                                   method="/update_message",
                                                                   data=data)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def message_delete(self, message_id, page, thread_id):
        try:
            params = {"id": message_id, "page": page, "thread": thread_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/message_delete",
                                                                   params=params)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def edit_thread(self, thread_id):
        # TODO return post_edit_date
        try:
            params = {"id": thread_id}
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/edit_thread",
                                                                   params=params)
            r_text = await response.text()
            resp = BeautifulSoup(await response.text(), "lxml")
            if "Содержание" in r_text:
                form = resp.find("form", {"method": "POST"})
                forum_id = form.find("input", {"name": "forum_id"})['value']
                thread_id = int(form.find("input", {"name": "thread_id"})['value'])
                thread_name = form.find("input", {"name": "thread_name"})['value']
                message_id = (form.find("input", {"name": "first_message_id"})[
                    'value'])
                message = form.find("textarea").text
                return models.EditThread(
                    status=True,
                    forum_id=forum_id,
                    id=thread_id,
                    name=thread_name,
                    message_id=message_id,
                    message=message
                )
            else:
                return BaseResponse(
                    status=True,
                    error=104,
                    error_message=""
                )
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def update_thread(self, thread_name: str, forum_id: int, thread_id: int,
                            thread_text: str,
                            club_only="on"):
        try:
            data = {"thread_name": thread_name, "forum_id": forum_id,
                    "thread_id": thread_id,
                    "first_message_id": 1, "thread_text": thread_text,
                    "club_only": club_only}
            response: ClientResponse = await self.base_api.request(type="POST",
                                                                   method="/update_thread",
                                                                   data=data)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def edit_vote(self, forum_id: int,
                        thread_id: int,
                        thread_name: str,
                        thread_text: str,
                        vote1: str,
                        vote2: str = "",
                        vote3: str = "",
                        vote4: str = "",
                        vote5: str = "",
                        club_only: str = "on"):
        try:
            data = {"thread_name": thread_name,
                    "forum_id": forum_id,
                    "thread_id": thread_id,
                    "first_message_id": 1,
                    "thread_text": thread_text,
                    "club_only": club_only,
                    "vote1": vote1, "vote2": vote2, "vote3": vote3,
                    "vote4": vote4, "vote5": vote5, "vote": ""}

            response: ClientResponse = await self.base_api.request(type="POST",
                                                                   method="/update_thread",
                                                                   data=data)
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def delete_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/delete_thread",
                                                                   params={"id": thread_id,
                                                                           "confirm": 1,
                                                                           "clear": 1})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def restore_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/restore_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def save_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/save_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def unsave_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/unsave_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def close_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/close_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def open_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/open_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def attach_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/attach_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )

    async def detach_thread(self, thread_id: int):
        try:
            response: ClientResponse = await self.base_api.request(type="GET",
                                                                   method="/detach_thread",
                                                                   params={"id": thread_id})
            return models.BooleanStatus(status=True)
        except Exception as ex:
            return BaseResponse(
                status=True,
                error=0,
                error_message=str(ex)
            )
