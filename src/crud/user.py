from typing import Optional

import models.user
import schemas.user
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_user_by_username(db: Session, username: str) -> Optional[models.user.User]:
    return (
        db.query(models.user.User).filter(models.user.User.username == username).first()
    )


def set_admin_rights_for_user(
    user: schemas.user.UserUpdate, db: Session, current_user: models.user.User
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found.")

    if user.is_admin is not None:
        db_user.is_admin = user.is_admin
    if user.have_access is not None:
        db_user.have_access = user.have_access
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have access.")

    return db.query(models.user.User).all()


def get_user(username: str, db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have access.")

    result = (
        db.query(models.user.User).filter(models.user.User.username == username).first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")

    return result
