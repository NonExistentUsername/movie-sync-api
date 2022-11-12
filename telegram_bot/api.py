import json

import requests
import os
from enum import Enum
from datetime import datetime
import websockets
import jwt
from typing import Optional, List


class Config:
    API_URL: str = "http://web-api:8000/"
    WS_API_URL: str = "ws://web-api:8000/"
    TIMEOUT = 10
    DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

    PATHS: dict = {
        # AUTH
        "register": "auth/register",
        "login": "auth/login",
        "get_me": "auth/me",

        # USERS
        "get_users": "users",
        "get_user": "users/user",
        "update_rights": "users/update_user",

        # ROOMS
        "get_rooms": "rooms",
        "get_room": "rooms/room",
        "create_room": "rooms/create/",
        "join_room": "rooms/join",
        "leave_room": "rooms/leave",
        "delete_room": "rooms/delete",
        "kick_member": "rooms/kick_member",

        # COMMANDS
        "send_command": "commands/send",
        "ws_get_commands": "commands/ws/get_commands",
        "delete_commands": "commands/delete_commands",

        # APP
        "get_last_update_app": "app/last_update",
        "download_app": "app/download",
    }


class ApiStatus(Enum):
    OK = 1,
    ERROR = 2,


class ApiException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.__message = message

    def __str__(self):
        return self.__message

    @property
    def message(self) -> str:
        return self.__message


class OldTokenApiException(ApiException):
    def __init__(self, message: str):
        super().__init__(message)


class Authorization(object):
    def __init__(self, token: str, token_type: str):
        self.__token = token
        self.__token_type = token_type

    def asdict(self) -> dict:
        return {"token": self.__token, "token_type": self.__token_type}

    @property
    def token(self) -> str:
        return self.__token

    @property
    def token_type(self) -> str:
        return self.__token_type


class User:
    def __init__(self, user_id: int, username: str, is_admin: bool, have_access: bool):
        self.__user_id = user_id
        self.__username = username
        self.__is_admin = is_admin
        self.__have_access = have_access

    @property
    def id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def is_admin(self) -> bool:
        return self.__is_admin

    @property
    def have_access(self) -> bool:
        return self.__have_access


class DeletedCommands:
    def __init__(self, commands: List[int]):
        self.__commands = commands

    @property
    def commands(self) -> List[int]:
        return self.__commands


class RoomMember:
    def __init__(self, user_id: int, username: str):
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username


class Room:
    def __init__(self, room_id: int, name: str, key: str, creator_id: int, members_of_room: List[RoomMember]):
        self.__room_id = room_id
        self.__name = name
        self.__key = key
        self.__creator_id = creator_id
        self.__members_of_room = members_of_room

    @property
    def room_id(self) -> int:
        return self.__room_id

    @property
    def room_name(self) -> str:
        return self.__name

    @property
    def key(self) -> str:
        return self.__key

    @property
    def creator_id(self) -> int:
        return self.__creator_id

    @property
    def members_of_room(self) -> List[RoomMember]:
        return self.__members_of_room


class Command:
    def __init__(self,
                 command_id: int,
                 command: str,
                 param: str,
                 sender_id: int,
                 room_id: int,
                 create_date: datetime):
        self.__command_id = command_id
        self.__command = command
        self.__param = param
        self.__sender_id = sender_id
        self.__room_id = room_id
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
    def room_id(self) -> int:
        return self.__room_id

    @property
    def create_date(self) -> datetime:
        return self.__create_date


