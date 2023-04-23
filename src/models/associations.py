from sqlalchemy import Column, ForeignKey, Table

from db.base_class import Base

user_room_member_association_table = Table(
    "user_room_member_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("room_id", ForeignKey("rooms.id"), primary_key=True),
)
