from pydantic import BaseModel, Field
from models.enums import ProductCategory


class ProductosModel(BaseModel):
    nombre : str
    categoria : ProductCategory