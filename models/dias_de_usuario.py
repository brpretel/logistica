import sqlalchemy

from db import metadata

dias_de_usiario = sqlalchemy.Table(
    "dias_de_usuarios",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("usuario", sqlalchemy.ForeignKey("usuarios.id"), unique=True, nullable=False),
    sqlalchemy.Column("dia", sqlalchemy.ForeignKey("dias.id"), nullable=False)
)
