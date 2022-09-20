from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas.command
import models.user
import models.command


def get_commands(db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)
    return db.query(models.command.Command).filter(models.command.Command.receiver_id == current_user.id).all()


def send_command(command: schemas.command.CommandCreate, db: Session, current_user: models.user.User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)
    admins = db.query(models.user.User).filter(models.user.User.is_admin == True)
    db_command = None

    if command.receiver_id is None:
        for admin in admins:
            db_command = models.command.Command(command=command.command, param=command.param, receiver_id=admin.id,
                                                sender_id=current_user.id)
            db.add(db_command)
            db.commit()
            db.refresh(db_command)
    else:
        pass
    return db_command
