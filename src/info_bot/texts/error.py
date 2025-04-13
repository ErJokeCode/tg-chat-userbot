class Registration():
    def no() -> str:
        return "Вы не зарегистрированы. Пожалуйста, введите вашу почту и номер студенческого билета. Для повторного входа используйте команду /start"
    
class Input():
    def incorrect() -> str:
        return "Мне непонятен текст))"
    


class UserAlreadyRegistered(Exception):
    def __init__(self):
        super().__init__("Пользователь уже зарегистрирован")


class ErrorAuth(Exception):
    def __init__(self):
        super().__init__("Ошибка регистрации")

    
class NotValueForAuth(Exception):
    def __init__(self):
        super().__init__("Не хватает данных")
    