import typing as t
from typing import Generator, Optional, Union

import jwt
from fastapi import Depends, HTTPException, Query, WebSocket, status
from jwt import PyJWTError
from sqlalchemy.orm import Session

import core.config as config
from core.auth import oauth2_scheme
from db.session import SessionLocal
from models.user import User


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_current_user_from_websocket(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    token: str = Query(default=None),
):
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.get_jwt_algorithm()],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        else:
            user_id = int(user_id)
    except PyJWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id: Optional[int] = None
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.get_jwt_algorithm()],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        else:
            user_id = int(user_id)
    except PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
