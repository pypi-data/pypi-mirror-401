import datetime

from mpets.utils.catch_error import catch_error


@catch_error
def get_all_threads(bs_content):
    forums = bs_content.find_all('div', class_='forums')
    thread_list = []
    for forum in forums:
        thread_list.append(forum.find_all("div", {"class": "mbtn orange"}))
    return thread_list


@catch_error
def get_thread_id(bs_content):
    # replace to regex
    thread_id = bs_content.find("a")['href'].split("=")[1]
    if "&" in thread_id:
        thread_id = thread_id.split("&")[0]
    return int(thread_id)


@catch_error
def get_thread_name(bs_content):
    thread_name = bs_content.find("div", {"class": "pt1"}).text
    return thread_name


@catch_error
def get_thread_name_inner(bs_content):
    thread_name = bs_content.find("div",
                                  {"class": "ttl lgreen mrg_ttl mt10"})
    thread_name = thread_name.find("div",
                                   {"class": "tc"}).next_element
    return thread_name


@catch_error
def get_author_id(bs_content, message_num):
    pet_id = bs_content.find_all("div", {"class": "thread_title"})[message_num]
    pet_id = pet_id.find("a", {"class": "orange_dark2"})["href"].split("=")[1]
    return int(pet_id)


@catch_error
def get_author_name(bs_content, message_num):
    name = bs_content.find_all("div", {"class": "thread_title"})[message_num]
    name = name.find("a", {"class": "orange_dark2"}).next_element
    return name


@catch_error
def get_message(bs_content, message_num):
    message = bs_content.find_all("div", {"class": "thread_content"})[message_num].get_text()
    message = message.replace("\n", "", 1)
    return message


@catch_error
def get_post_date(bs_content, message_num):
    post_date = bs_content.find_all("div", {"class": "thread_title"})[message_num]
    post_date = post_date.find("span", {
        "class": "post_date nowrap"}).next_element
    return post_date


@catch_error
def convert_post_date_to_normal_datetime(thread_id, post_date):
    # 2632996 - ....... = 2023
    # 2615983 - 2632995 = 2022
    # 2568190 - 2615980 = 2021
    # 2526558 - 2568177 = 2020
    # 2467680 - 2526532 = 2019
    # 2094082 - 2467676 = 2018
    # 1511481 - 2094065 = 2017
    # 1233675 - 1511369 = 2016
    # 839214 - 1233545 = 2015
    # 287960 - 839177 = 2014
    # 28457 - 287865 = 2013
    # 1 - 27558 = 2012
    years = [[1, 27558, 2012],
             [28457, 287865, 2013],
             [287960, 839177, 2014],
             [839214, 1233545, 2015],
             [1233675, 1511369, 2016],
             [1511481, 2094065, 2017],
             [2094082, 2467676, 2018],
             [2467680, 2526532, 2019],
             [2526558, 2568177, 2020],
             [2568190, 2615980, 2021],
             [2615983, 2632995, 2022],
             [2632996, 2_900_000, 2023]
             ]
    current_year = None
    for i in range(len(years)):
        if years[i][0] < thread_id < years[i][1]:
            current_year = years[i][2]

    months = {"янв": 1, "фев": 2, "мар": 3,
              "апр": 4, "мая": 5, "июн": 6,
              "июл": 7, "авг": 8, "сен": 9,
              "окт": 10, "ноя": 11, "дек": 12}
    normal_date = post_date.split(" ")
    if len(normal_date) > 1:
        hour, mins = map(int, normal_date[2].split(":"))
        current_date = datetime.date.today()
        dateobj = datetime.datetime(year=current_date.year if current_year is None else current_year,
                                    month=months[normal_date[1]],
                                    day=int(normal_date[0]),
                                    hour=hour,
                                    minute=mins)
        normal_date = dateobj
    else:
        hour, mins = map(int, normal_date[0].split(":"))
        current_date = datetime.date.today()
        dateobj = datetime.datetime(year=current_date.year,
                                    month=current_date.month,
                                    day=current_date.day,
                                    hour=hour,
                                    minute=mins)
        normal_date = dateobj
    return normal_date


@catch_error
def get_message_id(bs_content, message_num):
    if "правка" in \
            bs_content.find_all("div", {"class": "thread_content"})[message_num].text:
        try:
            msg_id = \
                bs_content.find_all("div", {"class": "thread_content"})[message_num]
            id = msg_id.find("a", {"class": "post_control"})[
                'href']
            id = id.split("id=")[1].split("&")[0]
            id = int(id)
        except:
            id = 0
    else:
        id = 0
    return id
