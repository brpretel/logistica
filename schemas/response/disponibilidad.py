from datetime import date

from pydantic import BaseModel


class DisponibilidadOut(BaseModel):
    id: int
    producto: str
    cantidad: float
    unidad: str
    status: str
    fecha_de_creacion: date
