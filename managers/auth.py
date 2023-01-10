from typing import Optional

from starlette.requests import Request

import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db import database
from models import RoleType, usuario


class AuthManager:
    """
    Encode: Esta funcion codifica el token con una fecha de expiracion y el ID del usuario
    """
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(days=1)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            raise ex


class CustomHHTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, config("SECRET_KEY"), algorithms=["HS256"])
            user_data = await database.fetch_one(usuario.select().where(usuario.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data

        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "El Token expiró ")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "El Token es invalido")


"""
Instancia de la Clase CustomHHTPBearer()
"""
oauth2_scheme = CustomHHTPBearer()

"""
Funcion encargara de revisar si el (role) del usuario es master
"""
def is_master(request: Request):
    if not request.state.user["role"] == RoleType.master:
        raise HTTPException(403, "prohibido")


"""
Funcion encargara de revisar si el (role) del usuario es distribuidor
"""
def is_distribuidor(request: Request):
    if not request.state.user["role"] == RoleType.distribuidor:
        raise HTTPException(403, "Forbidden")
