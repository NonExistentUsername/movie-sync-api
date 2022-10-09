from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.security import get_password_hash, verify_password
import schemas.user
import models.user
from core.auth import create_access_token
from crud.user import get_user_by_username


def register_user(user: schemas.user.UserCreate, db: Session):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="User with same username already registered.")

    db_user = models.user.User(username=user.username, is_admin=False, hashed_password=get_password_hash(user.password))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(user: schemas.user.UserLogin, db: Session):
    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="User with this username is not registered.")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password.")

    return {
        "access_token": create_access_token(sub=str(db_user.id)),
        "token_type": "bearer",
    }
