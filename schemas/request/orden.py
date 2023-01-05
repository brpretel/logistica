from pydantic import BaseModel


class OrderModel(BaseModel):
    producto: str
    cantidad: float
    unidad: str