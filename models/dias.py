import sqlalchemy

from db import metadata

dias = sqlalchemy.Table(
    "dias",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("dia", sqlalchemy.String(15), unique=True, nullable=False),
)
