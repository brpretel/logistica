import datetime
from typing import Optional

from datetime import datetime

import sqlalchemy

from db import database
from models import disponibilidad, RoleType, disp_dias_de_distribuidor, dias, copia_disponibilidad, \
    disp_usuario_producto, producto, usuario, UserStatus


class DisponibilidadManager:
    """
    get_all_disponibilidades: Funcion unica para el master que le regresara
    todas las disponibilidades de la base de datos.
    """

    @staticmethod
    # obtener las disponibilidades siendo el master o siendo el distribuidor
    async def get_disponibilidades(user, tipo: Optional[str] = None, distribuidor: Optional[str] = None):
        if user["role"] == RoleType.master:
            q1 = copia_disponibilidad.select()
            q2 = usuario.select()
            q3 = usuario.select().where(usuario.c.status == UserStatus.activo)
            q4 = producto.select()
            disponibilidades = await database.fetch_all(q1)
            usuarios = await database.fetch_all(q2)
            usuarios_activos = await database.fetch_all(q3)
            productos = await database.fetch_all(q4)
            cantidad_usuarios_activos = len(usuarios_activos)
            cantidad_disponibilidades = len(disponibilidades)
            cantidad_productos = len(productos)
            return disponibilidades, usuarios, cantidad_usuarios_activos, cantidad_disponibilidades, cantidad_productos

        elif user["role"] == RoleType.master and tipo == "Historial Completo":
            q = disponibilidad.select()
        elif user["role"] == RoleType.master and tipo == "Todas las Disponibilidades de un distribuidor":
            q = disponibilidad.select().where(disponibilidad.c.creador_id == distribuidor)
        elif user["role"] == RoleType.master and tipo == "Disponibilidades Actuales de un distribuidor":
            q = copia_disponibilidad.select().where(copia_disponibilidad.c.creador_id == distribuidor)
        else:
            q1 = copia_disponibilidad.select().where(copia_disponibilidad.c.creador_id == user["id"])
            q2 = (
                disp_dias_de_distribuidor.select()
                .select_from(disp_dias_de_distribuidor.join(dias))
                .where(disp_dias_de_distribuidor.c.usuario == user["id"])
                .with_only_columns([dias.c.dia, dias.c.fecha])
                .order_by(sqlalchemy.asc(dias.c.fecha))
            )
            q3 = (
                disp_usuario_producto.select()
                .select_from(disp_usuario_producto.join(producto))
                .where(usuario.c.id == user["id"])
                .with_only_columns([producto.c.nombre])
            )
            disponibilidades = await database.fetch_all(q1)
            dias_disp = await database.fetch_all(q2)
            productos = await database.fetch_all(q3)
            current_date = datetime.now().date()
            cant_dispos = len(disponibilidades)
            cant_dias = len(dias_disp)
            return disponibilidades, dias_disp, current_date, productos, cant_dispos, cant_dias
        return await database.fetch_all(q)

    """
    get_data_for_distribuidor: Retorna toda la informacion necesaria (disponibilidades) y 
    las fechas en las que los distribuidores pueden publicar disponibilidad.
    """

    @staticmethod
    # trae los datos para hacer el post de una disponibilidad del distribuidor
    async def get_data_for_disponibiliad(user):
        q1 = (
            disp_dias_de_distribuidor.select()
            .select_from(disp_dias_de_distribuidor.join(dias))
            .where(disp_dias_de_distribuidor.c.usuario == user["id"])
            .with_only_columns([dias.c.dia, dias.c.fecha])
        )
        q2 = (
            disp_usuario_producto.select()
            .select_from(disp_usuario_producto.join(producto))
            .where(disp_usuario_producto.c.usuario == user["id"])
            .with_only_columns([producto.c.nombre, producto.c.categoria])
        )

        dias_disponibles = await database.fetch_all(q1)
        productos_disponibles = await database.fetch_all(q2)

        return dias_disponibles, productos_disponibles

    """
    create_disponibilidad: está funcion sirve para crear una disponibilidad
    """

    @staticmethod
    async def create_disponibilidad(disp_data, user):

        fecha_query = sqlalchemy.select([dias.c.fecha]).where(dias.c.dia == disp_data["dia_de_disponibilidad"])
        fecha = await database.fetch_val(fecha_query)
        disp_data["fecha_de_disponibilidad"] = fecha
        disp_data["creador_id"] = user["id"]
        disp_data["modificador_id"] = user["id"]
        id_ = await database.execute(disponibilidad.insert().values(disp_data))

        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == id_))

    """
    update_disponibilidad: está funcion sirve para actualizar una disponibilidad
    """

    @staticmethod
    # modifica una disponibilidad para el master y para el distribuidor
    async def update_disponibilidad(disponibilidad_id, updated_data, user):
        updated_data["modificador_id"] = user["id"]
        q = disponibilidad.update().where(disponibilidad.c.id == disponibilidad_id)
        await database.execute(q.values(updated_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == disponibilidad_id))
