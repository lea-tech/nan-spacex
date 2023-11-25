import json

from os import environ, path

APP_PORT = int(environ.get("APP_PORT", 8000))
APP_VERSION = str(environ.get("APP_VERSION", "0.1"))

BOARD_NAME = "generic"
if path.exists("./cnf/trello_config.json"):
    with open("./cnf/trello_config.json", "r") as f:
        BOARD_NAME = json.loads(f.read())["board_name"]
