import sqlalchemy

from db import metadata

disp_usuario_producto = sqlalchemy.Table(
    "disp_usuario_productos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("producto", sqlalchemy.ForeignKey("productos.id"), nullable=False),
    sqlalchemy.Column("usuario", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)
)
