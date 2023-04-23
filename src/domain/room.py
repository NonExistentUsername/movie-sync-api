import typing as t


class Room:
    def __init__(self, id: int, name: str, key: str, creator_id: int, capacity: int) -> None:
        self._id = id
        self.name = name
        self.key = key
        self.creator_id = creator_id
        self.capacity = capacity

    @property
    def id(self) -> int:
        return self._id

    @property
    def members_of_room(self) -> t.List:
        raise NotImplementedError()
