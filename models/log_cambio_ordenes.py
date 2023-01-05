import sqlalchemy
from models.enums import ProductType, ProductMeasurement, ProductStatus
from db import metadata

log_cambio_orden = sqlalchemy.Table(
    "log_ordenes",
    metadata,
    sqlalchemy.Column("producto", sqlalchemy.Enum(ProductType), nullable=False),
    sqlalchemy.Column("cantidad", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("unidad", sqlalchemy.Enum(ProductMeasurement), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Enum(ProductStatus), nullable=False,
                      server_default=ProductStatus.modificado.name),
    sqlalchemy.Column("fecha_de_modificacion", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("modificador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False),
    sqlalchemy.Column("orden_id", sqlalchemy.ForeignKey("ordenes.id"), nullable=False)

)
