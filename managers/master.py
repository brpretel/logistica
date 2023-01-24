import sqlalchemy
from fastapi import HTTPException
from db import database
from managers.auth import AuthManager
from models import producto, dias, disp_dias_de_distribuidor, usuario,disp_usuario_producto
from models.enums import RoleType
from passlib.context import CryptContext
from sqlalchemy import and_

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
        try:
            id_ = await database.execute(producto.insert().values(product_data))
        except:
            return None
        return await database.fetch_one(producto.select().where(producto.c.id == id_))

    @staticmethod
    async def create_dia(dias_data):
        id_ = await database.execute(dias.insert().values(dias_data))
        return await database.fetch_one(dias.select().where(dias.c.id == id_))


    @staticmethod
    async def post_product_for_user(product_data):
        product_exists = await database.fetch_one(
            producto.select().where(producto.c.id == product_data["producto"])
        )
        user_exists = await database.fetch_one(
            usuario.select().where(usuario.c.id == product_data["usuario"])
        )
        if product_exists and user_exists:
            id_ = await database.execute(disp_usuario_producto.insert().values(product_data))
            return await database.fetch_one(
                disp_usuario_producto.select().where(disp_usuario_producto.c.id == id_))
        else:
            return None

    @staticmethod
    async def create_dia_for_distribuidor(dia_data):
        dia_exists = await database.fetch_one(
            dias.select().where(dias.c.id == dia_data["dia"])
        )

        user_exists = await database.fetch_one(
            usuario.select().where(usuario.c.id == dia_data["usuario"])
        )
        if dia_exists and user_exists:
            id_ = await database.execute(disp_dias_de_distribuidor.insert().values(dia_data))
            return await database.fetch_one(
                disp_dias_de_distribuidor.select().where(disp_dias_de_distribuidor.c.id == id_))
        else:
            return None

    @staticmethod
    async def get_all_users():
        q1 = usuario.select()
        users = await database.fetch_all(q1)
        return users

    @staticmethod
    async def get_all_products():
        q1 = producto.select()
        productos = await database.fetch_all(q1)
        return productos

    @staticmethod
    async def get_user_for_update(user_id):
        q1 = usuario.select().where(usuario.c.id == user_id)
        q2 = dias.select().where(~dias.c.id.in_(select([disp_dias_de_distribuidor.c.dia]).where(disp_dias_de_distribuidor.c.usuario == user_id))).order_by(sqlalchemy.asc(dias.c.fecha))
        q3 = producto.select().where(~producto.c.id.in_(select([disp_usuario_producto.c.producto]).where(disp_usuario_producto.c.usuario == user_id)))
        user = await database.fetch_one(q1)
        dias_semana = await database.fetch_all(q2)
        productos = await database.fetch_all(q3)
        return user, dias_semana, productos

    @staticmethod
    async def update_user(user_data):
        try:
            query = update(usuario).where(usuario.c.user_id == user_data["user_id"]).values(role=user_data["role"],
                                                                                            status=user_data["status"])
            await database.execute(query)
            return await database.fetch_one(usuario.select().where(usuario.c.user_id == user_data["user_id"]))
        except Exception as e:
            print("Error updating user: ", e)

    @staticmethod
    async def get_user_products_and_days(user_id):
        days_query = (
            select([dias.c.dia])
            .select_from(disp_dias_de_distribuidor.join(dias))
            .where(disp_dias_de_distribuidor.c.usuario == user_id)
        )
        days = await database.fetch_all(days_query)
        products_query = (
            select([producto.c.nombre, producto.c.categoria])
            .select_from(disp_usuario_producto.join(producto))
            .where(disp_usuario_producto.c.usuario == user_id)
        )
        products = await database.fetch_all(products_query)
        return days, products




