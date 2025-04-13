from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import settings
from schemas import OnboardCourse


def start_choice() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, расскажи",
                              callback_data="start_onboarding")],
        [InlineKeyboardButton(text="Нее, давай позже",
                              callback_data="end_onboarding")]
    ])


def to_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Главное меню", callback_data="next_onb")],
    ])


def next() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Продолжить", callback_data="next_onb")],
    ])


def yes_no_help() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, все получилось",
                              callback_data="next_onb")],
        [InlineKeyboardButton(text="Нет, помоги", callback_data="no_onb")]
    ])


def worked_and_chat_curator() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, все получилось",
                              callback_data="next_onb")],
        [InlineKeyboardButton(text="Чат с куратором",
                              url=settings.URL_BOT_CHAT_CURATOR)]
    ])


def que_iot(iot_disc: bool, iot_choice: bool) -> InlineKeyboardMarkup:
    inline_keyboard = []
    if iot_disc:
        inline_keyboard.append([InlineKeyboardButton(
            text="Отличие ядерных и неядерных дисциплин", callback_data="iot_disc")])
    if iot_choice:
        inline_keyboard.append([InlineKeyboardButton(
            text="Выбор дисциплин в Модеусе", callback_data="iot_choice")])
    inline_keyboard.append([InlineKeyboardButton(
        text="Нет, давай дальше", callback_data="next_onb")])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def que_exam() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Как проходят онлайн экзамены?", callback_data="info_exam")],
        [InlineKeyboardButton(text="Нее, давай дальше",
                              callback_data="next_onb")]
    ])


def que_rating() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Научный рейтинг",
                              callback_data="science_rating")],
        [InlineKeyboardButton(text="Внеучебный рейтинг",
                              callback_data="extr_rating")],
        [InlineKeyboardButton(
            text="Общий рейтинг и что он дает", callback_data="all_rating")],
        [InlineKeyboardButton(text="Нее, давай дальше",
                              callback_data="next_onb")]
    ])


def back_to_rating() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_rating")],
    ])


def yes_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="next_onb")],
        [InlineKeyboardButton(text="Нет", callback_data="no_onb")]
    ])


def end() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="До связи!", callback_data="end_onboarding")],
    ])


def get_sections_keyboard(data_course: OnboardCourse, from_add_course: bool = False, crossed_topics: dict = None) -> InlineKeyboardMarkup:
    if crossed_topics == None:
        crossed_topics = {}

    list_btn = []
    for section in data_course.sections:
        if data_course.name in crossed_topics.keys() and section.callback_data in crossed_topics[data_course.name].keys() and len(crossed_topics[data_course.name][section.callback_data]) == len(section.topics):
            btn = [InlineKeyboardButton(
                text=f"✅ {section.name}", callback_data=f"{section.callback_data}")]
        else:
            btn = [InlineKeyboardButton(
                text=f"☑️ {section.name}", callback_data=f"{section.callback_data}")]
        list_btn.append(btn)

    if from_add_course:
        list_btn.append([InlineKeyboardButton(
            text="Назад", callback_data="additional_courses")])
    else:
        list_btn.append([InlineKeyboardButton(
            text="Главное меню", callback_data="end_onboarding")])

    return InlineKeyboardMarkup(inline_keyboard=list_btn)


def get_topics_keyboard(data_course: OnboardCourse, callback_data_section: str, crossed_topics: dict = None) -> InlineKeyboardMarkup:
    if crossed_topics == None:
        crossed_topics = {}

    list_btn = []
    for section in data_course.sections:

        if section.callback_data == callback_data_section:
            for i in range(len(section.topics)):
                topic = section.topics[i]

                if data_course.name in crossed_topics.keys() and callback_data_section in crossed_topics[data_course.name].keys() and str(i) in crossed_topics[data_course.name][callback_data_section]:
                    btn = [InlineKeyboardButton(
                        text=f"✅ {topic.name}", callback_data=f"{callback_data_section}__{i}")]
                else:
                    btn = [InlineKeyboardButton(
                        text=f"☑️ {topic.name}", callback_data=f"{callback_data_section}__{i}")]
                list_btn.append(btn)
            break

    list_btn.append([InlineKeyboardButton(text="К разделам",
                    callback_data="onboarding_sections")])

    return InlineKeyboardMarkup(inline_keyboard=list_btn)


def topic_keyboard(data_course: OnboardCourse, callback_data_topic: str, is_help=False, not_question=False):
    split_callback = callback_data_topic.split("____")[0].split("__")
    index = int(split_callback[-1])
    callback_data_section = "__".join(split_callback[:-1])

    list_btn1 = []
    list_btn1.append(InlineKeyboardButton(
        text="↩️", callback_data=f"to_section___{callback_data_section}"))
    for section in data_course.sections:

        if section.callback_data == callback_data_section:
            topics = section.topics

            if index > 0:
                btn = InlineKeyboardButton(
                    text="⬅️", callback_data=f"{callback_data_section}__{index - 1}")
                list_btn1.append(btn)

            if index < len(topics) - 1:
                btn = InlineKeyboardButton(
                    text="➡️", callback_data=f"{callback_data_section}__{index + 1}")
                list_btn1.append(btn)

            break

    if not_question == False:
        list_btn2 = []
        if is_help == False:
            list_btn2.append(InlineKeyboardButton(
                text="Подсказка", callback_data=f"{callback_data_topic}____help"))
        list_btn2.append(InlineKeyboardButton(
            text="Чат с куратором", url=settings.URL_BOT_CHAT_CURATOR))
        return InlineKeyboardMarkup(inline_keyboard=[list_btn1, list_btn2])

    return InlineKeyboardMarkup(inline_keyboard=[list_btn1])


def additional_courses_keyboard(list_courses: list[tuple[int, str, int]], crossed_topics: dict = None):
    list_btn = []
    for course in list_courses:
        if crossed_topics != None and course[1] in crossed_topics.keys() and len(crossed_topics[course[1]].keys()) == course[2]:
            btn = [InlineKeyboardButton(
                text=f"✅ {course[1]}", callback_data=f"additional_courses__{course[0]}")]
        else:
            btn = [InlineKeyboardButton(
                text=f"☑️ {course[1]}", callback_data=f"additional_courses__{course[0]}")]
        list_btn.append(btn)

    list_btn.append([InlineKeyboardButton(
        text="Главное меню", callback_data="end_onboarding")])

    return InlineKeyboardMarkup(inline_keyboard=list_btn)
