from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from worker import manager_faq
from config import settings


def menu(is_active_add_course: bool, is_active_onboarding: bool) -> InlineKeyboardMarkup:
    btns = [
        [InlineKeyboardButton(text="Предметы", callback_data="subjects"), InlineKeyboardButton(
            text="Онлайн курсы", callback_data="online_courses")],
        [InlineKeyboardButton(text="Чат с куратором", url=settings.URL_BOT_CHAT_CURATOR),
         InlineKeyboardButton(text="FAQ", callback_data="faq")],
    ]

    if is_active_add_course and is_active_onboarding:
        btns.insert(0, [InlineKeyboardButton(
            text="Вводный курс", callback_data="start_onboarding")])
        btns.insert(1, [InlineKeyboardButton(
            text="Дополнительные курсы", callback_data="additional_courses")])
    elif is_active_onboarding:
        btns.insert(0, [InlineKeyboardButton(
            text="Вводный курс", callback_data="start_onboarding")])
    elif is_active_add_course:
        btns.insert(0, [InlineKeyboardButton(
            text="Дополнительные курсы", callback_data="additional_courses")])

    return InlineKeyboardMarkup(inline_keyboard=btns)


def back_to_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
    ])


def courses(courses_data) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text=courses_data[i]["name"], callback_data="course_" + str(i))] for i in range(len(courses_data))
    ]
    inline_keyboard.append([InlineKeyboardButton(
        text="Назад", callback_data="main_menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard


def FAQ() -> InlineKeyboardMarkup:
    # Создание разделов вопросов
    btns = [[InlineKeyboardButton(text=topic.name, callback_data="faq_" + topic.id)]
            for topic in manager_faq.get_list_topics()]
    btns.append([InlineKeyboardButton(
        text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def back_to_FAQ() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="faq")],
        [InlineKeyboardButton(text="Главное меню",
                              callback_data="main_menu")]
    ])


def back_to_courses() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="online_courses")],
        [InlineKeyboardButton(text="Главное меню",
                              callback_data="main_menu")]
    ])
    return keyboard
