import typing as t
from dataclasses import dataclass

from domain.permission import PermissionsGroup


class User:
    def __init__(self, id: int, username: str, hashes_password: str, permissions: PermissionsGroup, rooms: t.Set[int]):
        self._id = id
        self.username = username
        self.hashes_password = hashes_password
        self.permissions = permissions
        self._rooms = rooms

    @property
    def id(self) -> int:
        return self._id

    @property
    def rooms(self) -> t.Set[int]:
        return self._rooms

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, User):
            return self.id == __value.id

        return False