class CommandCreated:
    def __init__(self,
                 command: str,
                 param: str,
                 sender_id: int,
                 room_id: int,
                 create_date: datetime):
        self.__command = command
        self.__param = param
        self.__sender_id = sender_id
        self.__room_id = room_id
        self.__create_date = create_date

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
    def room_id(self) -> int:
        return self.__room_id

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
    def verify_authorization(cls, authorization: Authorization) -> bool:
        if not authorization.token_type.lower() == 'bearer':
            raise ApiException(f'Token type {authorization.token_type} does\'t supported.')

        decoded = jwt.decode(authorization.token, options={"verify_signature": False})
        exp = datetime.fromtimestamp(decoded["exp"])
        if datetime.now() > exp:
            raise OldTokenApiException('Old token.')

        return True

    @classmethod
    def make_authorization_headers(cls, authorization: Authorization) -> dict:
        if not Api.verify_authorization(authorization):
            return {}
        if authorization.token_type.lower() == 'bearer':
            return {
                "Authorization": 'Bearer ' + authorization.token
            }
        return {}

    @classmethod
    def _get_path(cls, path: str):
        if path in Config.PATHS:
            if path.startswith("ws"):
                return os.path.join(Config.WS_API_URL, Config.PATHS[path])
            return os.path.join(Config.API_URL, Config.PATHS[path])
        return ""

    @classmethod
    def _get_datetime(cls, date: str):
        try:
            return datetime.strptime(date, Config.DATE_FORMAT)
        except Exception as e:
            return datetime.strptime(date, Config.DATE_FORMAT + '.%f')

    @classmethod
    def _json_result_from_response(cls, response):
        if response.status_code in [200, 201]:
            return response.json()
        else:
            message = response.text
            try:
                message = str(response.json()["detail"])
            except Exception as e:
                pass
            raise ApiException(message)

    @classmethod
    def _command_object_from_json(cls, data) -> Command:
        print(data)
        return Command(command_id=data["id"],
                       command=data["command"],
                       param=data["param"],
                       sender_id=data["sender_id"],
                       room_id=data["room_id"],
                       create_date=Api._get_datetime(data["create_date"]))

    @classmethod
    def _command_created_object_from_json(cls, data) -> CommandCreated:
        return CommandCreated(command=data["command"],
                              param=data["param"],
                              sender_id=data["sender_id"],
                              room_id=data["room_id"],
                              create_date=Api._get_datetime(data["create_date"]))

    @classmethod
    def _page_object_from_json(cls, data, get_page_func=None, convert_item_func=None) -> Page:
        if convert_item_func is None:
            return Page(data["items"], data["total"], data["page"], data["size"], get_page_func)
        else:
            old_items = data["items"]
            new_items = []
            for item in old_items:
                new_items.append(convert_item_func(item))
            data["items"] = new_items
            return Api._page_object_from_json(data, get_page_func)

    @classmethod
    def _authorization_from_json(cls, data: dict) -> Optional[Authorization]:
        if "token_type" not in data or "access_token" not in data:
            raise ApiException('Unknown authorization type.')

        authorization = Authorization(token=data["access_token"], token_type=data["token_type"])
        if Api.verify_authorization(authorization):
            return authorization
        return None

    @classmethod
    def _user_object_from_json(cls, data) -> User:
        return User(data["id"], data["username"], data["is_admin"], data["have_access"])

    @classmethod
    def _room_member_from_json(cls, data: dict) -> RoomMember:
        return RoomMember(data["id"], data["username"])

    @classmethod
    def _room_members_from_json(cls, data: list) -> List[RoomMember]:
        result = []
        for json_member in data:
            result.append(Api._room_member_from_json(json_member))
        return result

    @classmethod
    def _room_from_json(cls, data: dict) -> Room:
        return Room(data["id"],
                    data["name"],
                    data["key"],
                    data["creator_id"],
                    Api._room_members_from_json(data["members_of_room"]))

    @classmethod
    def _deleted_commands_from_json(cls, data: dict) -> DeletedCommands:
        return DeletedCommands(data["deleted_commands"])

