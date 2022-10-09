from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.command
import schemas.app
import models.user
import crud.user
import crud.command
import crud.app
import core.deps
import core.global_variables
from handlers.commands_ws import commands_ws_router


commands_router = APIRouter()
commands_router.include_router(commands_ws_router, prefix='/ws')


@commands_router.post("/send_command", response_model=schemas.command.Command)
async def send_command(
        command: schemas.command.CommandCreate,
        db: Session = Depends(core.deps.get_db),
        current_user: models.user.User = Depends(core.deps.get_current_user)):
    return await crud.command.send_command(command, db, current_user)


@commands_router.delete("/delete_commands", response_model=schemas.command.CommandDeleted)
async def delete_commands(
        commands: schemas.command.CommandDelete,
        db: Session = Depends(core.deps.get_db),
        current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.command.delete_commands(commands, db, current_user)
