import typing as t


class User:
    def __init__(self, id: int, username: str, hashes_password: str, is_admin: bool, have_access: bool):
        self._id = id
        self.username = username
        self.hashes_password = hashes_password
        self.is_admin = is_admin
        self.have_access = have_access

    @property
    def id(self) -> int:
        return self._id

    @property
    def member_of_rooms(self) -> t.List:
        raise NotImplementedError()
