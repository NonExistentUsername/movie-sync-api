from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from models.associations import user_room_member_association_table

from db.base_class import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    members_of_room = relationship("User", secondary=user_room_member_association_table)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)