####################################################################################
#       AUTH
####################################################################################
    @classmethod
    def register(cls, username: str, password: str) -> User:
        request_body = {
            "username": username,
            "password": password,
        }

        response = requests.post(Api._get_path("register"), json=request_body)
        result = Api._json_result_from_response(response)
        return Api._user_object_from_json(result)

    @classmethod
    def login(cls, username: str, password: str) -> Optional[Authorization]:
        request_body = {
            "username": username,
            "password": password,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(Api._get_path("login"), headers=headers, data=request_body)
        return Api._authorization_from_json(Api._json_result_from_response(response))

    @classmethod
    def get_me(cls, authorization: Authorization) -> User:
        headers = Api.make_authorization_headers(authorization)
        response = requests.get(Api._get_path("get_me"), headers=headers)
        result = Api._json_result_from_response(response)
        return Api._user_object_from_json(result)

####################################################################################
#       USERS
####################################################################################
    @classmethod
    def get_users(cls, authorization: Authorization, page: int = 1, size: int = 50) -> Page:
        headers = Api.make_authorization_headers(authorization)
        params = {
            "page": page,
            "size": size,
        }
        response = requests.get(Api._get_path("get_users"), headers=headers, params=params)
        return Api._page_object_from_json(Api._json_result_from_response(response),
                                          convert_item_func=Api._user_object_from_json)

    @classmethod
    def get_user(cls, authorization: Authorization, username: str) -> User:
        headers = Api.make_authorization_headers(authorization)
        params = {
            "username": username,
        }
        response = requests.get(Api._get_path("get_user"), headers=headers, params=params)
        return Api._user_object_from_json(Api._json_result_from_response(response))

    @classmethod
    def update_rights(cls, authorization: Authorization, username: str,
                      is_admin: Optional[bool] = None, have_access: Optional[bool] = None) -> User:
        headers = Api.make_authorization_headers(authorization)
        request_json = {
            "username": username,
        }
        if is_admin is not None:
            request_json["is_admin"] = is_admin
        if have_access is not None:
            request_json["have_access"] = have_access
        response = requests.post(Api._get_path("update_rights"), headers=headers, json=request_json)
        return Api._user_object_from_json(Api._json_result_from_response(response))

####################################################################################
#       ROOMS
####################################################################################
    @classmethod
    def get_rooms(cls, authorization: Authorization, page: int = 1, size: int = 50) -> Page:
        headers = Api.make_authorization_headers(authorization)
        params = {
            "page": page,
            "size": size,
        }
        response = requests.get(Api._get_path("get_rooms"), headers=headers, params=params)
        return Api._page_object_from_json(Api._json_result_from_response(response),
                                          convert_item_func=Api._room_from_json)

    @classmethod
    def get_room(cls, authorization: Authorization, name: str) -> Room:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'room_name': name,
        }
        response = requests.get(Api._get_path("get_room"), headers=headers, params=params)
        return Api._room_from_json(Api._json_result_from_response(response))

    @classmethod
    def create_room(cls, authorization: Authorization, name: str, capacity: int = 10) -> Room:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'room_name': name,
            'capacity': capacity,
        }
        response = requests.post(Api._get_path("create_room"), headers=headers, params=params)
        return Api._room_from_json(Api._json_result_from_response(response))

    @classmethod
    def join_room(cls, authorization: Authorization, name: str, key: str) -> bool:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'room_name': name,
            'room_key': key,
        }
        response = requests.post(Api._get_path("join_room"), headers=headers, params=params)
        result: dict = Api._json_result_from_response(response)
        return result["status"] == "OK"

    @classmethod
    def leave_room(cls, authorization: Authorization, name: str) -> bool:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'room_name': name,
        }
        response = requests.post(Api._get_path("leave_room"), headers=headers, params=params)
        result: dict = Api._json_result_from_response(response)
        return result["status"] == "OK"

    @classmethod
    def delete_room(cls, authorization: Authorization, name: str) -> bool:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'room_name': name,
        }
        response = requests.post(Api._get_path("delete_room"), headers=headers, params=params)
        result: dict = Api._json_result_from_response(response)
        return result["status"] == "OK"

    @classmethod
    def kick_member(cls, authorization: Authorization, username: str, room_name: str) -> bool:
        headers = Api.make_authorization_headers(authorization)
        params = {
            'username': username,
            'room_name': room_name,
        }
        response = requests.post(Api._get_path("kick_member"), headers=headers, params=params)
        result: dict = Api._json_result_from_response(response)
        return result["status"] == "OK"

####################################################################################
#       COMMANDS
####################################################################################
    @classmethod
    def send_command(cls,
                     authorization: Authorization,
                     room_name: str,
                     command: str,
                     param: Optional[str] = None) -> CommandCreated:
        headers = Api.make_authorization_headers(authorization)
        request_json = {
            "command": command,
            "room_name": room_name,
        }
        if param is not None:
            request_json["param"] = param
        response = requests.post(Api._get_path("send_command"), headers=headers, json=request_json)
        return Api._command_created_object_from_json(Api._json_result_from_response(response))

    @classmethod
    async def ws_get_command(cls, authorization: Authorization, callback_function) -> None:
        async with websockets.connect(Api._get_path("ws_get_commands") + f'?token={authorization.token}',
                                      timeout=5) as websocket:
            running_flag = True
            while running_flag:
                command = await websocket.recv()
                running_flag = callback_function(Api._command_object_from_json(json.loads(json.loads(command))))

    @classmethod
    def delete_commands(cls, authorization: Authorization, commands: List[int]) -> DeletedCommands:
        headers = Api.make_authorization_headers(authorization)
        request_body = {
            "commands": commands
        }
        response = requests.delete(Api._get_path("delete_commands"), headers=headers, json=request_body)
        return Api._deleted_commands_from_json(Api._json_result_from_response(response))

