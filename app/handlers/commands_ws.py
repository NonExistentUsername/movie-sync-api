import core.deps
import core.global_variables
import crud.app
import crud.command
import crud.user
import models.user
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

commands_ws_router = APIRouter()


@commands_ws_router.websocket("/get_commands")
async def ws_get_updates(
    websocket: WebSocket,
    current_user: models.user.User = Depends(core.deps.get_current_user_from_websocket),
    db: Session = Depends(core.deps.get_db),
):
    await crud.command.ws_get_commands(websocket, current_user, db)
