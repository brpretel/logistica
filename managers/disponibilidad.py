from db import database
from models import disponibilidad, RoleType, disp_dias_de_distribuidor, dias, copia_disponibilidad


class DisponibilidadManager:
    """
    get_all_disponibilidades: Funcion unica para el master que le regresara
    todas las disponibilidades de la base de datos.
    """
    @staticmethod
    async def get_all_disponibilidades(user):
        if user["role"] == RoleType.master:
            q = disponibilidad.select()
        else:
            q = disponibilidad.select().where(disponibilidad.c.creador_id == user["id"])
        return await database.fetch_all(q)

    """
    get_data_for_distribuidor: Retorna toda la informacion necesaria (disponibilidades) y 
    las fechas en las que los distribuidores pueden publicar disponibilidad.
    """
    @staticmethod
    async def get_data_for_distribuidor(user_id):
        q1 = copia_disponibilidad.select().where(copia_disponibilidad.c.creador_id == user_id["id"])
        q2 = (
            disp_dias_de_distribuidor.select()
            .select_from(disp_dias_de_distribuidor.join(dias))
            .where(disp_dias_de_distribuidor.c.usuario == user_id["id"
                                                                  ""])
            .with_only_columns([dias.c.dia])
        )
        disponibilidades = await database.fetch_all(q1)
        disp_dias_de_distribuidores = await database.fetch_all(q2)
        return disponibilidades, disp_dias_de_distribuidores

    """
    create_disponibilidad: está funcion sirve para crear una disponibilidad
    """
    @staticmethod
    async def create_disponibilidad(disp_data, user):
        disp_data["creador_id"] = user["id"]
        disp_data["modificador_id"] = user["id"]
        id_ = await database.execute(disponibilidad.insert().values(disp_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == id_))

    """
    update_disponibilidad: está funcion sirve para actualizar una disponibilidad
    """
    @staticmethod
    async def update_disponibilidad(order_id, updated_data, user):
        updated_data["modificador_id"] = user["id"]
        q = disponibilidad.update().where(disponibilidad.c.id == order_id)
        await database.execute(q.values(updated_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == order_id))