####################################################################################
#       APPLICATION
####################################################################################
    @classmethod
    def get_last_update_app(cls, authorization: Authorization):
        headers = Api.make_authorization_headers(authorization)
        response = requests.get(Api._get_path("get_last_update_app"), headers=headers)
        result = Api._json_result_from_response(response)
        return Api._get_datetime(result["last_update"])

    @classmethod
    def download_app(cls, authorization: Authorization) -> str:
        headers = Api.make_authorization_headers(authorization)
        response = requests.get(Api._get_path("download_app"), headers=headers)
        return response.text


class Client:
    def __try_verify_authorization(self, authorization: Authorization) -> bool:
        try:
            return Api.verify_authorization(authorization)
        except ApiException as e:
            return False

    def __try_login(self, username: str, password: str) -> Optional[Authorization]:
        try:
            return Api.login(username, password)
        except ApiException as e:
            return None

    def __init__(self,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 authorization: Optional[Authorization] = None):
        self.__authorization: Optional[Authorization] = None

        if authorization is not None and self.__try_verify_authorization(authorization):
            self.__authorization = authorization
        elif username is not None and password is not None:
            self.__authorization = self.__try_login(username, password)

    @property
    def is_authorized(self) -> bool:
        if self.__authorization:
            return self.__try_verify_authorization(self.__authorization)
        return False

    @property
    def authorization(self) -> Optional[Authorization]:
        if self.__authorization is not None and not self.__try_verify_authorization(self.__authorization):
            self.__authorization = None
        return self.__authorization

    def register(self, username: str, password: str) -> User:
        result = Api.register(username, password)
        self.__authorization = Api.login(username, password)
        return result

    def login(self, username: str, password: str) -> None:
        self.__authorization = Api.login(username, password)

    def logout(self) -> bool:
        if self.__authorization:
            self.__authorization = None
            return True
        return False

    @property
    def me(self) -> User:
        return Api.get_me(self.__authorization)

    def get_users(self, page: int = 1, size: int = 50) -> Page:
        return Api.get_users(self.__authorization, page, size)

    def get_user(self, username: str) -> User:
        return Api.get_user(self.__authorization, username)

    def update_rights(self,
                      username: str,
                      is_admin: Optional[bool] = None,
                      have_access: Optional[bool] = None) -> User:
        return Api.update_rights(self.__authorization, username, is_admin, have_access)

    def get_last_update(self) -> datetime:
        return Api.get_last_update_app(self.__authorization)

    def get_rooms(self, page: int = 1, size: int = 50) -> Page:
        return Api.get_rooms(self.__authorization, page, size)

    def get_room(self, name: str) -> Room:
        return Api.get_room(self.__authorization, name)

    def create_room(self, name: str, capacity: int = 10) -> Room:
        return Api.create_room(self.__authorization, name, capacity)

    def join_room(self, name: str, key: str) -> bool:
        return Api.join_room(self.__authorization, name, key)

    def leave_room(self, name: str) -> bool:
        return Api.leave_room(self.__authorization, name)

    def delete_room(self, name: str) -> bool:
        return Api.delete_room(self.__authorization, name)

    def kick_member(self, room_name: str, username: str) -> bool:
        return Api.kick_member(self.__authorization, room_name, username)

    def send_command(self, room_name: str, command: str, param: Optional[str] = None) -> CommandCreated:
        return Api.send_command(self.__authorization, room_name, command, param)

    def __auto_delete_commands_callback_function_decorator(self, callback_function):
        def auto_delete_commands_callback_function(command: Command):
            callback_function(command)
            Api.delete_commands(self.__authorization, [command.id])
        return auto_delete_commands_callback_function

    async def ws_get_command(self, callback_function) -> None:
        await Api.ws_get_command(self.__authorization,
                                 self.__auto_delete_commands_callback_function_decorator(callback_function))

    def delete_commands(self, commands: List[int]) -> DeletedCommands:
        return Api.delete_commands(self.__authorization, commands)

    def get_last_update_app(self) -> datetime:
        return Api.get_last_update_app(self.__authorization)

    def download_app(self):
        return Api.download_app(self.__authorization)
