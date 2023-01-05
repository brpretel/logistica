from fastapi import HTTPException

from db import database
from managers.auth import AuthManager
from models import usuario
from passlib.context import CryptContext
from asyncpg import UniqueViolationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(usuario.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "Ya existe un usuario con este user_id")
        user_do = await database.fetch_one(usuario.select().where(usuario.c.id == id_))
        return AuthManager.encode_token(user_do)


    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(usuario.select().where(usuario.c.user_id == user_data["user_id"]))
        if not user_do:
            raise HTTPException(400, "Wrong user id or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong user id or password")
        return AuthManager.encode_token(user_do)


