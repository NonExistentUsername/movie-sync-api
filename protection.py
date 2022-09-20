from fastapi import HTTPException
from core.config import ACCESS_KEY


def protect_post(func_to_protect):
    def protection(object_create, db, *args, **kwargs):
        if object_create.access_key != ACCESS_KEY:
            raise HTTPException(status_code=403, detail="Wrong access key")
        else:
            return func_to_protect(object_create, db, *args, **kwargs)

    return protection
