import sqlalchemy
from models.enums import ProductMeasurement, ProductStatus
from db import metadata

log_cambio_orden = sqlalchemy.Table(
    "log_ordenes",
    metadata,
    sqlalchemy.Column("producto", sqlalchemy.String(60), nullable=False),
    sqlalchemy.Column("categoria", sqlalchemy.String(60), nullable=False),
    sqlalchemy.Column("cantidad", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("unidad", sqlalchemy.Enum(ProductMeasurement), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Enum(ProductStatus), nullable=False),
    sqlalchemy.Column("fecha_de_creacion", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("fecha_de_modificacion", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("fecha_de_disponibilidad", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("dia_de_disponibilidad", sqlalchemy.String(30), nullable=False),
    sqlalchemy.Column("modificador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False),
    sqlalchemy.Column("disponibilidad_id", sqlalchemy.ForeignKey("disponibilidades.id"), nullable=False)

)