import typing as t
from datetime import datetime, timedelta
from typing import List, MutableMapping, Union

from fastapi.security import OAuth2PasswordBearer

from core import config
from core.auth import create_token

JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(*, sub: str) -> str:
    lifetime = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: t.Dict[str, t.Any] = {
        "type": "access_token",
        "exp": datetime.utcnow() + lifetime,
        "iat": datetime.utcnow(),
    }

    return create_token(payload=payload)
