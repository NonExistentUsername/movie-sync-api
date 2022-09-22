from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.security import get_password_hash, verify_password
import schemas.user
import models.user
from core.auth import create_access_token
from typing import Optional
import re


def get_user_by_nickname(db: Session, nickname: str) -> Optional[models.user.User]:
    return db.query(models.user.User).filter(models.user.User.nickname == nickname).first()


def set_admin_rights_for_user(user: schemas.user.UserUpdate, db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    db_user = get_user_by_nickname(db, user.nickname)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found.")

    if db_user.id == current_user.id or db_user.id == 1:
        raise HTTPException(status_code=400, detail="Cannot change this user rights.")

    if not user.is_admin is None:
        db_user.is_admin = user.is_admin
    if not user.receives_commands is None:
        db_user.receives_commands = user.receives_commands
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    return db.query(models.user.User).all()


def get_user(nickname: str, db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    result = db.query(models.user.User).filter(models.user.User.nickname == nickname).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")

    return result


def validating_nickname(nickname: str) -> bool:
    regex_name = re.compile(r'^(?=.{4,256}$)[a-zA-Z_]\w*$', re.IGNORECASE)
    result = regex_name.search(nickname)
    if result and result.string == nickname:
        return True
    return False


def register_user(user: schemas.user.UserCreate, db: Session):
    if not validating_nickname(user.nickname):
        raise HTTPException(status_code=400,
                detail="This nickname is not allowed. You can use letters, digits and '_'. Nickname length must be at least 4 characters.")

    if len(user.password) < 4 or len(user.password) > 32:
        raise HTTPException(status_code=400, detail="This password is not allowed.")

    if get_user_by_nickname(db, user.nickname):
        raise HTTPException(status_code=400, detail="User with same nickname already registered.")

    db_user = models.user.User(nickname=user.nickname, is_admin=False, hashed_password=get_password_hash(user.password))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(user: schemas.user.UserLogin, db: Session):
    db_user = get_user_by_nickname(db, user.nickname)
    if not db_user:
        raise HTTPException(status_code=401, detail="User with this nickname is not registered.")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password.")

    return {
        "access_token": create_access_token(sub=str(db_user.id)),
        "token_type": "bearer",
    }
