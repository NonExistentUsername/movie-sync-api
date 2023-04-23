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

    def join(self, user_id: int) -> bool:
        raise NotImplementedError()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Room):
            return self.id == __value.id

        return False
