import core.deps
import core.global_variables
import crud.command
import crud.room
import crud.user
import models.user
import schemas.command
import schemas.room
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

rooms_router = APIRouter()


@rooms_router.get("/", response_model=Page[schemas.room.Room])
async def get_rooms(
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return paginate(crud.room.get_rooms(db, current_user))


@rooms_router.get("/room", response_model=schemas.room.Room)
async def get_room(
    room_name: str,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return paginate(crud.room.get_room(room_name, db, current_user))


@rooms_router.post("/create", response_model=schemas.room.Room, status_code=201)
async def create_room(
    room_name: str,
    capacity: int = 10,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return crud.room.create_room(room_name, capacity, db, current_user)


@rooms_router.post("/join")
async def join_room(
    room_name: str,
    room_key: str,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return crud.room.join_room(room_name, room_key, db, current_user)


@rooms_router.post("/leave")
async def leave_room(
    room_name: str,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return crud.room.leave_room(room_name, db, current_user)


@rooms_router.delete("/delete")
async def leave_room(
    room_name: str,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return crud.room.delete_room(room_name, db, current_user)


@rooms_router.post("/kick_member")
async def kick_member(
    username: str,
    room_name: str,
    db: Session = Depends(core.deps.get_db),
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    return crud.room.kick_user_from_room(username, room_name, db, current_user)
