import pytest
import json

from src.trelloTasks import FactoryTask, TaskTypeNotFound, NotValidCategory
from src.trelloQueries import TrelloQueries
from src.settings import BOARD_NAME
from src import app


@pytest.mark.parametrize(
    "req_data",
    [
        {
            "type": "issue",
            "title": "An Issue",
            "description": "I'm an issue",
        },
        {
            "type": "bug",
            "description": "I'm a bug",
        },
        {
            "type": "task",
            "title": "A Maintenance Task",
            "category": "Maintenance",
        },
        {
            "type": "task",
            "title": "A Research Task",
            "category": "Research",
        },
        {
            "type": "task",
            "title": "A Test Task",
            "category": "Test",
        },
    ],
)
def test_happy_inputs(req_data: dict):
    task = FactoryTask()
    task = task.build_task(data=req_data)
    card = task.create_task()
    query = TrelloQueries(board_name=BOARD_NAME)
    valid_card = len(query.get_a_card_by_id(card["id"]))
    query.delete_card_by_id(card["id"])

    assert valid_card > 0


@pytest.mark.parametrize(
    "req_data",
    [
        {
            "type": "sandwich",
            "title": "Continental Roll",
            "description": "I'm just hungry",
        },
    ],
)
def test_invalid_type_exception(req_data: dict):
    task = FactoryTask()
    try:
        task = task.build_task(data=req_data)
    except Exception as err:
        assert type(err) == type(TaskTypeNotFound("", ""))


@pytest.mark.parametrize(
    "req_data",
    [
        {
            "type": "task",
            "title": "A managing Task",
            "category": "Manage",
        },
    ],
)
def test_invalid_category_exception(req_data: dict):
    task = FactoryTask()
    try:
        task = task.build_task(data=req_data)
    except Exception as err:
        print(type(err))
        print(type(NotValidCategory("", "")))
        assert type(err) == type(NotValidCategory("", ""))



def test_app_status():
    response = app.test_client().get("v1/status")

    assert response.status_code == 200
    assert json.loads(response.text) == {"message":"Nan/SpaceX Challenge is working","status_code":200,"version":"0.1"}


@pytest.mark.parametrize(
    "req_data",
    [
        {
            "type": "issue",
            "title": "An Issue",
            "description": "I'm an issue",
        }
    ],
)
def test_app_happy_inputs(req_data: dict):
    response = app.test_client().post("/v1/create-task", json=req_data)
    card = dict(json.loads(response.text))
    query = TrelloQueries(board_name=BOARD_NAME)
    valid_card = len(query.get_a_card_by_id(card["id"]))
    query.delete_card_by_id(card["id"])

    assert response.status_code == 200
    assert valid_card > 0

