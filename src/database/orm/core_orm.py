from database.orm.orm_item import BaseItemOrm, ItemOrm


class CoreOrm:
    def __init__(self) -> None:
        self.base = BaseItemOrm()
