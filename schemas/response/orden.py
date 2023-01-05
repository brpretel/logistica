from datetime import datetime

from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    producto: str
    cantidad: float
    unidad: str
    status: str
    fecha_de_creacion: datetime
