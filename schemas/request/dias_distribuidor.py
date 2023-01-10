from pydantic import BaseModel
from models.enums import Dias_de_disponibilidad

class Dias_DistribuidorModel(BaseModel):
    distribuidor_id: str
    dia_id: Dias_de_disponibilidad