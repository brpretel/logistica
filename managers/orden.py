from db import database
from models import orden, RoleType


class OrderManager:
    @staticmethod
    async def get_orders(user):
        q = orden.select()
        if user["role"] == RoleType.distribuidor:
            q = q.where(orden.c.creador_id == user["id"])
        return await database.fetch_all(q)

    @staticmethod
    async def create_order(order_data, user):
        order_data["creador_id"] = user["id"]
        id_ = await database.execute(orden.insert().values(order_data))
        return await database.fetch_one(orden.select().where(orden.c.id == id_))
