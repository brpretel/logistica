import sqlalchemy

from db import metadata

disp_dias_de_distribuidor = sqlalchemy.Table(
    "disp_dias_de_distribuidores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("dia", sqlalchemy.ForeignKey("dias.id"), nullable=False),
    sqlalchemy.Column("usuario", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)
)
