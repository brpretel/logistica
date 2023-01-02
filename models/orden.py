import sqlalchemy


from models.enums import ProductType, ProductMeasurement, ProductStatus
from db import metadata

orden = sqlalchemy.Table(
    "ordenes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("producto", sqlalchemy.Enum(ProductType), nullable=False),
    sqlalchemy.Column("cantidad", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("unidad", sqlalchemy.Enum(ProductMeasurement), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Enum(ProductStatus), nullable=False,
                      server_default=ProductStatus.sin_modificar.name),
    sqlalchemy.Column("fecha_de_creacion", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("creador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False),

)