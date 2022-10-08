import requests
import os
from enum import Enum
from datetime import datetime, timedelta
import json
import jwt
from typing import Optional, List


class Config:
    # API_URL: str = "https://private-web-service.onrender.com/"
    TIMEOUT = 10
    API_URL: str = "http://127.0.0.1:8000/"
    DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

    PATHS: dict = {
        "register": "auth/register",
        "login": "auth/login",
        "get_me": "auth/me",
        "get_users": "users",
        "get_user": "users/user",
        "update_rights": "users/update_user",
        "get_commands": "app/get_commands",
        "send_command": "app/send_command",
        "delete_commands": "app/delete_commands",
        "app_last_update": "app/last_update",
        "app_download": "app/download",
    }


class ApiStatus(Enum):
    OK = 1,
    ERROR = 2,


class ApiException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.__message = message

    @property
    def message(self) -> str:
        return self.__message


class User:
    def __init__(self, user_id: int, nickname: str, is_admin: bool, receives_commands: bool):
        self.__user_id = user_id
        self.__nickname = nickname
        self.__is_admin = is_admin
        self.__receives_commands = receives_commands

    @property
    def id(self) -> int:
        return self.__user_id

    @property
    def nickname(self) -> str:
        return self.__nickname

    @property
    def is_admin(self) -> bool:
        return self.__is_admin

    @property
    def receives_commands(self) -> bool:
        return self.__receives_commands


class Command:
    def __init__(self, command_id: int, command: str, param: str, sender_id: int, create_date: datetime):
        self.__command_id = command_id
        self.__command = command
        self.__param = param
        self.__sender_id = sender_id
        self.__create_date = create_date

    @property
    def id(self) -> int:
        return self.__command_id

    @property
    def command(self) -> str:
        return self.__command

    @property
    def param(self) -> Optional[str]:
        return self.__param

    @property
    def sender_id(self) -> int:
        return self.__sender_id

    @property
    def create_date(self) -> datetime:
        return self.__create_date


class Page:
    def __init__(self, items: list, total: int, page: int, size: int, get_page_func=None):
        self.__items = items
        self.__total = total
        self.__page = page
        self.__size = size
        self.__get_page_func = get_page_func

    @property
    def items(self) -> list:
        return self.__items

    @property
    def total(self) -> int:
        return self.__total

    @property
    def page(self) -> int:
        return self.__page

    @property
    def size(self) -> int:
        return self.__size

    def previous(self):
        if self.__page > 1 and self.__get_page_func:
            return self.__get_page_func(self.__page - 1, self.__size)
        return None

    def next(self):
        if self.__get_page_func:
            return self.__get_page_func(self.__page + 1, self.__size)
        return None


class Api:
    @classmethod
    def _get_path(cls, path: str):
        if path in Config.PATHS:
            return os.path.join(Config.API_URL, Config.PATHS[path])
        return ""

    @classmethod
    def _get_datetime(cls, date: str):
        try:
            return datetime.strptime(date, Config.DATE_FORMAT)
        except:
            return datetime.strptime(date, Config.DATE_FORMAT + '.%f')

    @classmethod
    def _json_result_from_response(cls, response):
        if response.status_code in [200, 201]:
            return response.json()
        else:
            message = response.text
            try:
                message = response.json()["detail"]
            except:
                pass
            raise ApiException(message)

    @classmethod
    def _command_object_from_json(cls, data) -> Command:
        return Command(data["id"], data["command"], data["param"], data["sender_id"],
                       Api._get_datetime(data["create_date"]))

    @classmethod
    def _page_object_from_json(cls, data, get_page_func=None) -> Page:
        return Page(data["items"], data["total"], data["page"], data["size"], get_page_func)

    @classmethod
    def _user_object_from_json(cls, data) -> User:
        return User(data["id"], data["nickname"], data["is_admin"], data["receives_commands"])

    @classmethod
    def _page_of_commands_from_json(cls, data, get_page_func=None) -> Page:
        old_items = data["items"]
        new_items = []
        for item in old_items:
            new_items.append(Api._command_object_from_json(item))
        data["items"] = new_items
        return Api._page_object_from_json(data, get_page_func)

    @classmethod
    def register(cls, nickname: str, password: str) -> User:
        request_body = {
            "nickname": nickname,
            "password": password,
        }

        response = requests.post(Api._get_path("register"), json=request_body)
        result = Api._json_result_from_response(response)
        return Api._user_object_from_json(result)

    @classmethod
    def login(cls, nickname: str, password: str):
        request_body = {
            "nickname": nickname,
            "password": password,
        }

        response = requests.post(Api._get_path("login"), json=request_body)
        return Api._json_result_from_response(response)

    @classmethod
    def get_me(cls, authorization: str) -> User:
        headers = {
            "Authorization": authorization
        }
        response = requests.get(Api._get_path("get_me"), headers=headers)
        result = Api._json_result_from_response(response)
        return Api._user_object_from_json(result)

    @classmethod
    def send_command(cls, authorization: str, command: str, param: Optional[str] = None) -> Command:
        headers = {
            "Authorization": authorization
        }
        request_json = {
            "command": command
        }
        if param is not None:
            request_json["param"] = param
        response = requests.post(Api._get_path("send_command"), headers=headers, json=request_json)
        return Api._command_object_from_json(Api._json_result_from_response(response))

    @classmethod
    def ws_get_commands(cls, authorization: str):
        pass

    @classmethod
    def get_commands(cls, authorization: str, page: int = 1, size: int = 50) -> Page:
        headers = {
            "Authorization": authorization
        }
        params = {
            "page": page,
            "size": size,
        }
        response = requests.get(Api._get_path("get_commands"), headers=headers, params=params)
        result = Api._json_result_from_response(response)
        return Api._page_of_commands_from_json(result)

    @classmethod
    def delete_commands(cls, authorization: str, commands: List[int]):
        headers = {
            "Authorization": authorization
        }
        request_body = {
            "commands": commands
        }
        response = requests.delete(Api._get_path("delete_commands"), headers=headers, json=request_body)
        return Api._json_result_from_response(response)

    @classmethod
    def get_last_update(cls, authorization: str):
        headers = {
            "Authorization": authorization
        }
        response = requests.get(Api._get_path("app_last_update"), headers=headers)
        result = Api._json_result_from_response(response)
        return Api._get_datetime(result["last_update"])

    @classmethod
    def download_app(cls, authorization: str) -> str:
        headers = {
            "Authorization": authorization
        }
        response = requests.get(Api._get_path("app_download"), headers=headers)
        return response.text

    @classmethod
    def update_rights(cls, authorization: str, nickname: str,
                      is_admin: Optional[bool] = None, receives_commands: Optional[bool] = None):
        headers = {
            "Authorization": authorization
        }
        request_json = {
            "nickname": nickname
        }
        if is_admin is not None:
            request_json["is_admin"] = is_admin
        if receives_commands is not None:
            request_json["receives_commands"] = receives_commands
        response = requests.post(Api._get_path("update_rights"), headers=headers, json=request_json)
        return Api._user_object_from_json(Api._json_result_from_response(response))

    @classmethod
    def get_user(cls, authorization: str, nickname: str):
        headers = {
            "Authorization": authorization
        }
        params = {
            "nickname": nickname
        }
        response = requests.get(Api._get_path("get_user"), headers=headers, params=params)
        return Api._user_object_from_json(Api._json_result_from_response(response))


