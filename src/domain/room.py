import typing as t


class Room:
    def __init__(self, id: int, name: str, key: str, creator_id: int, capacity: int, members: t.Set[int]) -> None:
        self._id = id
        self.name = name
        self.key = key
        self.creator_id = creator_id
        self._capacity = capacity
        self._members = members

    @property
    def id(self) -> int:
        return self._id

    @property
    def members(self) -> t.Set[int]:
        return self._members

    @property
    def capacity(self) -> int:
        return self._capacity

    def join(self, user_id: int) -> None:
        if user_id in self._members:
            raise ValueError("The user is already in the room")

        if len(self._members) == self.capacity:
            raise ValueError("The room is full")

        self._members.add(user_id)

    def leave(self, user_id: int) -> None:
        if user_id not in self._members:
            raise ValueError("User not in the room")

        self._members.remove(user_id)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Room):
            return self.id == __value.id

        return False
