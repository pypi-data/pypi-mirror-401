from mpets import models
from mpets.utils.catch_error import catch_error


@catch_error
def get_club_id(url: str):
    club_id = str(url).split("=")[1]
    # отдельно, потому что может быть page
    # и проверка условия выше обязательна
    if "&" in club_id:
        club_id = club_id.split("&")[0]
    return int(club_id)


@catch_error
def get_club_name(bs_content):
    club_name = bs_content.find("div", {"class": "club_title cntr"}).text.replace("\n", "")
    if "Клуб" in club_name:
        club_name = club_name.rsplit("  ", maxsplit=1)[0].split("Клуб ")[1]
    else:
        club_name = club_name.rsplit("  ", maxsplit=1)[0]

    return club_name


@catch_error
def get_about_club(bs_content):
    stat_item = bs_content.find_all("div", {"class": "stat_item"})
    for stat in stat_item:
        if "О клубе" in stat.text:
            about_club = stat.find("span", {"class": "green_dark"}).text
            return about_club[1:]


@catch_error
def get_founded(bs_content):
    stat_item = bs_content.find_all("div", {"class": "stat_item"})
    for stat in stat_item:
        if "Основан" in stat.text:
            founded = stat.find("span", {"class": "green_dark"}).text
            return founded[1:]


@catch_error
def get_level(bs_content):
    stat_item = bs_content.find_all("div", {"class": "stat_item"})
    for stat in stat_item:
        if "Уровень клуба" in stat.text:
            level = stat.find("span", {"class": "green_dark"}).text
            return int(level)


@catch_error
def get_exp(bs_content):
    stat_item = bs_content.find("div", {"class": "wr_c4 left"}).find_all("span", {"class": "green_dark"})
    exp = stat_item[-1].text.strip().replace('\t', '')
    return exp


@catch_error
def get_builds(bs_content):
    builds = bs_content.find("div", {"class": "font_15 mb3 mt5"})
    builds = int(builds.text.split(": ")[1].split(" ")[0])
    return builds


@catch_error
def get_player_amount(bs_content):
    number_players = bs_content.find("span",
                                     {"class": "club_desc"}).text
    number_players = number_players.replace("\n", "")
    number_players = number_players.split("(")[1].split(")")[0]
    number_players = int(number_players.split(" из ")[0])
    return number_players


@catch_error
def get_pets(bs_content):
    pets = bs_content.find("div", {"class": "blub_list_pets"})
    pets = pets.find_all("span", {"class": ""})
    pets_list = []
    for pet in pets:
        pet_id = pet.find("a", {"class": "club_member"})["href"]
        pet_id = int(pet_id.split("=")[1])
        name = pet.find("a", {"class": "club_member"}).text
        exp = pet.text.rsplit(" -", maxsplit=1)[0].rsplit(" ",
                                                          maxsplit=1)[
            1]
        rank = pet.text.split("- ")[1]
        club_player = models.ClubPlayer(status=True,
                                        pet_id=pet_id,
                                        name=name,
                                        rank=rank,
                                        exp=exp)
        pets_list.append(club_player)

    return pets_list


@catch_error
def get_all_builds(bs_content):
    return bs_content.find_all("div", {"class": "item font_14 pb3"})


@catch_error
def get_build_name(bs_content):
    return bs_content.find("a", {"class": "build_link"}).text.replace(" ", "", 1)


@catch_error
def get_build_type(bs_content):
    build_type = bs_content.find("a", {"class": "build_link"})['href'].split("type=")[1]
    return int(build_type)


@catch_error
def get_current_level(bs_content):
    level_info = bs_content.find("span", {
        "class": "orange_dark2 font_14 ib"}).text
    level = int(level_info.split("(")[1].split(" ")[0])
    return level


@catch_error
def get_max_level(bs_content):
    level_info = bs_content.find("span", {
        "class": "orange_dark2 font_14 ib"}).text
    max_level = int(level_info.split("из ")[1].split(")")[0])
    return max_level


@catch_error
def get_bonus(bs_content):
    bonus = bs_content.find("span", {"class": "span2"}).text
    bonus = bonus.replace("\r", "").replace("\n", "").replace("\t",
                                                              "")
    return bonus


@catch_error
def get_(bs_content):
    pass


@catch_error
def get_bonus_bar(bs_content):
    bonus_bar = bs_content.find("div",
                                {"class": "msg mrg_msg1 mt5 c_brown3"}).text
    bonus_bar = bonus_bar.replace("\r", "").replace("\n", "").replace("\t", "")
    return bonus_bar


@catch_error
def get_health_bonus(bs_content):
    bonus_bar = get_bonus_bar(bs_content=bs_content)
    hearts_bonus = int(bonus_bar.split("участникам ")[1].split("%")[0])
    return hearts_bonus


@catch_error
def get_exp_bonus(bs_content):
    bonus_bar = get_bonus_bar(bs_content=bs_content)
    exp_bonus = int(bonus_bar.split("и ")[1].split("%")[0])
    return exp_bonus


@catch_error
def get_club_level(bs_content):
    bonus_bar = get_bonus_bar(bs_content=bs_content)
    club_level = int(bonus_bar.split(", ")[1].split(" ")[0])
    return club_level


@catch_error
def get_left_time(bs_content):
    if bs_content.find("span", {"class": "c_green mar5t"}) is not None:
        left_time = bs_content.find("span",
                                    {"class": "c_green mar5t"}).text
        left_time = left_time.split("Осталось ")[1]
        return left_time
    return None


@catch_error
def get_fix_build_bonus_if_build_is_improving(build_bonus):
    try:
        return build_bonus.split("Идет")[0]
    except Exception as ex:
        return build_bonus


@catch_error
def get_(bs_content):
    pass


@catch_error
def get_(bs_content):
    pass


@catch_error
def get_(bs_content):
    pass
