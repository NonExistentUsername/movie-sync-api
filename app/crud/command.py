from sqlalchemy.orm import Session
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
import schemas.command
import models.user
import models.command
import models.room
import core.global_variables


def get_commands(db: Session, current_user: models.user.User):
    if not current_user.receives_commands:
        raise HTTPException(status_code=403)
    return db.query(models.command.Command).filter(models.command.Command.receiver_id == current_user.id).all()


async def ws_get_commands(websocket: WebSocket, current_user: models.user.User):
    await core.global_variables.socket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await core.global_variables.socket_manager.disconnect(websocket)


async def send_command(command: schemas.command.CommandCreate, db: Session, current_user: models.user.User):
    if not current_user.have_access:
        raise HTTPException(status_code=403, detail="You don't have access.")

    db_room: models.room.Room = db.query(models.room.Room).filter(models.room.Room.name == command.room_name).first()
    if db_room is None or current_user not in db_room.members_of_room:
        raise HTTPException(status_code=400, detail="Room is not found.")
    db_command = None

    for member in db_room.members_of_room:
        db_command = models.command.Command(command=command.command, param=command.param, receiver_id=member.id,
                                            sender_id=current_user.id, room_id=db_room.id)
        db.add(db_command)
        db.commit()
        db.refresh(db_command)
        await core.global_variables.socket_manager.broadcast({"status": "updated"})
    else:
        pass
    return db_command


def delete_commands(commands: schemas.command.CommandDelete, db: Session, current_user: models.user.User):
    if not current_user.receives_commands:
        raise HTTPException(status_code=403)

    deleted_commands = []

    for command_id in commands.commands:
        command: models.command.Command = db.query(models.command.Command).filter(models.command.Command.id == command_id).first()
        if not command:
            continue
        if command.receiver_id == current_user.id or command.sender_id == current_user.id:
            db.delete(command)
            db.commit()
            deleted_commands.append(command_id)

    return {
        "deleted_commands": deleted_commands
    }
