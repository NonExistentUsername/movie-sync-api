import datetime
import random
import string

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from models.associations import user_room_member_association_table


def gen_key(key_len: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=key_len))


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False, unique=True)
    key = Column(String(8), nullable=False, default=gen_key)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    members_of_room = relationship(
        "User",
        secondary=user_room_member_association_table,
        back_populates="member_of_rooms",
    )
    capacity = Column(Integer, default=10)
    # create_date = Column(DateTime, default=datetime.datetime.utcnow)
