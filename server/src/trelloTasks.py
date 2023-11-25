import requests

from abc import ABC, abstractmethod
from random import randint

from src.settings import BOARD_NAME
from src.trelloQueries import TrelloQueries


class TaskTypeNotFound(Exception):
    """
    Exception raised for Invalid Task Type

    Attributes:
        message
    """

    def __init__(
        self,
        value: str,
        valid_tasks: list,
        message: str = "TaskTypeNotFound: only ",
    ):
        self.value = value
        self.valid_tasks = valid_tasks
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Value: {self.value} - {self.message} {self.valid_tasks}"


class NotValidCategory(Exception):
    """
    Exception raised for Invalid Category

    Attributes:
        message
    """

    def __init__(
        self,
        value: str,
        valid_categories: list,
        message: str = "NotValidCategory: admited categories are only",
    ):
        self.value = value
        self.message = message
        self.valid_categories = valid_categories
        super().__init__(self.message)

    def __str__(self):
        return f"Value: {self.value} - {self.message} {self.valid_categories}"


class BaseTask(ABC):
    @abstractmethod
    def create_task(self):
        pass


class FactoryTask(TaskTypeNotFound):
    def __init__(self, value: str = None, valid_tasks: list = None):
        super().__init__(value, valid_tasks)

    def build_task(self, data: dict):
        valid_tasks = ["issue", "bug", "task"]
        if data["type"].lower() == valid_tasks[0]:
            return Issue(title=data["title"], description=data["description"])
        elif data["type"].lower() == valid_tasks[1]:
            return Bug(description=data["description"])
        elif data["type"].lower() == valid_tasks[2]:
            return Task(title=data["title"], category=data["category"])
        else:
            raise TaskTypeNotFound(value=data["type"], valid_tasks=valid_tasks)


class Issue(BaseTask):
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    def create_task(self) -> dict:
        query_trello = TrelloQueries(BOARD_NAME)
        return query_trello.add_task_to_list(
            list_id=query_trello.get_list_id("ToDo"),
            name=self.title,
            desc=self.description,
        )


class Bug(BaseTask):
    def __init__(self, description: str) -> None:
        self.description = description
        self.__set_random_title()

    def __set_random_title(self) -> None:
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        self.title = f"bug-{response.content.splitlines()[randint(0, 9999)].decode()}-{randint(0, 9999)}"

    def __get_random_member_id(self, members: list) -> str:
        return members[randint(0, len(members) - 1)]["id"]

    def create_task(self) -> dict:
        query_trello = TrelloQueries(BOARD_NAME)
        return query_trello.add_task_to_list(
            list_id=query_trello.get_list_id("ToDo"),
            name=self.title,
            desc=self.description,
            members=self.__get_random_member_id(members=query_trello.get_all_members()),
            labels=query_trello.get_label_id("bug"),
        )


class Task(BaseTask, NotValidCategory):
    def __init__(self, title: str, category: str) -> None:
        valid_categories = ["Maintenance", "Research", "Test"]
        if category in valid_categories:
            self.category = category
        else:
            raise NotValidCategory(value=category, valid_categories=valid_categories)
        self.title = title

    def create_task(self) -> dict:
        query_trello = TrelloQueries(BOARD_NAME)
        return query_trello.add_task_to_list(
            list_id=query_trello.get_list_id("ToDo"),
            name=self.title,
            labels=query_trello.get_label_id(self.category.lower()),
        )