class Client:
    def __apply_authorization_token(self, data):
        if "access_token" not in data:
            return
        if "token_type" not in data:
            raise Exception(f'Token type unknown.')
        if data["token_type"] != 'bearer':
            raise Exception(f'Token type {data["token_type"]} does\'t supported.')

        decoded = jwt.decode(data["access_token"], options={"verify_signature": False})
        exp = datetime.fromtimestamp(decoded["exp"])
        if datetime.now() < exp:
            self.__authorization = "Bearer " + data["access_token"]

    def __try_load_authorization_token(self):
        if os.path.isfile("config.json"):
            data = {}
            with open("config.json", "r") as file:
                try:
                    data = json.loads(file.read())
                except:
                    pass
            self.__apply_authorization_token(data)

    def __try_get_last_update(self):
        if os.path.isfile("app.py"):
            time = os.path.getmtime("app.py")

            self.__last_update = datetime.fromtimestamp(time) - (datetime.now() - datetime.utcnow())

    def __save_authorization_token(self, data):
        with open("config.json", "w") as file:
            json.dump(data, file)
        self.__apply_authorization_token(data)

    def __init__(self):
        self.__authorization = None
        self.__me = None
        self.__last_update = None

    def init(self) -> None:
        self.__try_load_authorization_token()
        self.__try_get_last_update()

    @property
    def is_authorized(self) -> bool:
        return self.__authorization is not None

    @property
    def me(self) -> User:
        if not self.__me:
            self.__me = Api.get_me(self.__authorization)
        return self.__me

    def register(self, nickname: str, password: str) -> User:
        result = Api.register(nickname, password)
        access = Api.login(nickname, password)
        self.__save_authorization_token(access)
        return result

    def login(self, nickname: str, password: str) -> User:
        access = Api.login(nickname, password)
        self.__save_authorization_token(access)
        return self.me

    @property
    def have_update(self) -> bool:
        if not self.__last_update:
            return True
        result = Api.get_last_update(self.__authorization)
        return result > self.__last_update

    def download_app(self) -> None:
        content = Api.download_app(self.__authorization)
        with open("app.py", "w+") as file:
            file.write(content)

    def get_commands(self) -> List[Command]:
        result = Api.get_commands(self.__authorization, page=1, size=100)
        commands = result.items
        commands_to_remove = []
        for command in commands:
            commands_to_remove.append(command.id)
        Api.delete_commands(self.__authorization, commands_to_remove)
        return commands

    def get_user(self, nickname: str) -> User:
        return Api.get_user(self.__authorization, nickname)

    def update_rights(self, nickname: str,
                      is_admin: Optional[bool] = None, receives_commands: Optional[bool] = None) -> User:
        return Api.update_rights(self.__authorization, nickname, is_admin, receives_commands)

    def send_command(self, command: str, param: Optional[str] = None) -> Command:
        return Api.send_command(self.__authorization, command, param)

