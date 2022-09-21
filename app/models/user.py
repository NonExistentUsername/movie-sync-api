from sqlalchemy import Column, Integer, String, Boolean
from db.base_class import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(256), nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

