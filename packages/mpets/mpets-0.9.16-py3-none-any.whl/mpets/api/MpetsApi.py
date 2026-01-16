import asyncio
import random
from typing import Optional, Union

import aiohttp
from aiohttp import ClientResponse
from box import Box

from mpets import models
from mpets.api.BaseApi import BaseApi
from mpets.api.methods.Auth import Auth
from mpets.api.methods.Club import Club
from mpets.api.methods.Forum import Forum
from mpets.api.methods.Main import Main
from mpets.api.methods.Profile import Profile
from mpets.api.methods.Settings import Settings


class MpetsApi:
    def __init__(self, name: str = None,
                 password: str = None,
                 cookie: str = None,
                 timeout: int = 5,
                 connector: dict = None,
                 proxy: str = None,
                 rucaptcha_api: str = None,
                 fast_mode: bool = True,
                 requests_per_second: Optional[float] = None):

        self.__base_api: BaseApi = BaseApi(cookie=cookie,
                                           timeout=timeout,
                                           connector=connector,
                                           proxy=proxy,
                                           mpets_api=self,
                                           requests_per_second=requests_per_second)

        self.__connector = connector

        self.__auth = Auth(base_api=self.__base_api)
        self.__main = Main(base_api=self.__base_api)
        self.__settings = Settings(base_api=self.__base_api)
        self.__forum = Forum(base_api=self.__base_api)
        self.__club = Club(base_api=self.__base_api)
        self.__profile = Profile(base_api=self.__base_api)

        self.__pet_id: Optional[int] = None
        self.__name: str = name
        self.__password: str = password
        self.proxy: str = proxy

        self.__fast_mode: bool = True

        self.rucaptcha_api: str = rucaptcha_api
        self.captcha_file = None

        # add setter and getter
        self.__beauty: Optional[int] = None
        self.__coin: Optional[int] = None
        self.__heart: Optional[int] = None
        self.__club_id: Optional[int] = None

        if fast_mode is False:
            ...

    @property
    def cookie(self):
        return self.__base_api.cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__base_api._cookie = cookie

    @property
    def requests_per_second(self) -> Optional[float]:
        return self.__base_api.rate_limit

    def set_requests_per_second(self, requests_per_second: Optional[float]):
        self.__base_api.set_rate_limit(requests_per_second)

    @property
    def id(self):
        return self.__pet_id

    @id.setter
    def id(self, value):
        self.__pet_id = value

    async def check_cookies(self) -> Union[models.CookieStatus, models.Error]:
        return await self.__auth.check_cookie()

    """
        login.py
    """

    async def user_agreement(self, agreement_confirm: bool = True,
                             params: int = 1) -> models.BooleanStatus:
        """Принимает пользовательское соглашение

        Args:
            agreement_confirm (bool, optional): default True.
            params (int, optional): default  1.

        Returns:
            status (bool): Статус запроса;
        """

        return await self.__auth.user_agreement(agreement_confirm=agreement_confirm,
                                                params=params)

    async def get_captcha(self):
        """Возвращает капчу

        Returns:
            status (bool): Статус запроса;
            captcha (str): Путь до картинки с капчей;
            cookies (dict): куки;
            session (object): Сессия aiohttp.
        """
        resp = await self.__auth.get_captcha()
        if resp['status']:
            await self.__base_api.get_session(resp['cookie'])
        return Box(resp)

    async def start(self,
                    name: str = "standard",
                    password: str = None,
                    type: int = 1) -> Union[models.Start, models.Error]:  # noqa
        """ Регистрация питомца

            Args:
                name (str): имя аккаунта. По умолчанию регистрирует аккаунт со стандарным ником;
                password (str): пароль аккаунта. Если пароль не указан,
                                то генерируется 10-значный;
                type (int): тип аватарки. Доступны: 0, 1, 12, 13.

            Returns:
                status (bool): статус запроса;
                pet_id (int): id аккаунта;
                name (str): имя аккаунта;
                password (str): пароль от аккаунта;
                cookies (dict): куки.
        """
        # TODO add enum for nickname type
        return await self.__auth.start(name=name,
                                       password=password,
                                       type=type)

    async def login(self, code: int = None) -> models.Login:
        """ Авторизация

            Returns:
                status (bool): статус запроса;
                pet_id (int): id аккаунта;
                name (str): имя аккаунта;
                cookies (dict): куки.
        """

        resp = await self.__auth.login(name=self.__name,
                                       password=self.__password,
                                       code=code)
        return resp

    async def _save(self, name, password) -> models.Error:
        """
            Взамен этому методу используйте /login или /start.
        """
        # TODO переделать
        response = await self.__base_api.request(type="POST",
                                                 method="/save_pet",
                                                 data={"name": name,
                                                       "password": password,
                                                       "email": ""})
        return await self.__auth.save(response)

    async def actions(self) -> models.BooleanStatus:
        """
            Кормит, играет и ходит на выставку
        """
        await self.__main.actions(amount=3)
        return models.BooleanStatus(status=True)

    async def action(self, action: str, rand: int = random.randint(100, 9000)):
        """ Выполняет дейсвтие с питомцем

        Args:
            action (str): вид дейсвтия;
            rand (int): случайное число (default: от 100 до 9000).

        Resp:
            status (bool): статус запроса;
        """
        response = await self.__main.action(action_type=action)
        return response

    async def show(self) -> models.BooleanStatus:
        """ Выставка
        """
        await self.__main.show()
        return models.BooleanStatus(status=True)

    async def wakeup_sleep_info(self):
        """
            Информация о состоянии питомца.
        """
        raise NotImplementedError()

    async def wakeup_sleep(self):
        # TODO
        """
            Разбудить питомца
        """
        raise NotImplementedError()

    async def wakeup(self):
        """ Дает витаминку за 5 сердец и пропускает минутный сон
        """
        return await self.__main.wakeup()

    async def check_ban(self):
        """ Проверяет наличие бана на аккаунте
        """
        raise NotImplementedError()

    async def charm(self):
        # TODO
        """ Возвращает данные снежков

        """
        raise NotImplementedError()

    async def charm_in_queue(self):
        # TODO
        """ Встать в очередь в снежках

        """
        raise NotImplementedError()

    async def charm_out_queue(self):
        # TODO
        """ Покинуть очередь в снежках
        """
        raise NotImplementedError()

    async def charm_attack(self):
        # TODO
        """ Бросить снежок
        """
        raise NotImplementedError()

    async def charm_change(self):
        # TODO
        raise NotImplementedError()

    async def charm_dodge(self):
        # TODO
        raise NotImplementedError()

    async def races(self):
        # TODO
        """ Возвращает данные скачков

        """
        raise NotImplementedError()

    async def races_in_queue(self):
        raise NotImplementedError()

    async def races_out_queue(self):
        raise NotImplementedError()

    async def races_go(self):
        raise NotImplementedError()

    async def races_attack(self):
        raise NotImplementedError()

    async def races_change(self):
        raise NotImplementedError()

    async def glade(self):
        raise NotImplementedError()

    async def glade_dig(self):
        return await self.__main.glade_dig()

    async def travel(self):
        raise await self.__main.travel()

    async def go_travel(self, travel_id: int):
        return await self.__main.go_travel(travel_id=travel_id)

    async def train(self) -> models.TrainResponse:
        return await self.__main.train()

    async def train_skill(self, skill: str):
        resp = await main.train_skill(skill=skill,
                                      session=self.session)
        return Box(resp)

    async def assistants(self):
        raise NotImplementedError()

    async def assistants_train(self, type):
        raise NotImplementedError()

    async def jewels(self):
        raise NotImplementedError()

    async def collect_jewel(self, jewel_id):
        resp = await main.collect_jewel(jewel_id=jewel_id,
                                        session=self.session)
        return Box(resp)

    async def home(self):
        raise NotImplementedError()

    async def garden(self):
        raise NotImplementedError()

    async def garden_collect(self, garden_id):
        raise NotImplementedError()

    async def task(self):
        return await self.__main.task()

    async def task_reward(self, task_id):
        return await self.__main.task_reward(task_id=task_id)

    async def items(self, category):
        resp = await main.items(category=category,
                                session=self.session)
        return Box(resp)

    async def buy(self, category: str, item_id: id):
        resp = await self.__main.buy(category=category,
                                     item_id=item_id)
        return Box(resp)

    async def best(self, type: str = "user", page: int = 1):
        resp = await main.best(type=type,
                               page=page,
                               session=self.session)
        return Box(resp)

    async def buy_heart(self, heart: int = 100):
        resp = await main.buy_heart(heart=heart,
                                    session=self.session)
        return Box(resp)

    async def find_pet(self, name):
        """ Поиск питомца

       Args:
           name (str): имя аккаунта.

       Resp:
           status (bool): статус запроса;
           pet_id (int): id аккаунта;
           name (str): имя аккаунта;
           account_status (str): информация о бане.
        """
        resp = await main.find_pet(name=name,
                                   session=self.session)
        return Box(resp)

    async def find_club(self, name: str):
        """ Поиск клуба

           Args:
               name (str): имя клуба.

           Resp:
               status (bool): статус запроса;
               club_id (int): id клуба;
               name (str): имя клуба;
               account_status (str): информация о бане.
       """
        resp = await main.find_club(name=name,
                                    session=self.session)
        return Box(resp)

    async def show_coin(self):
        raise NotImplementedError()

    async def show_coin_get(self):
        raise NotImplementedError()

    async def online(self, page=1):
        resp = await main.online(page=page,
                                 session=self.session)

        return Box(resp)

    async def game_time(self):
        resp = await main.game_time(session=self.session)

        return Box(resp)

    '''
        Модуль: Forum.py
    '''

    async def threads(self, forum_id: int, page: int = 1) -> models.Forum:
        # TODO добавить возврат имени топа
        """ Получить список топов

            Args:
                forum_id (int): id форума;
                page (int): страница форума (default: 1).

            Resp:
                status (boolean): статус запроса;
                threads (dict): список топов на форуме;
                    thread_id (int): id топа;
                    thread_name (str): название топа.
        """
        return await self.__forum.threads(forum_id=forum_id,
                                          page=page)

    async def thread(self, thread_id: int, page: int = 1) -> models.ThreadContent:
        """ Получить содержимое топа

            Args:
                thread_id (int): id топика;
                page (int): страница форума (default: 1).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                page (int): страница топа;
                messages(dict): список сообщений в топе;
                    pet_id (int): id автора сообщения;
                    name (str): ник автора сообщения;
                    message_id (int): порядковый номер сообщения в топе;
                    message (str): текст сообщения;
                    post_date (str): дата сообщения.
                thread_status (str): статус топика (Открыт/Закрыт)
                moderator_id (int): id модератора,
                                    если топик закрыт (default: None)
                moderator_name (str): ник модератора,
                                            если топик закрыт (default: None)
        """

        return await self.__forum.thread(thread_id=thread_id,
                                         page=page)

    async def add_thread(self, forum_id: int,
                         thread_name: str,
                         thread_text: str,
                         club_only: str = "on") -> models.ThreadContent:
        """ Создает топик

            Args:
                forum_id (int): id форума;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
        """
        return await self.__forum.add_thread(forum_id=forum_id,
                                             thread_name=thread_name,
                                             thread_text=thread_text,
                                             club_only=club_only)

    async def add_vote(self, forum_id: int,
                       thread_name: str,
                       thread_text: str,
                       vote1: str,
                       vote2: str = "",
                       vote3: str = "",
                       vote4: str = "",
                       vote5: str = "",
                       club_only: str = "on") -> models.ThreadContent:
        """ Создать опрос

            Args:
                forum_id (int): id форума;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа;
                vote1 (str): вариант 1;
                vote2 (str): вариант 2;
                vote3 (str): вариант 3;
                vote4 (str): вариант 4;
                vote5 (str): вариант 5;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
                vote1 (str): вариант 1;
                vote2 (str): вариант 2;
                vote3 (str): вариант 3;
                vote4 (str): вариант 4;
                vote5 (str): вариант 5;
        """
        return await self.__forum.add_vote(forum_id=forum_id,
                                           thread_name=thread_name,
                                           thread_text=thread_text,
                                           vote1=vote1,
                                           vote2=vote2,
                                           vote3=vote3,
                                           vote4=vote4,
                                           vote5=vote5,
                                           club_only=club_only)

    async def thread_message(self, thread_id: int, message: str) :
        """ Отправить сообщение

            Args:
                thread_id (int): id топа;
                message (str): сообщение.

            Resp:
                status (boolean): статус запроса;

        """
        return await self.__forum.thread_message(thread_id=thread_id,
                                                 message=message)

    async def send_message(self, thread_id, message) -> models.BooleanStatus:
        """
            Аналог метода thread_message()
        """
        return await self.__forum.thread_message(thread_id=thread_id,
                                                 message=message)

    async def thread_vote(self, thread_id: int, vote: int) -> models.BooleanStatus:
        return await self.__forum.thread_vote(thread_id=thread_id,
                                              vote=vote)

    async def message_edit(self, message_id: int, thread_id: int = 1) -> models.MessageEdit:
        """ Вернуть текст сообщения по id.

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """
        return await self.__forum.message_edit(message_id=message_id,
                                               thread_id=thread_id)

    async def update_message(self, message_id: int,
                             message: str,
                             thread_id: int = 1) -> models.BooleanStatus:
        """ Отредактировать сообщение

            Args:
                message_id (int): id сообщения;
                message (str): текст сообщения;
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """
        return await self.__forum.update_message(message_id=message_id,
                                                 message=message,
                                                 thread_id=thread_id)

    async def message_delete(self, message_id: int, thread_id: int = 1,
                             page: int = 1) -> models.BooleanStatus:
        """ Удалить сообщение

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа (default: 1);
                page (int): номер страницы топа (default: 1).

            Resp:
                status (boolean): статус запроса.
        """

        return await self.__forum.message_delete(message_id=message_id,
                                                 thread_id=thread_id,
                                                 page=page)

    async def edit_thread(self, thread_id) -> models.EditThread:
        """ Вернуть содержимое топа

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """

        return await self.__forum.edit_thread(thread_id=thread_id)

    async def update_thread(self, thread_name: str,
                            thread_id: int,
                            thread_text: str,
                            forum_id: int = 3,
                            club_only: str = "on") -> models.BooleanStatus:
        """ Отредактировать топ

            Args:
                thread_name (str): заголовок топа;
                forum_id (int): id форума;
                thread_id (int): id топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса.
        """

        return await self.__forum.update_thread(thread_name=thread_name,
                                                forum_id=forum_id,
                                                thread_id=thread_id,
                                                thread_text=thread_text,
                                                club_only=club_only)

    async def edit_vote(self, forum_id: int,
                        thread_id: int,
                        thread_name: str,
                        thread_text: str,
                        vote1: str,
                        vote2: str = "",
                        vote3: str = "",
                        vote4: str = "",
                        vote5: str = "",
                        club_only: str = "on") -> models.BooleanStatus:
        """
        """

        return await self.__forum.edit_vote(forum_id=forum_id,
                                            thread_id=thread_id,
                                            thread_name=thread_name,
                                            thread_text=thread_text,
                                            vote1=vote1, vote2=vote2, vote3=vote3,
                                            vote4=vote4, vote5=vote5, club_only=club_only)

    async def delete_thread(self, thread_id) -> models.BooleanStatus:
        """ Удалить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """

        return await self.__forum.delete_thread(thread_id=thread_id)

    async def restore_thread(self, thread_id) -> models.BooleanStatus:
        """ Восстановить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """

        return await self.__forum.restore_thread(thread_id=thread_id)

    async def save_thread(self, thread_id) -> models.BooleanStatus:
        """ Защитить от очистки

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
       """
        return await self.__forum.save_thread(thread_id=thread_id)

    async def unsave_thread(self, thread_id: int) -> models.BooleanStatus:
        """ Снять защиту от очистки

            Args:
                thread_id (int): id топа.

           Resp:
                status (boolean): статус запроса.
       """
        return await self.__forum.unsave_thread(thread_id=thread_id)

    async def close_thread(self, thread_id: int) -> models.BooleanStatus:
        """ Закрыть топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (boolean): статус запроса.
       """

        return await self.__forum.close_thread(thread_id=thread_id)

    async def open_thread(self, thread_id: int) -> models.BooleanStatus:
        """ Открыть топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (boolean): статус запроса.
       """
        return await self.__forum.open_thread(thread_id=thread_id)

    async def attach_thread(self, thread_id: int) -> models.BooleanStatus:
        """ Прикрепить топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (str): статус запроса.
       """
        return await self.__forum.attach_thread(thread_id=thread_id)

    async def detach_thread(self, thread_id: int) -> models.BooleanStatus:
        """ Открепить топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (boolean): статус запроса.
        """
        return await self.__forum.detach_thread(thread_id=thread_id)

    '''
    Club.py
    '''

    async def club(self, club_id=None, page=1) -> models.Club:
        """ Получить информацию о клубе

           Args:
                club_id (int): id клуба. (без аргумента вернет информацию о
                 своем клубе, либо о приглашении в клуб);
                page (int): страница клуба.

           Returns:
                status (str): статус запроса;
                club (boolean): True, если клуб существует; False,
                                    если клуба нет;
                club_id (int): id клуба;
                club_name (str): название клуба;
                about_club (str): описание клуба (default: None);
                data (str): дата основания;
                level (int): уровень клуба;
                exp_club (dict): опыт клуба;
                    now (str): текущий опыт;
                    need (str): до следующего уровня.
                builds (int): уровень построек;
                budget (dict): копилка;
                    coins (int): монет в копилке (default: None);
                    hearts (int): сердце в копилке (default: None).
                number_players (int): количество игроков;
                players (dict): игроки;
                    pet_id (int): id игрока;
                    name (str): имя игрока;
                    exp (str): опыт игрока;
                    rank (str): ранк игрока.
        """
        return await self.__club.club(club_id=club_id,
                                      page=page)

    async def club_want(self) -> models.BooleanStatus:
        """
            Кнопка «Хочу в клуб»
        """
        return await self.__club.want()

    async def accept_invite(self, club_id) -> models.BooleanStatus:
        """ Принять приглашение от клуба

            Args:
                club_id (int): id клуба.
        """
        return await self.__club.accept_invite(club_id=club_id)

    async def decline_invite(self, club_id) -> models.BooleanStatus:
        """ Отменить приглашение от клуба

            Args:
                club_id (int): id клуба.
        """
        return await self.__club.decline_invite(club_id=club_id)

    async def enter_club(self, club_id, decline=False) -> models.BooleanStatus:
        """ Отправить заявку в клуб

            Args:
                club_id (int): id клуба;
                decline (bool): отменить заявку.
        """
        return await self.__club.enter_club(club_id=club_id,
                                            decline=decline)

    async def create_club(self, name: str) -> models.BooleanStatus:
        return await self.__club.create_club(name=name)

    async def builds(self, club_id: int) -> Union[models.ClubBuilds, models.Error]:
        return await self.__club.builds(club_id=club_id)

    async def build(self, club_id: int, type: int = 1):
        return await club.build(club_id=club_id,
                                type=type,
                                session=self.session)

    async def build_upgrade(self, club_id: int, type: int = 1):
        return await Club.build_upgrade(club_id=club_id,
                                        type=type,
                                        session=self.session)

    async def build_speed(self, club_id: int, type: int = 1):
        return await club.build_speed(club_id=club_id,
                                      type=type,
                                      session=self.session)

    async def club_budget(self, club_id: int):
        return await club.club_budget(club_id=club_id,
                                      session=self.session)

    async def add_club_budget(self, coin, heart):
        resp = await club.add_club_budget(coin=coin,
                                          heart=heart,
                                          session=self.session)
        return Box(resp)

    async def club_budget_history(self, club_id, sort=1, page=1):
        resp = await club.club_budget_history(club_id=club_id,
                                              sort=sort,
                                              page=page,
                                              session=self.session)
        return Box(resp)

    async def club_budget_history_all(self, club_id, sort=1, page=1):
        return await club.club_budget_history_all(club_id=club_id,
                                                  sort=sort,
                                                  page=page,
                                                  session=self.session)

    async def forums(self, club_id):
        resp = await Club.forums(club_id=club_id,
                                 session=self.session)
        return Box(resp)

    async def chat(self, club_id=0, page=1):
        resp = await self.__club.chat(club_id=club_id,
                                      page=page)
        return Box(resp)

    async def chat_message(self, club_id, message):
        resp = await self.__club.chat_message(club_id=club_id,
                                              message=message)
        return Box(resp)

    async def collection_changer(self):
        resp = await Club.collection_changer(session=self.session)
        return Box(resp)

    async def collection_changer_select(self, type: int = 1,
                                        collection_id: int = 1):
        resp = await club.collection_changer_select(type=type,
                                                    collection_id=collection_id,
                                                    session=self.session)
        return Box(resp)

    async def reception(self, club_id: int = 0, page: int = 1,
                        accept_id: int = None, decline_id: int = None,
                        decline_all: int = None):
        """ Желающие вступить в клуб

           Args:
                club_id (int): id клуба;
                page (int): страница списка;
                accept_id (int): id питомца, которого нужно принять;
                decline_id (int): id питомца, заявку которого нужно отклонить;
                decline_all (int): отклонить все заявки.

           Returns:
                status (str): статус запроса;
                club (int): id клуба;
                page (int): страница списка;
                members (list): список заявок в клуб;
                accepted (boolean): True, если заявка принята.
                declined (boolean): True, если заявка отклонена.
            """
        resp = await Club.reception(club_id=club_id,
                                    page=page,
                                    accept_id=accept_id,
                                    decline_id=decline_id,
                                    decline_all=decline_all,
                                    session=self.session)
        return Box(resp)

    async def club_history(self, club_id, type=1, page=1):
        return await self.__club.club_history(club_id=club_id,
                                              type=type,
                                              page=page)

    async def club_hint_add(self, text: str):
        resp = await Club.club_hint_add(text=text,
                                        session=self.session)
        return Box(resp)

    async def club_settings(self, club_id):
        resp = await Club.club_settings(club_id=club_id,
                                        session=self.session)
        return Box(resp)

    async def gerb(self, club_id, gerb_id: int = None, yes: int = None):
        resp = await club.gerb(club_id=club_id,
                               gerb_id=gerb_id,
                               yes=yes,
                               session=self.session)
        return Box(resp)

    async def club_about(self):
        resp = await club.club_about(session=self.session)
        return Box(resp)

    async def club_about_action(self, about: str):
        resp = await club.club_about_action(about=about,
                                            session=self.session)
        return Box(resp)

    async def club_rename(self):
        resp = await club.club_rename(session=self.session)
        return Box(resp)

    async def club_rename_action(self, name: str):
        resp = await Club.club_rename_action(name=name,
                                             session=self.session)
        return Box(resp)

    async def leave_club(self):
        return await club.leave_club(session=self.session)

    '''
    profile.md
    '''

    async def profile(self) -> models.Profile:
        return await self.__profile.profile()

    async def view_profile(self, pet_id: int) -> Union[models.ViewProfile, models.Error]:
        return await self.__profile.view_profile(pet_id=pet_id)

    async def view_anketa(self, pet_id: int):
        resp = await profile.view_anketa(pet_id=pet_id,
                                         session=self.session)
        return Box(resp)

    async def view_gifts(self, pet_id, page=1):
        return await profile.view_gifts(pet_id=pet_id,
                                        page=page,
                                        session=self.session)

    async def view_posters(self):
        resp = await profile.view_posters(session=self.session)
        return Box(resp)

    async def post_message(self, pet_id, page=1):
        return await profile.post_message(pet_id=pet_id,
                                          page=page,
                                          session=self.session)

    async def post_send(self, message, pet_id, page=1):
        return await profile.post_send(message_text=message,
                                       pet_id=pet_id,
                                       page=page,
                                       session=self.session)

    async def chest(self):
        response: ClientResponse = await self.request(type="GET",
                                                      method="/chest")
        return await profile.chest(response=response)

    async def wear_item(self, item_id: int):
        resp = await profile.wear_item(item_id=item_id,
                                       session=self.session)
        return Box(resp)

    async def sell_item(self, item_id: int):
        resp = await profile.sell_item(item_id=item_id,
                                       session=self.session)
        return Box(resp)

    async def gear(self):
        resp = await profile.gear(session=self.session)
        return Box(resp)

    async def gold_chest(self):
        resp = await self.__main.gold_chest()
        return Box(resp)

    async def open_gold_chest(self):
        resp = await self.__main.open_gold_chest()
        return resp

    async def open_gold_chest_key(self):
        # TODO added others rewards
        resp = await main.open_gold_chest_key(session=self.session)
        return Box(resp)

    async def set_avatar(self, avatar_id):
        resp = await main.set_avatar(avatar_id=avatar_id,
                                     session=self.session)
        return Box(resp)

    async def settings_game(self, main_menu_list=False):
        # TODO
        resp = await settings.settings_game(session=self.session)
        return Box(resp)

    async def change_name(self, name: str = None):
        """
            Если name = None, то возвращает текущий ник и количество изменений ника.
            Иначе происходит смена никнейма.

            Args:
                name (str): новый никнейм. Default: None

            Returns:
                status (bool): статус запроса;
                name (str): текущий никнейм;
                changed (int): количество изменений никнейма.
        """
        resp = await settings.change_name(name=name,
                                          session=self.session)
        return Box(resp)

    async def change_pw(self, password: str = None) -> Union[models.NewPassword, models.Error]:
        """ Изменяет текущий пароль. Если запрос отправлен без аргумента,
            то генерируется 12-значный новый пароль.

            Args:
                password (str): новый пароль. Default: None

            Returns:
                status (bool): статус запроса;
                password (str): новый пароль.
        """
        return await self.__settings.change_pw(password=password)

    async def close(self):
        await self.__base_api.close_session()

    async def ban_player(self, pet_id: int, reason: str, hours: int):
        resp = await profile.ban_player(pet_id=pet_id,
                                        reason=reason,
                                        hours=hours,
                                        session=self.session)
        return Box(resp)

    async def my_ip(self) -> str:
        await self.__base_api.get_session()
        print(self.proxy)
        try:
            response = await self.__base_api.session.get('https://api64.ipify.org?format=json',
                                                         proxy=self.proxy)
            data = await response.json()
            return data['ip']
        except Exception as ex:
            print("Прокси не работает")
