from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime

from db.base_class import Base


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    command = Column(String(64), nullable=False)
    param = Column(String(256), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)


