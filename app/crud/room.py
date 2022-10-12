from sqlalchemy.orm import Session
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
import schemas.command
import models.user
import schemas.room
from typing import Optional
import models.room
from models.associations import user_room_member_association_table


def get_rooms(db: Session, current_user: models.user.User):
    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")
    return current_user.member_of_rooms


def get_room(room_name: str, db: Session, current_user: models.user.User):
    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")
    db_room: Optional[models.room.Room] = db.query(models.room.Room).filter(models.room.Room == room_name).first()
    if db_room is None or current_user not in db_room.members_of_room:
        raise HTTPException(status_code=404, detail="Not found")
    return db_room


def create_room(room_name: str, db: Session, current_user: models.user.User):
    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    if db.query(models.room.Room).filter(models.room.Room.name == room_name).first() is not None:
        raise HTTPException(status_code=400, detail="Room with the same name already created.")

    if db.query(models.room.Room).filter(models.room.Room.creator_id == current_user.id).count() == 10:
        raise HTTPException(status_code=400, detail="You have created 10/10 rooms. Delete a room to create another.")

    room_db = models.room.Room(name=room_name, creator_id=current_user.id)
    room_db.members_of_room.append(current_user)
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db


def join_room(room_name: str, room_key: str, db: Session, current_user: models.user.User):

    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_room: models.room.Room = db.query(models.room.Room).filter(models.room.Room.name == room_name).first()
    if db_room is None or db_room.key != room_key:
        raise HTTPException(status_code=400, detail="Room is not found.")

    if current_user in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="You are already in this room.")

    db_room.members_of_room.append(current_user)
    db.commit()
    db.refresh(db_room)

    return {'status': 'OK'}


def leave_room(room_name: str, db: Session, current_user: models.user.User):

    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_room: models.room.Room = db.query(models.room.Room).filter(models.room.Room.name == room_name).first()
    if db_room is None or current_user not in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="Room is not found.")

    if db_room.creator_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot leave your room.")

    db_room.members_of_room.remove(current_user)
    db.commit()
    db.refresh(db_room)

    return {'status': 'OK'}


def delete_room(room_name: str, db: Session, current_user: models.user.User):

    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_room: models.room.Room = db.query(models.room.Room).filter(models.room.Room.name == room_name).first()
    if db_room is None or current_user not in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="Room is not found.")

    if db_room.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your room.")

    db.delete(db_room)
    db.commit()

    return {'status': 'OK'}


def kick_user_from_room(username: str, room_name: str, db: Session, current_user: models.user.User):

    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_room: models.room.Room = db.query(models.room.Room).filter(models.room.Room.name == room_name).first()
    if db_room is None or current_user not in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="Room is not found.")

    if db_room.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="It's not your room.")

    db_user: models.user.User = db.query(models.user.User).filter(models.user.User.username == username).first()
    if db_user is None or db_user not in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="User is not found.")

    db_room.members_of_room.remove(db_user)
    db.commit()
    db.refresh(db_room)
