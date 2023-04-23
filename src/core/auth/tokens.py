import typing as t

import jwt

from core import config

PAYLOAD_TYPE = t.Dict[str, t.Any]


def create_token(*, payload: PAYLOAD_TYPE = {}) -> str:
    return jwt.encode(payload=payload, key=config.JWT_SECRET, algorithm=config.get_jwt_algorithm())


def decode_token(token: str) -> t.Optional[PAYLOAD_TYPE]:
    return jwt.decode(jwt=token, key=config.JWT_SECRET, algorithms=[config.get_jwt_algorithm()])
