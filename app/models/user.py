from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.associations import user_room_member_association_table
from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    have_access = Column(Boolean, nullable=False, default=False)
    member_of_rooms = relationship(
        "Room", secondary=user_room_member_association_table, back_populates='members_of_room')
