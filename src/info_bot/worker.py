import asyncio
import logging
from sys import exit
import aiohttp
from schemas import FAQ, FAQTopic, OnboardCourse, OnboardTopic

_log = logging.getLogger(__name__)


class ManegerOnboarding():
    def __init__(self):
        self.__data: list[OnboardCourse] = []
        self.__index_is_main = None

    @property
    def onboarding(self) -> OnboardCourse:
        index = self.get_index_onboarding()
        return self.__data[index]

    def is_active_main(self) -> bool:
        return self.__index_is_main != None

    def is_active_add_course(self) -> bool:
        if len(self.__data) > 0 and self.__index_is_main == None or len(self.__data) > 1 and self.__index_is_main != None:
            return True
        return False

    def get_additional_courses(self) -> list[tuple[int, str, int]]:
        list = []
        for i in range(len(self.__data)):
            if i != self.__index_is_main:
                list.append(
                    (i, self.__data[i].name, len(self.__data[i].sections)))
        return list

    def get_index_onboarding(self) -> int:
        return self.__index_is_main

    def get_info_course(self, index: int) -> OnboardCourse:
        return self.__data[index]

    def get_info_course_topic(self, index, callback_data_topic) -> OnboardTopic | None:
        course = self.get_info_course(index)
        split_callback = callback_data_topic.split("__")
        index = int(split_callback[-1])
        callback_data_section = "__".join(split_callback[:-1])

        for section in course.sections:
            if section.callback_data == callback_data_section:
                return section.topics[index]
        return None

    def update_data(self, data: list[dict]):
        self.__data: list[OnboardCourse] = []
        i = 0
        for course in data:
            course_onboard = OnboardCourse(**course)
            if course_onboard.is_main == True:
                self.__index_is_main = i
            self.__data.append(course_onboard)
            i += 1


manager_onboarding = ManegerOnboarding()


class ManagerFaq():
    def __init__(self):
        self.__data: list[FAQTopic] = []

    def update_data(self, data: list[dict]):
        self.__data: list[FAQTopic] = []
        for t in data:
            self.__data.append(FAQTopic(**t))

    def get_all(self, id: str) -> FAQTopic | None:
        for t in self.__data:
            if t.id == id:
                return t
        return None

    def get_list_topics(self) -> list[FAQTopic]:
        return self.__data


manager_faq = ManagerFaq()


class Worker:
    def __init__(self, time_sleep, cookie: str):
        self.__time_sleep = time_sleep
        self.manager_onboarding = None
        self.cookie = cookie
        self.count_error_connect = 0

    def add_manager_onboarding(self, manager: ManegerOnboarding, url_update: str):
        self.manager_onboarding = manager
        self.url_update_onb = url_update

    def add_manager_faq(self, manager: ManagerFaq, url_update_data: str):
        self.manager_faq = manager
        self.url_update_faq = url_update_data

    async def work(self):
        if self.manager_onboarding == None:
            _log.error("Manager not found")
            raise Exception("Manager not found")

        while True:
            try:
                await asyncio.sleep(self.__time_sleep)

                await self.__update_onboarding_info()
                await self.__update_faq_info()

                if self.count_error_connect != 0:
                    self.count_error_connect = 0
            except Exception as e:
                # self.count_error_connect += 1

                # if self.count_error_connect >= 5:
                #     _log.error("Exit")
                #     exit()

                _log.error(e)

    async def __update_onboarding_info(self):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Basic {self.cookie}"}
            async with session.get(f"{self.url_update_onb}?is_active=true", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.manager_onboarding.update_data(data)
                else:
                    _log.error(f"Error update data {response.status}")

    async def __update_faq_info(self):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Basic {self.cookie}"}
            async with session.get(f"{self.url_update_faq}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.manager_faq.update_data(data)
                else:
                    _log.error(
                        f"Error update faq data {response.status}")
