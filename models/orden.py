import sqlalchemy
from sqlalchemy import DDL, event

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
    sqlalchemy.Column("creador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)

)

event.listen(
    metadata,
    "after_create",
    DDL(
        "ALTER TABLE log_ordenes ADD CONSTRAINT "
    ),
)

func = DDL(
    """create function order_function() returns trigger
    language plpgsql
    as
    $$BEGIN

    insert into "log_ordenes" values (old.producto, old.cantidad, old.unidad, old.status, old.creador_id, old.id, old.fecha_de_creacion);
    return new;
    
    END;$$;
    
    alter function order_function() owner to postgres;
""")

trigger = DDL(
    "CREATE TRIGGER order_trigger BEFORE UPDATE ON ordenes "
    "FOR EACH ROW EXECUTE PROCEDURE my_func();"
)

event.listen(orden, "after_create", func.execute_if(dialect="postgresql"))

event.listen(orden, "after_create", trigger.execute_if(dialect="postgresql"))
