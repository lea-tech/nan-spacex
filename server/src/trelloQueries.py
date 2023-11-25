import json
import requests


class BoardNotExist(Exception):
    """
    Exception raised for Invalid Board Name

    Attributes:
        message
    """

    def __init__(
        self,
        value: str,
        message: str = "BoardNotExist: the board name doesn't exist",
    ):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Value: {self.value} - {self.message}"


class ListNotExist(Exception):
    """
    Exception raised for Invalid List Name

    Attributes:
        message
    """

    def __init__(
        self,
        value: str,
        message: str = "ListNotExist: the list name doesn't exist",
    ):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Value: {self.value} - {self.message}"


class LabelNotExist(Exception):
    """
    Exception raised for Invalid Label Name

    Attributes:
        message
    """

    def __init__(
        self,
        value: str,
        message: str = "LabelNotExist: the label name doesn't exist",
    ):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Value: {self.value} - {self.message}"


class TrelloQueries(BoardNotExist, ListNotExist, LabelNotExist):
    def __init__(self, board_name: str = "") -> None:
        self.headers = {"Accept": "application/json"}
        self.__load_credentials()
        self.set_board_id(board_name=board_name)

    def __load_credentials(self, dir: str = "./cnf/credentials.json") -> None:
        with open(dir, "r") as f:
            self.__credentials = json.loads(f.read())

    def set_board_id(self, board_name: str) -> bool:
        url = "https://api.trello.com/1/members/me/boards?"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        for board in list(json.loads(response.text)):
            if board["name"] == board_name:
                self.board_id = board["id"]
                return True
        raise BoardNotExist(value=board_name)

    def get_all_lists(self) -> list:
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        return list(json.loads(response.text))

    def get_list_id(self, list_name: str) -> str:
        for li in self.get_all_lists():
            if li["name"].lower() == list_name.lower():
                return li["id"]
        raise ListNotExist(value=list_name)

    def get_all_members(self) -> list:
        url = f"https://api.trello.com/1/boards/{self.board_id}/members"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        return list(json.loads(response.text))

    def get_all_labels(self) -> list:
        url = f"https://api.trello.com/1/boards/{self.board_id}/labels"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        return list(json.loads(response.text))

    def get_label_id(self, label_name) -> str:
        for label in self.get_all_labels():
            if label["name"].lower() == label_name:
                return label["id"]
        raise LabelNotExist(value=label_name)

    def get_all_cards(self) -> list:
        url = f"https://api.trello.com/1/boards/{self.board_id}/cards"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        return list(json.loads(response.text))

    def get_a_card_by_id(self, card_id) -> list:
        url = f"https://api.trello.com/1/cards/{card_id}"
        response = requests.request(
            "GET", url, headers=self.headers, params=self.__credentials
        )
        if response.text == "invalid id":
            return []
        return list(json.loads(response.text))

    def delete_card_by_id(self, card_id) -> None:
        url = f"https://api.trello.com/1/cards/{card_id}"
        requests.request("DELETE", url, params=self.__credentials)

    def add_task_to_list(
        self, list_id: str, name: str, desc=False, members=False, labels=False
    ) -> dict:
        url = "https://api.trello.com/1/cards"
        query = {
            "key": self.__credentials["key"],
            "token": self.__credentials["token"],
            "idList": list_id,
            "name": name,
        }
        if desc:
            query["desc"] = desc
        if members:
            query["idMembers"] = members
        if labels:
            query["idLabels"] = labels
        response = requests.request("POST", url, headers=self.headers, params=query)
        return dict(json.loads(response.text))
