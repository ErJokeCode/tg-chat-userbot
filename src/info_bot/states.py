from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    WAITING_FOR_EMAIL = State()
    WAITING_FOR_STUDENT_ID = State()

class LKStates(StatesGroup):
    MAIN_MENU = State()
    WAITING_CHAT_WITH_CURATOR = State()
    COURSES = State()

class Info_teaching(StatesGroup):
    INFO = State()
    CARD = State()
    NUMBER_ROOM = State()
    NAVIGATOR = State()
    LK_URFU = State()
    ONLINE_COURSE = State()
    REITING = State()

class Onboarding(StatesGroup):
    INFO_START = State()
    QUE_START = State()

    INFO_PERSONAL_ACCOUNT = State()
    QUE_PERSONAL_ACCOUNT = State()
    ANS_PC = State()

    INFO_MODEUS = State()
    QUE_MODEUS = State()
    ANS_MODEUS = State()

    INFO_IOT = State()
    QUE_IOT = State()

    QUE_IOT_DISC = State()
    QUE_IOT_CHIOSE = State()

    INFO_STUD_CARD = State()
    QUE_STUD_CARD = State()
    ANS_STUD_CARD = State()

    INFO_ELECTR_PASS = State()

    INFO_BANK_CARD = State()

    INFO_PROGECT = State()

    INFO_EXAM = State()
    QUE_EXAM = State()

    INFO_RATNG = State()
    QUE_RATING = State()

    END = State()