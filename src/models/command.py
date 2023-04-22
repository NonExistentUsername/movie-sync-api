import datetime

from db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    command = Column(String(64), nullable=False)
    param = Column(String(256), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
