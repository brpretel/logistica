from fastapi import HTTPException
from db import database
from managers.auth import AuthManager
from models import producto, dias
from models.enums import RoleType
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MasterManager:

    @staticmethod
    async def register_master(contraseña, user_data):
        user_data["role"] = RoleType.master
        if contraseña == 123:
            return await AuthManager.register(user_data)
        else:
            raise HTTPException(400, "Token invalido abrase")

    @staticmethod
    async def create_product(product_data):
        id_ = await database.execute(producto.insert().values(product_data))
        return await database.fetch_one(producto.select().where(producto.c.id == id_))

    @staticmethod
    async def create_dia(dias_data):
        id_ = await database.execute(dias.insert().values(dias_data))
        return await database.fetch_one(dias.select().where(dias.c.id == id_))
