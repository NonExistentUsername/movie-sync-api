import typing as t
from dataclasses import dataclass

from domain.permission import PermissionsGroup


class User:
    def __init__(self, id: int, username: str, hashes_password: str, permissions: PermissionsGroup):
        self._id = id
        self.username = username
        self.hashes_password = hashes_password
        self.permissions = permissions

    @property
    def id(self) -> int:
        return self._id

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, User):
            return self.id == __value.id

        return False
