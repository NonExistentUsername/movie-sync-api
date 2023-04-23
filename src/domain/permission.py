import typing as t
from enum import Enum


class Permissions(Enum):
    pass


class PermissionsGroup:
    def __init__(self, id: int, name: str, permissions: t.Set[Permissions]) -> None:
        self._id = id
        self.name = name
        self.permissions = permissions

    @property
    def id(self) -> int:
        return self._id
