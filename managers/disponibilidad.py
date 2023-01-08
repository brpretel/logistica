from db import database
from models import disponibilidad, RoleType


class DisponibilidadManager:
    @staticmethod
    async def get_orders(user):
        q = disponibilidad.select()
        if user["role"] == RoleType.distribuidor:
            q = q.where(disponibilidad.c.creador_id == user["id"])
        return await database.fetch_all(q)

    @staticmethod
    async def create_order(order_data, user):
        order_data["creador_id"] = user["id"]
        id_ = await database.execute(orden.insert().values(order_data))
        return await database.fetch_one(orden.select().where(orden.c.id == id_))

    @staticmethod
    async def update_order(order_id, updated_data, user):
        q = disponibilidad.update().where(disponibilidad.c.id == order_id)
        if user["role"] == RoleType.distribuidor:
            q = q.where(disponibilidad.c.creador_id == user["id"])
        await database.execute(q.values(updated_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == order_id))
